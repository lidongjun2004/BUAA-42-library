"""沿用去年词云任务，调用学生自己的双向分词结果。"""
import argparse
from collections import Counter
from pathlib import Path
from 最大匹配 import FMM, BMM, BM
from 评测 import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, type=Path, help="UTF-8 自选章节文本")
    parser.add_argument("--font", required=True, type=Path, help="真实中文字体文件")
    args = parser.parse_args()
    if not args.text.is_file() or not args.font.is_file():
        parser.error("--text 和 --font 必须指向已有文件")
    try:
        from wordcloud import WordCloud
    except ImportError:
        parser.error("请先运行 python -m pip install -r 代码/requirements.txt")
    text = "".join(args.text.read_text("utf-8-sig").split())
    try:
        words = BM(FMM(text), BMM(text))
    except NotImplementedError as exc:
        parser.error(str(exc))
    stopwords = set((ROOT / "停用词/stop_word.txt").read_text("utf-8").splitlines())
    counts = Counter(word for word in words if word not in stopwords and word.strip())
    if not counts:
        parser.error("过滤后没有词，请检查章节文本和停用词")
    out = ROOT / "结果"
    out.mkdir(exist_ok=True)
    WordCloud(
        font_path=str(args.font.resolve()), background_color="white",
        width=1200, height=800, random_state=42,
    ).generate_from_frequencies(counts).to_file(str(out / "wordcloud.png"))
    with (out / "word_frequencies.csv").open("w", encoding="utf-8-sig", newline="") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(sorted(counts.items(), key=lambda x: (-x[1], x[0])))
    print("已生成 结果/wordcloud.png 和 结果/word_frequencies.csv")


if __name__ == "__main__":
    main()
