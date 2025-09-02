from pathlib import Path
from datetime import datetime, timedelta
from src.utils import get_api_key, load_json

import json
import requests
import logging

SESSION = requests.Session()
TIMEOUT = (10, 30)


def get_leagues_id(json_path="config/leagues.json"):
    """Load league IDs from a JSON configuration file."""

    data = load_json(json_path)
    if not isinstance(data, list) or not all("id" in lg for lg in data):
        raise ValueError("Leagues JSON must be a list of dicts with 'id' key.")
    return [lg["id"] for lg in data]


def get_historical_data(leagues_id=None, weeks=3):
    """Fetches historical match data from the SoccerDataAPI for the specified leagues and time frame."""

    api_key = get_api_key()

    if leagues_id is None:
        try:
            leagues_id = get_leagues_id()
        except ValueError as e:
            logging.error(f"[Error] loading leagues: {e}")
            raise ValueError(f"Leagues configuration is invalid: {e}")

    today_dt = datetime.now()
    now = today_dt - timedelta(hours=1)
    start_dt = today_dt - timedelta(weeks=weeks)
    games = []

    for league_id in leagues_id:
        url = "https://api.soccerdataapi.com/matches/"
        query = {"league_id": league_id, "auth_token": api_key}
        headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json"}
        try:
            response = SESSION.get(url, headers=headers, params=query, timeout=TIMEOUT)
            data = response.json()
        except Exception as e:
            logging.error(f"[ERROR] Request or JSON decode failed for league {league_id}: {e}")
            continue

        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            logging.warning(f"[WARNING] Unexpected data type: {type(data)} for league {league_id}")
            continue

        for obj in data:
            if not isinstance(obj, dict):
                logging.warning(f"[WARNING] Unexpected data format: {obj}")
                continue
            for stage in obj.get("stage", []):
                for match in stage.get("matches", []):
                    match_date_str = match.get("date")
                    if not match_date_str:
                        continue
                    try:
                        match_date = datetime.strptime(match_date_str, "%d/%m/%Y")
                    except Exception as e:
                        logging.warning(f"[WARNING] Date parsing failed: {match_date_str} ({e})")
                        continue
                    if start_dt.date() <= match_date.date() <= now.date():
                        home_team = match.get("teams", {}).get("home", {})
                        away_team = match.get("teams", {}).get("away", {})
                        is_cup = match.get("is_cup")
                        if is_cup is None:
                            is_cup = obj.get("is_cup")
                        games.append(
                            {
                                "date": match["date"],
                                "time": match.get("time", ""),
                                "home_name": home_team.get("name", "?"),
                                "away_name": away_team.get("name", "?"),
                                "home_id": home_team.get("id", "?"),
                                "away_id": away_team.get("id", "?"),
                                "match_id": match.get("id"),
                                "league_id": league_id,
                                "is_cup": is_cup,
                            }
                        )
    return games


def get_matches_details(match_id):
    """Fetches detailed information for a specific match by its ID."""

    api_key = get_api_key()

    url = "https://api.soccerdataapi.com/match/"
    querystring = {"match_id": match_id, "auth_token": api_key}
    headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json"}
    response = SESSION.get(url, headers=headers, params=querystring, timeout=TIMEOUT)
    try:
        return response.json()
    except Exception as e:
        logging.error(f"[ERROR] JSON decode failed for match {match_id}: {e}")
        return None


