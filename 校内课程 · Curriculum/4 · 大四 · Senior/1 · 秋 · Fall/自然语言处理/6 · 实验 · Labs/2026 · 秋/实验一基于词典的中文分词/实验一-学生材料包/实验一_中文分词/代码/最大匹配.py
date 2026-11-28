"""在去年最大匹配代码的函数接口上完成 TODO。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
dic = frozenset(
    x.strip() for x in (ROOT / "词典/pku_training_words.utf8")
    .read_text(encoding="utf-8").splitlines() if x.strip()
)
maxlen = max(map(len, dic))


def FMM(txt):
    """前向最大匹配。返回按原文顺序排列的词列表。"""
    # TODO 1：从左侧取最多 maxlen 个字符，不在词典时从右侧缩短。
    # 缩到单字即可输出，然后推进到下一段。空字符串返回 []。
    raise NotImplementedError("请完成 FMM")


def BMM(txt):
    """后向最大匹配。返回结果仍必须按原文顺序排列。"""
    # TODO 2：从右侧取最多 maxlen 个字符，不在词典时从左侧缩短。
    # 收集结果后反转列表。不要反转一个词内部的字符。
    raise NotImplementedError("请完成 BMM")


def BM(fmm, bmm):
    """双向消歧。fmm/bmm 均为正序词列表，沿用原稿打平规则。"""
    # TODO 3：先选词数少的，再选单字词少的。
    # 两项都相同时选 bmm，与去年原 BM 的最后一个分支一致。
    raise NotImplementedError("请完成 BM")
