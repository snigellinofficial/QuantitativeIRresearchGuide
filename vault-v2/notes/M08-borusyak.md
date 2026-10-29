---
id: M08
topic: M
short: "Borusyak 等 2022"
authors: "Kirill Borusyak; Peter Hull; Xavier Jaravel"
year: 2022
title: "Quasi-Experimental Shift-Share Research Designs"
venue: "The Review of Economic Studies"
volume: "89(1)"
doi: "10.1093/restud/rdab030"
cites: 1190
difficulty: 4
data_kind: "混合"
design: "份额移动设计"
unit: "通用"
tags: [份额移动, 暴露度, 识别, 等价回归]
---

# M08 Borusyak 等 2022

## 一句话概括

把份额移动写成处理暴露度并给出识别条件。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取份额与移动项合成的暴露度。
- **结果变量** 取单元层面的结果变量。
- **识别逻辑** 份额移动（shift-share），以移动项的准外生性为识别条件。

## 数据结构

- 单元与份额矩阵，空间属性为混合。
- 移动项时间序列，按行业或地区排列。
- 暴露度表，按单元计算。

## 可迁移的做法

1. 构造份额矩阵与移动项。
2. 把暴露度写成两者乘积。
3. 检验移动项的准外生性。
4. 用等价回归实现估计。

## 主要结论

- 识别只需移动项外生，不要求份额外生。
- 等价回归形式便于实现与诊断。

## 复制这项研究需要注意

- 份额的内生性会经移动项进入误差。
- 移动项的加总层级影响标准误。

## 关联文献

- [[M01-callaway]] 因为数据形态相同，两者同为混合，不同形态变量的挂接顺序须对齐。
- [[M02-goodman-bacon]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
- [[M09-adao]] 因为互为稳健性检验，M09 的暴露度推断检验该文的标准误。
- [[M10-cameron]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
