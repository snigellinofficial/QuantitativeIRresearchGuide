---
id: F07
topic: F
short: "Chen & Nordhaus 2011"
authors: "Xi Chen; William D. Nordhaus"
year: 2011
title: "Using luminosity data as a proxy for economic statistics"
venue: "Proceedings of the National Academy of Sciences"
volume: "108(21)"
doi: "10.1073/pnas.1017031108"
cites: 976
difficulty: 2
data_kind: "栅格"
design: "代理变量回归"
unit: "国家—年"
tags: [夜光, 代理, 测量误差, 国家—年]
---

# F07 Chen & Nordhaus 2011

## 一句话概括

检验灯光对产出的解释力并量化其误差结构。

## 研究设计

- **观测单元** 国家—年。
- **处理变量** 取国家—年的灯光总量。
- **结果变量** 取统计口径的产出。
- **识别逻辑** 代理变量回归，比较不同国家组的拟合优度。

## 数据结构

- 夜光栅格，空间属性为栅格。
- 国界与产出表，空间属性为面。
- 像元聚合规则，按面积加权到国家。

## 可迁移的做法

1. 按国界聚合灯光。
2. 分收入组估计弹性。
3. 比较拟合优度与残差结构。
4. 报告代理误差的分布。

## 主要结论

- 灯光对产出的解释力随收入下降。
- 低收入国家的代理误差更大。

## 复制这项研究需要注意

- 灯光饱和会压缩高密度区的信号。
- 国界聚合忽略次国家差异。

## 关联文献

- [[F11-ratledge]] 因为数据形态相同，两者同为栅格，像元聚合到单元的规则须一致。
- [[F12-fiaschi]] 因为识别逻辑相同，两者同为回归，样本筛选规则须同时报告。
- [[G01-henderson]] 因为互为稳健性检验，G01 的加权估计量以该文的弹性为输入。
