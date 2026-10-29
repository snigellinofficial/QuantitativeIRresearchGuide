# -*- coding: utf-8 -*-
"""回退误转的列表：只有全部条目以序数词开头时才保留为列表。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

MARK = re.compile(r"^(第[一二三四五六]步|第[一二三四五六]|[一二三四五六]是|[1-9]）)")
lists = list(re.finditer(r"<p>([^<]{0,90})</p>\s*<ol class=\"enum\">(.*?)</ol>", s, flags=re.S))
print("列表总数", len(lists))

keep = revert = 0
out = s
for m in reversed(lists):
    lead, body = m.group(1), m.group(2)
    items = re.findall(r"<li>(.*?)</li>", body, flags=re.S)
    if "三种读法" in lead:
        keep += 1
        continue
    if all(MARK.match(re.sub(r"<[^>]+>", "", x).strip()) for x in items):
        keep += 1
        continue
    joined = lead + "；".join(x.strip() for x in items)
    out = out[:m.start()] + "<p>%s</p>" % joined + out[m.end():]
    revert += 1

io.open(P, "w", encoding="utf-8").write(out)
print("保留", keep, "回退", revert)
