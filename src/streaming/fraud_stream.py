"""T19 (Hoà, hỗ trợ: Tố) — Spark Structured Streaming: Kafka → features → chấm điểm → sinks."""
from pyspark.sql import functions as F

from src.common.config import KAFKA_BOOTSTRAP, TOPIC_TX
from src.common.schema import PAYSIM_SCHEMA
from src.common.spark import get_spark
from src.features.build_features import build_features
from src.streaming.sinks import write_alerts, write_predictions

TX_SCHEMA = (PAYSIM_SCHEMA
             .add("tx_id", "string")
             .add("event_time", "timestamp"))


def main() -> None:
    spark = get_spark("fraud-stream")
    raw = (spark.readStream.format("kafka")
           .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
           .option("subscribe", TOPIC_TX)
           .option("startingOffsets", "latest")
           .load())

    tx = (raw.select(F.from_json(F.col("value").cast("string"), TX_SCHEMA).alias("t"))
             .select("t.*")
             .withWatermark("event_time", "1 minute"))

    feats = build_features(tx)
    # TODO T19: gọi src.models.registry.score() (T17) và tính xgb_score, ae_score, hybrid_score
    scored = feats.withColumn("hybrid_score", F.lit(0.0))

    write_predictions(scored)
    write_alerts(scored)
    spark.streams.awaitAnyTermination()


if __name__ == "__main__":
    main()
