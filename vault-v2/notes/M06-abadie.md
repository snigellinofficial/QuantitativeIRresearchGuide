---
id: M06
topic: M
short: "Abadie & Gardeazabal 2003"
authors: "Alberto Abadie; Javier Gardeazabal"
year: 2003
title: "The Economic Costs of Conflict: A Case Study of the Basque Country"
venue: "American Economic Review"
volume: "93(1)"
doi: "10.1257/000282803321455188"
cites: 3682
difficulty: 3
data_kind: "面"
design: "合成控制法"
unit: "巴斯克地区"
tags: [合成控制, 冲突代价, 巴斯克, 地区]
---

# M06 Abadie & Gardeazabal 2003

## 一句话概括

用合成控制估计恐怖冲突对巴斯克地区的经济代价。

## 研究设计

- **观测单元** 巴斯克地区。
- **处理变量** 取冲突的发生与停火时段。
- **结果变量** 取人均产出相对于合成对照的差距。
- **识别逻辑** 合成控制，以其它西班牙地区加权构造对照。

## 数据结构

- 地区与年份，空间属性为面。
- 人均产出序列，按地区排列。
- 冲突事件记录，按年份与地区编码。

## 可迁移的做法

1. 用冲突前的数据拟合权重。
2. 比较冲突期间的实际与合成路径。
3. 在停火期做对照检验。
4. 报告差距的时间路径。

## 主要结论

- 冲突期间人均产出低于合成对照。
- 停火期差距收窄，支持冲突的解释。

## 复制这项研究需要注意

- 其它地区同期政策须核对。
- 合成权重由少数地区主导时须报告。

## 关联文献

- [[M05-abadie]] 因为互为稳健性检验，M05 的排列推断可复核该文的合成权重。
- [[M07-abadie]] 因为数据形态相同，两者同为面，单元边界与年份版本须一致。
- [[M11-king]] 因为数据形态相同，两者同为面，单元重划须显式处理。
