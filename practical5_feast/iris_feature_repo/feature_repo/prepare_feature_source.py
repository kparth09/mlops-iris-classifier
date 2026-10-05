"""
Prepares the iris_features.csv from Experiment 4 into a Feast-ready
Parquet source with entity IDs and event timestamps.

Run from this directory (the Feast repo root):

    python prepare_feature_source.py
"""

import pandas as pd
from pathlib import Path

# Resolve relative to this file, not the current working directory,
# so the script works regardless of where it is invoked from.
feature_repo_dir = Path(__file__).resolve().parent

# Input from Experiment 4
input_file = (
    feature_repo_dir.parent.parent.parent
    / "data"
    / "processed"
    / "iris_features.csv"
)

# Output for Feast
output_file = feature_repo_dir / "data" / "iris_features.parquet"

if not input_file.exists():
    raise FileNotFoundError(
        f"Expected Experiment 4 output at {input_file}. "
        "Run 'dvc repro' from the repository root first."
    )

# Read feature-engineered data
df = pd.read_csv(input_file)

# Create sample_id
df.insert(0, "sample_id", range(len(df)))

# Create event timestamps
start_time = pd.Timestamp(
    "2026-08-15 15:20:02",
    tz="UTC"
)

df["event_timestamp"] = pd.date_range(
    start=start_time,
    periods=len(df),
    freq="min"
)

# Created timestamp
df["created_timestamp"] = df["event_timestamp"]

# Create output directory
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save as Parquet
df.to_parquet(
    output_file,
    index=False
)

print(
    f"Wrote {len(df)} rows to {output_file}"
)