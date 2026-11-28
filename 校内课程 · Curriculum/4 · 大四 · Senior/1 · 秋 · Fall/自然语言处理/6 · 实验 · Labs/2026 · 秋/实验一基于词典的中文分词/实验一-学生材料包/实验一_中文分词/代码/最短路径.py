"""最少词数的最短路径分词，保留去年函数名。"""
from 最大匹配 import dic, maxlen


def shortestPath(text):
    """每个合法词的代价为 1，单字也允许作为回退边。"""
    n = len(text)
    f = [n + 1] * (n + 1)
    previous = [-1] * (n + 1)
    f[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + maxlen) + 1):
            if j - i > 1 and text[i:j] not in dic:
                continue
            # TODO 4：候选代价是多少？何时更新 f[j] 和 previous[j]？
            # 只在代价严格变小时更新，保持确定的打平行为。
            raise NotImplementedError("请完成最短路径更新")
    # TODO 5：从 n 沿 previous 回到 0，取出词，再反转词列表。
    # 空字符串必须返回 []，不能使用 text[-1:0] 一类错误切片。
    raise NotImplementedError("请完成最短路径回溯")
