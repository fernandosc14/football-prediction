from pathlib import Path
import json


def validate_historical_matches():
    essentials_fields = [
        "date",
        "time",
        "league",
        "is_cup",
        "team1",
        "team2",
        "team1_goals",
        "team2_goals",
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
    data_path = Path("data/raw/matches_raw.json")

    with open(data_path, encoding="utf-8") as f:
        matches = json.load(f)

    errors = []
    warnings = []

    for i, match in enumerate(matches):
        for field in essentials_fields:
            if field not in match:
                errors.append(f"[ERROR] Missing field: {field} in match {i+1}")
            elif match[field] == "" or match[field] is None:
                warnings.append(f"[WARNING] Empty field: {field} in match {i+1}")
    if errors:
        for err in errors:
            print(err)
        raise ValueError("Validation failed due to missing fields.")
    if warnings:
        for warn in warnings:
            print(warn)
    print("Validation completed successfully.")


if __name__ == "__main__":
    validate_historical_matches()
