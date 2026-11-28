import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "代码"))
import 最大匹配 as mm
import 最短路径 as sp
from 评测 import spans, evaluate, load_data

LEX = frozenset({"研究", "研究生", "生命", "命", "科学"})


class Base(unittest.TestCase):
    def check(self, module, name, text, expected, lex=LEX):
        with patch.multiple(module, dic=lex, maxlen=max(map(len, lex))):
            result = getattr(module, name)(text)
        self.assertEqual(result, expected)
        self.assertEqual("".join(result), text)


class TestFMM(Base):
    def test_empty(self): self.check(mm, "FMM", "", [])
    def test_single(self): self.check(mm, "FMM", "研", ["研"])
    def test_unknown(self): self.check(mm, "FMM", "未知", ["未", "知"])
    def test_direction(self): self.check(mm, "FMM", "研究生命科学", ["研究生", "命", "科学"])
    def test_punctuation(self): self.check(mm, "FMM", "研究，科学", ["研究", "，", "科学"])


class TestBMM(Base):
    def test_empty(self): self.check(mm, "BMM", "", [])
    def test_single(self): self.check(mm, "BMM", "研", ["研"])
    def test_unknown(self): self.check(mm, "BMM", "未知", ["未", "知"])
    def test_direction(self): self.check(mm, "BMM", "研究生命科学", ["研究", "生命", "科学"])
    def test_order(self): self.check(mm, "BMM", "科学研究", ["科学", "研究"])


class TestBM(unittest.TestCase):
    def test_fewer_forward(self): self.assertEqual(mm.BM(["研究"], ["研", "究"]), ["研究"])
    def test_fewer_backward(self): self.assertEqual(mm.BM(["研", "究"], ["研究"]), ["研究"])
    def test_singletons(self): self.assertEqual(mm.BM(["研究生", "命", "科学"], ["研究", "生命", "科学"]), ["研究", "生命", "科学"])
    def test_full_tie(self): self.assertEqual(mm.BM(["百年", "前"], ["百", "年前"]), ["百", "年前"])
    def test_empty(self): self.assertEqual(mm.BM([], []), [])


class TestShortest(Base):
    def test_empty(self): self.check(sp, "shortestPath", "", [])
    def test_single(self): self.check(sp, "shortestPath", "研", ["研"])
    def test_unknown(self): self.check(sp, "shortestPath", "未知", ["未", "知"])
    def test_example(self): self.check(sp, "shortestPath", "研究生命科学", ["研究", "生命", "科学"])
    def test_global(self): self.check(sp, "shortestPath", "abcdef", ["abc", "def"], frozenset({"abcd", "abc", "def"}))
    def test_backtrack(self): self.check(sp, "shortestPath", "科学研究", ["科学", "研究"])


class TestSupport(unittest.TestCase):
    def test_repeated_words_have_positions(self):
        self.assertEqual(spans(["我", "我"]), {(0, 1), (1, 2)})
    def test_word_metrics(self):
        result = evaluate([(1, "研究生命", ["研究", "生命"])], lambda t: ["研究生", "命"])
        self.assertEqual(result["f1"], 0)
    def test_data_alignment(self):
        self.assertEqual(len(load_data()), 1944)


if __name__ == "__main__":
    unittest.main()
