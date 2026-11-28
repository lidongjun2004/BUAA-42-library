# -*- coding: utf-8 -*-
"""
BiLSTM-CRF 命名实体识别 —— 训练 + 评估主脚本。

流程:
  1. 读取 ResumeNER (BIO) 训练/验证/测试集；
  2. 由训练集构建字表与标签表；
  3. 训练 BiLSTM-CRF，每轮在 dev 上用实体级 F1 评估，保存最优模型(早停)；
  4. 载入最优模型，在 test 上输出实体级 Precision / Recall / F1 及各类别明细。

用法:
  python train.py                 # 用默认超参完整训练并评估
  python train.py --epochs 40     # 自定义
"""
import argparse
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from dataset import (NERDataset, build_vocab, collate_fn, load_dataset,
                     save_vocab)
from model import BiLSTM_CRF

from seqeval.metrics import (classification_report, f1_score, precision_score,
                             recall_score)

HERE = Path(__file__).resolve().parent


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def ids_to_tags(id_seqs, id2tag):
    return [[id2tag[i] for i in seq] for seq in id_seqs]


@torch.no_grad()
def evaluate(model, loader, id2tag, device):
    """在给定数据集上做预测，返回 (precision, recall, f1, 金标签, 预测标签)。"""
    model.eval()
    y_true, y_pred = [], []
    for x, y, mask, lengths in loader:
        x, mask = x.to(device), mask.to(device)
        pred = model.predict(x, mask, lengths.to(device))   # List[List[int]]
        for i, seq in enumerate(pred):
            n = lengths[i].item()
            gold = y[i, :n].tolist()
            y_true.append([id2tag[t] for t in gold])
            y_pred.append([id2tag[t] for t in seq])
    p = precision_score(y_true, y_pred)
    r = recall_score(y_true, y_pred)
    f = f1_score(y_true, y_pred)
    return p, r, f, y_true, y_pred


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default=str(HERE / "data_ner"))
    ap.add_argument("--ckpt_dir", default=str(HERE / "checkpoints"))
    ap.add_argument("--result_dir", default=str(HERE / "results"))
    ap.add_argument("--emb_dim", type=int, default=128)
    ap.add_argument("--hidden_dim", type=int, default=256)
    ap.add_argument("--num_layers", type=int, default=1)
    ap.add_argument("--dropout", type=float, default=0.5)
    ap.add_argument("--batch_size", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--weight_decay", type=float, default=1e-5)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--patience", type=int, default=8)
    ap.add_argument("--clip", type=float, default=5.0)
    ap.add_argument("--min_freq", type=int, default=1)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cpu", choices=["cpu", "mps", "cuda"])
    args = ap.parse_args()

    set_seed(args.seed)
    device = torch.device(args.device)
    Path(args.ckpt_dir).mkdir(parents=True, exist_ok=True)
    Path(args.result_dir).mkdir(parents=True, exist_ok=True)

    # ---------- 数据 ----------
    print(f"[data] 读取数据集: {args.data_dir}")
    data = load_dataset(args.data_dir)
    char2id, tag2id = build_vocab(data["train"], min_freq=args.min_freq)
    id2tag = {i: t for t, i in tag2id.items()}
    save_vocab(Path(args.ckpt_dir) / "vocab.json", char2id, tag2id)
    print(f"[data] 句子数  train={len(data['train'])} dev={len(data['dev'])} test={len(data['test'])}")
    print(f"[data] 字表大小={len(char2id)}  标签数={len(tag2id)}  标签={list(tag2id)}")

    train_loader = DataLoader(NERDataset(data["train"], char2id, tag2id),
                              batch_size=args.batch_size, shuffle=True, collate_fn=collate_fn)
    dev_loader = DataLoader(NERDataset(data["dev"], char2id, tag2id),
                            batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn)
    test_loader = DataLoader(NERDataset(data["test"], char2id, tag2id),
                             batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn)

    # ---------- 模型 ----------
    model = BiLSTM_CRF(
        vocab_size=len(char2id), num_tags=len(tag2id),
        emb_dim=args.emb_dim, hidden_dim=args.hidden_dim,
        num_layers=args.num_layers, dropout=args.dropout, pad_idx=0,
    ).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] BiLSTM-CRF 参数量={n_params:,}  device={device}")
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # ---------- 训练 ----------
    best_f1, best_epoch, no_improve = 0.0, 0, 0
    history = []
    ckpt_path = Path(args.ckpt_dir) / "best_model.pt"
    t0 = time.time()
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss, n_batch = 0.0, 0
        for x, y, mask, lengths in train_loader:
            x, y, mask, lengths = x.to(device), y.to(device), mask.to(device), lengths.to(device)
            optimizer.zero_grad()
            loss = model.neg_log_likelihood(x, y, mask, lengths)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)
            optimizer.step()
            total_loss += loss.item()
            n_batch += 1
        avg_loss = total_loss / max(n_batch, 1)

        p, r, f, _, _ = evaluate(model, dev_loader, id2tag, device)
        history.append({"epoch": epoch, "loss": avg_loss, "dev_p": p, "dev_r": r, "dev_f1": f})
        print(f"[epoch {epoch:02d}] loss={avg_loss:.4f}  dev: P={p:.4f} R={r:.4f} F1={f:.4f}"
              + ("  *最优" if f > best_f1 else ""))

        if f > best_f1:
            best_f1, best_epoch, no_improve = f, epoch, 0
            torch.save(model.state_dict(), ckpt_path)
        else:
            no_improve += 1
            if no_improve >= args.patience:
                print(f"[early-stop] dev F1 已 {args.patience} 轮无提升，停止训练。")
                break
    train_time = time.time() - t0
    print(f"[train] 完成，用时 {train_time:.1f}s，最优 dev F1={best_f1:.4f} (epoch {best_epoch})")

    # ---------- 测试集评估 ----------
    model.load_state_dict(torch.load(ckpt_path, map_location=device))
    p, r, f, y_true, y_pred = evaluate(model, test_loader, id2tag, device)
    report = classification_report(y_true, y_pred, digits=4)
    print("\n" + "=" * 60)
    print("测试集 (test.txt) 实体级评估结果")
    print("=" * 60)
    print(f"Precision = {p:.4f}")
    print(f"Recall    = {r:.4f}")
    print(f"F1-score  = {f:.4f}")
    print("-" * 60)
    print(report)

    # ---------- 保存结果 ----------
    with open(Path(args.result_dir) / "train_history.json", "w", encoding="utf-8") as fp:
        json.dump(history, fp, ensure_ascii=False, indent=2)
    with open(Path(args.result_dir) / "test_metrics.txt", "w", encoding="utf-8") as fp:
        fp.write("BiLSTM-CRF ResumeNER 测试集实体级评估\n")
        fp.write(f"best_dev_f1={best_f1:.4f} (epoch {best_epoch}), train_time={train_time:.1f}s\n")
        fp.write(f"test Precision={p:.4f}  Recall={r:.4f}  F1={f:.4f}\n")
        fp.write("-" * 60 + "\n")
        fp.write(report + "\n")
    print(f"\n[done] 训练历史与测试指标已写入: {args.result_dir}")


if __name__ == "__main__":
    main()
