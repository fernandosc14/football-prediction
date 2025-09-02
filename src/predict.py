import os
import sys
import json
import joblib
import pandas as pd
from src.api_fetch import fetch_upcoming_matches
from src.features import (
    add_rank_diff_feature,
    add_h2h_feature,
    add_odds_features,
    add_recent_form_to_upcoming,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def prepare_features(games, feature_columns, scaler=None, encoders=None):
    """Prepare features for prediction from raw game data."""

    df = pd.DataFrame(games)
    with open("config/leagues.json", encoding="utf-8") as f:
        leagues = json.load(f)
    id_to_name = {str(lg["id"]): lg["name"] for lg in leagues}
    df["League"] = df["league_id"].astype(str).map(id_to_name)
    df = add_rank_diff_feature(df)
    df = add_h2h_feature(df)
    df = add_odds_features(df)
    for col, key in zip(["home_win", "draw", "away_win"], ["home", "draw", "away"]):
        df[col] = df["odds"].apply(
            lambda x: x.get(key) if isinstance(x, dict) and key in x else None
        )
    le_league = joblib.load("models/le_league.pkl")
    df["League_Encoded"] = le_league.transform(df["League"])
    with open("data/raw/matches_raw.json", encoding="utf-8") as f:
        historical = pd.DataFrame(json.load(f))
    if "League" not in historical.columns and "league" in historical.columns:
        historical["League"] = historical["league"]
    if "Team1Goals" not in historical.columns and "team1_goals" in historical.columns:
        historical["Team1Goals"] = historical["team1_goals"]
    if "Team2Goals" not in historical.columns and "team2_goals" in historical.columns:
        historical["Team2Goals"] = historical["team2_goals"]
    df = add_recent_form_to_upcoming(df, historical, n_games=5)
    for i, game in enumerate(games):
        for odd_col in ["home_win", "draw", "away_win"]:
            if odd_col in df.columns:
                game[odd_col] = df.loc[i, odd_col]
    X = df[feature_columns].copy()
    if scaler:
        X = pd.DataFrame(scaler.transform(X), columns=feature_columns)
    return X


def main():
    """Load models and make predictions on upcoming matches."""

    with open("models/feature_columns.json") as f:
        with open("models/feature_columns.json") as f:
            feature_columns = json.load(f)
        scaler = joblib.load("models/feature_scaler.pkl")
        models = {
            "Winner": joblib.load("models/model_Winner.pkl"),
            "Over_2_5": joblib.load("models/model_Over_2_5.pkl"),
            "Over_1_5": joblib.load("models/model_Over_1_5.pkl"),
            "Double_Chance": joblib.load("models/model_Double_Chance.pkl"),
            "BTTS": joblib.load("models/model_BTTS.pkl"),
        }
        games = fetch_upcoming_matches()
        if not games:
            print("No upcoming matches found.")
            return
        X = prepare_features(games, feature_columns, scaler=scaler)
        for name, model in models.items():
            try:
                probs = model.predict_proba(X)
                preds = model.classes_[probs.argmax(axis=1)]
                confs = probs.max(axis=1)
            except Exception as e:
                print(f"Error predicting {name}: {e}")
                preds = [None] * len(games)
                confs = [0.0] * len(games)
            for i, game in enumerate(games):
                game[f"prediction_{name}"] = preds[i]
                game[f"confidence_{name}"] = confs[i]
        with open("config/leagues.json", encoding="utf-8") as f:
            leagues = json.load(f)
        id_to_name = {str(lg["id"]): lg["name"] for lg in leagues}
        for game in games:
            game["League"] = id_to_name.get(str(game["league_id"]), "?")
        results = []
        for game in games:
            result = {
                "date": game.get("date"),
                "time": game.get("time"),
                "league": game.get("League"),
                "home_team": game.get("home_name"),
                "away_team": game.get("away_name"),
                "odds": {
                    "home": game.get("home_win"),
                    "draw": game.get("draw"),
                    "away": game.get("away_win"),
                },
                "predictions": {
                    "winner": {
                        "class": (
                            int(game.get("prediction_Winner", -1))
                            if game.get("prediction_Winner") is not None
                            else None
                        ),
                        "confidence": float(game.get("confidence_Winner", 0)),
                    },
                    "over_2_5": {
                        "class": (
                            int(game.get("prediction_Over_2_5", -1))
                            if game.get("prediction_Over_2_5") is not None
                            else None
                        ),
                        "confidence": float(game.get("confidence_Over_2_5", 0)),
                    },
                    "over_1_5": {
                        "class": (
                            int(game.get("prediction_Over_1_5", -1))
                            if game.get("prediction_Over_1_5") is not None
                            else None
                        ),
                        "confidence": float(game.get("confidence_Over_1_5", 0)),
                    },
                    "double_chance": {
                        "class": (
                            int(game.get("prediction_Double_Chance", -1))
                            if game.get("prediction_Double_Chance") is not None
                            else None
                        ),
                        "confidence": float(game.get("confidence_Double_Chance", 0)),
                    },
                    "btts": {
                        "class": (
                            int(game.get("prediction_BTTS", -1))
                            if game.get("prediction_BTTS") is not None
                            else None
                        ),
                        "confidence": float(game.get("confidence_BTTS", 0)),
                    },
                },
            }
            results.append(result)
        output_dir = os.path.join("data", "predict")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "predictions.json")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Predictions saved to {output_path}")
        except Exception as e:
            print(f"Error saving predictions: {e}")
        return
    return


if __name__ == "__main__":
    main()
