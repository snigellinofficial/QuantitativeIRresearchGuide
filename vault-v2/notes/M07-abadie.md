---
id: M07
topic: M
short: "Abadie 2021"
authors: "Alberto Abadie"
year: 2021
title: "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects"
venue: "Journal of Economic Literature"
volume: "59(2)"
doi: "10.1257/jel.20191450"
cites: 1301
difficulty: 1
data_kind: "面"
design: "方法综述"
unit: "通用"
tags: [合成控制, 可行性, 推断, 综述]
---

# M07 Abadie 2021

## 一句话概括

系统整理合成控制的可行性条件与推断方式。

## 研究设计

- **观测单元** 通用。
- **处理变量** 取处理单元与对照池的构成。
- **结果变量** 取合成对照的拟合与推断。
- **识别逻辑** 方法综述，整理适用条件与诊断。

## 数据结构

- 单元与时期，空间属性为面。
- 面板表，含协变量与结果序列。
- 对照池表，记录候选单元。

## 可迁移的做法

1. 检查处理前的拟合优度。
2. 核对对照池的污染。
3. 选择推断方式。
4. 报告权重与敏感性。

## 主要结论

- 拟合优度不足时推断不可靠。
- 排列推断不依赖正态假设。

## 复制这项研究需要注意

- 对照池中受同一冲击的单元须剔除。
- 长期外推的可靠性下降。

## 关联文献

- [[M05-abadie]] 因为互为稳健性检验，M05 的安慰剂检验落实该文的可行性建议。
- [[M06-abadie]] 因为数据形态相同，两者同为面，单元内部的聚合权重须说明。
- [[M11-king]] 因为数据形态相同，两者同为面，单元重划须显式处理。
