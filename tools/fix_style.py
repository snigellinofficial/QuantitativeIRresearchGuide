# -*- coding: utf-8 -*-
"""依据第一轮机检结果修订：补表头、清禁用词、改写冒号句、合并短句。"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1 表头补列
# 专题表原先把期刊与卷期合并为一格，表头却分两列
s = s.replace("<th>期刊</th><th>卷期</th>", "<th>期刊与卷期</th>")
print("表头修复", s.count("<th>期刊与卷期</th>"))

# ---------------------------------------------------------------- 2 禁用词
REPL = [
    ("非常重要", "关键"),
    ("非常", "很"),
    ("极大", "明显"),
    ("至关重要", "关键"),
]
for a, b in REPL:
    s = s.replace(a, b)

# ---------------------------------------------------------------- 3 冒号引出完整句
def colon_fix(txt):
    return re.sub(r"：([^。！？\\n]{15,})。", lambda m: "。" + m.group(1) + "。", txt)

# ---------------------------------------------------------------- 4 合并短句
CONN = ("这", "该", "其", "此", "但", "而", "故", "所以", "因此", "若", "同时",
        "于是", "从而", "进而", "后者", "前者", "据此", "相对", "另外", "此外")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def merge(txt):
    if "$" in txt or cn(txt) < 40:
        return txt
    parts = re.split(r"(?<=[。！？])", txt)
    parts = [x for x in parts if x]
    out = []
    i = 0
    while i < len(parts):
        cur = parts[i]
        while i + 1 < len(parts):
            nxt = parts[i + 1]
            a, b = cn(cur), cn(nxt)
            if a + b > 86:
                break
            if b > 34:
                break
            if a <= 34 and (nxt.startswith(CONN) or a <= 22):
                cur = cur[:-1] + "；" + nxt
                i += 1
            else:
                break
        out.append(cur)
        i += 1
    return "".join(out)


def fix_node(m):
    t = m.group(1)
    if "<" in t or "MATH" in t:
        return m.group(0)
    t = colon_fix(t)
    t = merge(t)
    return ">" + t + "<"


s = re.sub(r">([^<>]+)<", fix_node, s)

io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
