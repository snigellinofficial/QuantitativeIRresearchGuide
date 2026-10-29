---
id: G14
topic: G
short: "Lipscomb 等 2013"
authors: "Molly Lipscomb; A. Mushfiq Mobarak; Tania Barham"
year: 2013
title: "Development Effects of Electrification: Evidence from the Topographic Placement of Hydropower Plants in Brazil"
venue: "American Economic Journal: Applied Economics"
volume: "5(2)"
doi: "10.1257/app.5.2.200"
cites: 193
difficulty: 3
data_kind: "混合"
design: "工具变量"
unit: "巴西自治市"
tags: [电气化, 水电, 工具变量, 自治市]
---

# G14 Lipscomb 等 2013

## 一句话概括

以河流落差代理发电潜力，作为电网落点的工具。

## 研究设计

- **观测单元** 巴西自治市。
- **处理变量** 取自治市是否接入电网。
- **结果变量** 取普查中的教育、就业与耐用消费品。
- **识别逻辑** 工具变量取河流落差与到水电厂的距离，通电时点由此预测。

## 数据结构

- 河流线，空间属性为线。
- 高程栅格，空间属性为栅格，用于计算落差。
- 自治市边界，空间属性为面。

## 可迁移的做法

1. 由高程栅格计算河段落差。
2. 把落差聚合到自治市。
3. 用落差预测通电时点。
4. 以预测值估计发展结果。

## 主要结论

- 落差大的自治市更早通电。
- 通电与教育、就业指标改善并存。

## 复制这项研究需要注意

- 落差工具可能经农业与运输渠道影响结果。
- 自治市边界变动须固定版本。

## 关联文献

- [[C03-miguel]] 因为识别逻辑相同，两者同为工具变量，排除限制是两端共同的薄弱环节。
- [[G04-baum-snow]] 因为识别逻辑相同，两者同为工具变量，第一阶段强度须在分组样本中复核。
- [[G05-faber]] 因为识别逻辑相同，两者同为工具变量，排除限制是两端共同的薄弱环节。
- [[G09-dinkelman]] 因为互为稳健性检验，G09 的坡度工具与该文的落差工具同属地形外生变量。
