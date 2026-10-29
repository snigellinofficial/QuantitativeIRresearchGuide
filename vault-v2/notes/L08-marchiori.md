---
id: L08
topic: L
short: "Marchiori 等 2012"
authors: "Luca Marchiori; Jean-François Maystadt; Ingmar Schumacher"
year: 2012
title: "The impact of weather anomalies on migration in sub-Saharan Africa"
venue: "Journal of Environmental Economics and Management"
volume: "63(3)"
doi: "10.1016/j.jeem.2012.02.001"
cites: 371
difficulty: 2
data_kind: "面"
design: "面板气象冲击"
unit: "撒哈拉以南国家—年"
tags: [迁移, 气象异常, 面板, 撒哈拉以南]
---

# L08 Marchiori 等 2012

## 一句话概括

把气象异常写成迁移率的解释变量。

## 研究设计

- **观测单元** 撒哈拉以南国家—年。
- **处理变量** 取国家—年的气象异常。
- **结果变量** 取迁出率。
- **识别逻辑** 面板气象冲击配合国家固定效应。

## 数据结构

- 国家与年份，空间属性为面。
- 气候栅格，空间属性为栅格。
- 迁移流量表，按国家对整理。

## 可迁移的做法

1. 按国界聚合气象异常。
2. 放入国家与年固定效应。
3. 分气候带估计响应。
4. 检验迁出与工资的关系。

## 主要结论

- 气象异常与迁出率的变化相关。
- 响应在不同气候带之间差异明显。

## 复制这项研究需要注意

- 迁移流量按目的地统计，来源国口径须对齐。
- 气象异常的基期选择影响结果。

## 关联文献

- [[C06-hegre]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
- [[L04-barreca]] 因为识别逻辑相同，两者同为面板，时间间隔的设定改变变动项的均值。
- [[L05-deschenes]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[L10-missirian]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
