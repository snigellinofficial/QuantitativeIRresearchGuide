# -*- coding: utf-8 -*-
"""数学占位保护的合并与拆分，避免含公式的段落被整段跳过。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

STOP_HEAD = ("第一", "第二", "第三", "第四", "第五", "表 ", "图 ", "「", "《", "注")
MAX_MERGE = 104
MAX_SENT = 110


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def merge(txt):
    if cn(txt) < 24:
        return txt
    parts = [x for x in re.split(r"(?<=[。！？])", txt) if x]
    out, i = [], 0
    while i < len(parts):
        cur = parts[i]
        while i + 1 < len(parts):
            nxt = parts[i + 1]
            if cn(cur) + cn(nxt) > MAX_MERGE:
                break
            if cur.endswith("？") or nxt.startswith(STOP_HEAD) or cn(nxt) > 62:
                break
            cur = cur[:-1] + "；" + nxt
            i += 1
        out.append(cur)
        i += 1
    return "".join(out)


def split_long(txt):
    out = []
    for sent in [x for x in re.split(r"(?<=[。！？])", txt) if x]:
        if cn(sent) <= MAX_SENT:
            out.append(sent)
            continue
        pos = [m.start() for m in re.finditer("；", sent)]
        body = cn(sent)
        cand = [p for p in pos if 20 <= cn(sent[:p]) <= body - 20]
        if not cand:
            out.append(sent)
            continue
        mid = body / 2
        p = min(cand, key=lambda x: abs(cn(sent[:x]) - mid))
        out.append(sent[:p] + "。")
        out.append(sent[p + 1:])
    return "".join(out)


def fix_node(m):
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
    t = split_long(t)
    for k, v in holder.items():
        t = t.replace(k, v)
    return ">" + t + "<"


s = re.sub(r">([^<>]+)<", fix_node, s)
io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
