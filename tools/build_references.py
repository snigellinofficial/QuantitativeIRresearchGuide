# -*- coding: utf-8 -*-
"""生成参考文献清单（CSV 与 Markdown）、新增序言章节与参考文献章节，并更新目录。"""
import csv
import html
import io
import json
import os

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
cat = json.load(io.open(os.path.join(ROOT, "catalog-v2.json"), encoding="utf-8"))
papers = cat["papers"]

TOPIC = {"G": "地理与基础设施", "C": "冲突与政治暴力", "S": "制裁与经济治国",
         "I": "国际制度与援助", "N": "网络与依赖", "L": "气候迁移与灾害",
         "F": "测量与机器学习", "M": "方法论基石"}

# ---------------------------------------------------------------- 1 CSV
csv_path = os.path.join(ROOT, "references.csv")
with io.open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["编号", "专题", "第一作者", "全部作者", "年份", "标题", "期刊",
                "卷期", "DOI", "DOI 链接", "Crossref 引用量", "方法难度", "识别策略", "数据形态"])
    for p in papers:
        first = p["authors"].split(";")[0].strip()
        w.writerow([p["id"], TOPIC[p["topic"]], first, p["authors"], p["year"], p["title"],
                    p["venue"], p["volume"], p["doi"],
                    "https://doi.org/" + p["doi"] if p["doi"] else "",
                    p["cites"], p["difficulty"], p["design"], p["data_kind"]])
print("csv", len(papers))

# ---------------------------------------------------------------- 2 Markdown
md = ["# 参考文献清单", "",
      "共 %d 条。DOI 已逐条核验，引用量为 Crossref 口径，检索日期 2026-10-29。" % len(papers), "",
      "| 编号 | 第一作者 | 年份 | 标题 | 期刊 | 卷期 | DOI |",
      "| --- | --- | --- | --- | --- | --- | --- |"]
for p in papers:
    first = p["authors"].split(";")[0].strip()
    md.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        p["id"], first, p["year"], p["title"].replace("|", "\\|"),
        p["venue"], p["volume"], p["doi"]))
io.open(os.path.join(ROOT, "references.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print("md ok")

# ---------------------------------------------------------------- 3 HTML 表格
rows = []
for p in papers:
    first = p["authors"].split(";")[0].strip()
    rows.append(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td><em>%s</em></td><td>%s</td>"
        "<td>%s</td><td><a href=\"https://doi.org/%s\">%s</a></td><td>%s</td></tr>"
        % (p["id"], html.escape(first), p["year"], html.escape(p["title"]),
           html.escape(p["venue"]), html.escape(p["volume"]),
           p["doi"], p["doi"], p["cites"]))

ref_section = """
<section id="c17">
<h2><span class="num">17</span>参考文献</h2>

<p>据全书引用，下表列出 %d 项文献的完整题录与数字对象标识符（digital object identifier，DOI）。<strong>每一条的 DOI 均可解析，卷期与年份取自 Crossref 记录。</strong></p>

<p>引用量一栏为 Crossref 的 <em>is-referenced-by-count</em> 计数，检索日期 2026 年 10 月 29 日。<strong>该口径与 OpenAlex 及谷歌学术不同，三者不可混用。</strong>同一文献在不同数据库中的计数差异可达数倍。</p>

<p>可机读的版本见项目根目录下的 references.csv 与 references.md 两个文件。前者带 UTF-8 字节序标记，可直接用电子表格软件打开。</p>

<table class="gen ref">
<caption>表 17.1　全书引用文献题录。编号首字母对应七个专题与方法论基石；难度按第 7 章的五级口径标注于文献库。页码从略，以 DOI 为准。</caption>
<thead><tr><th>编号</th><th>第一作者</th><th>年份</th><th>标题</th><th>期刊</th><th>卷期</th><th>DOI</th><th>引用量</th></tr></thead>
<tbody>
%s
</tbody>
</table>
</section>
""" % (len(papers), "\n".join(rows))

PREFACE = """
<section id="c0" class="preface">
<h2 class="plain">序　本书的结构与用途</h2>

<p>本书把国际政治与国际政治经济学的量化研究拆成两部分：可操作的方法，可模仿的案例。<strong>目标读者是刚进入大学、尚未系统学过统计学的学生，也供需要查找方法范本的研究者检索。</strong>书中假定读者知道均值与百分比的含义，其余概念均在首次出现处交代。</p>

<p>全书分四部分。第一部分为方法阶梯，含第 1 章至第 7 章。前六章从条件期望讲到双向固定效应、工具变量与断点回归，第 7 章补入合成控制、份额移动、异质性稳健的双重差分、网络模型与机器学习。<strong>七章的顺序即难度的顺序，每章只增加一类外部信息。</strong></p>

<p>第二部分为七个专题，含第 8 章至第 14 章，依次是地理与基础设施、冲突与政治暴力、制裁与经济治国、国际制度与援助、网络与依赖、气候与迁移、测量与机器学习。每个专题分两半。前半是综述，交代这一组文献共同面对的因果难题与三种常见解法；<strong>后半是三篇左右的文献拆解，按问题意识、数据边界、变量构造、方法理由、方程符号、论证链条、稳健性与争议的顺序，逐段复原作者的行文。</strong></p>

<p>第三部分为案例阶梯，即第 15 章。八个案例按难度排列，第一个只需横截面回归，第八个需要把聚合层级写进模型。第四部分为实务与文献，含第 16 章的数据流水线与常见错误，以及第 17 章的文献题录。</p>

<p>三种读法都成立。按章序通读，适合从零开始；先读第 15 章的某个案例，再回跳到对应专题，适合已有具体题目；只查方法与文献，适合把本书当工具书。配套的 vault-v2 目录存放一百张文献卡片，每张含七节正文与双向链接。</p>

<p>全部一百篇文献经 Crossref 逐条核验，<strong>DOI 可解析、标题相似度不低于 0.80、刊名与卷期一致</strong>。正文中的方法描述与结论概括取自原文摘要与引言，未逐段核对正文页码，涉及具体系数的表述均以「约」「量级」限定。</p>
</section>
"""

P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

# 插入序言
if '<section id="c0"' not in s:
    k = s.find('<section id="c1">')
    assert k > 0
    s = s[:k] + PREFACE + "\n" + s[k:]

# 插入参考文献
if '<section id="c17">' not in s:
    k = s.find("</main>")
    assert k > 0
    s = s[:k] + ref_section + "\n" + s[k:]

# 目录补两条
if 'href="#c0"' not in s:
    a = s.find('<ol class="toc">') + len('<ol class="toc">')
    s = s[:a] + '\n    <li class="lv1"><a href="#c0">序　本书的结构与用途</a></li>' + s[a:]
if 'href="#c17"' not in s:
    b = s.find('<p class="sb-label">文献库</p>')
    j = s.rfind("</ol>", 0, b)
    s = s[:j] + '    <li class="lv1"><a href="#c17">17　参考文献</a></li>\n  ' + s[j:]

io.open(P, "w", encoding="utf-8").write(s)
print("html", len(s))
