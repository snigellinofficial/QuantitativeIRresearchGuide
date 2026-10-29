---
id: N11
topic: N
short: "Ward 等 2013"
authors: "MICHAEL D. WARD; JOHN S. AHLQUIST; ARTURAS ROZENAS"
year: 2013
title: "Gravity's Rainbow: A dynamic latent space model for the world trade network"
venue: "Network Science"
volume: "1(1)"
doi: "10.1017/nws.2013.1"
cites: 94
difficulty: 4
data_kind: "关系边"
design: "动态潜在空间模型"
unit: "国家对—年"
tags: [潜在空间, 引力模型, 贸易, 动态]
---

# N11 Ward 等 2013

## 一句话概括

把国家亲疏压缩成低维坐标，用坐标距离替代虚拟变量。

## 研究设计

- **观测单元** 国家对—年。
- **处理变量** 取国家对在潜在空间中的距离。
- **结果变量** 取双边贸易流量。
- **识别逻辑** 动态潜在空间模型（latent space model），距离进入引力方程。

## 数据结构

- 贸易流，空间属性为关系边。
- 国家属性，空间属性为面。
- 逐年坐标，按年份估计。

## 可迁移的做法

1. 把贸易流写成引力方程。
2. 用低维坐标表示国家位置。
3. 允许坐标随时间移动。
4. 估计参数并检验拟合。

## 主要结论

- 低维坐标能复现贸易网络的主要结构。
- 坐标随年份移动，反映关系格局变化。

## 复制这项研究需要注意

- 坐标的旋转与尺度须固定以便比较。
- 贸易零流须单独建模。

## 关联文献

- [[F09-wilkerson]] 因为数据形态相同，两者同为关系边，矩阵的阈值设定须同时报告。
- [[N04-cranmer]] 因为数据形态相同，两者同为关系边，矩阵的阈值设定须同时报告。
- [[N07-maoz]] 因为数据形态相同，两者同为关系边，边的权重口径须逐项对照。
- [[N09-cranmer]] 因为数据形态相同，两者同为关系边，节点集合与边的方向须一致。
