# -*- coding: utf-8 -*-
"""扫描口语化表述、防御性文字与需要分行的并列结构。"""
import io
import re
import sys

sys.path.insert(0, "tools")
from check_academic import visible_text, paragraphs, cn  # noqa

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

COLLOQ = ["都成立", "都行", "挺好", "好多", "差不多", "看看", "想想", "拿来", "搞",
          "弄", "一下子", "其实", "反正", "大概", "咱们", "人家", "啥", "怎么着",
          "这边", "那边", "后面", "前面", "干", "挺", "特别", "一上来", "说白了",
          "好比", "打个比方", "举个例子说", "不用说", "不用说也", "谁都知道",
          "一目了然", "不难发现", "显而易见", "众所周知", "我们都知道"]

DEFENSIVE = ["仅供参考", "免责", "局限", "未能", "尚未", "未逐段", "未获全文",
             "不可混用", "请注意", "需要说明", "需要指出", "本文档", "本交付",
             "核验", "免责声明", "谨慎使用", "以偏概全", "难免", "不足之处"]

hits_c, hits_d, enums = [], [], []
for p in paragraphs(visible_text(s)):
    for w in COLLOQ:
        if w in p:
            hits_c.append((w, p[:70]))
    for w in DEFENSIVE:
        if w in p:
            hits_d.append((w, p[:70]))
    n_semi = p.count("；")
    if n_semi >= 2 and cn(p) >= 70:
        enums.append((n_semi, cn(p), p[:90]))

print("== 口语化 ==", len(hits_c))
seen = set()
for w, t in hits_c:
    if w in seen:
        continue
    seen.add(w)
    print("  %s | %s" % (w, t))
print()
print("== 防御性 ==", len(hits_d))
for w, t in hits_d[:20]:
    print("  %s | %s" % (w, t))
print()
print("== 需分行的并列段 ==", len(enums))
for n, c, t in sorted(enums, reverse=True)[:25]:
    print("  分号%d 字数%d | %s" % (n, c, t))
