# -*- coding: utf-8 -*-
"""把过长的复句在合适的分号处断开，恢复长短句交错。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

TAG = re.compile(r"<[^>]+>")
LIMIT = 82


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", TAG.sub("", x)))


def split_long(txt):
    out = []
    for sent in [x for x in re.split(r"(?<=[。！？])", txt) if x]:
        if cn(sent) <= LIMIT or "；" not in sent:
            out.append(sent)
            continue
        body = cn(sent)
        pos = [m.start() for m in re.finditer("；", sent)]
        cand = [p for p in pos if 22 <= cn(sent[:p]) <= body - 22]
        if not cand:
            out.append(sent)
            continue
        mid = body / 2
        p = min(cand, key=lambda x: abs(cn(sent[:x]) - mid))
        out.append(sent[:p] + "。")
        out.append(sent[p + 1:])
    return "".join(out)


def process(m):
    inner = m.group(1)
    if "<ol" in inner:
        return m.group(0)
    store = {}

    def keep(x):
        k = "@@%d@@" % len(store)
        store[k] = x.group(0)
        return k

    t = re.sub(r"<[^>]+>|\$[^$]*\$", keep, inner)
    t = split_long(t)
    for k, v in store.items():
        t = t.replace(k, v)
    return "<p>%s</p>" % t


s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", process, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("len", len(s2))
