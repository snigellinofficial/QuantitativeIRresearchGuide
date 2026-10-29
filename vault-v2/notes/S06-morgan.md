---
id: S06
topic: S
short: "Morgan 等 2014"
authors: "T. Clifton Morgan; Navin Bapat; Yoshiharu Kobayashi"
year: 2014
title: "Threat and imposition of economic sanctions 1945–2005: Updating the TIES dataset"
venue: "Conflict Management and Peace Science"
volume: "31(5)"
doi: "10.1177/0738894213520379"
cites: 292
difficulty: 1
data_kind: "面"
design: "威胁—实施两阶段"
unit: "威胁事件"
tags: [制裁, 威胁, 两阶段, 事件]
---

# S06 Morgan 等 2014

## 一句话概括

把制裁拆成威胁与实施两个阶段并编码。

## 研究设计

- **观测单元** 威胁事件。
- **处理变量** 取威胁的发出与实施作为两个状态。
- **结果变量** 取制裁事件的结果编码。
- **识别逻辑** 两阶段编码，威胁与实施分别记录。

## 数据结构

- 威胁事件表，空间属性为面，单元为事件。
- 发起国与目标国，空间属性为关系边。
- 事件时间序列，记录起止月份。

## 可迁移的做法

1. 按威胁的发出编码起点。
2. 记录实施、部分实施与撤回。
3. 标注结果与持续时长。
4. 核对多来源记录。

## 主要结论

- 多数威胁未进入实施阶段。
- 两阶段编码把选择性问题显式化。

## 复制这项研究需要注意

- 威胁的界定依赖文献与新闻来源。
- 结果编码含主观判断。

## 关联文献

- [[S05-gopinath]] 因为数据形态相同，两者同为面，单元内部的聚合权重须说明。
- [[S07-benguria]] 因为数据形态相同，两者同为面，单元内部的聚合权重须说明。
- [[S08-crozet]] 因为数据形态相同，两者同为面，单元重划须显式处理。
- [[S10-kelley]] 因为数据形态相同，两者同为面，单元边界与年份版本须一致。
