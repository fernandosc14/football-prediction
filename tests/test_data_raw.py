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
