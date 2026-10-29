---
id: N03
topic: N
short: "Boehm 等 2019"
authors: "Christoph E. Boehm; Aaron Flaaen; Nitya Pandalai-Nayar"
year: 2019
title: "Input Linkages and the Transmission of Shocks: Firm-Level Evidence from the 2011 Tōhoku Earthquake"
venue: "The Review of Economics and Statistics"
volume: "101(1)"
doi: "10.1162/rest_a_00750"
cites: 593
difficulty: 4
data_kind: "关系边"
design: "投入产出网络＋企业差分"
unit: "日本企业与其海外子公司"
tags: [投入产出, 传导, 跨国公司, 企业]
---

# N03 Boehm 等 2019

## 一句话概括

用母公司冲击识别投入联系对子公司产出的传导。

## 研究设计

- **观测单元** 日本企业与其海外子公司。
- **处理变量** 取母公司的产出冲击。
- **结果变量** 取子公司与关联企业的产出。
- **识别逻辑** 投入产出网络（input-output network）配合企业层面差分。

## 数据结构

- 母子公司与投入联系，空间属性为关系边。
- 企业财务表，空间属性为面。
- 受灾母公司，空间属性为点。

## 可迁移的做法

1. 匹配母公司与海外子公司的所有权关系。
2. 标注母公司受灾程度。
3. 比较关联与非关联子公司的产出。
4. 按投入联系强度分组。

## 主要结论

- 母公司冲击经投入联系传导到子公司。
- 传导强度随投入联系紧密度下降。

## 复制这项研究需要注意

- 所有权匹配依赖企业名称与登记信息。
- 子公司产出含当地需求变动。

## 关联文献

- [[N01-carvalho]] 因为互为稳健性检验，N01 的网络传播为该文投入联系提供参照系。
- [[N02-banerjee]] 因为识别逻辑相同，两者同为网络模型，边的方向性决定中心性的含义。
- [[N05-elliott]] 因为识别逻辑相同，两者同为网络模型，关系矩阵的对称化与加权规则须一致。
- [[N08-cederman]] 因为识别逻辑相同，两者同为网络模型，边的方向性决定中心性的含义。
