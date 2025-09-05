import os
import redis
from dotenv import load_dotenv

load_dotenv()

LAST_UPDATE_KEY = "last_update_timestamp"
redis_client = redis.from_url(os.getenv("REDIS_URL"))
