"""T20 (Hoà) — Ghi kết quả ra HDFS/Hive (Parquet) và topic fraud-alerts."""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from src.common.config import (
    CHECKPOINT_PATH,
    CURATED_PATH,
    FRAUD_THRESHOLD,
    KAFKA_BOOTSTRAP,
    TOPIC_ALERTS,
)


def write_predictions(df: DataFrame):
    return (df.withColumn("dt", F.to_date("event_time").cast("string"))
              .writeStream.format("parquet")
              .option("path", f"{CURATED_PATH}/predictions")
              .option("checkpointLocation", f"{CHECKPOINT_PATH}/predictions")
              .partitionBy("dt")
              .trigger(processingTime="5 seconds")
              .start())


def write_alerts(df: DataFrame):
    alerts = df.filter(F.col("hybrid_score") >= FRAUD_THRESHOLD)
    return (alerts.select(F.col("tx_id").alias("key"),
                          F.to_json(F.struct("*")).alias("value"))
                  .writeStream.format("kafka")
                  .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
                  .option("topic", TOPIC_ALERTS)
                  .option("checkpointLocation", f"{CHECKPOINT_PATH}/alerts")
                  .start())
