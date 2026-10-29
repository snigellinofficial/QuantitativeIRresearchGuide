# -*- coding: utf-8 -*-
"""按汉语标点规范复核分号。

规范：分号用于并列分句之间，或非并列多重复句的第一层分句之间，或分项列举的各项之间。
判据：以下四条满足其一，判为并列，保留分号；否则改为句号。

一、后一分句以「而、则、也、同时、另外、反之、相反、此外、并且」起头。
二、分句以序数词或列举词起头，如「第一」「二是」「第N步」。
三、两侧分句都不超过三十二字，属短句并列。
四、两侧分句以相同两字起头，属同构并列。
"""
import io
import re

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

TAG = re.compile(r"<[^>]+>")
PARA_START = ("而", "则", "也", "同时", "另外", "反之", "相反", "此外", "并且", "但")
ORD = re.compile(r"^(第[一二三四五六]步|第[一二三四五六]|[一二三四五六]是|[1-9]）|一是|二是|三是)")


def cn(x):
    return len(re.findall(r"[\u4e00-\u9fff]", TAG.sub("", x)))


def keep(left, right):
    r = TAG.sub("", right).strip()
    l = TAG.sub("", left).strip()
    if r.startswith(PARA_START):
        return True
    if ORD.match(r) or ORD.match(l):
        return True
    if cn(left) <= 32 and cn(right) <= 32:
        return True
    if len(l) >= 2 and len(r) >= 2 and l[:2] == r[:2]:
        return True
    return False


stats = {"keep": 0, "drop": 0}


def process(m):
    inner = m.group(1)
    if "<ol" in inner or "<table" in inner:
        return m.group(0)
    if "；" not in inner:
        return m.group(0)
    parts = inner.split("；")
    out = [parts[0]]
    for seg in parts[1:]:
        if keep(out[-1], seg):
            out[-1] = out[-1] + "；"
            stats["keep"] += 1
        else:
            out[-1] = out[-1] + "。"
            stats["drop"] += 1
        out.append(seg)
    return "<p>%s</p>" % "".join(out)


s2 = re.sub(r"<p>((?:(?!</p>).)*?)</p>", process, s, flags=re.S)
io.open(P, "w", encoding="utf-8").write(s2)
print("保留", stats["keep"], "｜改句号", stats["drop"], "｜分号总数", s.count("；"), "->", s2.count("；"))
