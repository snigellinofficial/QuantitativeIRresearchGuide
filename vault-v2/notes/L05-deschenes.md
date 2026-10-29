---
id: L05
topic: L
short: "Deschenes & Greenstone 2011"
authors: "Olivier Deschênes; Michael Greenstone"
year: 2011
title: "Climate Change, Mortality, and Adaptation: Evidence from Annual Fluctuations in Weather in the US"
venue: "American Economic Journal: Applied Economics"
volume: "3(4)"
doi: "10.1257/app.3.4.152"
cites: 596
difficulty: 2
data_kind: "面"
design: "面板气象冲击"
unit: "美国县—年"
tags: [气温, 死亡率, 面板, 县]
---

# L05 Deschenes & Greenstone 2011

## 一句话概括

用年度天气波动识别气温对死亡率的因果效应。

## 研究设计

- **观测单元** 美国县—年。
- **处理变量** 取县—年的气温与降水分布。
- **结果变量** 取县—年的死亡率。
- **识别逻辑** 面板气象冲击，以年际波动识别。

## 数据结构

- 县与年份，空间属性为面。
- 气象栅格，空间属性为栅格。
- 气象站点，空间属性为点，用于插值。

## 可迁移的做法

1. 把气象站数据插值到县。
2. 构造温度分箱与降水项。
3. 放入县与年固定效应。
4. 按年龄组估计响应。

## 主要结论

- 极端高温提高死亡率。
- 响应在老年组更强。

## 复制这项研究需要注意

- 气象插值误差在山区更大。
- 县界变动影响面板平衡。

## 关联文献

- [[L03-dell]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
- [[L04-barreca]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[L07-cattaneo]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[L08-marchiori]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
