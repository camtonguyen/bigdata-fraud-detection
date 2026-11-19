"""T18 (Phúc, hỗ trợ: Hoà) — Phát lại PaySim vào Kafka theo thứ tự step, điều chỉnh tốc độ."""
import argparse
import csv
import json
import time
import uuid
from datetime import UTC, datetime

from kafka import KafkaProducer

from src.common.config import KAFKA_BOOTSTRAP, TOPIC_TX


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="data/sample/paysim_sample.csv")
    ap.add_argument("--rate", type=int, default=100, help="giao dịch / giây")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP,
                             value_serializer=lambda v: json.dumps(v).encode(),
                             linger_ms=10)
    interval = 1.0 / args.rate
    with open(args.file, newline="") as f:
        for i, row in enumerate(csv.DictReader(f)):
            if args.limit and i >= args.limit:
                break
            row["tx_id"] = str(uuid.uuid4())
            row["event_time"] = datetime.now(UTC).isoformat()
            producer.send(TOPIC_TX, key=row["nameOrig"].encode(), value=row)
            time.sleep(interval)
    producer.flush()


if __name__ == "__main__":
    main()
