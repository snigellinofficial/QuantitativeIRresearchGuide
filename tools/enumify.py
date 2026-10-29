# -*- coding: utf-8 -*-
"""把以序数词开头的并列段落改为编号列表。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

MARK = re.compile(r"^(第[一二三四五六]步|第[一二三四五六]|其[一二三四五]|[一二三四五]是|[1-9]）)")


def split_items(body):
    parts = [x.strip() for x in body.split("；")]
    if len(parts) < 3:
        return None
    marked = sum(1 for x in parts if MARK.match(x))
    if marked < len(parts) - 1:
        return None
    return parts


def conv(m):
    head, body = m.group(1), m.group(2)
    if "<" in body:
        return m.group(0)
    items = split_items(body)
    if not items:
        return m.group(0)
    out = []
    for x in items:
        x = MARK.sub("", x).strip()
        if not x.endswith("。"):
            x += "。"
        out.append("  <li>%s</li>" % x)
    return "<p>%s</p>\n<ol class=\"enum\">\n%s\n</ol>" % (head, "\n".join(out))


pat = re.compile(r"<p>([^<]{0,60}?。)((?:[^<]|[，、：（）《》「」])*?；[^<]*?。)(?:[^<]{0,30})?</p>")
s2, n = pat.subn(conv, s)
io.open(P, "w", encoding="utf-8").write(s2)
print("转换", n, "｜现有列表", s2.count('<ol class="enum">'))
