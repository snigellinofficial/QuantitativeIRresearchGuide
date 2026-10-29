---
id: I04
topic: I
short: "Dreher 等 2009"
authors: "Axel Dreher; Jan-Egbert Sturm; James Raymond Vreeland"
year: 2009
title: "Development aid and international politics: Does membership on the UN Security Council influence World Bank decisions?"
venue: "Journal of Development Economics"
volume: "88(1)"
doi: "10.1016/j.jdeveco.2008.02.003"
cites: 428
difficulty: 3
data_kind: "面"
design: "安理会席位作为外生变动"
unit: "受援国—年"
tags: [安理会, 世界银行, 席位, 援助]
---

# I04 Dreher 等 2009

## 一句话概括

用非常任理事国席位轮换识别世界银行贷款的政治偏向。

## 研究设计

- **观测单元** 受援国—年。
- **处理变量** 取受援国是否为非常任理事国。
- **结果变量** 取世界银行的项目数量与贷款额。
- **识别逻辑** 席位轮换提供外生变动，比较同一国家在任与不在任的年份。

## 数据结构

- 受援国与年份，空间属性为面。
- 投票与援助，空间属性为关系边。
- 席位任期表，按年份挂到国家。

## 可迁移的做法

1. 编码各国在安理会的任期年份。
2. 比较任期内外获得的贷款。
3. 放入国家与年固定效应。
4. 检验任期内的投票一致性。

## 主要结论

- 任期内的受援国获得更多世界银行贷款。
- 贷款增加与投票一致性相关。

## 复制这项研究需要注意

- 席位轮换与地区分组相关，须控制地区—年效应。
- 贷款审批周期长于任期。

## 关联文献

- [[I03-nielson]] 因为数据形态相同，两者同为面，单元边界与年份版本须一致。
- [[I06-blair]] 因为数据形态相同，两者同为面，单元边界与年份版本须一致。
- [[I07-abbott]] 因为数据形态相同，两者同为面，单元内部的聚合权重须说明。
- [[I08-carnegie]] 因为数据形态相同，两者同为面，单元重划须显式处理。
