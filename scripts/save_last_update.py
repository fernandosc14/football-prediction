import os
import json
from datetime import datetime


def save_last_update():
    meta_dir = os.path.join("data", "meta")
    os.makedirs(meta_dir, exist_ok=True)
    last_update_path = os.path.join(meta_dir, "last_update.json")
    tmp_path = last_update_path + ".tmp"
    now = datetime.utcnow().isoformat() + "Z"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump({"last_update": now}, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, last_update_path)
    print(f"Last update saved: {now}")


if __name__ == "__main__":
    save_last_update()
