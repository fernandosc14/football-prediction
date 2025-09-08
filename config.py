import os
import redis
from dotenv import load_dotenv

load_dotenv()

LAST_UPDATE_KEY = "last_update_timestamp"
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(redis_url)
