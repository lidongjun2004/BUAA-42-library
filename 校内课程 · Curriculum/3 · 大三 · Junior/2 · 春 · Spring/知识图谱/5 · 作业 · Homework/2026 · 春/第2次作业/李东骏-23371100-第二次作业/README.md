# 第二次作业：TransE 知识图谱表示学习（FB15K237）

> 李东骏  23371100  ·  知识图谱课程

## 一、任务说明

知识图谱表示学习作业：**实现 TransE 模型在 FB15K237 数据集上的训练和推理**。
本作业基于清华大学自然语言处理实验室（刘知远、孙茂松团队）开源的
**OpenKE** 平台（<https://github.com/thunlp/OpenKE>）复现官方 TransE，
并在 FB15K237 的测试集上完成链接预测（link prediction）评测。

## 二、TransE 模型原理

TransE 把每个实体和关系都嵌入到同一个低维向量空间，核心假设是
**关系是头实体到尾实体的“平移”**：

```text
            h  +  r  ≈  t          （对成立的三元组 (h, r, t)）
```

- 打分（能量）函数：`f(h, r, t) = ||h + r − t||_{L1/L2}`，越小表示三元组越可信；
- 训练用 **margin-based ranking loss**（合页损失）拉开正例与负例的距离：

```text
  L = Σ_(h,r,t)∈正例 Σ_(h',r,t')∈负例  max(0,  γ + f(h,r,t) − f(h',r,t'))
```

其中 γ 是间隔超参；负例 `(h', r, t')` 由替换正例三元组的头或尾实体随机构造
（负采样）。每步训练对实体向量做 L2 归一化以防止向量无限增大。

> 直观理解：让正确三元组的 `h+r` 尽量靠近 `t`，错误三元组尽量远离，
> 从而学到能反映关系语义的实体/关系向量，服务于下游知识推理（链接预测）。

## 三、数据集 FB15K237

FB15K237 是 Freebase 的子集（去除了 FB15K 中的逆关系泄漏，更具挑战性）：

| 项目 | 数量 |
| --- | ---: |
| 实体数 | 14,541 |
| 关系数 | 237 |
| 训练三元组 | 272,115 |
| 验证三元组 | 17,535 |
| 测试三元组 | 20,466 |

数据位于 `OpenKE/benchmarks/FB15K237/`（OpenKE 自带，已转成 id 格式）。

## 四、文件结构

```text
李东骏-23371100-第二次作业/
├── train.py              # 训练 TransE 并保存 checkpoint，训练后自动评测（主入口）
├── test.py               # 载入 checkpoint 做链接预测，打印指标（截图用）
├── requirements.txt      # Python 依赖
├── checkpoint/           # 训练得到的 transe_fb15k237.ckpt
├── results/              # 训练日志、最终指标
└── OpenKE/               # OpenKE 官方代码（已精简，仅保留 FB15K237 与核心代码）
    ├── openke/           #   ├─ TransE 模型 / 训练器 / 评测器 / C++ 数据后端
    │   ├── make.sh       #   └─ 编译 C++ 后端的脚本
    │   └── release/Base.so   # 已为 macOS arm64 编译好的后端
    └── benchmarks/FB15K237/  # 数据集
```

## 五、环境准备

```bash
# 1) 安装 Python 依赖
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) 编译 OpenKE 的 C++ 数据后端（负采样 / 链接预测）
cd OpenKE/openke && bash make.sh && cd ../..
#   （本作业已编译好 OpenKE/openke/release/Base.so，arm64 mac 可直接用；
#     若在其它平台运行，请重新执行上面的 make.sh）
```

## 六、运行方式

```bash
# 训练（CPU，约 50 分钟）：dim=200, 250 轮, SGD lr=1.0, margin=5, neg_ent=25
python train.py

# 推理 + 打印评测指标（约 2 分钟）——“最终终端打印指标截图”运行这个
python test.py
```

训练超参（与 OpenKE 官方 `train_transe_FB15K237.py` 一致，轮数按本机算力调整）：

