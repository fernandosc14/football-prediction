from datetime import datetime, timezone
import config


def save_last_update():
    now_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    config.redis_client.set(config.LAST_UPDATE_KEY, now_utc)


if __name__ == "__main__":
    save_last_update()
