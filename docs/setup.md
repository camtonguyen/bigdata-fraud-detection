# Hướng dẫn cài đặt (T05 – Phúc)

Yêu cầu: Docker Desktop (≥ 8 GB RAM), **Python 3.10–3.12** (tensorflow chưa hỗ trợ 3.13+), Java 11, tài khoản Kaggle (API token).

```bash
make setup                     # tạo .venv, cài requirements, kiểm tra môi trường, bật git hook
cp .env.example .env
make up && make topics && make data && make tables
```

`make setup` tự chọn python3.12 / 3.11 / 3.10 có trên máy và báo cách cài nếu thiếu. `make test`, `make lint`, `make produce`, `make dashboard` tự dùng `.venv`, không cần `source .venv/bin/activate`.

## Cấu hình riêng từng người (tùy chọn)

Sao chép `Makefile.local.example` thành `Makefile.local` (file này không bị commit) rồi bỏ comment dòng cần dùng:

```make
PY = /opt/homebrew/bin/python3.12             # chọn đúng bản Python
export JAVA_HOME = /opt/homebrew/opt/openjdk@11   # Java 11 không phải bản mặc định
```

Hoặc chỉ ghi đè một lần: `make setup PY=python3.11`. Người dùng pyenv/uv có sẵn `.python-version` (3.12).

## Lỗi thường gặp trên macOS

| Triệu chứng | Cách xử lý |
|---|---|
| `No matching distribution found for tensorflow` | `python3` mặc định là 3.13+. `brew install python@3.12` rồi `make setup` |
| `libomp.dylib could not be loaded` (xgboost) | `brew install libomp` |
| `Unable to locate a Java Runtime` | `brew install openjdk@11`, đặt `JAVA_HOME` (xem trên) |
| `PYTHON_VERSION_MISMATCH` (Spark) | worker dùng Python khác driver: chạy qua `make test`, hoặc `export PYSPARK_PYTHON=$PWD/.venv/bin/python` |

## Không muốn cài Python/Java trên máy (tùy chọn, Docker)

Image `fraud-spark` đã có pyspark, xgboost, tensorflow và Java, repo được mount ở `/opt/app`. `make train` và `make stream` vốn đã chạy trong container. Chạy test trong container:

```bash
make up
docker compose -f infra/docker-compose.yml exec spark-master sh -c "pip install -q pytest && cd /opt/app && python -m pytest -q"
```

Cách này chậm hơn và cần Docker đang chạy; lint (`ruff`, `mypy`) và hook git vẫn cần `make setup` trên máy.

`make tables` tạo bảng Hive `fraud.*`; chạy lại sau khi streaming ghi dữ liệu mới để đăng ký partition. Derby chỉ cho 1 phiên truy vấn bảng cùng lúc.

Giao diện:
- HDFS NameNode: http://localhost:9870
- Spark Master: http://localhost:8080
- Dashboard: http://localhost:8501
