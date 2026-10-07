"""Write and read a tiny local Delta table; each run uses a new directory."""

import os
import sys
from pathlib import Path
from uuid import uuid4

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def main():
    root = Path(__file__).resolve().parents[1]
    table = root / "data" / "smoke" / uuid4().hex
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    builder = (
        SparkSession.builder.appName("RetailFlow-Delta-Smoke")
        .master("local[2]")
        .config("spark.driver.memory", "1g")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.default.parallelism", "2")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.jars.ivy", str(root / ".ivy2"))
    )
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    try:
        # Spark range avoids Python workers during the first JVM/Delta check.
        expected = spark.range(3).selectExpr("id AS order_id", "(id + 1) * 10 AS amount")
        expected.write.format("delta").mode("errorifexists").save(str(table))
        actual = spark.read.format("delta").load(str(table))
        rows = actual.orderBy("order_id").collect()
        assert [(r.order_id, r.amount) for r in rows] == [(0, 10), (1, 20), (2, 30)]
        assert (table / "_delta_log").is_dir()
        actual.show()
        print(f"PASS: Delta write/read verified at {table}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
