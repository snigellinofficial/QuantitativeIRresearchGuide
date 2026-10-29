---
id: L03
topic: L
short: "Dell 等 2012"
authors: "Melissa Dell; Benjamin F Jones; Benjamin A Olken"
year: 2012
title: "Temperature Shocks and Economic Growth: Evidence from the Last Half Century"
venue: "American Economic Journal: Macroeconomics"
volume: "4(3)"
doi: "10.1257/mac.4.3.66"
cites: 1260
difficulty: 2
data_kind: "面"
design: "面板温度冲击"
unit: "国家—年"
tags: [温度, 增长, 非线性, 面板]
---

# L03 Dell 等 2012

## 一句话概括

把温度与降水的高阶项放进增长回归。

## 研究设计

- **观测单元** 国家—年。
- **处理变量** 取国家—年的温度与降水及其平方项。
- **结果变量** 取人均产出的增长率。
- **识别逻辑** 面板数据（panel data）固定效应，以年度波动识别。

## 数据结构

- 国家与年份，空间属性为面。
- 气象栅格，空间属性为栅格。
- 气象站点，空间属性为点。

## 可迁移的做法

1. 把气象栅格聚合到国家—年。
2. 加入平方项刻画非线性。
3. 放入国家与年固定效应。
4. 按收入水平分组估计。

## 主要结论

- 高温对穷国增长的影响更明显。
- 富裕国家的响应接近于零。

## 复制这项研究需要注意

- 气象聚合的空间权重影响系数。
- 年度波动与长期趋势须分开。

## 关联文献

- [[L04-barreca]] 因为识别逻辑相同，两者同为面板，缺失单元的填补方式影响系数。
- [[L05-deschenes]] 因为识别逻辑相同，两者同为面板，时间间隔的设定改变变动项的均值。
- [[L06-carleton]] 因为互为稳健性检验，L06 把该文的增长弹性扩到死亡率结果。
- [[L07-cattaneo]] 因为识别逻辑相同，两者同为面板，单元与年份固定效应的层次须对齐。
