---
id: M05
topic: M
short: "Abadie 等 2010"
authors: "Alberto Abadie; Alexis Diamond; Jens Hainmueller"
year: 2010
title: "Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California’s Tobacco Control Program"
venue: "Journal of the American Statistical Association"
volume: "105(490)"
doi: "10.1198/jasa.2009.ap08746"
cites: 4745
difficulty: 3
data_kind: "面"
design: "合成控制法"
unit: "单个处理单元"
tags: [合成控制, 反事实, 安慰剂检验, 面]
---

# M05 Abadie 等 2010

## 一句话概括

用加权组合的对照单元构造反事实。

## 研究设计

- **观测单元** 单个处理单元。
- **处理变量** 取加利福尼亚控烟计划的实施。
- **结果变量** 取人均香烟消费量。
- **识别逻辑** 合成控制（synthetic control），以处理前的拟合选择权重。

## 数据结构

- 州与年份，空间属性为面。
- 处理单元的时间序列，按年份排列。
- 对照池表，记录候选州的协变量。

## 可迁移的做法

1. 选取未受处理的对照州集合。
2. 用处理前数据拟合权重。
3. 把权重用于处理后，构造反事实。
4. 做安慰剂检验与排列推断。

## 主要结论

- 处理后的消费低于合成对照。
- 处理前的拟合优度决定可信度。

## 复制这项研究需要注意

- 对照池中受同一政策影响的单元须剔除。
- 权重对处理前窗口的选择敏感。

## 关联文献

- [[M06-abadie]] 因为互为稳健性检验，M06 的早期应用是该文推断方式的先例。
- [[M07-abadie]] 因为互为稳健性检验，M07 的可行性条件是该文的推断前提。
- [[M11-king]] 因为数据形态相同，两者同为面，单元内部的聚合权重须说明。
