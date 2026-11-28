"""统一按词的起止位置计算 P/R/F1，学生无需修改。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def spans(tokens):
    result, offset = set(), 0
    for word in tokens:
        if not isinstance(word, str) or not word:
            raise ValueError("词列表必须由非空字符串组成")
        result.add((offset, offset + len(word)))
        offset += len(word)
    return result


def load_data():
    raw = (ROOT / "待分词文件/corpus.txt").read_text("utf-8").splitlines()
    gold = (ROOT / "分词对比文件/gold.txt").read_text("utf-8").splitlines()
    if len(raw) != len(gold):
        raise ValueError("corpus 与 gold 行数不同")
    pairs = []
    for line_no, (text, line) in enumerate(zip(raw, gold), 1):
        text, words = text.strip(), line.split()
        if "".join(words) != text:
            raise ValueError(f"第 {line_no} 行原文与 gold 不一致")
        if text:
            pairs.append((line_no, text, words))
    return pairs


def evaluate(pairs, method):
    tp = predicted = expected = exact = 0
    for line_no, text, gold in pairs:
        words = method(text)
        if not isinstance(words, list) or "".join(words) != text:
            raise ValueError(f"第 {line_no} 行输出丢字、乱序或不是列表")
        p, g = spans(words), spans(gold)
        tp += len(p & g)
        predicted += len(p)
        expected += len(g)
        exact += int(words == gold)
    precision = tp / predicted if predicted else 0.0
    recall = tp / expected if expected else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision, "recall": recall, "f1": f1,
        "sentence_accuracy": exact / len(pairs) if pairs else 0.0,
        "sentences": len(pairs), "correct_words": tp,
        "predicted_words": predicted, "gold_words": expected,
    }
