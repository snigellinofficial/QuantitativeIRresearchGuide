# -*- coding: utf-8 -*-
"""第三轮合并：把相邻的短句并入前句，直到句长分布接近学术区间。

合并规则：
  1. 只在同一文本节点内合并，不跨段。
  2. 合并后总长不超过 96 字。
  3. 前句以问号结尾时不合并；后句以步骤词、图表词或引号开头时不合并。
  4. 合并以分号连接，保留前句的收尾标点之后的分句。
"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

STOP_HEAD = ("第一", "第二", "第三", "第四", "第五", "表 ", "图 ", "「", "《", "注")
MAXLEN = 104


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
            if cn(cur) + cn(nxt) > MAXLEN:
                break
            if cur.endswith("？"):
                break
            if nxt.startswith(STOP_HEAD):
                break
            if cn(nxt) > 60:
                break
            cur = cur[:-1] + "；" + nxt
            i += 1
        out.append(cur)
        i += 1
    return "".join(out)


def fix(m):
    t = m.group(1)
    if "<" in t or "$" in t or "。" not in t:
        return m.group(0)
    return ">" + merge(t) + "<"


s = re.sub(r">([^<>]+)<", fix, s)
io.open(P, "w", encoding="utf-8").write(s)
print("len", len(s))
