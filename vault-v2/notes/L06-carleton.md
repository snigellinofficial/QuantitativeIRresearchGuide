---
id: L06
topic: L
short: "Carleton 等 2022"
authors: "Tamma Carleton; Amir Jina; Michael Delgado; Michael Greenstone; Trevor Houser"
year: 2022
title: "Valuing the Global Mortality Consequences of Climate Change Accounting for Adaptation Costs and Benefits"
venue: "The Quarterly Journal of Economics"
volume: "137(4)"
doi: "10.1093/qje/qjac020"
cites: 429
difficulty: 5
data_kind: "栅格"
design: "全局剂量反应＋结构外推"
unit: "全球次国家单元"
tags: [剂量反应, 死亡率, 适应, 外推]
---

# L06 Carleton 等 2022

## 一句话概括

用跨四十一国的面板估计统一的气温与死亡率反应函数。

## 研究设计

- **观测单元** 全球次国家单元。
- **处理变量** 取次国家单元的气温分布。
- **结果变量** 取死亡率。
- **识别逻辑** 剂量反应（dose-response）估计配合结构外推，适应由收入与技术刻画。

## 数据结构

- 气温栅格，空间属性为栅格。
- 次国家单元，空间属性为面。
- 死亡登记与调查，空间属性为点。

## 可迁移的做法

1. 把气温栅格按人口加权聚合。
2. 估计分单元的温度响应。
3. 用收入与技术解释响应差异。
4. 把函数外推到未来情景。

## 主要结论

- 收入水平决定温度响应的强度。
- 统一函数使跨国外推可行。

## 复制这项研究需要注意

- 死亡登记覆盖不全的国家须插补。
- 外推依赖适应速度的假设。

## 关联文献

- [[G03-donaldson]] 因为识别逻辑相同，两者同为结构模型，参数校准与估计的分工须说明。
- [[L01-dell]] 因为数据形态相同，两者同为栅格，边界像元的归属规则须对齐。
- [[L02-hsiang]] 因为互为稳健性检验，L02 的效应量可对照该文的剂量反应曲线。
- [[L03-dell]] 因为互为稳健性检验，L03 的增长结论给出该文温度响应的独立检验。
