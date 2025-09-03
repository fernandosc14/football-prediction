from dotenv import load_dotenv


import yaml
import json
import os
import logging


def load_config(path="config/config.yaml"):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_api_key(var_name="API_KEY"):
    """Load API key from .env file"""
    load_dotenv()
    api_key = os.getenv(var_name)
    if not api_key:
        raise EnvironmentError(f"{var_name} not found in environment variables.")
    return api_key


def load_json(path):
    """Load JSON file from the given path"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(obj, path, indent=2):
    """Save object as JSON file to the given path"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)


def setup_logging(logfile=None, level=logging.INFO):
    """Setup logging configuration"""
    handlers = [logging.StreamHandler()]
    if logfile:
        handlers.append(logging.FileHandler(logfile, encoding="utf-8"))
    logging.basicConfig(
        level=level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers
    )
