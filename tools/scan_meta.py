# -*- coding: utf-8 -*-
"""扫描防御性、元信息与冒号误用。"""
import io
import re
import sys

sys.path.insert(0, "tools")
from check_academic import visible_text, paragraphs  # noqa

P = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述\index.html"
s = io.open(P, encoding="utf-8").read()

META = ["口径", "检索日期", "Crossref", "OpenAlex", "谷歌学术", "不可比", "核验",
        "标注", "项目根目录", "UTF-8", "字节序", "可机读", "见本书", "参见第",
        "引用量", "统计口径", "数值不具可比性"]

print("== 元信息与防御性 ==")
seen = set()
for p in paragraphs(visible_text(s)):
    for w in META:
        if w in p and p[:40] not in seen:
            seen.add(p[:40])
            print("  [%s] %s" % (w, p[:120]))
            break

print()
print("== 图注与表注 ==")
for m in re.finditer(r"<caption>(.*?)</caption>", s, flags=re.S):
    t = re.sub(r"<[^>]+>", "", m.group(1))
    if any(w in t for w in ("口径", "Crossref", "不可比", "检索日期")):
        print("  ", t[:110])

print()
print("== 冒号被分号替代的可疑处 ==")
for m in re.finditer(r"[^。；]{0,30}(部分|方面|层级|类|项|步|条|个)[^。；]{0,6}；第[一二三四]", visible_text(s)):
    print("  ", m.group(0)[:80])
