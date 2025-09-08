import os
import redis
from dotenv import load_dotenv

load_dotenv()

LAST_UPDATE_KEY = "last_update_timestamp"
redis_url = os.getenv("REDIS_URL")
if not redis_url:
    raise RuntimeError("REDIS_URL environment variable is not set")
redis_client = redis.from_url(redis_url)
