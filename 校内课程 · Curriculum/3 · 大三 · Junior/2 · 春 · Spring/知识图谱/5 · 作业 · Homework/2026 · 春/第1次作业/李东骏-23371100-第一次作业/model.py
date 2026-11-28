# -*- coding: utf-8 -*-
"""
BiLSTM + CRF 命名实体识别模型。

包含两部分：
  1. CRF  —— 手写的线性链条件随机场层（前向算法求配分函数 + Viterbi 解码），
            不依赖任何第三方 CRF 库，便于展示原理。
  2. BiLSTM_CRF —— 字向量 Embedding -> 双向 LSTM 编码 -> 线性层得到发射分数(emission)
                   -> CRF 层建模标签转移约束，输出最优标签序列。
"""
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class CRF(nn.Module):
    """线性链条件随机场 (Linear-chain CRF)。

    参考经典实现 (kmkurn/pytorch-crf) 的算法，自行实现以展示原理：
      - transitions[i, j]   : 从标签 i 转移到标签 j 的分数
      - start_transitions[i]: 句首取标签 i 的分数
      - end_transitions[i]  : 句尾取标签 i 的分数
    约定输入为 batch_first，即 (batch, seq_len, num_tags)。
    """

    def __init__(self, num_tags: int):
        super().__init__()
        self.num_tags = num_tags
        self.start_transitions = nn.Parameter(torch.empty(num_tags))
        self.end_transitions = nn.Parameter(torch.empty(num_tags))
        self.transitions = nn.Parameter(torch.empty(num_tags, num_tags))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.uniform_(self.start_transitions, -0.1, 0.1)
        nn.init.uniform_(self.end_transitions, -0.1, 0.1)
        nn.init.uniform_(self.transitions, -0.1, 0.1)

    def forward(self, emissions, tags, mask):
        """返回一个 batch 的平均对数似然 log P(tags | emissions)。

        emissions: (batch, seq_len, num_tags) 发射分数
        tags:      (batch, seq_len)            金标签
        mask:      (batch, seq_len)            有效位置为 1 的 bool 掩码
        """
        # 转成 (seq_len, batch, ...) 方便沿时间维循环
        emissions = emissions.transpose(0, 1)
        tags = tags.transpose(0, 1)
        mask = mask.transpose(0, 1).to(emissions.dtype)

        numerator = self._score_sentence(emissions, tags, mask)   # 真实路径分数
        denominator = self._forward_alg(emissions, mask)          # 所有路径的 logsumexp(配分函数)
        llh = numerator - denominator                              # 对数似然
        return llh.mean()

    def decode(self, emissions, mask):
        """Viterbi 解码，返回 List[List[int]]，每条为一句的最优标签序列。"""
        emissions = emissions.transpose(0, 1)
        mask = mask.transpose(0, 1).to(torch.bool)
        return self._viterbi_decode(emissions, mask)

    # ---------- 内部算法 ----------
    def _score_sentence(self, emissions, tags, mask):
        """计算金标签路径的分数 (seq_len, batch, ...)。"""
        seq_len, batch_size = tags.shape
        score = self.start_transitions[tags[0]]                    # 句首转移分
        score = score + emissions[0, torch.arange(batch_size), tags[0]]

        for i in range(1, seq_len):
            score = score + self.transitions[tags[i - 1], tags[i]] * mask[i]
            score = score + emissions[i, torch.arange(batch_size), tags[i]] * mask[i]

        # 找到每条序列最后一个有效位置的标签，加上句尾转移分
        seq_ends = mask.long().sum(dim=0) - 1
        last_tags = tags[seq_ends, torch.arange(batch_size)]
        score = score + self.end_transitions[last_tags]
        return score

    def _forward_alg(self, emissions, mask):
        """前向算法计算配分函数 log sum_{all paths} exp(score)。"""
        seq_len = emissions.size(0)
        # score: (batch, num_tags) 到当前位置、以各标签结尾的所有路径的 logsumexp
        score = self.start_transitions + emissions[0]

        for i in range(1, seq_len):
            # broadcast: (batch, num_tags, 1) + (num_tags, num_tags) + (batch, 1, num_tags)
            broadcast_score = score.unsqueeze(2)
            broadcast_emissions = emissions[i].unsqueeze(1)
            next_score = broadcast_score + self.transitions + broadcast_emissions
            next_score = torch.logsumexp(next_score, dim=1)        # (batch, num_tags)
            # 只在有效位置更新，padding 位置保持原值
            score = torch.where(mask[i].unsqueeze(1).bool(), next_score, score)

        score = score + self.end_transitions
        return torch.logsumexp(score, dim=1)                       # (batch,)

    def _viterbi_decode(self, emissions, mask):
        seq_len, batch_size = mask.shape
        score = self.start_transitions + emissions[0]              # (batch, num_tags)
        history = []

        for i in range(1, seq_len):
            broadcast_score = score.unsqueeze(2)
            broadcast_emission = emissions[i].unsqueeze(1)
            next_score = broadcast_score + self.transitions + broadcast_emission
            next_score, indices = next_score.max(dim=1)            # 沿上一标签维取最大
            score = torch.where(mask[i].unsqueeze(1), next_score, score)
            history.append(indices)

        score = score + self.end_transitions
        seq_ends = mask.long().sum(dim=0) - 1

        best_tags_list = []
        for idx in range(batch_size):
            _, best_last_tag = score[idx].max(dim=0)
            best_tags = [best_last_tag.item()]
            # 回溯，注意只回溯到该序列的真实长度
            for hist in reversed(history[: seq_ends[idx]]):
                best_last_tag = hist[idx][best_tags[-1]]
                best_tags.append(best_last_tag.item())
            best_tags.reverse()
            best_tags_list.append(best_tags)
        return best_tags_list


class BiLSTM_CRF(nn.Module):
    """字符级 BiLSTM + CRF 序列标注模型。"""

    def __init__(self, vocab_size, num_tags, emb_dim=128, hidden_dim=256,
                 num_layers=1, dropout=0.5, pad_idx=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb_dim, padding_idx=pad_idx)
        self.lstm = nn.LSTM(
            input_size=emb_dim,
            hidden_size=hidden_dim // 2,        # 双向，拼接后即 hidden_dim
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.dropout = nn.Dropout(dropout)
        self.hidden2tag = nn.Linear(hidden_dim, num_tags)
        self.crf = CRF(num_tags)

    def _emissions(self, x, lengths):
        emb = self.dropout(self.embedding(x))
        packed = pack_padded_sequence(emb, lengths.cpu(), batch_first=True, enforce_sorted=False)
        out, _ = self.lstm(packed)
        out, _ = pad_packed_sequence(out, batch_first=True, total_length=x.size(1))
        out = self.dropout(out)
        return self.hidden2tag(out)               # (batch, seq_len, num_tags)

    def neg_log_likelihood(self, x, tags, mask, lengths):
        """训练用：返回平均负对数似然作为 loss。"""
        emissions = self._emissions(x, lengths)
        return -self.crf(emissions, tags, mask)

    def predict(self, x, mask, lengths):
        """推理用：返回 Viterbi 最优标签序列 List[List[int]]。"""
        emissions = self._emissions(x, lengths)
        return self.crf.decode(emissions, mask)
