# -*- coding: utf-8 -*-
"""通过 GitHub API 上传仓库内容。

空仓库不接受 Git Data 接口，故先用 Contents 接口建立首个提交，再一次性写入全量树。
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = "snigellinofficial/QuantitativeIRresearchGuide"
TOKEN = os.environ.get("GH_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIST = os.path.join(ROOT, "tools", "_files.txt")


def api(method, path, payload=None):
    url = "https://api.github.com" + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "lit-review-push",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def b64_of(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def blob(rel):
    body = {"content": b64_of(rel), "encoding": "base64"}
    for attempt in range(3):
        try:
            return rel, api("POST", "/repos/%s/git/blobs" % REPO, body)["sha"]
        except urllib.error.HTTPError as e:
            if attempt == 2:
                print("FAIL", rel, e.code, e.read()[:80], flush=True)
                return rel, None
        except Exception as e:
            if attempt == 2:
                print("FAIL", rel, repr(e)[:80], flush=True)
                return rel, None
    return rel, None


def main():
    files = [x.strip().lstrip("\ufeff") for x in open(LIST, encoding="utf-8-sig") if x.strip()]
    files = [f for f in files if os.path.exists(os.path.join(ROOT, f))]
    print("files", len(files), flush=True)

    # 首个提交：用 Contents 接口建立 README，使仓库非空
    try:
        head = api("GET", "/repos/%s/commits/main" % REPO)
        base_commit = head["sha"]
        base_tree = head["commit"]["tree"]["sha"]
        print("existing head", base_commit, flush=True)
    except Exception:
        seed = api("PUT", "/repos/%s/contents/README.md" % REPO, {
            "message": "建立仓库",
            "content": b64_of("README.md"),
            "branch": "main",
        })
        base_commit = seed["commit"]["sha"]
        base_tree = seed["commit"]["tree"]["sha"]
        print("seed commit", base_commit, flush=True)

    entries, done = [], 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        for rel, sha in ex.map(blob, files):
            done += 1
            if sha:
                entries.append({"path": rel.replace("\\", "/"), "mode": "100644",
                                "type": "blob", "sha": sha})
            if done % 50 == 0:
                print("uploaded", done, flush=True)

    print("blobs", len(entries), flush=True)
    tree = api("POST", "/repos/%s/git/trees" % REPO, {"tree": entries, "base_tree": base_tree})
    print("tree", tree["sha"], flush=True)

    msg = ("初始化：国际政治量化研究读本\n\n"
           "- index.html：序、16 章正文与参考文献\n"
           "- catalog-v2.json：一百篇顶刊文献题录\n"
           "- references.csv / references.md：DOI 清单\n"
           "- vault-v2：一百张文献卡片与对照矩阵\n"
           "- assets：样式、脚本、矢量图与本地 MathJax\n"
           "- tools：收割、核验与两轮机检脚本")
    commit = api("POST", "/repos/%s/git/commits" % REPO,
                 {"message": msg, "tree": tree["sha"], "parents": [base_commit]})
    print("commit", commit["sha"], flush=True)

    ref = api("PATCH", "/repos/%s/git/refs/heads/main" % REPO,
              {"sha": commit["sha"], "force": True})
    print("ref", ref["object"]["sha"], flush=True)
    print("done")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
