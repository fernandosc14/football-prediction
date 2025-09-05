from sklearn.preprocessing import LabelEncoder

import numpy as np
import pandas as pd


def add_winner_feature(df):
    """Add a feature representing the match winner."""
    df["Winner"] = np.where(
        df["Team1Goals"] > df["Team2Goals"],
        "1",
        np.where(df["Team1Goals"] < df["Team2Goals"], "2", "X"),
    )
    return df


def add_double_chance_feature(df):
    """Add a feature representing the double chance outcome."""
    df["Double_Chance"] = df["Winner"].map({"1": "1X", "2": "X2", "X": "1X"})
    return df


def add_over_feature(df):
    """Add features for over 1.5 and over 2.5 goals."""
    df["Over_1_5"] = ((df["Team1Goals"] + df["Team2Goals"]) > 1.5).astype(int)
    df["Over_2_5"] = ((df["Team1Goals"] + df["Team2Goals"]) > 2.5).astype(int)
    return df


def add_btts_feature(df):
    """Add a feature indicating if both teams scored."""
    df["BTTS"] = ((df["Team1Goals"] > 0) & (df["Team2Goals"] > 0)).astype(int)
    return df


def add_rank_diff_feature(df):
    """Add a feature representing the rank difference between the two teams."""
    df["team1_rank"] = pd.to_numeric(df["team1_rank"], errors="coerce")
    df["team2_rank"] = pd.to_numeric(df["team2_rank"], errors="coerce")
    df["Rank_Diff"] = df["team1_rank"] - df["team2_rank"]
    return df


def add_h2h_feature(df):
    """Add head-to-head related features."""
    denom = df["h2h_games_played"].replace(0, np.nan)
    df["H2H_Team1_Win_Rate"] = df["h2h_team1_wins"] / denom
    df["H2H_Team2_Win_Rate"] = df["h2h_team2_wins"] / denom
    df["H2H_Draw_Rate"] = df["h2h_draws"] / denom

    df["H2H_Team1_Goals_Per_Game"] = df["h2h_team1_scored"] / df["h2h_games_played"]
    df["H2H_Team2_Goals_Per_Game"] = df["h2h_team2_scored"] / df["h2h_games_played"]

    t1_home_total = (
        df["h2h_team1_home_wins"] + df["h2h_team1_home_draws"] + df["h2h_team1_home_losses"]
    ).replace(0, np.nan)
    t2_home_total = (
        df["h2h_team2_home_wins"] + df["h2h_team2_home_draws"] + df["h2h_team2_home_losses"]
    ).replace(0, np.nan)
    df["H2H_Team1_Home_Win_Rate"] = df["h2h_team1_home_wins"] / t1_home_total
    df["H2H_Team2_Home_Win_Rate"] = df["h2h_team2_home_wins"] / t2_home_total

    df["H2H_Team1_Home_Goals_Per_Game"] = df["h2h_team1_home_scored"] / t1_home_total
    df["H2H_Team2_Home_Goals_Per_Game"] = df["h2h_team2_home_scored"] / t2_home_total

    df["H2H_Total_Goals"] = df["h2h_team1_scored"] + df["h2h_team2_scored"]
    return df


def encode_league(df):
    """Encode the league names into numerical values."""
    le_league = LabelEncoder()
    df["League_Encoded"] = le_league.fit_transform(df["League"])
    return df, le_league


def add_recent_form_features(df, n_games=5):
    """Add features based on recent form of both teams, grouped by league and season."""
    df = df.copy()
    required_cols = {"date", "team1", "team2", "Team1Goals", "Team2Goals", "League"}
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for recent form: {missing}")
    if not np.issubdtype(df["date"].dtype, np.datetime64):
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    df = df.dropna(subset=["date"])

    season_col = None
    for col in ["season", "ano", "year"]:
        if col in df.columns:
            season_col = col
            break

    group_cols = ["League"]
    if season_col:
        group_cols.append(season_col)

    df = df.sort_values(group_cols + ["date"])

    team1_form, team2_form = [], []
    team1_goals, team2_goals = [], []
    for idx, row in df.iterrows():
        t1 = row["team1"]
        t2 = row["team2"]
        date = row["date"]
        league = row["League"]
        season_val = row[season_col] if season_col else None

        mask_t1 = df["League"] == league
        mask_t2 = df["League"] == league
        if season_col:
            mask_t1 &= df[season_col] == season_val
            mask_t2 &= df[season_col] == season_val

        prev_t1 = df[
            mask_t1 & ((df["team1"] == t1) | (df["team2"] == t1)) & (df["date"] < date)
        ].tail(n_games)
        prev_t2 = df[
            mask_t2 & ((df["team1"] == t2) | (df["team2"] == t2)) & (df["date"] < date)
        ].tail(n_games)

        def calc_stats(prev, team):
            if prev.empty:
                return 0, 0
            points = 0
            goals = 0
            for _, g in prev.iterrows():
                if g["team1"] == team:
                    goals += g["Team1Goals"]
                    if g["Team1Goals"] > g["Team2Goals"]:
                        points += 3
                    elif g["Team1Goals"] == g["Team2Goals"]:
                        points += 1
                else:
                    goals += g["Team2Goals"]
                    if g["Team2Goals"] > g["Team1Goals"]:
                        points += 3
                    elif g["Team2Goals"] == g["Team1Goals"]:
                        points += 1
            return points / n_games, goals / n_games

        t1_points, t1_avg_goals = calc_stats(prev_t1, t1)
        t2_points, t2_avg_goals = calc_stats(prev_t2, t2)
        team1_form.append(t1_points)
        team2_form.append(t2_points)
        team1_goals.append(t1_avg_goals)
        team2_goals.append(t2_avg_goals)
    df["team1_last5_avg_points"] = team1_form
    df["team2_last5_avg_points"] = team2_form
    df["team1_last5_avg_goals"] = team1_goals
    df["team2_last5_avg_goals"] = team2_goals
    return df


