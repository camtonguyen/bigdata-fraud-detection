"""T08 (Hoà) — Đọc PaySim CSV trên HDFS, ghi Parquet vào bảng fraud.transactions_raw."""
from src.common.config import CURATED_PATH, RAW_PATH
from src.common.schema import PAYSIM_SCHEMA
from src.common.spark import get_spark


def main() -> None:
    spark = get_spark("paysim-ingestion")
    df = spark.read.csv(RAW_PATH, header=True, schema=PAYSIM_SCHEMA)
    df.write.mode("overwrite").parquet(f"{CURATED_PATH}/transactions_raw")
    print("rows:", df.count())


if __name__ == "__main__":
    main()
