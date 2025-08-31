from sklearn.preprocessing import StandardScaler
from features import apply_all_features
from utils import load_json

import pandas as pd
import joblib
import logging
import json
import os


def preprocess_data(targets=None):
    """Preprocess historical match data for ML. Returns DataFrame, feature columns, and optionally targets."""

    models_dir = "models"
    if os.path.exists(models_dir):
        for fname in ["le_league.pkl", "feature_scaler.pkl", "feature_columns.json"]:
            fpath = os.path.join(models_dir, fname)
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except Exception as e:
                    logging.warning(f"Could not delete {fpath}: {e}")

    path = "data/raw/matches_raw.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing data file: {path}")
    try:
        data = load_json(path)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e

    df = pd.DataFrame(data)
    df.rename(
        columns={
            "team1_goals": "Team1Goals",
            "team2_goals": "Team2Goals",
            "league": "League",
        },
        inplace=True,
    )

    for gcol in ("Team1Goals", "Team2Goals"):
        df[gcol] = pd.to_numeric(df[gcol], errors="coerce")
    df = df.dropna(subset=["Team1Goals", "Team2Goals"])

    df, le_league = apply_all_features(df)

    h2h_cols = [
        "team1_rank",
        "team2_rank",
        "h2h_games_played",
        "h2h_team1_wins",
        "h2h_team2_wins",
        "h2h_draws",
        "h2h_team1_scored",
        "h2h_team2_scored",
        "h2h_team1_home_wins",
        "h2h_team1_home_draws",
        "h2h_team1_home_losses",
        "h2h_team1_home_scored",
        "h2h_team1_home_conceded",
        "h2h_team2_home_wins",
        "h2h_team2_home_draws",
        "h2h_team2_home_losses",
        "h2h_team2_home_scored",
        "h2h_team2_home_conceded",
    ]

    for col in h2h_cols:
        if col not in df.columns:
            df[col] = 0
            logging.warning(f"[INFO] Column '{col}' not found in DataFrame. Created with zeros.")

    numeric_primaries = ["team1_rank", "team2_rank", "h2h_games_played"] + h2h_cols
    for col in numeric_primaries:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    feature_columns = [
        "team1_rank",
        "team2_rank",
        "h2h_team1_wins",
        "h2h_team2_wins",
        "h2h_draws",
        "h2h_team1_scored",
        "h2h_team2_scored",
        "h2h_team1_home_wins",
        "h2h_team1_home_draws",
        "h2h_team1_home_losses",
        "h2h_team1_home_scored",
        "h2h_team1_home_conceded",
        "h2h_team2_home_wins",
        "h2h_team2_home_draws",
        "h2h_team2_home_losses",
        "h2h_team2_home_scored",
        "h2h_team2_home_conceded",
        "Goal_Difference",
        "Rank_Diff",
        "League_Encoded",
    ]

    feature_columns_valid = [
        col for col in feature_columns if col in df.columns and not df[col].isna().all()
    ]

    for col in feature_columns_valid:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df[feature_columns_valid] = df[feature_columns_valid].fillna(
        df[feature_columns_valid].median(numeric_only=True)
    )
    scaler = StandardScaler()
    df[feature_columns_valid] = scaler.fit_transform(df[feature_columns_valid])

    os.makedirs("models", exist_ok=True)
    joblib.dump(le_league, "models/le_league.pkl")
    joblib.dump(scaler, "models/feature_scaler.pkl")
    with open("models/feature_columns.json", "w") as f:
        json.dump(feature_columns_valid, f)

    if targets is not None:
        return df, feature_columns_valid, df[targets]
    return df, feature_columns_valid


if __name__ == "__main__":
    preprocess_data()
