from pyspark.sql import SparkSession

from src.common.config import HIVE_METASTORE


def get_spark(app_name: str, hive: bool = True) -> SparkSession:
    builder = (SparkSession.builder.appName(app_name)
               .config("spark.sql.shuffle.partitions", "12")
               .config("hive.metastore.uris", HIVE_METASTORE))
    if hive:
        builder = builder.enableHiveSupport()
    return builder.getOrCreate()
