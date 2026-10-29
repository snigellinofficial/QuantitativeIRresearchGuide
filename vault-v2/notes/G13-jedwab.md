---
id: G13
topic: G
short: "Jedwab & Moradi 2016"
authors: "Rémi Jedwab; Alexander Moradi"
year: 2016
title: "The Permanent Effects of Transportation Revolutions in Poor Countries: Evidence from Africa"
venue: "Review of Economics and Statistics"
volume: "98(2)"
doi: "10.1162/rest_a_00540"
cites: 329
difficulty: 2
data_kind: "点"
design: "准外生路线的长期比较"
unit: "加纳城镇点位"
tags: [铁路, 殖民, 持久效应, 城镇]
---

# G13 Jedwab & Moradi 2016

## 一句话概括

用殖民路线的规划走向识别交通投资的持久影响。

## 研究设计

- **观测单元** 加纳城镇点位。
- **处理变量** 取城镇是否位于殖民铁路或公路沿线。
- **结果变量** 取当代城镇人口与夜光强度。
- **识别逻辑** 准外生路线由地形与殖民目标决定，规划走向与当代增长无关。

## 数据结构

- 城镇点位，空间属性为点。
- 殖民路线，空间属性为线，区分建成与规划。
- 夜光栅格，空间属性为栅格，作当代结果的补充。

## 可迁移的做法

1. 把殖民路线数字化并区分建成与规划。
2. 计算城镇到路线的距离。
3. 比较沿线与非沿线城镇的长期人口。
4. 以地形检验路线走向的外生性。

## 主要结论

- 沿线城镇的当代人口规模更大。
- 路线走向受地形约束，与当代增长无关。

## 复制这项研究需要注意

- 城镇点位的历史边界与当代行政区不一致。
- 路线改线的年代须逐段核对。

## 关联文献

- [[F10-aiken]] 因为数据形态相同，两者同为点，点位坐标的精度与去重规则须一致。
- [[G11-asher]] 因为数据形态相同，两者同为点，点位到单元的挂接规则须对齐。
- [[L09-bohra-mishra]] 因为数据形态相同，两者同为点，点的空间落位误差须报告。
