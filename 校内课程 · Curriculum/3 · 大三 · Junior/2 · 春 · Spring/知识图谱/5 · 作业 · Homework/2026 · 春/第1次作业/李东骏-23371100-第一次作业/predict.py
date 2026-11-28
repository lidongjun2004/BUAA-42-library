# -*- coding: utf-8 -*-
"""载入训练好的 BiLSTM-CRF 模型，对任意中文句子做实体识别（推理 demo）。

用法:
  python predict.py --text "高勇：男，中国国籍，汉族，本科学历。"
  python predict.py            # 用内置示例
"""
import argparse
from pathlib import Path

import torch

from dataset import UNK, load_vocab
from model import BiLSTM_CRF

HERE = Path(__file__).resolve().parent


def extract_entities(chars, tags):
    """从 BIO 标签序列里抽取实体 (类型, 文本, 起止下标)。"""
    ents, cur_type, cur_chars, start = [], None, [], 0
    for i, (c, t) in enumerate(zip(chars, tags)):
        if t.startswith("B-"):
            if cur_type:
                ents.append((cur_type, "".join(cur_chars), start, i - 1))
            cur_type, cur_chars, start = t[2:], [c], i
        elif t.startswith("I-") and cur_type == t[2:]:
            cur_chars.append(c)
        else:
            if cur_type:
                ents.append((cur_type, "".join(cur_chars), start, i - 1))
            cur_type, cur_chars = None, []
    if cur_type:
        ents.append((cur_type, "".join(cur_chars), start, len(chars) - 1))
    return ents


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="顾建国先生：研究生学历，高级经济师，现任本公司董事长，毕业于清华大学。")
    ap.add_argument("--ckpt_dir", default=str(HERE / "checkpoints"))
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    char2id, tag2id = load_vocab(Path(args.ckpt_dir) / "vocab.json")
    id2tag = {i: t for t, i in tag2id.items()}
    device = torch.device(args.device)

    model = BiLSTM_CRF(vocab_size=len(char2id), num_tags=len(tag2id))
    model.load_state_dict(torch.load(Path(args.ckpt_dir) / "best_model.pt", map_location=device))
    model.to(device).eval()

    chars = list(args.text)
    x = torch.tensor([[char2id.get(c, char2id[UNK]) for c in chars]], dtype=torch.long, device=device)
    mask = torch.ones_like(x, dtype=torch.bool)
    lengths = torch.tensor([len(chars)], dtype=torch.long)
    with torch.no_grad():
        pred = model.predict(x, mask, lengths)[0]
    tags = [id2tag[i] for i in pred]

    print("输入:", args.text)
    print("逐字标签:")
    print(" ".join(f"{c}/{t}" for c, t in zip(chars, tags)))
    print("\n抽取到的实体:")
    ents = extract_entities(chars, tags)
    if not ents:
        print("  (无)")
    for etype, text, s, e in ents:
        print(f"  [{etype}] {text}  (位置 {s}-{e})")


if __name__ == "__main__":
    main()