def add_odds_features(df):
    """Add features derived from odds: ratios, min/max, implied probabilities, etc."""
    if all(col in df.columns for col in ["home_win", "draw", "away_win"]):
        df["odds_ratio_home_away"] = df["home_win"] / df["away_win"].replace(0, np.nan)
        df["odds_min"] = df[["home_win", "draw", "away_win"]].min(axis=1)
        df["odds_max"] = df[["home_win", "draw", "away_win"]].max(axis=1)
        df["odds_sum"] = df[["home_win", "draw", "away_win"]].sum(axis=1)

        df["implied_prob_home"] = 1 / df["home_win"].replace(0, np.nan)
        df["implied_prob_draw"] = 1 / df["draw"].replace(0, np.nan)
        df["implied_prob_away"] = 1 / df["away_win"].replace(0, np.nan)
        df["implied_prob_sum"] = (
            df["implied_prob_home"] + df["implied_prob_draw"] + df["implied_prob_away"]
        )
        df["implied_prob_diff"] = df["implied_prob_home"] - df["implied_prob_away"]
    return df


def apply_all_features(df):
    """Apply all feature engineering functions to the DataFrame."""
    df = add_winner_feature(df)
    df = add_double_chance_feature(df)
    df = add_over_feature(df)
    df = add_btts_feature(df)
    df = add_rank_diff_feature(df)
    df = add_h2h_feature(df)
    df = add_odds_features(df)
    df, le_league = encode_league(df)
    return df, le_league


def add_recent_form_to_upcoming(upcoming_df, historical_df, n_games=5):
    """Add recent form features to upcoming matches based on historical data."""
    historical_df = historical_df.copy()
    upcoming_df = upcoming_df.copy()
    historical_df["date"] = pd.to_datetime(historical_df["date"], errors="coerce", dayfirst=True)
    upcoming_df["date"] = pd.to_datetime(upcoming_df["date"], errors="coerce", dayfirst=True)

    team1_form, team2_form = [], []
    team1_goals, team2_goals = [], []

    for idx, row in upcoming_df.iterrows():
        t1 = row["home_name"]
        t2 = row["away_name"]
        date = row["date"]
        league = row["League"]

        prev_t1 = (
            historical_df[
                (historical_df["League"] == league)
                & ((historical_df["team1"] == t1) | (historical_df["team2"] == t1))
                & (historical_df["date"] < date)
            ]
            .sort_values("date")
            .tail(n_games)
        )

        prev_t2 = (
            historical_df[
                (historical_df["League"] == league)
                & ((historical_df["team1"] == t2) | (historical_df["team2"] == t2))
                & (historical_df["date"] < date)
            ]
            .sort_values("date")
            .tail(n_games)
        )

        def calc_stats(prev, team):
            if prev.empty:
                return 0, 0
            points = 0
            goals = 0
            for _, g in prev.iterrows():
                if g["team1"] == team:
                    goals += g["Team1Goals"]
                    if g["Team1Goals"] > g["Team2Goals"]:
                        points += 3
                    elif g["Team1Goals"] == g["Team2Goals"]:
                        points += 1
                else:
                    goals += g["Team2Goals"]
                    if g["Team2Goals"] > g["Team1Goals"]:
                        points += 3
                    elif g["Team2Goals"] == g["Team1Goals"]:
                        points += 1
            return points / n_games, goals / n_games

        t1_points, t1_avg_goals = calc_stats(prev_t1, t1)
        t2_points, t2_avg_goals = calc_stats(prev_t2, t2)
        team1_form.append(t1_points)
        team2_form.append(t2_points)
        team1_goals.append(t1_avg_goals)
        team2_goals.append(t2_avg_goals)

    upcoming_df["team1_last5_avg_points"] = team1_form
    upcoming_df["team2_last5_avg_points"] = team2_form
    upcoming_df["team1_last5_avg_goals"] = team1_goals
    upcoming_df["team2_last5_avg_goals"] = team2_goals
    return upcoming_df
