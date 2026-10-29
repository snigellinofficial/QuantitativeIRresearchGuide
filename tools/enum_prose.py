# -*- coding: utf-8 -*-
"""把以分号压缩的并列段拆成引导句加编号列表。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

TAG = re.compile(r"<[^>]+>")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def conv(m):
    inner = m.group(1)
    if "<ol" in inner or "<table" in inner:
        return m.group(0)
    plain = TAG.sub("", inner)
    segs = [x.strip() for x in plain.split("；") if x.strip()]
    if len(segs) < 4:
        return m.group(0)
    short = sum(1 for x in segs if cn(x) < 20)
    if short < 2:
        return m.group(0)
    if len(segs) > 8:
        return m.group(0)

    # 按分号切分原始 HTML，保持行内标签
    parts = [x.strip() for x in inner.split("；") if x.strip()]
    if len(parts) < 4:
        return m.group(0)

    lead = parts[0]
    if not lead.endswith("。"):
        lead += "。"
    items = []
    for x in parts[1:]:
        x = x.strip()
        x = re.sub(r"^(第[一二三四五六]步|第[一二三四五六]|[一二三四五六]是|[1-9]）)[，、]?", "", x)
        if not x.endswith("。"):
            x += "。"
        items.append("  <li>%s</li>" % x)
    return "<p>%s</p>\n<ol class=\"enum\">\n%s\n</ol>" % (lead, "\n".join(items))


before = s.count('<ol class="enum">')
s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", conv, s, flags=re.S)
after = s2.count('<ol class="enum">')
io.open(P, "w", encoding="utf-8").write(s2)
print("列表", before, "->", after)
