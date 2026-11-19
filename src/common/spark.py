from pyspark.sql import SparkSession

from src.common.config import HDFS_URI


def get_spark(app_name: str, hive: bool = False) -> SparkSession:
    """SparkSession dùng chung.

    hive=True: bật Hive support (metastore Derby nhúng, lưu ở /opt/app/metastore_db) để truy vấn
    bảng fraud.*. Derby chỉ cho 1 tiến trình dùng cùng lúc → chỉ bật khi cần truy vấn bảng;
    job train/stream đọc-ghi Parquet trực tiếp theo đường dẫn HDFS nên để hive=False.
    """
    builder = (SparkSession.builder.appName(app_name)
               .config("spark.sql.shuffle.partitions", "12"))
    if hive:
        builder = (builder.enableHiveSupport()
                   .config("spark.sql.warehouse.dir", f"{HDFS_URI}/user/hive/warehouse")
                   .config("spark.hadoop.javax.jdo.option.ConnectionURL",
                           "jdbc:derby:;databaseName=/opt/app/metastore_db;create=true"))
    return builder.getOrCreate()
