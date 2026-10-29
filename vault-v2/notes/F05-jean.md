---
id: F05
topic: F
short: "Jean 等 2016"
authors: "Neal Jean; Marshall Burke; Michael Xie; W. Matthew Davis; David B. Lobell"
year: 2016
title: "Combining satellite imagery and machine learning to predict poverty"
venue: "Science"
volume: "353(6301)"
doi: "10.1126/science.aaf7894"
cites: 1352
difficulty: 4
data_kind: "栅格"
design: "迁移学习"
unit: "非洲五国小区域"
tags: [迁移学习, 贫困, 卫星影像, 栅格]
---

# F05 Jean 等 2016

## 一句话概括

用夜光预训练再以调查数据校准，两个阶段分离。

## 研究设计

- **观测单元** 非洲五国小区域。
- **处理变量** 取卫星影像特征。
- **结果变量** 取家庭消费或资产指数。
- **识别逻辑** 迁移学习（transfer learning），先预训练再小样本校准。

## 数据结构

- 影像与夜光栅格，空间属性为栅格。
- 调查簇点位，空间属性为点。
- 小区域边界，空间属性为面，用于外推。

## 可迁移的做法

1. 用夜光与影像训练特征提取器。
2. 以调查簇的消费作标签。
3. 在小样本上校准回归。
4. 把预测外推到无调查区域。

## 主要结论

- 影像特征可解释区域间的消费差异。
- 两阶段分离使标注成本下降。

## 复制这项研究需要注意

- 调查簇与影像的匹配尺度影响精度。
- 外推区域的光照条件须可比。

## 关联文献

- [[F01-chernozhukov]] 因为识别逻辑相同，两者同为机器学习，样本外预测的验证方式须一致。
- [[F08-blumenstock]] 因为互为稳健性检验，F08 的手机信号提供该文影像之外的另一路测量。
- [[F10-aiken]] 因为互为稳健性检验，F10 的瞄准误差检验该文贫困预测的下游表现。
- [[F12-fiaschi]] 因为识别逻辑相同，两者同为机器学习，样本外预测的验证方式须一致。
