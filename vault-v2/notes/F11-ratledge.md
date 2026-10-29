---
id: F11
topic: F
short: "Ratledge 等 2022"
authors: "Nathan Ratledge; Gabe Cadamuro; Brandon de la Cuesta; Matthieu Stigler; Marshall Burke"
year: 2022
title: "Using machine learning to assess the livelihood impact of electricity access"
venue: "Nature"
volume: "611(7936)"
doi: "10.1038/s41586-022-05322-8"
cites: 82
difficulty: 5
data_kind: "栅格"
design: "影像测量＋双重稳健去偏"
unit: "乌干达村庄"
tags: [影像, 双重稳健, 电气化, 测量]
---

# F11 Ratledge 等 2022

## 一句话概括

把构造结果变量与估计因果效应分成两个独立步骤。

## 研究设计

- **观测单元** 乌干达村庄。
- **处理变量** 取村庄是否接入电网。
- **结果变量** 取由影像预测的生计指标。
- **识别逻辑** 影像测量配合双重稳健去偏，预测误差在第二步校正。

## 数据结构

- 影像栅格，空间属性为栅格。
- 村庄点位，空间属性为点。
- 行政区边界，空间属性为面。

## 可迁移的做法

1. 用影像训练生计指标模型。
2. 把预测值作为结果变量。
3. 用双重稳健方法校正预测误差。
4. 估计通电的效应。

## 主要结论

- 两步分离避免拟合误差进入因果估计。
- 预测精度与估计偏差可以分开报告。

## 复制这项研究需要注意

- 预测模型的误差须有独立验证集。
- 影像年份与通电年份须对齐。

## 关联文献

- [[C09-berman]] 因为数据形态相同，两者同为栅格，边界像元的归属规则须对齐。
- [[F01-chernozhukov]] 因为互为稳健性检验，F01 的正交矩是该文两步去偏的估计框架。
- [[F07-chen]] 因为数据形态相同，两者同为栅格，投影与重采样的方式须一致。
