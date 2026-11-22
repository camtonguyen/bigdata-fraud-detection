import os
import subprocess
import sys

import pytest

pyspark = pytest.importorskip("pyspark")
from pyspark.sql import SparkSession

from src.features.build_features import build_features


@pytest.fixture(scope="module")
def spark():
    if subprocess.run(["java", "-version"], check=False, capture_output=True).returncode != 0:
        pytest.skip("Java not installed (CI runs this test)")
    # Worker dùng đúng Python của venv, tránh lệch phiên bản với python3 mặc định của máy
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    s = SparkSession.builder.master("local[1]").appName("test").getOrCreate()
    yield s
    s.stop()


def test_filters_and_error_balance(spark):
    rows = [(1, "TRANSFER", 100.0, "C1", 100.0, 0.0, "C2", 0.0, 0.0, 1, 0),
            (1, "PAYMENT", 10.0, "C3", 50.0, 40.0, "M1", 0.0, 0.0, 0, 0)]
    cols = ["step", "type", "amount", "nameOrig", "oldbalanceOrg", "newbalanceOrig",
            "nameDest", "oldbalanceDest", "newbalanceDest", "isFraud", "isFlaggedFraud"]
    out = build_features(spark.createDataFrame(rows, cols)).collect()
    assert len(out) == 1
    assert out[0]["errorBalanceOrig"] == 0.0
    assert out[0]["errorBalanceDest"] == 100.0