def get_h2h(team1_id, team2_id):
    """Fetches head-to-head statistics between two teams by their IDs."""

    api_key = get_api_key()

    url = "https://api.soccerdataapi.com/head-to-head/"
    querystring = {"team_1_id": team1_id, "team_2_id": team2_id, "auth_token": api_key}
    headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json"}
    try:
        resp = SESSION.get(url, headers=headers, params=querystring, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logging.error(f"[ERROR] H2H request failed for {team1_id} vs {team2_id}: {e}")
        return {}
    if isinstance(data, dict):
        return data.get("stats", {})
    logging.warning(f"[WARNING] Unexpected H2H payload type: {type(data)}")
    return {}


def get_standings(league_id):
    """Fetches the current standings for a specific league by its ID."""

    api_key = get_api_key()

    url = "https://api.soccerdataapi.com/standing/"
    query = {"league_id": league_id, "auth_token": api_key}
    headers = {"Accept-Encoding": "gzip", "Content-Type": "application/json"}
    response = SESSION.get(url, headers=headers, params=query, timeout=TIMEOUT)
    try:
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logging.error(f"[ERROR] JSON decode failed for standings of league {league_id}: {e}")
        return []
    try:
        if (
            isinstance(data, dict)
            and data.get("stage")
            and isinstance(data["stage"][0], dict)
            and "standings" in data["stage"][0]
        ):
            return data["stage"][0]["standings"]
    except Exception:
        logging.exception("Unexpected data format for standings of league %s", league_id)
    return []


def main():
    """Main function to fetch historical match data and save it to a JSON file."""

    matches = get_historical_data()
    logging.info(f"[INFO] Fetched {len(matches)} historical matches.")

    output_path = Path("data/raw/matches_raw.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_saved = 0
    total_ignored = 0
    saved_matches = []

    try:
        for match in matches:
            try:
                match_id = match["match_id"]
                is_cup = match.get("is_cup")
                details = get_matches_details(match_id)
                if not details or details.get("status") != "finished":
                    continue
                date = details.get("date", "")
                time = details.get("time", "")
                league = details.get("league", {}).get("name", "")
                team1 = details.get("teams", {}).get("home", {}).get("name", "")
                team2 = details.get("teams", {}).get("away", {}).get("name", "")
                team1_goals = details.get("goals", {}).get("home_ft_goals", "")
                team2_goals = details.get("goals", {}).get("away_ft_goals", "")

                team1_id = details.get("teams", {}).get("home", {}).get("id", None)
                team2_id = details.get("teams", {}).get("away", {}).get("id", None)

                team1_rank = team2_rank = ""
                league_id = details.get("league", {}).get("id", None)
                standings = []
                if league_id:
                    try:
                        standings = get_standings(league_id)
                    except Exception as e:
                        logging.warning(f"Error getting standings for league_id {league_id}: {e}")
                if standings:
                    for team in standings:
                        if team1_id and str(team.get("team_id")) == str(team1_id):
                            team1_rank = team.get("position", "")
                        if team2_id and str(team.get("team_id")) == str(team2_id):
                            team2_rank = team.get("position", "")

                h2h_games_played = h2h_team1_wins = h2h_team2_wins = h2h_draws = ""
                h2h_team1_scored = h2h_team2_scored = ""
                h2h_team1_home_wins = h2h_team1_home_draws = h2h_team1_home_losses = ""
                h2h_team1_home_scored = h2h_team1_home_conceded = ""
                h2h_team2_home_wins = h2h_team2_home_draws = h2h_team2_home_losses = ""
                h2h_team2_home_scored = h2h_team2_home_conceded = ""
                if team1_id and team2_id:
                    h2h_data = get_h2h(team1_id, team2_id)
                    stats = h2h_data.get("overall", {}) if isinstance(h2h_data, dict) else {}
                    h2h_games_played = stats.get("overall_games_played", "")
                    h2h_team1_wins = stats.get("overall_team1_wins", "")
                    h2h_team2_wins = stats.get("overall_team2_wins", "")
                    h2h_draws = stats.get("overall_draws", "")
                    h2h_team1_scored = stats.get("overall_team1_scored", "")
                    h2h_team2_scored = stats.get("overall_team2_scored", "")
                    t1_home = h2h_data.get("team1_at_home", {})
                    h2h_team1_home_wins = t1_home.get("team1_wins_at_home", "")
                    h2h_team1_home_draws = t1_home.get("team1_draws_at_home", "")
                    h2h_team1_home_losses = t1_home.get("team1_losses_at_home", "")
                    h2h_team1_home_scored = t1_home.get("team1_scored_at_home", "")
                    h2h_team1_home_conceded = t1_home.get("team1_conceded_at_home", "")
                    t2_home = h2h_data.get("team2_at_home", {})
                    h2h_team2_home_wins = t2_home.get("team2_wins_at_home", "")
                    h2h_team2_home_draws = t2_home.get("team2_draws_at_home", "")
                    h2h_team2_home_losses = t2_home.get("team2_losses_at_home", "")
                    h2h_team2_home_scored = t2_home.get("team2_scored_at_home", "")
                    h2h_team2_home_conceded = t2_home.get("team2_conceded_at_home", "")

                match_data = {
                    "date": date,
                    "time": time,
                    "league": league,
                    "is_cup": is_cup,
                    "team1": team1,
                    "team2": team2,
                    "team1_goals": team1_goals,
                    "team2_goals": team2_goals,
                    "team1_rank": team1_rank,
                    "team2_rank": team2_rank,
                    "h2h_games_played": h2h_games_played,
                    "h2h_team1_wins": h2h_team1_wins,
                    "h2h_team2_wins": h2h_team2_wins,
                    "h2h_draws": h2h_draws,
                    "h2h_team1_scored": h2h_team1_scored,
                    "h2h_team2_scored": h2h_team2_scored,
                    "h2h_team1_home_wins": h2h_team1_home_wins,
                    "h2h_team1_home_draws": h2h_team1_home_draws,
                    "h2h_team1_home_losses": h2h_team1_home_losses,
                    "h2h_team1_home_scored": h2h_team1_home_scored,
                    "h2h_team1_home_conceded": h2h_team1_home_conceded,
                    "h2h_team2_home_wins": h2h_team2_home_wins,
                    "h2h_team2_home_draws": h2h_team2_home_draws,
                    "h2h_team2_home_losses": h2h_team2_home_losses,
                    "h2h_team2_home_scored": h2h_team2_home_scored,
                    "h2h_team2_home_conceded": h2h_team2_home_conceded,
                }

                rank_indexes = ["team1_rank", "team2_rank"]
                if is_cup is True:
                    essential_fields = [v for k, v in match_data.items() if k not in rank_indexes]
                else:
                    essential_fields = list(match_data.values())
                if all(str(x).strip() != "" for x in essential_fields):
                    saved_matches.append(match_data)
                    total_saved += 1
                else:
                    total_ignored += 1
                    empty_fields = [
                        k
                        for k, v in match_data.items()
                        if (str(v).strip() == "")
                        and ((is_cup is True and k not in rank_indexes) or (is_cup is not True))
                    ]
                    logging.info(
                        f"[SKIPPED] Match {team1} vs {team2} | Empty essential fields: {empty_fields}"
                    )
            except Exception as e:
                logging.error(
                    f"[ERROR] Unexpected error processing match {match.get('match_id', '?')}: {e}"
                )
        with open(output_path, "w", encoding="utf-8") as f:
            print("Writing data to", output_path)
            json.dump(saved_matches, f, ensure_ascii=False, indent=2)
        logging.info(f"[INFO] Total saved matches: {total_saved}")
        logging.info(f"[INFO] Total games skipped: {total_ignored}")
    except Exception as e:
        logging.critical(f"[CRITICAL] Fatal error in main loop: {e}")


def fetch_upcoming_matches():
    # TODO: implement this function to fetch upcoming matches
    return


if __name__ == "__main__":
    main()
