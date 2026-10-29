---
id: F09
topic: F
short: "Wilkerson & Casas 2017"
authors: "John Wilkerson; Andreu Casas"
year: 2017
title: "Large-Scale Computerized Text Analysis in Political Science: Opportunities and Challenges"
venue: "Annual Review of Political Science"
volume: "20(1)"
doi: "10.1146/annurev-polisci-052615-025542"
cites: 241
difficulty: 1
data_kind: "关系边"
design: "文本计分与降维"
unit: "政治文本"
tags: [文本, 降维, 计分, 效度]
---

# F09 Wilkerson & Casas 2017

## 一句话概括

把大规模文本压缩成可回归的连续维度。

## 研究设计

- **观测单元** 政治文本。
- **处理变量** 取文本的词项分布。
- **结果变量** 取降维后的连续得分。
- **识别逻辑** 文本计分与降维，以监督或半监督方式定标。

## 数据结构

- 文档与词项，空间属性为关系边。
- 文本语料，按机构与年份归档。
- 外部指标表，用于检验得分。

## 可迁移的做法

1. 构造文档词项矩阵。
2. 用监督标签或种子词定标。
3. 降维得到连续得分。
4. 检验得分与外部指标的相关。

## 主要结论

- 降维得分可替代人工编码用于回归。
- 监督定标的效度高于纯无监督方法。

## 复制这项研究需要注意

- 语料的选择偏差会进入得分。
- 词表随时间的含义漂移须处理。

## 关联文献

- [[F02-grimmer]] 因为互为稳健性检验，F02 的人工校验比例约束该文得分的可信度。
- [[N10-kinne]] 因为数据形态相同，两者同为关系边，边的权重口径须逐项对照。
- [[N11-ward]] 因为数据形态相同，两者同为关系边，节点集合与边的方向须一致。
