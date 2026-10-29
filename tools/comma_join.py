# -*- coding: utf-8 -*-
"""用逗号承接短句，替代分号串联。

汉语中逗号可以承接以连词起头的分句，分号只用于并列。此法在不滥用分号的前提下恢复句长。
"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

TAG = re.compile(r"<[^>]+>")
CONN = ("因此", "所以", "但", "而", "这", "该", "其", "同时", "于是", "从而",
        "进而", "故", "若", "如果", "此外", "另外", "其中", "此时", "这时")
MAX = 96


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", TAG.sub("", x)))


def join(txt):
    parts = [x for x in re.split(r"(?<=[。！？])", txt) if x]
    out, i = [], 0
    while i < len(parts):
        cur = parts[i]
        while i + 1 < len(parts):
            nxt = parts[i + 1]
            r = TAG.sub("", nxt).lstrip()
            if cn(cur) + cn(nxt) > MAX:
                break
            if cur.rstrip().endswith("？"):
                break
            if r.startswith(CONN) and cn(cur) >= 12:
                cur = cur.rstrip()[:-1] + "，" + nxt.lstrip()
                i += 1
            else:
                break
        out.append(cur)
        i += 1
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
    t = join(t)
    for k, v in store.items():
        t = t.replace(k, v)
    return "<p>%s</p>" % t


s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", process, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("len", len(s2))
