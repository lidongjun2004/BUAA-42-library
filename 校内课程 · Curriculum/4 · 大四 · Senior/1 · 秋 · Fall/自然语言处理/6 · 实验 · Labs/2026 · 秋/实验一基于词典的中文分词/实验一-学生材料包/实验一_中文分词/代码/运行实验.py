"""从实验根目录运行。支持分阶段完成算法后逐个评价。"""
import argparse
import csv
import json
import sys
from pathlib import Path
from 最大匹配 import FMM, BMM, BM
from 最短路径 import shortestPath
from 评测 import ROOT, evaluate, load_data

METHODS = {
    "fmm": FMM, "bmm": BMM,
    "bimm": lambda text: BM(FMM(text), BMM(text)),
    "shortest": shortestPath,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", nargs="+", choices=METHODS, default=list(METHODS))
    parser.add_argument("--text", help="只查看一个自选句子的切分")
    parser.add_argument("--line", type=int, help="查看 corpus 原始行号及其 gold")
    args = parser.parse_args()
    try:
        if args.text is not None or args.line is not None:
            text, gold = args.text, None
            if args.line is not None:
                case = next((p for p in load_data() if p[0] == args.line), None)
                if case is None:
                    raise ValueError("该行号不存在或是空行")
                _, text, gold = case
            print("原文", text)
            if gold is not None:
                print("gold", " / ".join(gold))
            for name in args.methods:
                print(name, " / ".join(METHODS[name](text)))
            return
        pairs = load_data()
        rows = []
        for name in args.methods:
            values = evaluate(pairs, METHODS[name])
            rows.append({"method": name, **values})
            print(name, " ".join(f"{k}={values[k]:.4f}" for k in
                                ("precision", "recall", "f1")))
        out = ROOT / "结果"
        out.mkdir(exist_ok=True)
        # 每组方法独立命名，单方法运行不会覆盖完整四方法结果。
        stem = "metrics" if args.methods == list(METHODS) else "metrics_" + "_".join(args.methods)
        with (out / (stem + ".csv")).open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        (out / (stem + ".json")).write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print("结果已保存至", out / (stem + ".csv"))
    except NotImplementedError as exc:
        print("该部分尚未完成：", exc, file=sys.stderr)
        raise SystemExit(2)
    except ValueError as exc:
        print("检查失败：", exc, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
