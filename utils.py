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

EMPTY_STRING = "";

def log_error(err_msg: str):
    logger.error(err_msg)

def log_info(info_msg: str):
    logger.info(info_msg)

def generate_random_id():
    return datetime.now().strftime("%d%m%Y%H%M%S")

def read_app_config(key_name: str):
    if not os.path.exists("app_config.json"):
        return {}

    with open("app_config.json", "r") as f:
        data = json.load(f)
    if not data:
        return {}

    if key_name not in data:
        return {}

    return data[key_name]

def get_database_config():
    return read_app_config("database")


def get_ollama_conf(key_name=""):
    return read_app_config("Ollama")

def get_llm_source():
    return read_app_config("LLM")["source"]

def construct_llm_url():
    llm_conf = read_app_config("LLM")
    if not llm_conf:
        return EMPTY_STRING

    match llm_conf["source"]:
        case "runpod":
            return f"https://{llm_conf["POD_ID"]}-{str(llm_conf["PORT"])}.proxy.runpod.net"
        case _:
            return EMPTY_STRING

def get_supported_field_types():
    return read_app_config("Supported_Input_Fields_Type")

def get_form_layout():
    if not os.path.exists("form_layout.json"):
        return EMPTY_STRING

    with open("form_layout.json", "r") as f:
        return json.dumps(json.load(f))


