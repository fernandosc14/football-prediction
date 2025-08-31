import joblib
import os
import logging

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from utils import setup_logging, save_json
from src.data_prep import preprocess_data

setup_logging()


def train_model():

    targets = ["Winner", "BTTS", "Over_1_5", "Over_2_5", "Double_Chance"]

    df, feature_columns, target_df = preprocess_data(targets=targets)

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
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        train_acc = model.score(X, y)
        metrics[target] = {"train_accuracy": train_acc}
        logging.info(f"Train accuracy for {target}: {train_acc:.4f}")

        joblib.dump(model, f"models/model_{target}.pkl")
        logging.info(f"Model saved for target '{target}' in models/model_{target}.pkl")

    save_json(metrics, "models/train_metrics.json")
    logging.info("Training metrics saved in models/train_metrics.json.")

    logging.info("Training completed for all targets.")


if __name__ == "__main__":
    train_model()
