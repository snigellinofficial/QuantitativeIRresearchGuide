---
id: F06
topic: F
short: "Athey & Imbens 2019"
authors: "Susan Athey; Guido W. Imbens"
year: 2019
title: "Machine Learning Methods That Economists Should Know About"
venue: "Annual Review of Economics"
volume: "11(1)"
doi: "10.1146/annurev-economics-080217-053433"
cites: 999
difficulty: 1
data_kind: "混合"
design: "方法综述"
unit: "通用"
tags: [机器学习, 综述, 统计目标, 推断]
---

# F06 Athey & Imbens 2019

## 一句话概括

把机器学习方法按统计目标分类整理。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取方法的统计目标，例如预测、分类与异质性。
- **结果变量** 取方法适用的估计对象。
- **识别逻辑** 方法综述，按目标与假设归类。

## 数据结构

- 通用数据形态，空间属性为混合。
- 协变量矩阵与结果变量。
- 样本分割表，按折叠记录。

## 可迁移的做法

1. 按目标列出方法。
2. 标注每种方法的假设。
3. 给出交叉验证与样本分割的用法。
4. 整理与计量框架的接口。

## 主要结论

- 多数方法可归入少数统计目标。
- 样本分割是连接预测与推断的关键步骤。

## 复制这项研究需要注意

- 方法的适用条件常被忽略。
- 综述无法替代具体设计的识别论证。

## 关联文献

- [[F01-chernozhukov]] 因为数据形态相同，两者同为混合，不同形态变量的挂接顺序须对齐。
- [[F04-mullainathan]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
- [[M10-cameron]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
