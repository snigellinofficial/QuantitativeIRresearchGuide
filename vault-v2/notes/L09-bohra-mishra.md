---
id: L09
topic: L
short: "Bohra-Mishra 等 2014"
authors: "Pratikshya Bohra-Mishra; Michael Oppenheimer; Solomon M. Hsiang"
year: 2014
title: "Nonlinear permanent migration response to climatic variations but minimal response to disasters"
venue: "Proceedings of the National Academy of Sciences"
volume: "111(27)"
doi: "10.1073/pnas.1317166111"
cites: 359
difficulty: 2
data_kind: "点"
design: "非线性剂量反应"
unit: "印度尼西亚家庭"
tags: [迁移, 非线性, 家庭, 气候]
---

# L09 Bohra-Mishra 等 2014

## 一句话概括

估计气候异常对永久迁移的非线性响应。

## 研究设计

- **观测单元** 印度尼西亚家庭。
- **处理变量** 取家庭所在社区的温度与降水异常。
- **结果变量** 取家庭的永久迁移决定。
- **识别逻辑** 剂量反应估计，按气候区间分箱。

## 数据结构

- 家庭点位，空间属性为点。
- 气候栅格，空间属性为栅格。
- 社区边界，空间属性为面。

## 可迁移的做法

1. 把气候栅格挂到社区点位。
2. 按温度与降水区间分箱。
3. 估计迁移概率的响应曲线。
4. 区分临时与永久迁移。

## 主要结论

- 迁移响应在高温区间更强。
- 灾害事件本身的响应较弱。

## 复制这项研究需要注意

- 家庭面板的追踪率下降会带来选择性。
- 迁移的定义决定结果口径。

## 关联文献

- [[C05-sundberg]] 因为数据形态相同，两者同为点，点位坐标的精度与去重规则须一致。
- [[C12-sanchez-de-la-sierra]] 因为数据形态相同，两者同为点，点的空间落位误差须报告。
- [[G13-jedwab]] 因为数据形态相同，两者同为点，点位到单元的挂接规则须对齐。
