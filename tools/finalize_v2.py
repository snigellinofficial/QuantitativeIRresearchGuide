# -*- coding: utf-8 -*-
"""收尾修补：编号重映射、分布口径更新、错误清单扩充、文献总表插入。"""
import html
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")

s = io.open(P, encoding="utf-8").read()
cat = json.load(open(os.path.join(ROOT, "catalog-v2.json"), encoding="utf-8"))

# ---------------------------------------------------------------- 1 谱系表编号
REPL = [
    ("<td>A1 Dell 2010；A2、A3 Michalopoulos 与 Papaioannou；A5 Ahlfeldt 等 2015</td>",
     "<td>G02 Dell 2010；G07、G08 Michalopoulos 与 Papaioannou；G10 Ahlfeldt 等 2015</td>"),
    ("<td>B1 至 B5；A4 Burgess 等 2015；C1、C2</td>",
     "<td>G11 Asher 与 Novosad 2020；G12 Burgess 等 2015；G13 Jedwab 与 Moradi 2016；G06 Banerjee 等 2020</td>"),
    ("<td>B2 Faber 2014；B5 Baum-Snow 2007；C1、C2；D1 Miguel 等 2004</td>",
     "<td>G05 Faber 2014；G04 Baum-Snow 2007；G09 Dinkelman 2011；G14 Lipscomb 等 2013；C03 Miguel 等 2004</td>"),
    ("<td>D2 Berman 等 2017；D4 Hodler 与 Raschky 2014</td>",
     "<td>C09 Berman 等 2017；G16 Hodler 与 Raschky 2014</td>"),
    ("<td>F1 Henderson 等 2012；F2 Jean 等 2016；C3 Ratledge 等 2022</td>",
     "<td>G01 Henderson 等 2012；F05 Jean 等 2016；F11 Ratledge 等 2022；F01 Chernozhukov 等 2018</td>"),
    ("<td>E1 至 E4</td>",
     "<td>N04 Cranmer 与 Desmarais 2011；N09 Cranmer 等 2012；N11 Ward 等 2013；N02 Banerjee 等 2013</td>"),
    # ------------------------------------------------------------ 2 数据源表
    ("<td>点</td><td>D1、D2、E1</td>", "<td>点</td><td>C03、C09、N08</td>"),
    ("<td>面</td><td>A3、B1 至 B5</td>", "<td>面</td><td>G08、G03、G11</td>"),
    ("<td>线</td><td>B1 至 B5</td>", "<td>线</td><td>G03、G05、G15</td>"),
    ("<td>栅格</td><td>C1、C2、B2</td>", "<td>栅格</td><td>G09、G14、G05</td>"),
    ("<td>栅格</td><td>D4、F1、F5</td>", "<td>栅格</td><td>G16、G01、F07、F12</td>"),
    ("<td>点</td><td>D2</td>", "<td>点</td><td>C09</td>"),
    ("<td>面</td><td>A2、A3、E1</td>", "<td>面</td><td>G07、G08、N08</td>"),
    # ------------------------------------------------------------ 3 分布句
    ("据本库的实际分布，二十六篇文献中，主要数据形态为栅格者九篇，为混合形态者五篇，为线者四篇，为关系边者四篇，为点者三篇，为面者一篇。<strong>形态的选择与识别策略高度相关，并非自由选项。</strong>",
     "据本库的实际分布，一百篇文献中，主要数据形态为面者三十八篇，为关系边者十七篇，为栅格者十五篇，为混合者十五篇，为点者九篇，为线者六篇。<strong>形态的选择与识别策略高度相关，并非自由选项。</strong>"),
]
miss = []
for a, b in REPL:
    if a in s:
        s = s.replace(a, b, 1)
    else:
        miss.append(a[:44])
print("未命中", len(miss))
for m in miss:
    print("   ", m)

# ---------------------------------------------------------------- 4 错误清单扩到十二
old_rows = "<tr><td>十</td><td>把网络边当独立观测</td><td>依赖结构被忽略，标准误严重低估</td><td>8.7 节</td></tr>"
new_rows = ("<tr><td>十</td><td>把网络边当独立观测</td><td>依赖结构被忽略，标准误严重低估</td><td>7.4 节、12.3 节</td></tr>\n"
            "<tr><td>十一</td><td>用传统双向固定效应处理交错时点</td><td>权重可能为负，估计量可能符号反转</td><td>7.3 节</td></tr>\n"
            "<tr><td>十二</td><td>把代理变量当真实值使用</td><td>衰减偏误被读成真实效应</td><td>5.6 节、14.3 节</td></tr>")
if old_rows in s:
    s = s.replace(old_rows, new_rows, 1)
else:
    print("未命中 错误第十行")

s = s.replace("据上表，十项错误可以归为三个原因。第一是空间对象被当作普通数值，第一、二、三项属于此类。第二是识别假设未被检验，第四至第七项属于此类。第三是推断被简化，第八至第十项属于此类。",
              "据上表，十二项错误可以归为三个原因。第一是空间对象被当作普通数值，第一至第三项属于此类。第二是识别假设未被检验，第四至第七项与第十一项属于此类。第三是推断被简化，第八至第十项与第十二项属于此类。")
s = s.replace("第十一章", "第十一章")

# ---------------------------------------------------------------- 5 文献总表
rows = []
for p in cat["papers"]:
    pub = "%s %s" % (p["venue"], p["volume"]) if p["volume"] else p["venue"]
    rows.append("<tr><td>%s</td><td>%s</td><td><em>%s</em></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        html.escape(p["id"]), html.escape(p["short"]), html.escape(p["title"]),
        html.escape(pub.strip()), p["year"], p["difficulty"], p["cites"]))

table = """
<h3>16.3　文献总表</h3>

<p>据第 7 章至第 15 章的引用，下表给出一百篇文献的完整对应关系。编号前缀对应七个专题与方法论基石。</p>

<table class="gen ref">
<caption>表 16.1　一百篇文献的编号、题录与难度。卷期与 DOI 已核验，页码从略。引用量为 Crossref 口径，检索日期 2026 年 10 月 29 日，与 OpenAlex 及谷歌学术不可混用。</caption>
<thead><tr><th>编号</th><th>简称</th><th>标题</th><th>期刊与卷期</th><th>年份</th><th>难度</th><th>引用量</th></tr></thead>
<tbody>
%s
</tbody>
</table>
""" % ("\n".join(rows))

k = s.rfind("</section>")
s = s[:k] + table + s[k:]

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s), "rows", len(rows))
