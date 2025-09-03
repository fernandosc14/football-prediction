import os
import sys
import json
import joblib
import pandas as pd
import logging
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
    if encoders and "le_league" in encoders:
        le = encoders["le_league"]
        known = set(le.classes_)
        placeholder = next(iter(known)) if len(known) else None
        safe_leagues = df["League"].where(df["League"].isin(known), placeholder)
        df["League_Encoded"] = le.transform(safe_leagues)
    else:
        raise RuntimeError("Missing league encoder in prediction bundle.")
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
    missing = [c for c in feature_columns if c not in df.columns]
    for c in missing:
        df[c] = 0
    X = df[feature_columns].copy()
    if scaler:
        X = pd.DataFrame(scaler.transform(X), columns=feature_columns)
    return X


def main():
    """Load models and make predictions on upcoming matches."""

    targets = ["Winner", "Over_2_5", "Over_1_5", "Double_Chance", "BTTS"]
    bundles = {}
    for t in targets:
        path = f"models/bundle_{t}.pkl"
        try:
            bundles[t] = joblib.load(path)
        except Exception as e:
            logging.error(f"[ERROR] Could not load model bundle for {t}: {e}")
    if not bundles:
        logging.critical("[CRITICAL] No models loaded. Exiting prediction.")
        return
    games = fetch_upcoming_matches()
    if not games:
        logging.warning("[WARNING] No upcoming matches found.")
        return
    for name, bundle in bundles.items():
        model = bundle["model"]
        feature_columns = bundle.get("feature_columns", [])
        scaler = bundle.get("scaler", None)
        le_league = bundle.get("le_league", None)
        try:
            X = prepare_features(
                games, feature_columns, scaler=scaler, encoders={"le_league": le_league}
            )
            probs = model.predict_proba(X)
            preds = model.classes_[probs.argmax(axis=1)]
            confs = probs.max(axis=1)
        except Exception as e:
            logging.error(f"[ERROR] Error predicting {name}: {e}")
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
            "match_id": game.get("match_id"),
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

    results_sorted = sorted(
        results, key=lambda x: x["predictions"]["winner"]["confidence"], reverse=True
    )
    top_results = results_sorted[:6]
    output_dir = os.path.join("data", "predict")
    os.makedirs(output_dir, exist_ok=True)
    predictions_path = os.path.join(output_dir, "predictions.json")
    with open(predictions_path, "w", encoding="utf-8") as f:
        json.dump(top_results, f, ensure_ascii=False, indent=2)
    logging.info(f"[INFO] Predictions saved to {predictions_path} (top 6 by confidence)")

    history_path = os.path.join(output_dir, "predictions_history.json")
    try:
        if os.path.exists(history_path):
            with open(history_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
        else:
            existing = []
        existing.extend(top_results)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        logging.info(f"[INFO] Appended top 6 predictions to {history_path}")
    except Exception as e:
        logging.error(f"[ERROR] Error saving predictions history: {e}")
    return


if __name__ == "__main__":
    main()
