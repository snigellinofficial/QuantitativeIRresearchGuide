# -*- coding: utf-8 -*-
"""以占位符保护行内标签与公式，在整段范围内合并短句。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

STOP_HEAD = ("表 ", "图 ", "「", "《", "注")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", TAG.sub("", x)))


TAG = re.compile(r"<[^>]+>")


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
            if cur.rstrip().endswith("？") or nxt.lstrip().startswith(STOP_HEAD):
                break
            if a <= 26 or b <= 22:
                cur = cur.rstrip()[:-1] + "；" + nxt.lstrip()
                i += 1
            else:
                break
        out.append(cur)
        i += 1
    return "".join(out)


def process_p(m):
    inner = m.group(1)
    if "<ol" in inner:
        return m.group(0)
    store = {}

    def keep(x):
        k = "@@%d@@" % len(store)
        store[k] = x.group(0)
        return k

    t = re.sub(r"<[^>]+>|\$[^$]*\$", keep, inner)
    t = merge(t)
    for k, v in store.items():
        t = t.replace(k, v)
    return "<p>%s</p>" % t


s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", process_p, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("len", len(s2))
