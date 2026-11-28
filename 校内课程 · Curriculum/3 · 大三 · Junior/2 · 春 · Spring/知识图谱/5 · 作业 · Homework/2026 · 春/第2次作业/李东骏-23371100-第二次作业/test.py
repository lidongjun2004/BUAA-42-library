# -*- coding: utf-8 -*-
"""
载入已训练好的 TransE checkpoint，在 FB15K237 测试集上做链接预测（推理），
打印标准评测指标：MRR / MR / Hit@10 / Hit@3 / Hit@1（raw 与 filter 两种设置）。

这是「提交：最终终端打印指标截图」对应的脚本——运行它即可在终端看到指标。

用法:
  python test.py                       # 用 ./checkpoint/transe_fb15k237.ckpt
  python test.py --type_constrain      # 额外使用类型约束评测
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPENKE = HERE / "OpenKE"
sys.path.insert(0, str(OPENKE))

from openke.config import Tester
from openke.data import TestDataLoader
from openke.module.model import TransE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(OPENKE / "benchmarks" / "FB15K237") + "/")
    ap.add_argument("--ckpt", default=str(HERE / "checkpoint" / "transe_fb15k237.ckpt"))
    ap.add_argument("--dim", type=int, default=200)
    ap.add_argument("--p_norm", type=int, default=1)
    ap.add_argument("--type_constrain", action="store_true")
    ap.add_argument("--use_gpu", action="store_true")
    args = ap.parse_args()

    if not Path(args.ckpt).exists():
        sys.exit(f"[error] 找不到 checkpoint: {args.ckpt}\n请先运行 python train.py 进行训练。")

    test_dataloader = TestDataLoader(args.data, "link")

    transe = TransE(
        ent_tot=test_dataloader.get_ent_tot(),
        rel_tot=test_dataloader.get_rel_tot(),
        dim=args.dim,
        p_norm=args.p_norm,
        norm_flag=True,
    )
    transe.load_checkpoint(args.ckpt)
    print(f"[test] 已载入 checkpoint: {args.ckpt}")
    print(f"[test] TransE  ent={test_dataloader.get_ent_tot()}  "
          f"rel={test_dataloader.get_rel_tot()}  dim={args.dim}  p_norm=L{args.p_norm}")

    tester = Tester(model=transe, data_loader=test_dataloader, use_gpu=args.use_gpu)
    print("\n[test] FB15K237 测试集链接预测进行中（OpenKE C++ 后端会打印 raw / filter 指标表）...\n")
    mrr, mr, hit10, hit3, hit1 = tester.run_link_prediction(type_constrain=args.type_constrain)

    tag = "type-constrain" if args.type_constrain else "filter"
    print("\n============ TransE / FB15K237 链接预测最终指标 ({}) ============".format(tag))
    print(f"  MRR     = {mrr:.4f}   (平均倒数排名, 越大越好)")
    print(f"  MR      = {mr:.2f}   (平均排名, 越小越好)")
    print(f"  Hit@10  = {hit10:.4f}")
    print(f"  Hit@3   = {hit3:.4f}")
    print(f"  Hit@1   = {hit1:.4f}")
    print("================================================================")


if __name__ == "__main__":
    main()
