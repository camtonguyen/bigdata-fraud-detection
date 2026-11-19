#!/usr/bin/env bash
# T08 (Hoà) — Tải PaySim từ Kaggle (cần ~/.kaggle/kaggle.json)
set -euo pipefail
mkdir -p data/raw
kaggle datasets download -d ealaxi/paysim1 -p data/raw --unzip
ls -lh data/raw
