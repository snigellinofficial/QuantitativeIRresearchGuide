# -*- coding: utf-8 -*-
"""加大合并力度，把短句连成短—长—短的节奏。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

CONN = ("这", "该", "其", "此", "但", "而", "故", "所以", "因此", "若", "同时",
        "于是", "从而", "进而", "后者", "前者", "据此", "相对", "另外", "此外",
        "在", "对", "据", "从", "把", "由", "当", "与")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def merge(txt):
    if cn(txt) < 45:
        return txt
    parts = [x for x in re.split(r"(?<=[。！？])", txt) if x]
    out, i = [], 0
    while i < len(parts):
        cur = parts[i]
        while i + 1 < len(parts):
            nxt = parts[i + 1]
            a, b = cn(cur), cn(nxt)
            if a + b > 108:
                break
            if b > 58:
                break
            if nxt.startswith(CONN) or a <= 30 or b <= 22:
                cur = cur[:-1] + "；" + nxt
                i += 1
            else:
                break
        out.append(cur)
        i += 1
    return "".join(out)


def fix_node(m):
    t = m.group(1)
    if "<" in t or "MATH" in t or "。" not in t:
        return m.group(0)
    return ">" + merge(t) + "<"


s = re.sub(r">([^<>]+)<", fix_node, s)
io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
