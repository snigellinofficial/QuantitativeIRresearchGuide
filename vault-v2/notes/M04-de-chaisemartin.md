---
id: M04
topic: M
short: "de Chaisemartin & D'Haultfoeuille 2020"
authors: "Clément de Chaisemartin; Xavier D’Haultfœuille"
year: 2020
title: "Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects"
venue: "American Economic Review"
volume: "110(9)"
doi: "10.1257/aer.20181169"
cites: 5215
difficulty: 5
data_kind: "混合"
design: "负权重诊断"
unit: "通用"
tags: [双重差分, 负权重, 诊断, 面板]
---

# M04 de Chaisemartin & D'Haultfoeuille 2020

## 一句话概括

证明双向固定效应估计量在效应异质时可能出现符号反转。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取处理状态的变化。
- **结果变量** 取双向固定效应系数。
- **识别逻辑** 负权重诊断，检验系数是否为凸组合。

## 数据结构

- 单元与时期，空间属性为混合。
- 面板表，记录处理状态路径。
- 权重表，按单元与时期计算。

## 可迁移的做法

1. 计算每个单元的权重。
2. 检查权重是否出现负值。
3. 报告负权重占的比重。
4. 用替代估计量重估。

## 主要结论

- 负权重会使系数与平均效应符号相反。
- 诊断可在估计之后直接执行。

## 复制这项研究需要注意

- 权重依赖处理路径的分布。
- 替代估计量在交错处理下定义不同。

## 关联文献

- [[M01-callaway]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
- [[M02-goodman-bacon]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
- [[M03-sun]] 因为互为稳健性检验，M03 的队列加权是该文负权重的规避方案。
- [[M09-adao]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
