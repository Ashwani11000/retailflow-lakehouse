# RetailFlow — Batch & Streaming Retail Lakehouse

An independent, synthetic retail data engineering portfolio project.

## Current status

- Python 3.10.5 virtual environment and Temurin Java 11 verified locally.
- Git initialized; generated data, environments and IDE files excluded.
- PySpark 3.5.3, Delta 3.3.1 and pytest 9.1.1 installed; dependency check passed.
- Local Delta write/read verified: three expected rows and transaction log, exit code 0.
- GitHub remote connection pending.

## Local setup (PowerShell)

Run these commands from the repository root using the same `.venv` selected in PyCharm.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts\delta_smoke.py
```

The first command installs the dependencies, the second checks compatibility, and the third writes and reads three rows in a fresh Delta table.

The first Spark run downloads Delta JVM jars from Maven; internet access is required.
The script uses two local threads and a 1 GB driver heap; total process memory exceeds the heap size.
Each run retains a small ignored table under `data/smoke/` for inspection.
A `PASS` message confirms the rows and Delta transaction log were verified.
This initial check does not exercise Python workers, Kafka or production pipelines.
The verified Windows run emitted shutdown errors while deleting temporary JAR files;
the table write/read assertions passed before cleanup. Temporary-file cleanup remains an open issue.

## Planned scope — not implemented

Synthetic sales, orders, products, customers and inventory; batch ingestion;
Kafka and Spark Structured Streaming; Bronze/Silver/Gold Delta tables;
nested JSON, joins, windows, incremental loads, deduplication and MERGE;
quality checks, reconciliation and recovery; Delta maintenance and measured
performance experiments; pytest, GitHub Actions, later Jenkins and a free visualization layer.

Services will be introduced gradually for an 8 GB Windows laptop.
Use synthetic data and neutral names; do not include previous client names,
credentials or private data in source, documentation or repository metadata.
