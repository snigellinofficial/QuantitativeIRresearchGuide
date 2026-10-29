---
id: G05
topic: G
short: "Faber 2014"
authors: "Benjamin Faber"
year: 2014
title: "Trade Integration, Market Size, and Industrialization: Evidence from China's National Trunk Highway System"
venue: "The Review of Economic Studies"
volume: "81(3)"
doi: "10.1093/restud/rdu010"
cites: 969
difficulty: 3
data_kind: "混合"
design: "双重差分＋工具变量"
unit: "中国县"
tags: [公路, 工业化, 双重差分, 县]
---

# G05 Faber 2014

## 一句话概括

以规划线路而非建成线路构造处理变量，避开路网选址的内生性。

## 研究设计

- **观测单元** 中国县。
- **处理变量** 取县是否被规划中的国家干线公路连接。
- **结果变量** 取县级工业产出、就业与工资。
- **识别逻辑** 双重差分（difference-in-differences）叠加工具变量。处理时点由规划线路的连接年给出。

## 数据结构

- 规划与建成的干线公路，空间属性为线。
- 县界与县级统计表，空间属性为面。
- 县与线路的连接矩阵，空间属性为关系边。

## 可迁移的做法

1. 按规划图确定每个县的连接年份。
2. 把未连接县作为对照，构造县与年的双重差分。
3. 以规划连接作工具，检验建成连接的内生性。
4. 报告连接县与未连接县的事前趋势。

## 主要结论

- 规划线路的连接时点提供外生处理时点。
- 连接县的工业产出随连接上升。

## 复制这项研究需要注意

- 规划线路可能绕开增长快的县，须检验事前趋势。
- 县界口径在年份间变动，须固定边界版本。

## 关联文献

- [[G04-baum-snow]] 因为互为稳健性检验，G04 的规划路网工具与该文的规划线路同源。
- [[G06-banerjee]] 因为识别逻辑相同，两者同为工具变量，工具的外生性论证可以互相借用。
- [[G09-dinkelman]] 因为识别逻辑相同，两者同为工具变量，第一阶段强度须在分组样本中复核。
- [[G14-lipscomb]] 因为识别逻辑相同，两者同为工具变量，弱工具下的推断方式须一并报告。
