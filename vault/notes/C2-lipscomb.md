---
id: C2
group: C
short: "Lipscomb, Mobarak & Barham 2013"
authors: "Molly Lipscomb, Ahmed Mushfiq Mobarak, Tania Barham"
year: 2013
title: "Development Effects of Electrification: Evidence from the Topographic Placement of Hydropower Plants in Brazil"
venue: "American Economic Journal: Applied Economics"
volume: "5(2)"
doi: "10.1257/APP.5.2.200"
cites: 392
unit: "巴西自治市（municipality）"
design: "工具变量"
tags: [电气化, 水电, 工具变量, 地形]
---

## 一句话概括

用河流落差决定的发电潜力构造工具，估计巴西水电接入对市政发展的影响。

## 研究设计

- 针对观测单元，取巴西自治市（municipality）。
- 针对处理变量，取市政是否被水电项目接入电网。
- 针对结果变量，取人均 GDP、就业结构、入学率、婴儿死亡率与夜光。
- 针对识别逻辑，采用以纯地理变量为来源的工具变量。
- 河流落差由地形决定，与市政当期经济潜力无关，故可作外生来源。

## 数据结构

- 水电站点位，空间属性为点。
- 河流落差栅格，空间属性为栅格。
- 输电线路矢量，空间属性为线。
- 市政统计与人口普查，空间属性为面。

## 可迁移的做法

1. 用数字高程模型算出河流沿程落差。
2. 把落差按河段聚合，得到发电潜力的空间分布。
3. 用落差预测水电站与输电线路的落点。
4. 把预测落点作为接入的工具，做两阶段估计。
5. 逐项论证电站选址的其他用途，说明排除限制成立。

## 主要结论

电气化提高人均 GDP 与教育指标，并降低婴儿死亡率。制造业就业的响应强于农业。

## 复制这项研究需要注意

- 水电站选址同时考虑防洪与灌溉，故排除限制须逐项论证。
- 落差若同时影响农业生产条件，工具就难以只通过电气化影响结果。

## 关联文献

- [[C1-dinkelman]] 因为识别逻辑相同，C2 与 C1 都把自然地理当作电气化选址的外生来源，坡度与落差同角色。
- [[C3-ratledge]] 因为互为稳健性检验，C2 用工具变量估计电气化效应，C3 用机器学习去偏估计同一命题。
- [[D1-miguel]] 因为识别逻辑相同，C2 与 D1 都用纯地理变量作为工具，即河流落差与降雨。
