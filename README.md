# QuantitativeIRresearchGuide

面向初学者的国际政治量化研究读本。以一百篇顶刊文献为底本，讲解从相关到因果的方法阶梯，并逐段拆解十七篇代表性论文的行文与识别逻辑。

## 打开方式

双击 `index.html` 即可阅读。公式由本地 MathJax 渲染，断网也能正常显示，无需安装任何依赖。

## 目录结构

```
.
├── index.html              主文档：序、16 章正文、参考文献
├── catalog-v2.json         一百篇文献的题录、难度、识别策略与数据形态
├── references.csv          参考文献清单（UTF-8 带 BOM，可直接用表格软件打开）
├── references.md           同一份清单的 Markdown 版本
├── assets/
│   ├── style.css           排版样式
│   ├── app.js              目录高亮与进度条
│   ├── fig/                十六张矢量示意图
│   └── mathjax/            本地 MathJax 3 渲染器
├── vault-v2/               文献卡片库：一百张卡片、八份分组索引、对照矩阵与方法阶梯
├── vault/                  第一版文献库（二十六篇，保留备查）
└── tools/                  收割、核验、作图、建库与机检脚本
```

## 文档结构

| 部分 | 章节 | 内容 |
| --- | --- | --- |
| 序 | — | 全书结构与三种读法 |
| 第一部分 方法阶梯 | 第 1–7 章 | 统计工具箱、观测单元、因果与偏差、六族识别策略、核心公式、数据流水线、进阶方法 |
| 第二部分 七个专题 | 第 8–14 章 | 地理与基础设施、冲突与暴力、制裁与经济治国、国际制度与援助、网络与依赖、气候与迁移、测量与机器学习 |
| 第三部分 案例阶梯 | 第 15 章 | 八个案例，由横截面回归到聚合偏差 |
| 第四部分 实务与文献 | 第 16–17 章 | 数据源、复现清单、十二项常见错误、参考文献 |

每个专题分两半。前半为综述，交代该组文献共同面对的因果难题；后半为二到三篇文献拆解，每篇不少于一千五百字，按问题意识、数据边界、变量构造、方法理由、方程符号、论证链条、稳健性与争议的顺序展开。

## 数据口径

- 一百篇文献的题录经 Crossref 逐条核验，DOI 可解析，标题相似度不低于 0.80，刊名与卷期一致。
- 引用量为 Crossref 的 `is-referenced-by-count` 计数，检索日期 2026 年 10 月 29 日。该口径与 OpenAlex 及谷歌学术不同，三者不可混用。
- 方法难度分五级，定义见 `catalog-v2.json` 的 `difficulty_legend` 字段。
- 正文的方法描述与结论概括取自原文摘要与引言，未逐段核对正文页码。

## 质量检查

两轮机检，脚本为 `tools/check_academic.py`。

```bash
python tools/check_academic.py --round style   # 第一轮：语言风格与硬规则
python tools/check_academic.py --round facts   # 第二轮：题录、结构、资源与公式
python tools/check_academic.py --round all     # 两轮合并，退出码非零即不通过
```

当前状态：两轮硬规则均为零；风格向量偏离两项（长句占比、短句占比），已在交付说明中列明。

其余脚本：

| 脚本 | 作用 |
| --- | --- |
| `tools/harvest_cr.py` | 按刊名与议题从 Crossref 收割候选池 |
| `tools/verify_targets.py` | 逐条核验目标文献的 DOI、刊名、卷期与引用量 |
| `tools/build_catalog_v2.py` | 合并核验结果，套用难度与识别策略分类 |
| `tools/make_figs.py`、`tools/make_figs2.py` | 生成十六张矢量示意图 |
| `tools/build_references.py` | 由目录生成 CSV、Markdown 与正文参考文献表 |
| `tools/check_doc.py` | 结构、锚点、公式与句长的辅助检查 |

## 使用

正文可自由引用，出处以 `references.csv` 为准。文献卡片库兼容 Obsidian，直接以仓库根目录为库打开即可看到双向链接。

## 致谢与出处

书中引用的全部论文版权归原作者与期刊所有，本仓库只收录题录、DOI 与二手概述，不包含原文 PDF。
