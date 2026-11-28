"""沿用去年三支卷积的MindSpore TextCNN。"""
import mindspore as ms
from mindspore import nn, ops


class TextCNN(nn.Cell):
    def __init__(self, vocab_size, word_len, kernels=(3, 4, 5), vec_length=40):
        super().__init__()
        self.word_len = word_len
        self.embedding = nn.Embedding(vocab_size, vec_length, embedding_table='normal', padding_idx=0)
        self.convs = nn.CellList([
            nn.Conv2d(1, 96, kernel_size=(height, vec_length), pad_mode='valid', has_bias=True)
            for height in kernels
        ])
        self.relu = nn.ReLU()
        self.max_pool = ops.ReduceMax(keep_dims=False)
        self.dropout = nn.Dropout(p=0.5)
        self.fc = nn.Dense(96 * len(kernels), 2)

    def construct(self, x):
        """x的形状为[batch, word_len]，返回[batch, 2]的logits。"""
        # TODO 2  完成Embedding、三支卷积、最大池化、拼接、Dropout和全连接。
        raise NotImplementedError("请完成任务2")
