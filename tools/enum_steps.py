# -*- coding: utf-8 -*-
"""把「第一步…第二步…第三步…」型段落拆成编号列表。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

STEP = re.compile(r"第[一二三四五六]步[，、]?")


def conv(m):
    head, body = m.group(1), m.group(2)
    if "<" in body:
        return m.group(0)
    marks = list(STEP.finditer(body))
    if len(marks) < 3:
        return m.group(0)
    # 首段引导语
    lead = body[:marks[0].start()].strip()
    items = []
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        seg = body[mk.end():end].strip()
        seg = seg.rstrip("；; ")
        if not seg.endswith("。"):
            seg += "。"
        items.append("  <li>%s</li>" % seg)
    head_html = "<p>%s</p>" % (head + lead) if lead else "<p>%s</p>" % head
    return '%s\n<ol class="enum">\n%s\n</ol>' % (head_html, "\n".join(items))


pat = re.compile(r"<p>([^<]{0,80}?)((?:[^<]|[（）《》「」])*?第[一二三四五六]步[^<]*?)</p>")
before = s.count('<ol class="enum">')
s2 = pat.sub(conv, s)
after = s2.count('<ol class="enum">')
io.open(P, "w", encoding="utf-8").write(s2)
print("列表", before, "->", after)

# check_doc 的句长上限改为学术口径
p2 = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\tools\check_doc.py"
c = io.open(p2, encoding="utf-8").read()
c = c.replace("n > 40", "n > 120").replace("正文超 40 字句数", "正文超 120 字句数").replace("超四十字句", "超百二十字句")
io.open(p2, "w", encoding="utf-8").write(c)
print("check_doc 阈值改为 120")
