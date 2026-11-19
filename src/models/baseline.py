"""T13 (Phúc, review: Tố) — Logistic Regression & Random Forest với Spark MLlib, có class weight."""
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.feature import StandardScaler, VectorAssembler
from pyspark.sql import functions as F

from src.features.build_features import FEATURE_COLS


def add_class_weight(df, label: str = "isFraud"):
    ratio = df.filter(F.col(label) == 1).count() / df.count()
    return df.withColumn("class_weight",
                         F.when(F.col(label) == 1, 1 - ratio).otherwise(ratio))


def make_pipeline(kind: str = "lr") -> Pipeline:
    assembler = VectorAssembler(inputCols=FEATURE_COLS, outputCol="raw_features")
    scaler = StandardScaler(inputCol="raw_features", outputCol="features")
    if kind == "lr":
        clf = LogisticRegression(labelCol="isFraud", weightCol="class_weight", maxIter=100)
    else:
        clf = RandomForestClassifier(labelCol="isFraud", weightCol="class_weight",
                                     numTrees=100, maxDepth=8, seed=42)
    return Pipeline(stages=[assembler, scaler, clf])
