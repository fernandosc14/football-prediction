import joblib
import os
import logging
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from src.utils import setup_logging, save_json
from src.data_prep import preprocess_data

setup_logging()


def train_model():

    targets = ["Winner", "BTTS", "Over_1_5", "Over_2_5", "Double_Chance"]

    df, feature_columns, target_df = preprocess_data(targets=targets)

    odds_cols = ["home_win", "draw", "away_win"]

    mask = df[odds_cols].apply(pd.to_numeric, errors="coerce").notna().all(axis=1)
    df = df[mask]

    target_df = target_df.loc[df.index]

    os.makedirs("models", exist_ok=True)

    X = df[feature_columns]

    metrics = {}
    for target in targets:
        logging.info(f"Training model for target: {target}")
        y = target_df[target]

        if y.dtype == object or y.dtype.name == "category":
            le = LabelEncoder()
            y = le.fit_transform(y)
            joblib.dump(le, f"models/le_{target}.pkl")

        model_cv = RandomForestClassifier(
            n_estimators=100, max_depth=5, min_samples_leaf=10, random_state=42
        )
        cv_scores = cross_val_score(model_cv, X, y, cv=5, scoring="accuracy")
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
                f"Stratify disabled for target '{target}' (only one class present: {unique_classes}). Check your data!"
            )

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=stratify_param
        )

        model = RandomForestClassifier(
            n_estimators=100, max_depth=5, min_samples_leaf=10, random_state=42
        )
        model.fit(X_train, y_train)

        train_acc = model.score(X_train, y_train)
        val_acc = model.score(X_val, y_val)
        metrics[target].update({"train_accuracy": train_acc, "val_accuracy": val_acc})
        logging.info(f"[INFO] Train accuracy for {target}: {train_acc:.4f}")
        logging.info(f"[INFO] Validation accuracy for {target}: {val_acc:.4f}")

        joblib.dump(model, f"models/model_{target}.pkl")
        logging.info(f"Model saved for target '{target}' in models/model_{target}.pkl")

    save_json(metrics, "models/train_metrics.json")
    logging.info("[INFO] Training metrics saved in models/train_metrics.json.")

    logging.info("[INFO] Training completed for all targets.")
