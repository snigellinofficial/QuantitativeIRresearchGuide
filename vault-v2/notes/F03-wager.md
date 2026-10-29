---
id: F03
topic: F
short: "Wager & Athey 2018"
authors: "Stefan Wager; Susan Athey"
year: 2018
title: "Estimation and Inference of Heterogeneous Treatment Effects using Random Forests"
venue: "Journal of the American Statistical Association"
volume: "113(523)"
doi: "10.1080/01621459.2017.1319839"
cites: 2495
difficulty: 5
data_kind: "混合"
design: "因果森林"
unit: "通用"
tags: [因果森林, 异质性, 推断, 机器学习]
---

# F03 Wager & Athey 2018

## 一句话概括

把随机森林改造成异质处理效应的估计量并给出推断。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取处理变量与协变量。
- **结果变量** 取个体处理效应。
- **识别逻辑** 因果森林（causal forest），以局部矩条件构造估计。

## 数据结构

- 单元与观测，空间属性为混合。
- 协变量矩阵，不依赖空间坐标。
- 处理变量，按单元记录。

## 可迁移的做法

1. 用诚实分样本构造分割。
2. 在每个叶内估计局部效应。
3. 用影响函数给出标准误。
4. 检验异质性的显著性。

## 主要结论

- 异质性检验须与效应估计同时报告。
- 诚实分割减少选择偏误。

## 复制这项研究需要注意

- 小样本下区间覆盖不足。
- 协变量的测量误差会影响分割。

## 关联文献

- [[F01-chernozhukov]] 因为识别逻辑相同，两者同为机器学习，超参数的选择须在训练集内完成。
- [[F04-mullainathan]] 因为数据形态相同，两者同为混合，各源的年份覆盖须逐项核对。
- [[F08-blumenstock]] 因为识别逻辑相同，两者同为机器学习，样本外预测的验证方式须一致。
- [[F12-fiaschi]] 因为识别逻辑相同，两者同为机器学习，训练集与评估集的切分须各自独立。
