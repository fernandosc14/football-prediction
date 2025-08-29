from sklearn.preprocessing import StandardScaler, LabelEncoder
import pandas as pd
import numpy as np
import joblib
import logging
import json
import os


def preprocess_data(targets=None):
    """Preprocess historical match data for ML. Returns DataFrame, feature columns, and optionally targets."""

    with open("data/raw/matches_raw.json", "r", encoding="utf-8") as f:
        data = json.load(f)
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

    h2h_cols = [
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
    ]

    for col in h2h_cols:
        if col not in df.columns:
            df[col] = 0
            logging.warning(f"[INFO] Column '{col}' not found in DataFrame. Created with zeros.")

    df["Winner"] = np.where(
        df["Team1Goals"] > df["Team2Goals"],
        "1",
        np.where(df["Team1Goals"] < df["Team2Goals"], "2", "X"),
    )
    df["Rank_Diff"] = df["team1_rank"] - df["team2_rank"]

    df["BTTS"] = ((df["Team1Goals"] > 0) & (df["Team2Goals"] > 0)).astype(int)
    df["Over_1_5"] = ((df["Team1Goals"] + df["Team2Goals"]) > 1.5).astype(int)
    df["Over_2_5"] = ((df["Team1Goals"] + df["Team2Goals"]) > 2.5).astype(int)

    df["H2H_Team1_Win_Rate"] = df["h2h_team1_wins"] / df["h2h_games_played"]
    df["H2H_Team2_Win_Rate"] = df["h2h_team2_wins"] / df["h2h_games_played"]
    df["H2H_Draw_Rate"] = df["h2h_draws"] / df["h2h_games_played"]

    df["H2H_Team1_Goals_Per_Game"] = df["h2h_team1_scored"] / df["h2h_games_played"]
    df["H2H_Team2_Goals_Per_Game"] = df["h2h_team2_scored"] / df["h2h_games_played"]

    df["H2H_Team1_Home_Win_Rate"] = df["h2h_team1_home_wins"] / (
        df["h2h_team1_home_wins"] + df["h2h_team1_home_draws"] + df["h2h_team1_home_losses"]
    )
    df["H2H_Team2_Home_Win_Rate"] = df["h2h_team2_home_wins"] / (
        df["h2h_team2_home_wins"] + df["h2h_team2_home_draws"] + df["h2h_team2_home_losses"]
    )

    df["H2H_Team1_Home_Goals_Per_Game"] = df["h2h_team1_home_scored"] / (
        df["h2h_team1_home_wins"] + df["h2h_team1_home_draws"] + df["h2h_team1_home_losses"]
    )
    df["H2H_Team2_Home_Goals_Per_Game"] = df["h2h_team2_home_scored"] / (
        df["h2h_team2_home_wins"] + df["h2h_team2_home_draws"] + df["h2h_team2_home_losses"]
    )

    df["H2H_Total_Goals"] = df["h2h_team1_scored"] + df["h2h_team2_scored"]

    df["Double_Chance"] = df["Winner"].map({"1": "1X", "2": "X2", "X": "1X"})
    df["Goal_Difference"] = df["Team1Goals"] - df["Team2Goals"]

    le_league = LabelEncoder()
    df["League_Encoded"] = le_league.fit_transform(df["League"])

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

    if targets:
        return df, feature_columns_valid, df[targets]
    return df, feature_columns_valid


if __name__ == "__main__":
    preprocess_data()
