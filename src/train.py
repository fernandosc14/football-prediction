import joblib
import os
import logging
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from src.utils import setup_logging, save_json, load_config
from src.data_prep import preprocess_data

setup_logging()


def train_model():
    config = load_config()
    targets = config.get("targets", ["Winner", "BTTS", "Over_1_5", "Over_2_5", "Double_Chance"])
    train_params = config.get("train_params", {})
    random_seed = config.get("random_seed", 42)
    model_dir = config.get("paths", {}).get("model_dir", "models/")
    os.makedirs(model_dir, exist_ok=True)

    df, feature_columns, target_df, scaler, le_league = preprocess_data(targets=targets)
    odds_cols = ["home_win", "draw", "away_win"]
    mask = df[odds_cols].apply(pd.to_numeric, errors="coerce").notna().all(axis=1)
    df = df[mask]
    target_df = target_df.loc[df.index]
    X = df[feature_columns]
    metrics = {}
    for target in targets:
        logging.info(f"[INFO] Training model for target: {target}")
        y = target_df[target]
        encoder = None
        if y.dtype == object or y.dtype.name == "category":
            encoder = LabelEncoder()
            y = encoder.fit_transform(y)
        model_cv = RandomForestClassifier(
            n_estimators=train_params.get("n_estimators", 100),
            max_depth=train_params.get("max_depth", 5),
            min_samples_leaf=train_params.get("min_samples_leaf", 10),
            random_state=random_seed,
        )
        cv_scores = cross_val_score(
            model_cv, X, y, cv=train_params.get("cv_folds", 5), scoring="accuracy"
        )
        logging.info(
            f"[INFO] Cross-validation accuracy for {target}: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}"
        )
        metrics[target] = {
            "cv_mean_accuracy": float(cv_scores.mean()),
            "cv_std_accuracy": float(cv_scores.std()),
        }
        unique_classes = np.unique(y)
        if unique_classes.shape[0] > 1:
            stratify_param = y
        else:
            stratify_param = None
            logging.warning(
                f"[WARNING] Stratify disabled for target '{target}' (only one class present: {unique_classes}). Check your data!"
            )
        X_train, X_val, y_train, y_val = train_test_split(
            X,
            y,
            test_size=train_params.get("test_size", 0.2),
            random_state=random_seed,
            stratify=stratify_param,
        )
        model = RandomForestClassifier(
            n_estimators=train_params.get("n_estimators", 100),
            max_depth=train_params.get("max_depth", 5),
            min_samples_leaf=train_params.get("min_samples_leaf", 10),
            random_state=random_seed,
        )
        model.fit(X_train, y_train)
        train_acc = model.score(X_train, y_train)
        val_acc = model.score(X_val, y_val)
        metrics[target].update({"train_accuracy": train_acc, "val_accuracy": val_acc})
        logging.info(f"[INFO] Train accuracy for {target}: {train_acc:.4f}")
        logging.info(f"[INFO] Validation accuracy for {target}: {val_acc:.4f}")
        bundle = {
            "model": model,
            "feature_columns": feature_columns,
            "scaler": scaler,
            "le_league": le_league,
            "encoder": encoder,
        }
        joblib.dump(bundle, os.path.join(model_dir, f"bundle_{target}.pkl"))
        logging.info(f"[INFO] Bundle saved for target '{target}' in {model_dir}bundle_{target}.pkl")
    save_json(metrics, os.path.join(model_dir, "train_metrics.json"))
    logging.info(f"[INFO] Training metrics saved in {model_dir}train_metrics.json.")
    logging.info("[INFO] Training completed for all targets.")
