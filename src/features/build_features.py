"""T11 (Tố; unit test: Phúc) — Feature engineering dùng chung cho batch (train) và streaming (score).

Giữ logic ở một chỗ để tránh lệch feature giữa offline và online.
"""
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

FRAUD_TYPES = ["TRANSFER", "CASH_OUT"]  # gian lận PaySim chỉ xuất hiện ở 2 loại này

FEATURE_COLS = [
    "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest",
    "errorBalanceOrig", "errorBalanceDest", "is_transfer", "hour_of_day",
]


def build_features(df: DataFrame) -> DataFrame:
    return (df.filter(F.col("type").isin(FRAUD_TYPES))
              .withColumn("errorBalanceOrig",
                          F.col("newbalanceOrig") + F.col("amount") - F.col("oldbalanceOrg"))
              .withColumn("errorBalanceDest",
                          F.col("oldbalanceDest") + F.col("amount") - F.col("newbalanceDest"))
              .withColumn("is_transfer", (F.col("type") == "TRANSFER").cast("int"))
              .withColumn("hour_of_day", F.col("step") % 24))
