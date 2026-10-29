# -*- coding: utf-8 -*-
"""补齐最后两篇；重建三级目录；替换标题与拆解的排版样式。"""
import io
import re

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = ROOT + r"\index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1 补最后两篇
ADDS = [
("<strong>把援助拆成基础设施、教育与治理三类重估，是后续文献常用的一步。</strong></p>",
 """<p><strong>还有一个口径问题。</strong>援助额若按当年汇率换算，汇率波动会被读成援助变化。<strong>该文以美元不变价计价，并在附录报告以特别提款权计价的结果，两者的差别决定了结论是否稳健。</strong></p>"""),
("<strong>缺少检验意味着维数仍是一个研究者的判断，而非数据的结论。</strong></p>",
 """<p><strong>这一点的实际后果。</strong>维数增加会让坐标更贴合数据，但也会吸收噪声。<strong>若把维数当作调参项，任何结论都可以通过增加维数得到，故该文只报告二到三维，并说明理由来自解释力而非拟合。</strong></p>"""),
]
miss = []
for anchor, add in ADDS:
    k = s.find(anchor)
    if k < 0:
        miss.append(anchor[:24]); continue
    k += len(anchor)
    s = s[:k] + add + s[k:]
print("补段未命中", miss)

# ---------------------------------------------------------------- 2 重建目录
main_start = s.find("<main")
main = s[main_start:s.find("</main>")]

sections = []
for m in re.finditer(r'<section id="(c\d+)">(.*?)</section>', main, flags=re.S):
    sid, body = m.group(1), m.group(2)
    h2 = re.search(r'<h2><span class="num">\d+</span>([^<]+)</h2>', body)
    if not h2:
        continue
    title = h2.group(1)
    num = re.search(r'<span class="num">(\d+)</span>', body).group(1)
    items = []
    # h3 / h4 按出现顺序
    for mm in re.finditer(r'<h([34]) id="([^"]+)">([^<]+)</h\1>', body):
        items.append((int(mm.group(1)), mm.group(2), mm.group(3)))
    # 案例
    for mm in re.finditer(r'<div class="case" id="(case\d+)">\s*<p class="case-head">([^<]+)</p>', body):
        items.append((4, mm.group(1), mm.group(2)))
    sections.append((sid, num, title, items))

print("章节", len(sections), [len(x[3]) for x in sections])

out = ['  <ol class="toc">']
for sid, num, title, items in sections:
    out.append('    <li class="lv1"><a href="#%s">%s　%s</a>' % (sid, num, title))
    if items:
        out.append('      <ol class="sub">')
        for lvl, aid, txt in items:
            cls = "lv3" if lvl == 4 else "lv2"
            out.append('        <li class="%s"><a href="#%s">%s</a></li>' % (cls, aid, txt))
        out.append('      </ol>')
    out.append('    </li>')
out.append('  </ol>')

toc_html = "\n".join(out)

a = s.find('  <ol class="toc">')
b = s.find('  <p class="sb-label">文献库</p>')
assert a > 0 and b > a
s = s[:a] + toc_html + "\n" + s[b:]
print("目录条目", toc_html.count("<li"))

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
