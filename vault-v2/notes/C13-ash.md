---
id: C13
topic: C
short: "Ash & Obradovich 2020"
authors: "Konstantin Ash; Nick Obradovich"
year: 2020
title: "Climatic Stress, Internal Migration, and Syrian Civil War Onset"
venue: "Journal of Conflict Resolution"
volume: "64(1)"
doi: "10.1177/0022002719864140"
cites: 75
difficulty: 2
data_kind: "栅格"
design: "中介分析＋面板"
unit: "叙利亚次国家区域"
tags: [气候, 迁移, 中介, 叙利亚]
---

# C13 Ash & Obradovich 2020

## 一句话概括

把气候压力经迁移传导到冲突的路径拆成两步。

## 研究设计

- **观测单元** 叙利亚次国家区域。
- **处理变量** 取区域的降水与温度异常。
- **结果变量** 取区域内的冲突发生与迁移流量。
- **识别逻辑** 中介分析（mediation analysis）配合面板固定效应。先估计气候对迁移，再估计迁移对冲突。

## 数据结构

- 气候栅格，空间属性为栅格。
- 次国家区域，空间属性为面。
- 迁移与冲突记录，空间属性为点与流。

## 可迁移的做法

1. 按区域聚合气候异常。
2. 估计气候对迁出率的第一段关系。
3. 估计迁入对冲突的第二段关系。
4. 报告间接效应与直接效应。

## 主要结论

- 气候压力与迁出率的变化相关。
- 迁移构成气候与冲突之间的中间环节。

## 复制这项研究需要注意

- 中介分析要求中间变量无遗漏，条件较强。
- 次国家区域的迁移数据覆盖不全。

## 关联文献

- [[C03-miguel]] 因为数据形态相同，两者同为栅格，边界像元的归属规则须对齐。
- [[L11-couttenier]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[S04-ilzetzki]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
