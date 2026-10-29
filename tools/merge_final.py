# -*- coding: utf-8 -*-
"""收尾合并：优先吞并二十字以下的短句。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

STOP_HEAD = ("表 ", "图 ", "「", "《", "注")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def merge(txt):
    parts = [x for x in re.split(r"(?<=[。！？])", txt) if x]
    out, i = [], 0
    while i < len(parts):
        cur = parts[i]
        while i + 1 < len(parts):
            nxt = parts[i + 1]
            a, b = cn(cur), cn(nxt)
            if a + b > 100:
                break
            if cur.endswith("？") or nxt.startswith(STOP_HEAD):
                break
            if a <= 24 or b <= 24:
                cur = cur[:-1] + "；" + nxt
                i += 1
            else:
                break
        out.append(cur)
        i += 1
    return "".join(out)


def fix(m):
    t = m.group(1)
    if "<" in t:
        return m.group(0)
    holder = {}

    def keep(x):
        k = "@@M%d@@" % len(holder)
        holder[k] = x.group(0)
        return k

    t = re.sub(r"\$[^$]*\$", keep, t)
    t = merge(t)
    for k, v in holder.items():
        t = t.replace(k, v)
    return ">" + t + "<"


s = re.sub(r">([^<>]+)<", fix, s)
io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
