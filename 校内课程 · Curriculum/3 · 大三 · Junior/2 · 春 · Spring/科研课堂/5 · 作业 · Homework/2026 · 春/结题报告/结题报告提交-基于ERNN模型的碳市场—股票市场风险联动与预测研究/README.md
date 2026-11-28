# 基于 ERNN 模型的"碳市场—股票市场"风险联动与预测研究 — 结题报告提交包

**小组成员**：李东骏、赵鑫、赵君昊
**报名名称**：基于 ERNN 模型的碳市场—股票市场风险联动与预测研究
**数据区间**：2018-01-03 ~ 2025-12-15（2028 个交易日，日度）

## 目录结构

```text
.
├── 李东骏、赵鑫、赵君昊-基于ERNN模型的碳市场—股票市场风险联动与预测研究.pdf   # 结题报告（30 页）
├── code/    # 实证代码（step1~step8 流水线 + 绘图脚本）
├── data/    # 清洗后主数据 + 全部结果表（CSV）+ 图表（figs/）
└── README.md
```

## 报告章节（对应提交要求）

1. 引言（第一章）
2. 数据来源与描述（第二章）
3. 模型与方法（第三章：风险度量、L-ER、ERNN、基准模型、双损失评价指标）
4. 实证分析结果分析（第四章：联动识别、主对比、优劣剖析、区间校准）
5. 稳健性检验（第五章：剔除 COVID、网络结构、宏观控制、滚动窗口）
6. 结论与展望（第六章）
7. 参考文献

## 复现流程

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install numpy pandas torch scikit-learn quantile-forest statsmodels scipy matplotlib

# 已含清洗后主数据 data/master_data.csv，可从 step2 起复现全部结果
python code/step2_descriptive_and_linkage.py     # 描述统计 + 滚动相关 + Granger
python code/step2b_granger_robustness.py          # 风险层面 / 子样本期 Granger
python code/step3_ernn_model.py                   # ERNN 模型（自检）
python code/step4_baselines.py                    # L-ER / QRNN / QRF / Q-GBM
python code/step5_main_experiment.py              # 主实验（105 组 + DM 双口径）
python code/step5b_plot_results.py
python code/step6_robustness.py                   # 稳健性 A/B/C
python code/step6b_plot_robustness.py
python code/step7_quantile_coverage.py            # 区间校准
python code/step8_rolling_forecast.py             # 滚动窗口预测
python code/step8b_plot_rolling.py
```

从原始 xlsx 重跑 `step1_clean_data.py` 需另行同步约 2.3GB 原始数据集（EUA 期货 / MSCI / 宏观指标）；本提交包仅含清洗后主数据，足以复现 step2~step8 的全部结果。

## data/ 结果文件清单

| 文件 | 内容 |
| --- | --- |
| `master_data.csv` | 清洗后主数据（2028 行日度） |
| `desc_stats.csv` | 描述性统计（均值/标准差/偏度/峰度/JB/ADF） |
| `rolling_correlation.csv`、`granger_*.csv` | 滚动相关、价格/风险层面 Granger |
| `main_results.csv` | 主实验结果（105 行，含 Pinball/Expectile 损失、双 R²、RMSE、MAE） |
| `dm_test.csv` | 主回归 DM 检验（168 行 = 21 场景 × 4 基准 × 2 口径） |
| `robustness_a/b/c_*.csv` | 三类稳健性 |
| `rolling_forecast*.csv` | 滚动窗口预测（双口径） |
| `coverage_test.csv` | 90%/80%/50% 区间校准 |
| `figs/` | 全部 15 张图表（PNG） |
