# -*- coding: utf-8 -*-
"""找出被机械断句切断的复句，并把断点改回逗号。

判据：一句含「若／如果／虽然／因为／由于／即使」，却缺「就／则／便／也／才／都／故／所以／因此」，
说明条件从句被单独切出，后一句才是主句。
"""
import io
import re
import sys

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = ROOT + r"\index.html"
s = io.open(P, encoding="utf-8").read()

COND = ("若", "如果", "虽然", "因为", "由于", "即使", "尽管")
VERT = ("就", "则", "便", "也", "才", "都", "故", "所以", "因此", "于是")

TAG = re.compile(r"<[^>]+>")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def broken(seg):
    plain = TAG.sub("", seg)
    if not any(c in plain for c in COND):
        return False
    return not any(v in plain for v in VERT)


report = []
out = []
count = 0


def process(m):
    global count
    inner = m.group(1)
    if "<ol" in inner:
        return m.group(0)
    parts = re.split(r"(?<=[。！？])", inner)
    parts = [x for x in parts if x]
    if len(parts) < 2:
        return m.group(0)
    res = []
    i = 0
    while i < len(parts):
        cur = parts[i]
        if i + 1 < len(parts) and cur.endswith("。") and broken(cur):
            nxt = parts[i + 1]
            if cn(cur) + cn(nxt) <= 130:
                res.append(cur[:-1] + "，" + nxt)
                report.append((TAG.sub("", cur)[:40], TAG.sub("", nxt)[:24]))
                count += 1
                i += 2
                continue
        res.append(cur)
        i += 1
    return "<p>%s</p>" % "".join(res)


s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", process, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("修复断句", count)
for a, b in report[:20]:
    print("  ", a, "‖", b)
