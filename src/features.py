from sklearn.preprocessing import LabelEncoder

import numpy as np


def add_winner_feature(df):
    """Add a feature representing the match winner."""
    df["Winner"] = np.where(
        df["Team1Goals"] > df["Team2Goals"],
        "1",
        np.where(df["Team1Goals"] < df["Team2Goals"], "2", "X"),
    )
    return df


def add_goal_difference_feature(df):
    """Add a feature representing the goal difference."""
    df["Goal_Difference"] = df["Team1Goals"] - df["Team2Goals"]
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


def apply_all_features(df):
    """Apply all feature engineering functions to the DataFrame."""
    df = add_winner_feature(df)
    df = add_goal_difference_feature(df)
    df = add_double_chance_feature(df)
    df = add_over_feature(df)
    df = add_btts_feature(df)
    df = add_rank_diff_feature(df)
    df = add_h2h_feature(df)
    df, le_league = encode_league(df)
    return df, le_league
