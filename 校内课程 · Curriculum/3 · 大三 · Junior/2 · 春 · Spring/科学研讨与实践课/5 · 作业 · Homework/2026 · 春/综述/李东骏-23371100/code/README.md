# 代码复现:动态网络上策略与结构的共演化

最小可执行的 active linking + Fermi 模仿动力学模型,复现 Pacheco 2006 (PRL) 与 Leung 2024 等综述里关于「网络结构重连促进合作」的核心结论。

## 依赖

- Python 3.9+(实测 3.11.15)
- numpy >= 1.24
- networkx >= 3.0
- matplotlib >= 3.7

推荐用 `uv`(已经验证可跑):

```bash
uv venv .venv --python 3.11
source .venv/bin/activate
uv pip install numpy networkx matplotlib
```

或者用标准 venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy networkx matplotlib
```

## 运行

```bash
source .venv/bin/activate
python code/run_all.py
```

预期 wall time ≈ 60-80s(M 系列 Mac;Intel 大约 1.5-2x)。

跑完会得到:
- `figure/cooperation_vs_W.png`
- `figure/cooperation_vs_b_static_vs_dynamic.png`
- `figure/edge_type_evolution.png`
- `figure/cooperation_heatmap.png`
- `code/results.json`(所有数值结果)

## 文件结构

```
code/
  dynamics.py        # Population class + strategy_update + link_update + 单次仿真接口
  experiments.py     # 4 个图各自的实验函数 + assertions
  plot_utils.py      # 学术风格 matplotlib 配置 + 配色常量
  run_all.py         # 入口:依次跑 4 个实验,把图写到 ../figure/
  results.json       # 所有数值结果(run_all 跑完后生成)
  README.md          # 本文件
figure/              # 所有 300 dpi PNG
```

## 模型参数(全部在 `experiments.py::DefaultParameters` 集中定义)

| 参数 | 符号 | 取值 |
| --- | --- | --- |
| 节点数 | N | 100 |
| 初始 ER 平均度 | z | 6 |
| 初始合作者比例 | x₀ | 0.5 |
| 选择压力 | β | 1.0 |
| 边死亡概率(CC/CD/DD) | γ | (0.1, 0.8, 0.3) |
| 收益矩阵 | (R,S,T,P) | (1, 0, b, 0) |
| 每个参数点种子数 | num_seeds | 50 |
| 总步数 | total_steps | 5000 |
| 末尾平均窗口 | window | 1000 |
| 默认随机种子起点 | base_seed | 42 |

链路更新与策略更新的时间尺度比 W 通过 `p_link = W / (1+W)` 决定每步是 link update 还是 strategy update。

## 实验设定(每张图)

### 图 1:`cooperation_vs_W.png`
- 变量:`W ∈ {0, 0.1, 0.5, 1, 2, 5, 10, 20}`
- 固定:`b = 1.3`
- 50 seeds/点,5000 步,取后 1000 步均值;x 轴 log scale
- 期望:W 越大合作率越高(快速重连给合作者更多重组机会)

### 图 2:`cooperation_vs_b_static_vs_dynamic.png`
- 变量:`b ∈ {1.0, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0}`
- 两条曲线:`W = 0`(静态网络) vs `W = 10`(快速重连)
- 50 seeds/点
- 期望:动态网络在更大 b 区间维持合作

### 图 3:`edge_type_evolution.png`
- 单次代表性运行,`W = 5, b = 1.3, seed = 42`
- 记录每步三类边数量(CC/CD/DD) + 合作者比例
- 期望:CD 边数量被压低(γ_CD = 0.8 最高)

### 图 4:`cooperation_heatmap.png`(可选,已生成)
- 网格:`W ∈ {0.1, 0.5, 1, 2, 5, 10}` × `b ∈ {1.0, 1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 2.0}`
- 50 seeds/cell
- 期望:右下角(高 b 低 W)合作灭绝,左上角(低 b 高 W)合作占优

## 可复现性

- 随机数全程走 `numpy.random.default_rng(seed)`
- 每个 seed = `base_seed + index`,可直接复算单次结果
- 默认 `base_seed = 42`,可在 `experiments.py` 顶部修改

## 物理上界 sanity

每个实验函数完成后会自动 assert:
- 合作率 ∈ [0, 1]
- 标准差 ≥ 0
- 边数 ∈ [0, N(N-1)/2]

跑通即代表所有 sanity 通过。
