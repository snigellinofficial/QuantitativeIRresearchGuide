# -*- coding: utf-8 -*-
"""把超过四十字的句子在合适的逗号处断开。

规则：
  1. 只处理纯文本节点，含 $ 数学的行内片段整体跳过。
  2. 断点优先取句中最接近中点的逗号。
  3. 该逗号后若为列举连接词（以及、和、与、或、并且、同时），跳过。
  4. 反复处理直到不超过四十字，或找不到合适断点。
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

BAD_NEXT = ("以及", "和", "与", "或", "并且", "同时", "乃至", "及")


def cn_len(x):
    return len(re.findall(r"[\u4e00-\u9fff]", x))


def split_once(sent):
    if cn_len(sent) <= 40:
        return [sent]
    cands = []
    for m in re.finditer("，", sent):
        p = m.start()
        before = cn_len(sent[:p])
        after = cn_len(sent[p + 1:])
        if before < 12 or after < 12:
            continue
        nxt = sent[p + 1:p + 3]
        if any(nxt.startswith(b) for b in BAD_NEXT):
            continue
        score = abs(before - after)
        cands.append((score, p))
    if not cands:
        return [sent]
    cands.sort()
    p = cands[0][1]
    left = sent[:p] + "。"
    right = sent[p + 1:]
    return split_once(left) + split_once(right)


def fix_text(txt):
    if "$" in txt or cn_len(txt) <= 40:
        return txt
    parts = re.split(r"([。！？])", txt)
    out = []
    buf = ""
    for piece in parts:
        if piece in "。！？":
            buf += piece
            out.append("".join(split_once(buf)))
            buf = ""
        else:
            buf += piece
    if buf:
        out.append("".join(split_once(buf)))
    return "".join(out)


def repl(m):
    return ">" + fix_text(m.group(1)) + "<"


before = len(s)
s2 = re.sub(r">([^<>]+)<", repl, s)
io.open(P, "w", encoding="utf-8").write(s2)
print("字符变化", before, "->", len(s2))
