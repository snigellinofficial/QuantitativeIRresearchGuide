---
id: A4
group: A
short: "Burgess, Jedwab, Miguel, Morjaria & Padró i Miquel 2015"
authors: "Robin Burgess, Rémi Jedwab, Edward Miguel, Ameet Morjaria, Gerard Padró i Miquel"
year: 2015
title: "The Value of Democracy: Evidence from Road Building in Kenya"
venue: "American Economic Review"
volume: "105(6)"
doi: "10.1257/AER.20131031"
cites: 657
unit: "肯尼亚道路分段（road segment）与相邻选区"
design: "双重差分"
tags: [双重差分, 路网, 族群政治, 公共品]
---

## 一句话概括

用肯尼亚民主化前后道路投资的族群倾斜变化，估计民主制度对公共品配置的价值。

## 研究设计

- 针对观测单元，取肯尼亚道路分段（road segment）与相邻选区。
- 针对处理变量，取选区是否与执政者同族群，以及与民主时期的交互。
- 针对结果变量，取道路铺装里程、道路等级提升与夜光。
- 针对识别逻辑，采用差分中的差分（difference-in-differences）。
- 民主化前后两组选区的投资差额发生变化，共同时间冲击被差分吸收。

## 数据结构

- 殖民时期与独立后的路网矢量，空间属性为线。
- 选举结果，空间属性为面，单元为选区。
- 族群分布图，空间属性为面。
- 道路投资支出记录，空间属性为表格记录，经选区挂接。

## 可迁移的做法

1. 把路网拆成独立分段，逐段记录几何与属性。
2. 用线段落入的选区做空间连接，得到分段的行政归属。
3. 把政治变量与民主时期虚拟变量相乘。
4. 报告不同空间权重下的估计，检验分段归属的敏感性。
5. 对族群边界的编码误差做模拟，重复估计。

## 主要结论

民主化之后，道路投资向执政者同族群选区的倾斜显著收窄。选举竞争压力是主要机制。

## 复制这项研究需要注意

- 道路分段的空间权重选择会改变结果。
- 族群边界的编码误差须做稳健性检验。

## 关联文献

- [[A2-michalopoulos]] 因为数据形态相同，A4 与 A2 的观测单元都是行政多边形，处理变量由几何叠加得到。
- [[B1-donaldson]] 因为数据形态相同，A4 与 B1 都把线状路网拆成分段，再与面状行政单元做连接。
- [[D4-hodler]] 因为识别逻辑相同，A4 与 D4 都用多层固定效应吸收水平差异，只留交互项变动。
