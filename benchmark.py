#!/usr/bin/env python3
"""Benchmark CPU + LightGBM cho dataset Credit Card Fraud Detection.

Chay don gian:
    python3 benchmark.py

Mac dinh script tim ``creditcard.csv`` trong thu muc hien tai, thu muc cua
script, hoac ``~/ml-benchmark/creditcard.csv``. Co the chi ro duong dan khac
bang ``--dataset`` neu can.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COLUMN = "Class"
INFERENCE_ROWS = 1000
SINGLE_ROW_REPEATS = 100


def find_dataset(dataset_argument: str | None) -> Path:
    """Tim dataset ma khong can hard-code duong dan Windows."""

    if dataset_argument:
        dataset_path = Path(dataset_argument).expanduser()
        if dataset_path.is_file():
            return dataset_path
        raise FileNotFoundError(
            f"Khong tim thay dataset tai duong dan da chi ro: {dataset_path}"
        )

    candidates = [
        Path.cwd() / "creditcard.csv",
        Path(__file__).resolve().parent / "creditcard.csv",
        Path.home() / "ml-benchmark" / "creditcard.csv",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    locations = "\n".join(f"- {candidate}" for candidate in candidates)
    raise FileNotFoundError(
        "Khong tim thay creditcard.csv. Hay tai dataset vao mot trong cac "
        f"vi tri sau:\n{locations}"
    )


def build_model() -> LGBMClassifier:
    """Tao LightGBM classifier CPU voi cau hinh co the lap lai."""

    return LGBMClassifier(
        objective="binary",
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=31,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=2,
        device_type="cpu",
        deterministic=True,
        force_col_wise=True,
        verbosity=-1,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train va benchmark LightGBM tren CPU voi creditcard.csv."
    )
    parser.add_argument(
        "--dataset",
        default=None,
        help="Duong dan tuy chon toi creditcard.csv.",
    )
    parser.add_argument(
        "--output",
        default="benchmark_result.json",
        help="File JSON dau ra (mac dinh: benchmark_result.json).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        dataset_path = find_dataset(args.dataset)
        load_started = time.perf_counter()
        dataframe = pd.read_csv(dataset_path)
        data_load_time = time.perf_counter() - load_started

        if dataframe.empty:
            raise ValueError("creditcard.csv khong co dong du lieu nao.")
        if TARGET_COLUMN not in dataframe.columns:
            raise ValueError(
                f"Dataset phai co cot target '{TARGET_COLUMN}', "
                f"nhung cac cot hien co la: {list(dataframe.columns)}"
            )

        features = dataframe.drop(columns=[TARGET_COLUMN])
        target = dataframe[TARGET_COLUMN]
        if target.isna().any():
            raise ValueError("Cot Class co gia tri thieu; khong the benchmark an toan.")
        if target.nunique() != 2:
            raise ValueError("Cot Class phai co dung 2 lop de tinh AUC.")

        x_train, x_test, y_train, y_test = train_test_split(
            features,
            target,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=target,
        )

        model = build_model()
        training_started = time.perf_counter()
        model.fit(x_train, y_train)
        training_time = time.perf_counter() - training_started

        predictions = model.predict(x_test)
        probabilities = model.predict_proba(x_test)
        positive_class_index = list(model.classes_).index(1)
        positive_probabilities = probabilities[:, positive_class_index]

        inference_rows = min(INFERENCE_ROWS, len(x_test))
        if inference_rows == 0:
            raise ValueError("Test set khong co dong du lieu de benchmark inference.")
        inference_batch = x_test.iloc[:inference_rows]
        single_row = x_test.iloc[[0]]

        # Warm-up truoc khi do de giam anh huong cua lan goi dau tien.
        model.predict_proba(single_row)
        single_row_started = time.perf_counter()
        for _ in range(SINGLE_ROW_REPEATS):
            model.predict_proba(single_row)
        single_row_elapsed = time.perf_counter() - single_row_started
        latency_ms_per_row = (
            single_row_elapsed / SINGLE_ROW_REPEATS * 1000
        )

        batch_started = time.perf_counter()
        model.predict_proba(inference_batch)
        batch_elapsed = time.perf_counter() - batch_started
        throughput_rows_per_second = inference_rows / batch_elapsed

        metrics = {
            "data_load_time_seconds": float(data_load_time),
            "training_time_seconds": float(training_time),
            "best_iteration": getattr(model, "best_iteration_", None),
            "accuracy": float(accuracy_score(y_test, predictions)),
            "auc": float(roc_auc_score(y_test, positive_probabilities)),
            "f1": float(f1_score(y_test, predictions, zero_division=0)),
            "precision": float(
                precision_score(y_test, predictions, zero_division=0)
            ),
            "recall": float(recall_score(y_test, predictions, zero_division=0)),
            "inference_latency_ms_per_row": float(latency_ms_per_row),
            "throughput_rows_per_second": float(throughput_rows_per_second),
        }

        result = {
            "dataset": {
                "file": dataset_path.name,
                "rows": int(len(dataframe)),
                "features": int(features.shape[1]),
                "target": TARGET_COLUMN,
                "train_rows": int(len(x_train)),
                "test_rows": int(len(x_test)),
            },
            "configuration": {
                "model": "LightGBM LGBMClassifier",
                "device": "CPU",
                "random_state": RANDOM_STATE,
                "test_size": TEST_SIZE,
                "inference_benchmark_rows": inference_rows,
                "single_row_repeats": SINGLE_ROW_REPEATS,
            },
            "metrics": metrics,
        }

        output_path = Path(args.output).expanduser()
        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=2)
            output_file.write("\n")

    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"LOI: {error}")
        return 1

    print("=== CPU + LightGBM Benchmark ===")
    print(f"Dataset: {dataset_path}")
    print(f"Rows: {len(dataframe):,}; train: {len(x_train):,}; test: {len(x_test):,}")
    print("Device: CPU")
    print(f"Training time (seconds): {metrics['training_time_seconds']:.6f}")
    print(f"Accuracy: {metrics['accuracy']:.6f}")
    print(f"AUC: {metrics['auc']:.6f}")
    print(f"F1: {metrics['f1']:.6f}")
    print(f"Precision: {metrics['precision']:.6f}")
    print(f"Recall: {metrics['recall']:.6f}")
    print(
        "Inference latency (ms/row): "
        f"{metrics['inference_latency_ms_per_row']:.6f}"
    )
    print(
        "Inference throughput (rows/second): "
        f"{metrics['throughput_rows_per_second']:.2f}"
    )
    print(f"Ket qua da ghi vao: {Path(args.output).expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
