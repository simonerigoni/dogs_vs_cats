# Config
#
# python -m src.config

import json
import os

from dotenv import load_dotenv

DATA_FOLDER = "data/"
KAGGLE_FOLDER = DATA_FOLDER + "kaggle/train/"
GCP_FOLDER = DATA_FOLDER + "gcp/"
CSV_FILENAME = "all_data.csv"
LABELS = ["cat", "dog"]
DEFAULT_TEST_IMAGE = DATA_FOLDER + "test/1.jpg"


def _load_local_settings():
    """Load environment variables from .env or local.settings.json if present."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, "../.env")
    local_settings_json_path = os.path.join(current_dir, "../local.settings.json")

    if os.path.isfile(env_path):
        load_dotenv(env_path)
    elif os.path.isfile(local_settings_json_path):
        with open(local_settings_json_path) as f:
            settings = json.load(f)
        for key, value in settings["Values"].items():
            os.environ[key] = str(value)


if not os.getenv("ENV"):
    _load_local_settings()
else:
    pass


ENV = os.getenv("ENV")
BUCKET_NAME = os.getenv("BUCKET_NAME")
CREDENTIALS_JSON_FILE_PATH = os.getenv("CREDENTIALS_JSON_FILE_PATH")
PROJECT_ID = os.getenv("PROJECT_ID")
MODEL_ID = os.getenv("MODEL_ID")


if __name__ == "__main__":
    print("Config")
    print(f"{DATA_FOLDER = }")
    print(f"{KAGGLE_FOLDER = }")
    print(f"{GCP_FOLDER = }")
    print(f"{CSV_FILENAME = }")
    print(f"{LABELS = }")
    print(f"{DEFAULT_TEST_IMAGE = }")
    print(f"{ENV = }")
    print(f"{BUCKET_NAME = }")
    # print(f"{CREDENTIALS_JSON_FILE_PATH = }")
    # print(f"{PROJECT_ID = }")
    # print(f"{MODEL_ID = }")
else:
    pass
