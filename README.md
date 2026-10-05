# MLOps Iris Classifier

A sample ML project used to demonstrate Git-based version control
workflows in an MLOps context.

## Setup

```bash
pip install -r requirements.txt
python src/train.py
```

## Practicals

| Practical | Topic | Entry Point |
|---|---|---|
| 1 | Git version control workflows | `docs/VERSION_CONTROL_WORKFLOW.md` |
| 2 | Dataset generation & augmentation | `src/generate_data.py`, `src/augment_data.py` |
| 3 | DVC data versioning & pipeline | `dvc.yaml`, `docs/DVC_WORKFLOW.md` |
| 4 | DVC data pipeline | `dvc.yaml`, `docs/DATA_PIPELINE.md` |
| 5 | MLflow tracking, tuning & model registry | `src/train_with_mlflow.py`, `src/baseline_model.py`, `src/register_best_model.py`, `src/load_registered_model.py` |
| 6 | Feast feature store | `practical5_feast/iris_feature_repo/feature_repo/` |

## DVC Pipeline

```bash
dvc repro
```

The pipeline runs four stages: `collect` -> `preprocess` -> `features` -> `validate`.

## MLflow

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts
```

Set `MLFLOW_TRACKING_URI` to point the scripts at a running server:

```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
python src/train_with_mlflow.py
python src/register_best_model.py
python src/load_registered_model.py
```

## Feast

```bash
cd practical5_feast/iris_feature_repo
feast apply
cd feature_repo
python prepare_feature_source.py
feast materialize-incremental
python get_historical_features.py
python get_online_features.py
python reuse_features_for_clustering.py
```
