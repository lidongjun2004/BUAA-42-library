"""电影评论的读取、划分和词编号。"""
from pathlib import Path
import hashlib
import json
import random
import string

import numpy as np

ROOT = Path(__file__).resolve().parent
PAD_ID = 0
UNK_ID = 1
SEED = 42


def tokenize(text):
    # 删去英文标点，转成小写，再按空白分词。
    return text.strip().translate(str.maketrans('', '', string.punctuation)).lower().split()


def encode(text, vocab, word_len):
    """返回长度为word_len的一维int32数组，长句截断，短句补0。"""
    # TODO 1  将文本转为长度固定的词编号数组。未知词用1，补齐用0。
    raise NotImplementedError("请完成任务1")


def load_rows(data_dir=ROOT / 'data' / 'rt-polaritydata'):
    rows = []
    for name, label in [('rt-polarity.neg', 0), ('rt-polarity.pos', 1)]:
        path = Path(data_dir) / name
        if not path.is_file():
            raise FileNotFoundError(f'缺少{path}。先运行python prepare_data.py。')
        lines = [s.strip() for s in path.read_text(encoding='cp1252').splitlines() if s.strip()]
        if len(lines) != 5331:
            raise ValueError(f'{name}应有5331条评论，实际{len(lines)}条。请使用随包正式数据。')
        rows.extend((text, label) for text in lines)
    return rows


def prepare_data(data_dir=ROOT / 'data' / 'rt-polaritydata'):
    rows = load_rows(data_dir)
    rng = random.Random(SEED)
    train_rows, valid_rows = [], []
    for label in (0, 1):
        group = [row for row in rows if row[1] == label]
        rng.shuffle(group)
        cut = int(len(group) * 0.7)
        train_rows.extend(group[:cut])
        valid_rows.extend(group[cut:])
    rng.shuffle(train_rows)
    rng.shuffle(valid_rows)
    # 只用训练集建立词表，0与1分别留给PAD和UNK。
    vocab = {'<PAD>': PAD_ID, '<UNK>': UNK_ID}
    for text, _ in train_rows:
        for word in tokenize(text):
            if word not in vocab:
                vocab[word] = len(vocab)
    word_len = max(5, max(len(tokenize(text)) for text, _ in train_rows))

    def arrays(selected_rows):
        x = np.stack([encode(text, vocab, word_len) for text, _ in selected_rows])
        y = np.asarray([label for _, label in selected_rows], dtype=np.int32)
        if x.min() < 0 or x.max() >= len(vocab):
            raise ValueError('词编号超出词表范围，请检查encode。')
        return x, y

    split_bytes = json.dumps([train_rows, valid_rows], ensure_ascii=False).encode('utf-8')
    info = {
        'seed': SEED, 'train_size': len(train_rows), 'valid_size': len(valid_rows),
        'vocab_size': len(vocab), 'word_len': word_len,
        'split_sha256': hashlib.sha256(split_bytes).hexdigest(),
    }
    return arrays(train_rows), arrays(valid_rows), vocab, info, valid_rows


if __name__ == '__main__':
    train, valid, vocab, info, _ = prepare_data()
    print(json.dumps(info, ensure_ascii=False, indent=2))
    print('训练输入', train[0].shape, '验证输入', valid[0].shape)
    print('首条编码', train[0][0].tolist())
