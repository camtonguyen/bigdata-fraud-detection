COMPOSE = docker compose -f infra/docker-compose.yml
SPARK_SUBMIT = $(COMPOSE) exec -u root -e PYTHONPATH=/opt/app spark-master spark-submit \
	--conf spark.executorEnv.PYTHONPATH=/opt/app --conf spark.jars.ivy=/tmp/.ivy2 \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0

.PHONY: up down data topics tables train stream produce dashboard test lint issues setup-hooks

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
	python -m src.producer.paysim_producer --rate 200

dashboard:
	streamlit run src/dashboard/app.py

test:
	pytest -q

lint:
	ruff check src tests
	mypy src --ignore-missing-imports

issues:        ## Tạo GitHub issue từ .github/tasks.csv (cần gh CLI)
	bash scripts/create_issues.sh

setup-hooks:     ## Bật git hook lint/test trước commit/push
	git config core.hooksPath .githooks
