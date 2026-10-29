---
id: F01
topic: F
short: "Chernozhukov 等 2018"
authors: "Victor Chernozhukov; Denis Chetverikov; Mert Demirer; Esther Duflo; Christian Hansen"
year: 2018
title: "Double/debiased machine learning for treatment and structural parameters"
venue: "The Econometrics Journal"
volume: "21(1)"
doi: "10.1111/ectj.12097"
cites: 3014
difficulty: 5
data_kind: "混合"
design: "双重机器学习"
unit: "通用"
tags: [双重机器学习, 正交矩, 交叉拟合, 高维]
---

# F01 Chernozhukov 等 2018

## 一句话概括

用交叉拟合与正交矩条件消除机器学习带来的正则化偏误。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取高维控制变量下的处理变量。
- **结果变量** 取结构参数，例如平均处理效应。
- **识别逻辑** 双重机器学习（double machine learning）。正交矩条件配合交叉拟合。

## 数据结构

- 单元与观测，空间属性为混合。
- 高维协变量矩阵，不依赖空间坐标。
- 折叠划分表，记录样本分组。

## 可迁移的做法

1. 把样本分成若干折叠。
2. 用机器学习分别拟合结果方程与处理方程。
3. 用正交矩构造估计方程。
4. 交叉拟合后汇总参数与标准误。

## 主要结论

- 正交化使参数估计恢复常规收敛速度。
- 交叉拟合消除过拟合带来的偏误。

## 复制这项研究需要注意

- 折叠数与学习器选择影响有限样本表现。
- 正交矩要求 nuisance 估计达到一定收敛速度。

## 关联文献

- [[F03-wager]] 因为识别逻辑相同，两者同为机器学习，样本外预测的验证方式须一致。
- [[F05-jean]] 因为识别逻辑相同，两者同为机器学习，超参数的选择须在训练集内完成。
- [[F06-athey]] 因为数据形态相同，两者同为混合，多源单元的连接键须一致。
- [[F08-blumenstock]] 因为识别逻辑相同，两者同为机器学习，训练集与评估集的切分须各自独立。
- [[F11-ratledge]] 因为互为稳健性检验，F11 的影像测量给出该文正交化的具体场景。
