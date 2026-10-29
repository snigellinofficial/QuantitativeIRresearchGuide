---
id: F02
topic: F
short: "Grimmer & Stewart 2013"
authors: "Justin Grimmer; Brandon M. Stewart"
year: 2013
title: "Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts"
venue: "Political Analysis"
volume: "21(3)"
doi: "10.1093/pan/mps028"
cites: 2580
difficulty: 1
data_kind: "关系边"
design: "文本编码与效度检验"
unit: "政治文本"
tags: [文本, 效度, 编码, 测量]
---

# F02 Grimmer & Stewart 2013

## 一句话概括

提出文本分类必须做人工验证与效度检查。

## 研究设计

- **观测单元** 政治文本。
- **处理变量** 取文本的自动分类结果。
- **结果变量** 取人工编码的参照标签。
- **识别逻辑** 文本编码配合效度检验，以人工编码为参照。

## 数据结构

- 文档与词项，空间属性为关系边。
- 文本语料，按时间与来源归档。
- 人工编码样本，作为验证集。

## 可迁移的做法

1. 定义编码类目与规则。
2. 抽取样本做人工编码。
3. 比较自动分类与人工标签。
4. 报告一致性与误差来源。

## 主要结论

- 自动方法的效度须以人工编码为参照。
- 无监督结果需要验证才能用于测量。

## 复制这项研究需要注意

- 人工编码的一致性决定验证的上限。
- 语料的时间跨度影响词表稳定性。

## 关联文献

- [[F09-wilkerson]] 因为互为稳健性检验，F09 的降维得分是该文人工验证对象的规模化版本。
- [[I02-abbott]] 因为识别逻辑相同，两者同为概念编码，条款与实际做法的差距须交代。
- [[I09-tallberg]] 因为识别逻辑相同，两者同为文本方法，类目定义的一致性须同时报告。
- [[S12-cha]] 因为数据形态相同，两者同为关系边，节点集合与边的方向须一致。