| 超参 | 取值 | 说明 |
| --- | --- | --- |
| dim | 200 | 实体/关系向量维度 |
| p_norm | 1 | 距离用 L1 范数 |
| margin γ | 5.0 | 合页损失间隔 |
| neg_ent | 25 | 每个正例负采样个数 |
| nbatches | 100 | 每轮 batch 数 |
| 负采样 | bern | 伯努利采样 |
| filter | 是 | 过滤已知三元组 |
| 优化器 | SGD, lr=1.0 | |
| train_times | 250 | 训练轮数 |

## 七、评测协议

链接预测（link prediction）：对每个测试三元组 `(h, r, t)`，分别遮住头实体和尾实体，
用所有实体去替换并按打分排序，看正确实体排在第几名。指标：

- **MRR**（Mean Reciprocal Rank，平均倒数排名）：越大越好；
- **MR**（Mean Rank，平均排名）：越小越好；
- **Hit@K**（正确实体排进前 K 的比例，K=1/3/10）：越大越好。

每个指标都有两种设置：

- **raw**：直接排名；
- **filter**：排序时过滤掉训练/验证/测试中本就存在的其它正确三元组（更公允，是主要参考指标）。

## 八、实验结果

> 以下为本次训练（250 轮）在 **FB15K237 测试集**上的链接预测结果（filter 设置，head/tail 平均）。
> 完整 raw / filter、head / tail 明细见 `results/test_result.txt`，**终端打印指标截图见 `链接预测指标截图.png`**。

<!-- RESULTS_TABLE_PLACEHOLDER -->

**主要指标（filter，head/tail 平均）：**

| 指标 | 数值 |
| --- | --- |
| **MRR** | **0.2840** |
| **MR** | **225.90** |
| **Hit@10** | **0.4713** |
| **Hit@3** | **0.3218** |
| **Hit@1** | **0.1883** |

**完整结果（raw vs filter，方向明细）：**

| 设置 | 方向 | MRR | MR | Hit@10 | Hit@3 | Hit@1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| raw | 预测头 l | 0.0887 | 562.68 | 0.2064 | 0.0861 | 0.0332 |
| raw | 预测尾 r | 0.2490 | 163.78 | 0.4386 | 0.2734 | 0.1555 |
| raw | **平均** | 0.1689 | 363.23 | 0.3225 | 0.1798 | 0.0943 |
| filter | 预测头 l | 0.1856 | 313.26 | 0.3540 | 0.2085 | 0.1022 |
| filter | 预测尾 r | 0.3825 | 138.54 | 0.5885 | 0.4351 | 0.2744 |
| filter | **平均** | **0.2840** | **225.90** | **0.4713** | **0.3218** | **0.1883** |

> 训练用时约 50 分钟（CPU，250 轮）；上表对应的终端原始输出见 `results/test_result.txt`、`results/train_run.log`。

**结果分析：** filter 设置下 Hit@10 ≈ **0.47**、MRR ≈ **0.28**，与 OpenKE 官方/原论文在
FB15K237 上报告的 TransE 水平（Hit@10 约 0.47、MRR 约 0.28）基本一致，复现成功。
可以看到「预测尾实体(r)」明显比「预测头实体(l)」容易（Hit@10 0.59 vs 0.35），
这是因为 Freebase 关系多为「一对多」（如 *出生地、国籍*），给定 (h, r) 推 t 的歧义更小。

## 九、说明

- 本作业复现的是 OpenKE 官方 TransE 实现；模型、训练器（`Trainer`）、评测器（`Tester`）
  及负采样/链接预测的 C++ 后端均来自 OpenKE，`train.py` / `test.py` 是按官方
  `examples/train_transe_FB15K237.py` 编写的训练与推理入口（本机无 GPU，已设 `use_gpu=False`）。
- 由于本机为 CPU（Apple Silicon，无 CUDA），训练轮数从官方的 1000 轮调整为 250 轮以控制时间；
  TransE 在 SGD(lr=1.0) 下收敛较快，250 轮已能得到合理的链接预测指标。
