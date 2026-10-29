# -*- coding: utf-8 -*-
"""文档机检：标签配对、公式定界、数学内中文字符、资源存在性、句长、编号序列。"""
import io
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

VOID = {"br", "img", "meta", "link", "input", "hr", "source"}


class Balancer(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.err = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.err.append(("多余闭合", tag, self.getpos()))
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.err.append(("不匹配", tag, self.stack[-1][0], self.getpos()))
            for k in range(len(self.stack) - 1, -1, -1):
                if self.stack[k][0] == tag:
                    del self.stack[k:]
                    break


p = Balancer()
p.feed(s)
print("未闭合标签:", p.stack[:6])
print("标签错误:", p.err[:6])

disp = s.count("$$")
inline = s.replace("$$", "").count("$")
print("$$ 个数 %d（偶数 %s）｜行内 $ 个数 %d（偶数 %s）"
      % (disp, disp % 2 == 0, inline, inline % 2 == 0))

bad = []
for m in re.finditer(r"\$\$(.+?)\$\$", s, re.S):
    if any(ord(ch) > 127 for ch in m.group(1)):
        bad.append(m.group(1)[:60].replace("\n", " "))
for m in re.finditer(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", s):
    if any(ord(ch) > 127 for ch in m.group(1)):
        bad.append(m.group(1)[:60])
print("数学内的中文:", len(bad), bad[:3])

nums = re.findall(r'class="eqno">\(([\d.]+)\)<', s)
print("编号公式:", len(nums), nums)

missing = []
for m in re.finditer(r'(?:src|href)="((?:assets|vault-v2|vault)/[^"]+)"', s):
    if not os.path.exists(os.path.join(ROOT, m.group(1))):
        missing.append(m.group(1))
print("缺失资源:", missing)

ids = set(re.findall(r'id="([^"]+)"', s))
links = set(re.findall(r'href="#([^"]+)"', s))
print("失效锚点:", sorted(links - ids)[:8])

main = s[s.find("<main"):s.find("</main>")]
t = re.sub(r"<table.*?</table>", "。", main, flags=re.S)
t = re.sub(r"<figure.*?</figure>", "。", t, flags=re.S)
t = re.sub(r'<div class="trace">', "", t)
t = re.sub(r"<h[1-4][^>]*>.*?</h[1-4]>", "。", t, flags=re.S)
t = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
t = re.sub(r"\$[^$]*\$", "", t)
t = re.sub(r"<strong>|</strong>|<em>|</em>", "", t)
t = re.sub(r"<[^>]+>", "", t)
t = re.sub(r"\s+", "", t)
sents = [x for x in re.split(r"[。！？]", t) if x]
over = [(len(re.findall(r"[\u4e00-\u9fff]", x)), x[:40]) for x in sents]
over = [x for x in over if x[0] > 40]
print("超百二十字句:", len(over), "共 %d 句" % len(sents))
for n, x in sorted(over, reverse=True)[:8]:
    print("   %d %s" % (n, x))

cn = len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"<[^>]+>", " ", main)))
print("正文汉字:", cn, "｜文件大小:", os.path.getsize(P))
