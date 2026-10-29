---
id: M10
topic: M
short: "Cameron 等 2011"
authors: "A. Colin Cameron; Jonah B. Gelbach; Douglas L. Miller"
year: 2011
title: "Robust Inference With Multiway Clustering"
venue: "Journal of Business & Economic Statistics"
volume: "29(2)"
doi: "10.1198/jbes.2010.07136"
cites: 2583
difficulty: 5
data_kind: "混合"
design: "多维聚类"
unit: "通用"
tags: [聚类, 标准误, 推断, 方差]
---

# M10 Cameron 等 2011

## 一句话概括

给出双向与多维聚类的三明治方差估计量。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取聚类的维度组合。
- **结果变量** 取系数标准误。
- **识别逻辑** 多维聚类，按交叠维度调整方差。

## 数据结构

- 单元与观测，空间属性为混合。
- 多个分组标识，按单元记录。
- 聚类维度表，记录每维的组数。

## 可迁移的做法

1. 确定相关性的来源维度。
2. 按每个维度单独聚类。
3. 用包含与排除公式合并。
4. 检查聚类数是否足够。

## 主要结论

- 单向聚类会低估交叠维度的方差。
- 合并公式在维度独立时近似成立。

## 复制这项研究需要注意

- 聚类数少时渐近近似失效。
- 维度选择须有实质理由。

## 关联文献

- [[F04-mullainathan]] 因为数据形态相同，两者同为混合，不同形态变量的挂接顺序须对齐。
- [[F06-athey]] 因为数据形态相同，两者同为混合，不同形态变量的挂接顺序须对齐。
- [[M08-borusyak]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
- [[M09-adao]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
