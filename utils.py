import logging
import os
from datetime import datetime
import json

# 1. Setup the Root Logger to a high level (to silence the server/libraries)
logging.basicConfig(level=logging.WARNING) 

# 2. Create a specific logger for YOUR app
logger = logging.getLogger("my_app")
logger.setLevel(logging.INFO) # Your app will log INFO and above
logger.propagate = False # This prevents logs from "bubbling up" to the root logger

# 3. Add a FileHandler specifically to your logger
log_path = os.path.join(os.path.dirname(__file__), "app.log")
file_handler = logging.FileHandler(log_path, encoding="utf-8")
formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

EMPTY_STRING = ""; EMPTY_DICT = {}

def log_error(err_msg: str):
    logger.error(err_msg)

def log_info(info_msg: str):
    logger.info(info_msg)

def generate_random_id():
    return datetime.now().strftime("%d%m%Y%H%M%S")

def get_database_config():
    if not os.path.exists("app_config.json"):
        return EMPTY_DICT

    with open("app_config.json","r") as r:
        data = json.load(r)

    if "database" in data:
        return data["database"]

    return EMPTY_DICT


def get_ollama_conf(key_name=""):
    if not os.path.exists("app_config.json"):
        return EMPTY_DICT

    with open("app_config.json", "r") as f:
        data = json.load(f)
    if not data:
        return EMPTY_DICT

    if key_name and key_name in data["Ollama"]:
        return data["Ollama"][key_name]
    return data["Ollama"]

def get_form_layout():
    if not os.path.exists("form_layout.json"):
        return EMPTY_STRING

    with open("form_layout.json", "r") as f:
        return json.dumps(json.load(f))


def get_supported_field_types():
    if not os.path.exists("app_config.json"):
        return EMPTY_STRING

    with open("app_config.json", "r") as f:
        data = json.load(f)

    if not data:
        return EMPTY_STRING
    if "Supported_Input_Fields_Type" not in data:
        return EMPTY_STRING

    supported = data["Supported_Input_Fields_Type"]
    return ", ".join("'" + elem + "'" for elem in supported)