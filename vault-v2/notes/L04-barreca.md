---
id: L04
topic: L
short: "Barreca 等 2016"
authors: "Alan Barreca; Karen Clay; Olivier Deschenes; Michael Greenstone; Joseph S. Shapiro"
year: 2016
title: "Adapting to Climate Change: The Remarkable Decline in the US Temperature-Mortality Relationship over the Twentieth Century"
venue: "Journal of Political Economy"
volume: "124(1)"
doi: "10.1086/684582"
cites: 777
difficulty: 2
data_kind: "面"
design: "长期面板＋技术变迁"
unit: "美国州—年"
tags: [温度, 死亡率, 适应, 长期面板]
---

# L04 Barreca 等 2016

## 一句话概括

证明温度与死亡率关系的下降来自适应技术。

## 研究设计

- **观测单元** 美国州—年。
- **处理变量** 取州—年的温度分布。
- **结果变量** 取全因死亡率。
- **识别逻辑** 长期面板，比较不同年代的温度响应。

## 数据结构

- 州与年份，空间属性为面。
- 气象站点，空间属性为点。
- 技术变量，按年份挂到州。

## 可迁移的做法

1. 按州与年整理死亡率。
2. 构造温度分箱。
3. 分年代估计响应曲线。
4. 把空调普及作为适应变量。

## 主要结论

- 温度与死亡率的关系随年代减弱。
- 空调普及与响应减弱同步。

## 复制这项研究需要注意

- 医疗技术进步与空调普及难以分离。
- 死亡率编码口径在世纪中调整。

## 关联文献

- [[L03-dell]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
- [[L05-deschenes]] 因为识别逻辑相同，两者同为面板，时间间隔的设定改变变动项的均值。
- [[L07-cattaneo]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[L08-marchiori]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
