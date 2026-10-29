---
id: N01
topic: N
short: "Carvalho 等 2021"
authors: "Vasco M Carvalho; Makoto Nirei; Yukiko U Saito; Alireza Tahbaz-Salehi"
year: 2021
title: "Supply Chain Disruptions: Evidence from the Great East Japan Earthquake*"
venue: "The Quarterly Journal of Economics"
volume: "136(2)"
doi: "10.1093/qje/qjaa044"
cites: 940
difficulty: 4
data_kind: "关系边"
design: "网络传播模型"
unit: "日本企业"
tags: [供应链, 传播, 震灾, 企业]
---

# N01 Carvalho 等 2021

## 一句话概括

用震灾冲击估计供应链网络的传播与恢复。

## 研究设计

- **观测单元** 日本企业。
- **处理变量** 取企业是否受灾或与受灾企业直接相连。
- **结果变量** 取企业的销售额增长。
- **识别逻辑** 网络传播模型，把冲击沿投入产出边逐轮传播。

## 数据结构

- 企业间交易关系，空间属性为关系边。
- 企业财务表，空间属性为面。
- 受灾企业与震度，空间属性为点。

## 可迁移的做法

1. 把企业交易关系写成有向网络。
2. 标注受灾企业与空间距离。
3. 估计直接冲击与一轮间接冲击。
4. 按网络距离分组比较恢复速度。

## 主要结论

- 冲击沿供应链向下游传播。
- 间接冲击随网络距离衰减。

## 复制这项研究需要注意

- 企业交易关系的覆盖不完整。
- 受灾标注依赖震度与停产记录。

## 关联文献

- [[N02-banerjee]] 因为识别逻辑相同，两者同为网络模型，边的方向性决定中心性的含义。
- [[N03-boehm]] 因为互为稳健性检验，N03 的母公司冲击检验该文传播的同国边界。
- [[N05-elliott]] 因为识别逻辑相同，两者同为网络模型，阈值与二值化规则须同时报告。
- [[N06-dorussen]] 因为识别逻辑相同，两者同为网络模型，节点集合的边界须同时固定。
