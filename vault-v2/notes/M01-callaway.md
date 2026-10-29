---
id: M01
topic: M
short: "Callaway & Sant'Anna 2021"
authors: "Brantly Callaway; Pedro H.C. Sant’Anna"
year: 2021
title: "Difference-in-Differences with multiple time periods"
venue: "Journal of Econometrics"
volume: "225(2)"
doi: "10.1016/j.jeconom.2020.12.001"
cites: 8785
difficulty: 5
data_kind: "混合"
design: "分组—时点稳健估计"
unit: "通用"
tags: [双重差分, 异质性, 分组, 面板]
---

# M01 Callaway & Sant'Anna 2021

## 一句话概括

用分组与处理时点定义的条件效应替代双向固定效应。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取处理组与处理时点的组合。
- **结果变量** 取各组合的平均处理效应。
- **识别逻辑** 分组—时点稳健估计，按队列构造对照。

## 数据结构

- 单元与时期，空间属性为混合。
- 面板表，记录首次处理时点。
- 对照池，按未处理与尚未处理划分。

## 可迁移的做法

1. 按首次处理时点分组。
2. 为每组选未处理或尚未处理的对照。
3. 估计组—时点效应并加权汇总。
4. 报告不同加权方案下的结果。

## 主要结论

- 双向固定效应在效应异质时不等权。
- 分组估计给出可解释的加权平均。

## 复制这项研究需要注意

- 对照组的选取依赖无预期假设。
- 处理时点须准确到时期。

## 关联文献

- [[M02-goodman-bacon]] 因为互为稳健性检验，M02 的分解解释该文为何改用分组估计。
- [[M03-sun]] 因为数据形态相同，两者同为混合，不同形态变量的挂接顺序须对齐。
- [[M04-de-chaisemartin]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
- [[M08-borusyak]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
