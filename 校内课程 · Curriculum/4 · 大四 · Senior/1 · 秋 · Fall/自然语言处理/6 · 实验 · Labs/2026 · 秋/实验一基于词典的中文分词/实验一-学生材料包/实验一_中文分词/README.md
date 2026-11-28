# 实验一：最大匹配与最少分词

核心算法由学生填写，文件读取、评测和词云工具已提供。

## 1. 任务描述

1. 完成代码/最大匹配.py 中的 FMM、BMM、BM。
2. 完成代码/最短路径.py 中的 shortestPath 更新与回溯。
3. 在给定语料上比较四种方法的 P、R、F1。
4. 选取一本书的一章文字，用自己的分词结果去除停用词并制作词云。

核心分词只用 Python 标准库。Python 3.9 或以上即可。词云需安装 wordcloud，并提供中文字体。

## 2. 数据集与文件

| 位置 | 用途 |
| --- | --- |
| 词典/pku_training_words.utf8 | 原词典 |
| 待分词文件/corpus.txt | 原待分词语料 |
| 分词对比文件/gold.txt | 原人工分词对照 |
| 停用词/stop_word.txt | 词云过滤 |
| 我的文本/章节.txt | 学生上传的自选章节，UTF-8 编码 |
| 字体/中文字体.ttf | 学生上传的真实中文字体文件 |
| 代码/运行实验.py、评测.py、cloud.py | 已提供工具，无需重写 |
| 实验报告.md | 填写模板 |

## 3. 最大匹配算法

打开代码/最大匹配.py，依次完成三个 TODO。词典已读入 dic，maxlen 已算好。

- FMM 从左侧取最长候选，匹配失败就从右侧缩短，单字可回退。
- BMM 从右侧取最长候选，匹配失败就从左侧缩短，最后反转词列表。
- BM 先选词数少的结果，再选单字词少的结果，完全打平时选 BMM。

每完成一部分，就运行对应测试：

~~~bash
python -m unittest 测试.test_algorithms.TestFMM -v
python -m unittest 测试.test_algorithms.TestBMM -v
python -m unittest 测试.test_algorithms.TestBM -v
~~~

先看单句，再批量评测已完成的方法：

~~~bash
python 代码/运行实验.py --methods fmm bmm bimm --text "研究生命科学"
python 代码/运行实验.py --methods fmm bmm bimm
~~~

测试用微型词典不含“生命科学”，真实词典含该词，两个场景的正确输出可能不同。

## 4. 最少分词法（最短路径法）

打开代码/最短路径.py。合法词的代价都是 1，目标是词数最少。补齐更新与回溯：

- 候选代价来自 f[i] 加一。代价更小时更新 f[j]，同时记录从哪个位置来到 j。
- 从句末沿 previous 回到句首，取出词后反转列表。
- 每次返回都保留全部字符及原顺序，空字符串返回空列表。

~~~bash
python -m unittest 测试.test_algorithms.TestShortest -v
python -m unittest discover -s 测试 -v
python 代码/运行实验.py
~~~

全部完成后，应有24个测试通过。批量评价会生成结果/metrics.csv 与 metrics.json，四种方法各一行。

本次按“词在原句中的起止位置”计算 P/R/F1，不能只用“这个词是否出现”判正确。空行不作为句子，评价1944条非空文本。不同于此前整理版的词边界指标，数值不要混用。

选两句有分歧的文本，在报告中写出各方法结果并解释原因。可用 --line 查看原语料行号：

~~~bash
python 代码/运行实验.py --line 1034
~~~

## 5. 制作词云

上传自选章节到“我的文本”，上传有权使用的中文字体到“字体”。报告注明章节来源。没有准备文本时，可以先用代码/80周年阅兵讲话.txt 检查流程，正式作业使用自选章节。

~~~bash
python -m pip install -r 代码/requirements.txt
python 代码/cloud.py --text "我的文本/章节.txt" --font "字体/中文字体.ttf"
~~~

生成结果/wordcloud.png 与 word_frequencies.csv。cloud.py 已调用你完成的 BM(FMM(text), BMM(text))，不用 jieba 代替核心算法。
