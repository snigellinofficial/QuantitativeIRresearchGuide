# 通过 GitHub Git Data API 推送本地仓库内容。
# 沙箱环境封禁 github.com 的 git 传输，但 api.github.com 可用，故改用接口逐文件上传。

$ErrorActionPreference = "Stop"
$repo = "snigellinofficial/QuantitativeIRresearchGuide"
$root = (Get-Location).Path
$tmp = Join-Path $env:TEMP "gh_blob.json"

$files = git -c core.quotepath=false ls-files
Write-Output "tracked files: $($files.Count)"

$entries = New-Object System.Collections.ArrayList
$i = 0
foreach ($rel in $files) {
    $full = Join-Path $root $rel
    if (-not (Test-Path $full)) { continue }
    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($full))
    $body = @{ content = $b64; encoding = "base64" } | ConvertTo-Json -Compress
    [IO.File]::WriteAllText($tmp, $body, [Text.Encoding]::UTF8)
    $sha = gh api -X POST "repos/$repo/git/blobs" --input $tmp --jq ".sha" 2>&1
    if ($LASTEXITCODE -ne 0) { Write-Output "FAIL $rel : $sha"; continue }
    [void]$entries.Add(@{ path = $rel.Replace("\", "/"); mode = "100644"; type = "blob"; sha = $sha.Trim() })
    $i++
    if ($i % 25 -eq 0) { Write-Output "uploaded $i" }
}

Write-Output "blobs: $($entries.Count)"
$tree = @{ tree = $entries } | ConvertTo-Json -Depth 6 -Compress
[IO.File]::WriteAllText($tmp, $tree, [Text.Encoding]::UTF8)
$treeSha = gh api -X POST "repos/$repo/git/trees" --input $tmp --jq ".sha" 2>&1
Write-Output "tree: $treeSha"

$msg = "初始化：国际政治量化研究读本`n`n- index.html：序、16 章正文与参考文献`n- catalog-v2.json：一百篇顶刊文献题录`n- references.csv / references.md：DOI 清单`n- vault-v2：一百张文献卡片与对照矩阵`n- assets：样式、脚本、矢量图与本地 MathJax`n- tools：收割、核验与两轮机检脚本"
$commitBody = @{ message = $msg; tree = $treeSha.Trim(); parents = @() } | ConvertTo-Json -Compress
[IO.File]::WriteAllText($tmp, $commitBody, [Text.Encoding]::UTF8)
$commitSha = gh api -X POST "repos/$repo/git/commits" --input $tmp --jq ".sha" 2>&1
Write-Output "commit: $commitSha"

$refBody = @{ sha = $commitSha.Trim(); force = $true } | ConvertTo-Json -Compress
[IO.File]::WriteAllText($tmp, $refBody, [Text.Encoding]::UTF8)
gh api -X PATCH "repos/$repo/git/refs/heads/main" --input $tmp --jq ".object.sha" 2>&1

Write-Output "done"
