# DVC Workflow

## Overview

DVC (Data Version Control) is used to version and manage datasets alongside Git.

Git tracks the DVC metadata files (`.dvc`), while DVC tracks the actual dataset contents.

## DVC Remote

A local directory is configured as the DVC remote:

```bash
mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage
```

> Note: the configured remote in `.dvc/config` points to a local path on the
> original author's machine. Recreate it for your own environment with
> `dvc remote add -d myremote <your-path>` before running `dvc push`.

## Tracking a Dataset

```bash
dvc add data/raw/iris_v1.csv
git add data/raw/iris_v1.csv.dvc data/raw/.gitignore
git commit -m "feat: add DVC tracked iris dataset"
```

## Pipeline

```bash
dvc repro
```

## Syncing with the Remote

```bash
dvc push
dvc pull
```