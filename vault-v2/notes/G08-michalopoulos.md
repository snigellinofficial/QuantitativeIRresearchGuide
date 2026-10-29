---
id: G08
topic: G
short: "Michalopoulos & Papaioannou 2014"
authors: "Stelios Michalopoulos; Elias Papaioannou"
year: 2014
title: "National Institutions and Subnational Development in Africa *"
venue: "The Quarterly Journal of Economics"
volume: "129(1)"
doi: "10.1093/qje/qjt029"
cites: 431
difficulty: 3
data_kind: "栅格"
design: "跨国界空间断点"
unit: "国界两侧网格"
tags: [国界, 断点, 制度, 栅格]
---

# G08 Michalopoulos & Papaioannou 2014

## 一句话概括

同一族群被国界切开，两侧制度不同而地理相同。

## 研究设计

- **观测单元** 国界两侧网格。
- **处理变量** 取网格所在国家的制度指标。
- **结果变量** 取夜光强度与家庭调查中的资产。
- **识别逻辑** 跨国界空间断点，带宽内配对同一族群的网格。国界段固定效应替代国家固定效应。

## 数据结构

- 夜光与人口栅格，空间属性为栅格。
- 国界与族群分布，空间属性为面。
- 网格质心，空间属性为点。

## 可迁移的做法

1. 按族群分布确定被国界切开的族群。
2. 在国界两侧取同带宽网格。
3. 以国界段固定效应吸收地理差异。
4. 比较两侧的制度指标与夜光。

## 主要结论

- 同一族群两侧的发展差异与国家制度对应。
- 带宽内的地理条件近似连续。

## 复制这项研究需要注意

- 国界位置与地形相关，连续性须检验。
- 夜光在低密度区易饱和，须剔除。

## 关联文献

- [[C12-sanchez-de-la-sierra]] 因为识别逻辑相同，两者同为空间断点，带宽内的协变量平衡须逐项检验。
- [[G02-dell]] 因为识别逻辑相同，两者同为空间断点，两侧样本的配对方式决定可比性。
- [[G07-michalopoulos]] 因为互为稳健性检验，G07 的族群边界构成该文国界配对的族群内部对照。
- [[G10-ahlfeldt]] 因为识别逻辑相同，两者同为空间断点，两侧样本的配对方式决定可比性。
