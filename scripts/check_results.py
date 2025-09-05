import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils import load_json, save_json

PREDICTIONS_HISTORY_PATH = os.path.join("data", "predict", "predictions_history.json")
MATCHES_RAW_PATH = os.path.join("data", "raw", "matches_raw.json")


def main():
    predictions = load_json(PREDICTIONS_HISTORY_PATH)
    matches = load_json(MATCHES_RAW_PATH)
    matches_by_id = {m["match_id"]: m for m in matches if "match_id" in m}

    finished_count = 0
    unfinished_count = 0

    correct = {"winner": 0, "over_2_5": 0, "over_1_5": 0, "double_chance": 0, "btts": 0}
    total = {"winner": 0, "over_2_5": 0, "over_1_5": 0, "double_chance": 0, "btts": 0}
    for pred in predictions:
        match_id = pred.get("match_id")
        match = matches_by_id.get(match_id)
        if match:
            pred["finished"] = True
            finished_count += 1
            team1_goals = match.get("team1_goals")
            team2_goals = match.get("team2_goals")
            if team1_goals is not None and team2_goals is not None:
                winner_pred = pred["predictions"]["winner"]["class"]
                if winner_pred == 0:
                    winner_correct = team1_goals > team2_goals
                elif winner_pred == 1:
                    winner_correct = team1_goals == team2_goals
                elif winner_pred == 2:
                    winner_correct = team1_goals < team2_goals
                else:
                    winner_correct = False
                correct["winner"] += int(winner_correct)
                total["winner"] += 1

                over_2_5_pred = pred["predictions"]["over_2_5"]["class"]
                over_2_5_correct = (
                    (team1_goals + team2_goals > 2.5)
                    if over_2_5_pred == 1
                    else (team1_goals + team2_goals <= 2.5)
                )
                correct["over_2_5"] += int(over_2_5_correct)
                total["over_2_5"] += 1

                over_1_5_pred = pred["predictions"]["over_1_5"]["class"]
                over_1_5_correct = (
                    (team1_goals + team2_goals > 1.5)
                    if over_1_5_pred == 1
                    else (team1_goals + team2_goals <= 1.5)
                )
                correct["over_1_5"] += int(over_1_5_correct)
                total["over_1_5"] += 1

                double_chance_pred = pred["predictions"]["double_chance"]["class"]
                if double_chance_pred == 0:
                    double_chance_correct = team1_goals >= team2_goals
                elif double_chance_pred == 1:
                    double_chance_correct = team1_goals <= team2_goals
                elif double_chance_pred == 2:
                    double_chance_correct = team1_goals != team2_goals
                else:
                    double_chance_correct = False
                correct["double_chance"] += int(double_chance_correct)
                total["double_chance"] += 1

                btts_pred = pred["predictions"]["btts"]["class"]
                if btts_pred == 1:
                    btts_correct = team1_goals > 0 and team2_goals > 0
                else:
                    btts_correct = not (team1_goals > 0 and team2_goals > 0)
                correct["btts"] += int(btts_correct)
                total["btts"] += 1
        else:
            pred["finished"] = False
            unfinished_count += 1
    save_json(predictions, PREDICTIONS_HISTORY_PATH)

    stats = {}
    for key in correct:
        percent = correct[key] / total[key] * 100 if total[key] else 0
        stats[key] = {"correct": correct[key], "total": total[key], "percent": round(percent, 2)}

    best_type = max(stats, key=lambda k: stats[k]["percent"] if stats[k]["total"] > 0 else -1)
    stats["best_type"] = best_type

    stats_path = os.path.join("data", "stats", "prediction_stats.json")
    save_json(stats, stats_path)


if __name__ == "__main__":
    main()
