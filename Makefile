# Cấu hình riêng từng người (PY=, JAVA_HOME=...), không commit: xem Makefile.local.example
-include Makefile.local

# tensorflow chỉ có cho Python 3.10-3.12: tự chọn bản có sẵn trên máy; ghi đè bằng `make setup PY=...`
PY ?= $(firstword $(foreach v,3.12 3.11 3.10,$(shell command -v python$(v))))
# Dùng công cụ trong .venv (nếu có) cho test, lint, produce, dashboard mà không cần activate
BIN = $(if $(wildcard .venv/bin/python),.venv/bin/)

COMPOSE = docker compose -f infra/docker-compose.yml
SPARK_SUBMIT = $(COMPOSE) exec -u root -e PYTHONPATH=/opt/app spark-master spark-submit \
	--conf spark.executorEnv.PYTHONPATH=/opt/app --conf spark.jars.ivy=/tmp/.ivy2 \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0

.PHONY: up down data topics tables train stream produce dashboard test lint issues setup setup-hooks

up:            ## Khởi động hạ tầng
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

data:          ## Tải PaySim và đưa lên HDFS
	bash scripts/download_data.sh
	bash scripts/init_hdfs.sh

topics:        ## Tạo topic Kafka
	bash scripts/create_topics.sh

tables:        ## Tạo bảng Hive (external, Parquet trên HDFS)
	$(COMPOSE) exec -u root -e PYTHONPATH=/opt/app spark-master spark-sql -f /opt/app/sql/hive/01_create_tables.sql \
		--conf spark.hadoop.javax.jdo.option.ConnectionURL='jdbc:derby:;databaseName=/opt/app/metastore_db;create=true' \
		--conf spark.sql.warehouse.dir=hdfs://namenode:9000/user/hive/warehouse --conf spark.jars.ivy=/tmp/.ivy2

train:         ## Huấn luyện offline
	$(SPARK_SUBMIT) /opt/app/src/models/train.py

stream:        ## Chạy job streaming
	$(SPARK_SUBMIT) /opt/app/src/streaming/fraud_stream.py

produce:       ## Phát giao dịch vào Kafka
	$(BIN)python -m src.producer.paysim_producer --rate 200

dashboard:
	$(BIN)streamlit run src/dashboard/app.py

test:
	$(BIN)pytest -q

lint:
	$(BIN)ruff check src tests
	$(BIN)mypy src --ignore-missing-imports

issues:        ## Tạo GitHub issue từ .github/tasks.csv (cần gh CLI)
	bash scripts/create_issues.sh

setup:           ## Tạo .venv (Python 3.10-3.12), cài requirements, kiểm tra môi trường, bật git hook
	@[ -n "$(PY)" ] || { echo "Không thấy Python 3.10-3.12 (tensorflow chưa hỗ trợ 3.13+). Cài: brew install python@3.12, hoặc make setup PY=/đường/dẫn/python"; exit 1; }
	$(PY) -m venv .venv && .venv/bin/pip install -q -r requirements.txt
	@.venv/bin/python -c "import tensorflow, xgboost" 2>&1 | tail -1 | grep . && echo "^ Lỗi import. macOS thiếu OpenMP: brew install libomp" || true
	@java -version >/dev/null 2>&1 || echo "Cảnh báo: chưa có Java 11 (cần cho Spark/pytest): brew install openjdk@11 rồi đặt JAVA_HOME"
	$(MAKE) setup-hooks

setup-hooks:     ## Bật git hook lint/test trước commit/push
	git config core.hooksPath .githooks
