COMPOSE = docker compose -f infra/docker-compose.yml
SPARK_SUBMIT = $(COMPOSE) exec spark-master spark-submit \
	--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0

.PHONY: up down data topics train stream produce dashboard test lint issues

up:            ## Khởi động hạ tầng
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

data:          ## Tải PaySim và đưa lên HDFS
	bash scripts/download_data.sh
	bash scripts/init_hdfs.sh

topics:        ## Tạo topic Kafka
	bash scripts/create_topics.sh

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

issues:        ## Tạo GitHub issue từ .github/tasks.csv (cần gh CLI)
	bash scripts/create_issues.sh
