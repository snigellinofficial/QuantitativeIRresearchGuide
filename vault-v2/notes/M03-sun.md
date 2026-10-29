---
id: M03
topic: M
short: "Sun & Abraham 2021"
authors: "Liyang Sun; Sarah Abraham"
year: 2021
title: "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects"
venue: "Journal of Econometrics"
volume: "225(2)"
doi: "10.1016/j.jeconom.2020.09.006"
cites: 5386
difficulty: 5
data_kind: "混合"
design: "交互加权事件研究"
unit: "通用"
tags: [事件研究, 异质性, 队列, 面板]
---

# M03 Sun & Abraham 2021

## 一句话概括

指出事件研究中污染系数的来源并给出修正估计量。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取相对处理时点的时间指标。
- **结果变量** 取各相对时点的处理效应。
- **识别逻辑** 交互加权事件研究，按队列与相对时点估计。

## 数据结构

- 单元与时期，空间属性为混合。
- 面板表，记录队列与相对时点。
- 队列份额表，按样本计算。

## 可迁移的做法

1. 按队列与相对时点构造交互项。
2. 只用干净对照估计。
3. 按队列份额加权汇总。
4. 报告修正前后的系数对比。

## 主要结论

- 传统事件研究系数混入了其它队列的效应。
- 修正估计量在异质效应下保持可解释。

## 复制这项研究需要注意

- 相对时点的窗口选择影响结论。
- 队列份额的估计须与样本一致。

## 关联文献

- [[G11-asher]] 因为识别逻辑相同，两者同为事件研究，事前系数的排列方式可以互相参照。
- [[M01-callaway]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
- [[M02-goodman-bacon]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
- [[M04-de-chaisemartin]] 因为互为稳健性检验，M04 的负权重诊断与该文的事件研究修正同源。
