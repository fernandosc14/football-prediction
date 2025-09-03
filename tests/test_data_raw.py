import json


def find_duplicates(data):
    """Find duplicate matches based on date, team1, and team2."""
    seen = set()
    duplicates = []
    for m in data:
        key = (m.get("date"), m.get("team1"), m.get("team2"))
        if all(key):
            if key in seen:
                duplicates.append(key)
            else:
                seen.add(key)
    return duplicates


def test_data_raw():
    """Test to ensure no duplicate matches in raw data."""
    path = "data/raw/matches_raw.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    duplicates = find_duplicates(data)
    assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate matches!"


def test_essential_fields_not_null():
    """Test that essential fields are present and not null."""
    path = "data/raw/matches_raw.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    essentials = [
        "date",
        "time",
        "league",
        "team1",
        "team2",
        "team1_goals",
        "team2_goals",
        "h2h_games_played",
        "h2h_team1_wins",
        "h2h_team2_wins",
        "h2h_draws",
    ]
    for match in data:
        for field in essentials:
            assert field in match, f"Missing field: {field}"
            assert match[field] not in (None, ""), f"Field {field} is null or empty"
