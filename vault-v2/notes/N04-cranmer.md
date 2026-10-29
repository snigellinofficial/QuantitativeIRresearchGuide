---
id: N04
topic: N
short: "Cranmer & Desmarais 2011"
authors: "Skyler J. Cranmer; Bruce A. Desmarais"
year: 2011
title: "Inferential Network Analysis with Exponential Random Graph Models"
venue: "Political Analysis"
volume: "19(1)"
doi: "10.1093/pan/mpq037"
cites: 350
difficulty: 4
data_kind: "关系边"
design: "指数随机图模型"
unit: "国际组织成员网络"
tags: [指数随机图, 网络推断, 互惠, 成员网络]
---

# N04 Cranmer & Desmarais 2011

## 一句话概括

把整张图当因变量，用结构统计量建立似然。

## 研究设计

- **观测单元** 国际组织成员网络。
- **处理变量** 取网络的结构统计量，例如互惠与传递。
- **结果变量** 取观测到的整张网络。
- **识别逻辑** 指数随机图模型（exponential random graph model）。结构统计量定义边的联合分布。

## 数据结构

- 国际组织成员关系，空间属性为关系边。
- 国家属性，空间属性为面。
- 邻接矩阵，按国家对逐年构造。

## 可迁移的做法

1. 把成员关系写成二值邻接矩阵。
2. 选取互惠、传递与度数分布作为统计量。
3. 用伪似然或马尔可夫链估计参数。
4. 检验拟合优度。

## 主要结论

- 国际组织成员网络呈现互惠与聚类结构。
- 整图建模避免把边当作独立观测。

## 复制这项研究需要注意

- 退化问题使估计不稳定，须报告诊断。
- 网络统计量之间高度共线。

## 关联文献

- [[N07-maoz]] 因为数据形态相同，两者同为关系边，矩阵的阈值设定须同时报告。
- [[N09-cranmer]] 因为识别逻辑相同，两者同为指数随机图模型，退化诊断与拟合优度须一并报告。
- [[N10-kinne]] 因为数据形态相同，两者同为关系边，边的权重口径须逐项对照。
- [[N11-ward]] 因为数据形态相同，两者同为关系边，节点集合与边的方向须一致。
