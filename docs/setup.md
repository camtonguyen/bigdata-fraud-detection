# Hướng dẫn cài đặt (T05 – Phúc)

Yêu cầu: Docker Desktop (≥ 8 GB RAM), Python 3.10, Java 11, tài khoản Kaggle (API token).

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
make up && make topics && make data
```

Giao diện:
- HDFS NameNode: http://localhost:9870
- Spark Master: http://localhost:8080
- Dashboard: http://localhost:8501
