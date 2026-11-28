# -*- coding: utf-8 -*-
"""
复现 TransE（基于清华 OpenKE 官方实现）在 FB15K237 上的训练。

模型: TransE —— 把关系建模为头尾实体向量间的平移 h + r ≈ t，
打分函数 f(h,r,t) = -||h + r - t||_{L1/L2}，越大表示三元组越可信。

训练完成后保存 checkpoint 到 ./checkpoint/transe_fb15k237.ckpt，
并随即在测试集上做链接预测，打印 MRR / MR / Hit@10 / Hit@3 / Hit@1。

用法:
  python train.py                  # 标准配置: dim=200, 1000 epoch
  python train.py --train_times 500
"""
import argparse
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPENKE = HERE / "OpenKE"
sys.path.insert(0, str(OPENKE))

from openke.config import Trainer, Tester
from openke.data import TestDataLoader, TrainDataLoader
from openke.module.loss import MarginLoss
from openke.module.model import TransE
from openke.module.strategy import NegativeSampling


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(OPENKE / "benchmarks" / "FB15K237") + "/")
    ap.add_argument("--ckpt", default=str(HERE / "checkpoint" / "transe_fb15k237.ckpt"))
    ap.add_argument("--dim", type=int, default=200, help="实体/关系向量维度")
    ap.add_argument("--p_norm", type=int, default=1, help="距离范数 L1/L2")
    ap.add_argument("--margin", type=float, default=5.0, help="MarginLoss 间隔 γ")
    ap.add_argument("--neg_ent", type=int, default=25, help="每个正例的负采样个数")
    ap.add_argument("--nbatches", type=int, default=100)
    ap.add_argument("--train_times", type=int, default=1000, help="训练轮数")
    ap.add_argument("--alpha", type=float, default=1.0, help="学习率")
    ap.add_argument("--opt", default="sgd")
    ap.add_argument("--bern", type=int, default=1, help="是否用 bern 负采样")
    ap.add_argument("--use_gpu", action="store_true", help="本机无 CUDA，默认 CPU")
    ap.add_argument("--no_test", action="store_true", help="只训练并存档，不在末尾做链接预测")
    ap.add_argument("--save_steps", type=int, default=0, help=">0 时每隔若干轮存一次中间 checkpoint")
    ap.add_argument("--threads", type=int, default=0, help=">0 时设置 torch CPU 线程数")
    args = ap.parse_args()

    if args.threads > 0:
        import torch
        torch.set_num_threads(args.threads)

    Path(args.ckpt).parent.mkdir(parents=True, exist_ok=True)

    # ---------- 训练数据加载（C++ 后端，多线程负采样）----------
    train_dataloader = TrainDataLoader(
        in_path=args.data,
        nbatches=args.nbatches,
        threads=8,
        sampling_mode="normal",
        bern_flag=args.bern,
        filter_flag=1,
        neg_ent=args.neg_ent,
        neg_rel=0,
    )
    test_dataloader = TestDataLoader(args.data, "link")

    # ---------- 定义 TransE 模型 ----------
    transe = TransE(
        ent_tot=train_dataloader.get_ent_tot(),
        rel_tot=train_dataloader.get_rel_tot(),
        dim=args.dim,
        p_norm=args.p_norm,
        norm_flag=True,            # 每步对实体向量做 L2 归一化
    )
    print(f"[model] TransE  ent={train_dataloader.get_ent_tot()}  "
          f"rel={train_dataloader.get_rel_tot()}  dim={args.dim}  p_norm=L{args.p_norm}")

    # ---------- 负采样 + Margin 损失 ----------
    model = NegativeSampling(
        model=transe,
        loss=MarginLoss(margin=args.margin),
        batch_size=train_dataloader.get_batch_size(),
    )

    # ---------- 训练 ----------
    trainer = Trainer(
        model=model,
        data_loader=train_dataloader,
        train_times=args.train_times,
        alpha=args.alpha,
        opt_method=args.opt,
        use_gpu=args.use_gpu,
        save_steps=args.save_steps if args.save_steps > 0 else None,
        checkpoint_dir=str(Path(args.ckpt).with_suffix("")) if args.save_steps > 0 else None,
    )
    print(f"[train] train_times={args.train_times}  opt={args.opt}  lr={args.alpha}  "
          f"margin={args.margin}  neg_ent={args.neg_ent}  bern={args.bern}")
    t0 = time.time()
    trainer.run()
    print(f"[train] 训练完成，用时 {time.time() - t0:.1f}s")

    transe.save_checkpoint(args.ckpt)
    print(f"[train] checkpoint 已保存: {args.ckpt}")

    if args.no_test:
        print("[train] --no_test 已设置，跳过链接预测。")
        return

    # ---------- 训练后立即测试 ----------
    transe.load_checkpoint(args.ckpt)
    tester = Tester(model=transe, data_loader=test_dataloader, use_gpu=args.use_gpu)
    print("\n[test] 在 FB15K237 测试集上做链接预测（filter 设置即过滤掉训练/验证中已存在的三元组）...")
    mrr, mr, hit10, hit3, hit1 = tester.run_link_prediction(type_constrain=False)
    print("\n================ TransE / FB15K237 链接预测结果 (filter) ================")
    print(f"  MRR     = {mrr:.4f}")
    print(f"  MR      = {mr:.2f}")
    print(f"  Hit@10  = {hit10:.4f}")
    print(f"  Hit@3   = {hit3:.4f}")
    print(f"  Hit@1   = {hit1:.4f}")
    print("=======================================================================")


if __name__ == "__main__":
    main()
