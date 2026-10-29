# -*- coding: utf-8 -*-
"""把条目全部以序数词开头的并列段改成编号列表。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

MARK = re.compile(r"^(第[一二三四五六]步|第[一二三四五六]|[一二三四五六]是|[1-9]）)")
TAG = re.compile(r"<[^>]+>")


def balanced(x):
    return x.count("<strong>") == x.count("</strong>") and x.count("<em>") == x.count("</em>")


def conv(m):
    inner = m.group(1)
    if "<ol" in inner or "<p" in inner:
        return m.group(0)
    plain = TAG.sub("", inner)
    segs = [x.strip() for x in plain.split("；") if x.strip()]
    if len(segs) < 3:
        return m.group(0)
    if not all(MARK.match(x) for x in segs[1:]):
        return m.group(0)
    parts = [x.strip() for x in inner.split("；") if x.strip()]
    if len(parts) != len(segs):
        return m.group(0)
    if not all(balanced(x) for x in parts):
        return m.group(0)
    lead = parts[0] if MARK.match(segs[0]) is None else ""
    body_items = parts[1:] if lead else parts
    if lead and not lead.endswith("。"):
        lead += "。"
    items = []
    for x in body_items:
        x = MARK.sub("", x).strip()
        if not x.endswith("。"):
            x += "。"
        items.append("  <li>%s</li>" % x)
    head = "<p>%s</p>\n" % lead if lead else ""
    return '%s<ol class="enum">\n%s\n</ol>' % (head, "\n".join(items))


before = s.count('<ol class="enum">')
s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", conv, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("列表", before, "->", s2.count('<ol class="enum">'))
