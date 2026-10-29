# -*- coding: utf-8 -*-
"""把外链 SVG 改为内嵌数据地址，使图片不依赖目录结构。"""
import base64
import io
import os
import re

ROOT = r"C:\Users\87878\Desktop\毕业论文\地理量化文献综述"
P = os.path.join(ROOT, "index.html")
s = io.open(P, encoding="utf-8").read()

count = 0
for path in sorted(set(re.findall(r'src="(assets/fig/[^"]+)"', s))):
    fp = os.path.join(ROOT, path.replace("/", os.sep))
    with open(fp, "rb") as f:
        uri = "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")
    s = s.replace('src="%s"' % path, 'src="%s"' % uri)
    count += 1

io.open(P, "w", encoding="utf-8").write(s)
print("内嵌图数", count, "｜文件字节", len(s))
