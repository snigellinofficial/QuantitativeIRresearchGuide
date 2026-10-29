---
id: F08
topic: F
short: "Blumenstock 等 2015"
authors: "Joshua Blumenstock; Gabriel Cadamuro; Robert On"
year: 2015
title: "Predicting poverty and wealth from mobile phone metadata"
venue: "Science"
volume: "350(6264)"
doi: "10.1126/science.aac4420"
cites: 558
difficulty: 4
data_kind: "点"
design: "监督学习"
unit: "卢旺达手机用户"
tags: [手机数据, 贫困, 监督学习, 预测]
---

# F08 Blumenstock 等 2015

## 一句话概括

用通话与充值记录预测个人财富。

## 研究设计

- **观测单元** 卢旺达手机用户。
- **处理变量** 取通话与充值的元数据特征。
- **结果变量** 取调查得到的财富指数。
- **识别逻辑** 监督学习（supervised learning），以调查样本为标签。

## 数据结构

- 手机用户，空间属性为点。
- 调查区域，空间属性为面。
- 通话与充值记录，按用户与月份排列。

## 可迁移的做法

1. 抽取通话与充值的特征。
2. 匹配调查受访者。
3. 训练并交叉验证模型。
4. 把预测外推到全量用户。

## 主要结论

- 元数据特征可预测财富水平。
- 预测精度在样本外下降。

## 复制这项研究需要注意

- 手机用户与总人口的代表性差异。
- 运营商数据的时间窗影响特征。

## 关联文献

- [[F01-chernozhukov]] 因为识别逻辑相同，两者同为机器学习，超参数的选择须在训练集内完成。
- [[F03-wager]] 因为识别逻辑相同，两者同为机器学习，训练集与评估集的切分须各自独立。
- [[F05-jean]] 因为互为稳健性检验，F05 的影像预测与该文的手机预测针对同一目标。
- [[F10-aiken]] 因为数据形态相同，两者同为点，点位到单元的挂接规则须对齐。
