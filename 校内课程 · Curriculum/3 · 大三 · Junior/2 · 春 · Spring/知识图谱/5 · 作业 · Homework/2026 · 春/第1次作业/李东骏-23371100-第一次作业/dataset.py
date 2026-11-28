# -*- coding: utf-8 -*-
"""数据读取与预处理：读取 BIO 格式语料，构建字表/标签表，生成可训练的 batch。"""
import json
from pathlib import Path

import torch
from torch.utils.data import Dataset

PAD = "<PAD>"
UNK = "<UNK>"


def read_bio(path):
    """读取 BIO 标注文件。每行 `字 标签`，空行分句。

    返回: List[(chars, tags)]，chars/tags 均为等长字符串列表。
    """
    sentences = []
    chars, tags = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip() == "":
                if chars:
                    sentences.append((chars, tags))
                    chars, tags = [], []
                continue
            parts = line.split()
            if len(parts) == 1:                # 只有字、缺标签 -> 视为 O
                chars.append(parts[0])
                tags.append("O")
            else:
                chars.append(parts[0])
                tags.append(parts[-1])
    if chars:
        sentences.append((chars, tags))
    return sentences


def build_vocab(sentences, min_freq=1):
    """从训练集构建字表与标签表。"""
    char_freq = {}
    tag_set = set()
    for chars, tags in sentences:
        for c in chars:
            char_freq[c] = char_freq.get(c, 0) + 1
        tag_set.update(tags)

    char2id = {PAD: 0, UNK: 1}
    for c, freq in sorted(char_freq.items(), key=lambda x: (-x[1], x[0])):
        if freq >= min_freq:
            char2id[c] = len(char2id)

    # 标签表：把 O 放在最前，其余按字母序，保证可复现
    tags_sorted = ["O"] + sorted(t for t in tag_set if t != "O")
    tag2id = {t: i for i, t in enumerate(tags_sorted)}
    return char2id, tag2id


def save_vocab(path, char2id, tag2id):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"char2id": char2id, "tag2id": tag2id}, f, ensure_ascii=False, indent=2)


def load_vocab(path):
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d["char2id"], d["tag2id"]


class NERDataset(Dataset):
    def __init__(self, sentences, char2id, tag2id):
        self.data = sentences
        self.char2id = char2id
        self.tag2id = tag2id

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        chars, tags = self.data[idx]
        x = [self.char2id.get(c, self.char2id[UNK]) for c in chars]
        y = [self.tag2id[t] for t in tags]
        return x, y


def collate_fn(batch):
    """对一个 batch 做 padding，返回 x, y, mask, lengths（均为 tensor）。"""
    batch = sorted(batch, key=lambda b: len(b[0]), reverse=True)
    lengths = [len(x) for x, _ in batch]
    max_len = max(lengths)

    xs, ys, masks = [], [], []
    for x, y in batch:
        pad = max_len - len(x)
        xs.append(x + [0] * pad)
        ys.append(y + [0] * pad)           # padding 的标签随便填 0，靠 mask 屏蔽
        masks.append([1] * len(x) + [0] * pad)

    x = torch.tensor(xs, dtype=torch.long)
    y = torch.tensor(ys, dtype=torch.long)
    mask = torch.tensor(masks, dtype=torch.bool)
    lengths = torch.tensor(lengths, dtype=torch.long)
    return x, y, mask, lengths


def load_dataset(data_dir):
    """读取 train/dev/test 三个文件，返回句子列表的字典。"""
    data_dir = Path(data_dir)
    return {
        "train": read_bio(data_dir / "train.txt"),
        "dev": read_bio(data_dir / "dev.txt"),
        "test": read_bio(data_dir / "test.txt"),
    }
