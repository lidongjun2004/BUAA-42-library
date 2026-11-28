# 计算机系统基础 · 实验 · 计组-Cache调试 · 2026春 · Cache调试说明

| Reset | Data_in | MemRead | MemWrite | Tag | 组地址 | 块内地址 | Byte(补0) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 31 | [30:14] | 13 | 12 | [11:6] | [5:4] | [3:2] | [1:0] |

用十进制填写`data.csv`表格内容，运行`convert.py`可将表格转换为`ROM`命令`func.hex`

打开`debug.circ`，load你自己的`cache.circ`，导入`func.hex`到`ROM`，时钟运行即可
