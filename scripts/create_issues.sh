#!/usr/bin/env bash
# T01 (hỗ trợ: Phúc) — Tạo GitHub issue cho mọi task trong .github/tasks.csv. Cần gh CLI đã đăng nhập.
# Dùng: bash scripts/create_issues.sh            (chạy thật)
#       DRY_RUN=1 bash scripts/create_issues.sh  (chỉ in ra)
set -euo pipefail
python3 - <<'PY'
import csv, os, subprocess
dry = os.getenv("DRY_RUN") == "1"
with open(".github/tasks.csv", newline="") as f:
    for r in csv.DictReader(f):
        title = f"[{r['id']}] {r['title']}"
        body = (f"**Phụ trách:** {r['owner']}\n**Hỗ trợ:** {r['supporter'] or '—'} {('– ' + r['support_task']) if r['support_task'] else ''}\n"
                f"**Phụ thuộc:** {r['deps']}\n**Tuần:** {r['week']} · **Hạn:** {r['due']}\n**Thư mục:** `{r['folder']}`\n**Ưu tiên:** {r['priority']}")
        cmd = ["gh", "issue", "create", "--title", title, "--body", body, "--label", "task"]
        print(title) if dry else subprocess.run(cmd, check=True)
PY
