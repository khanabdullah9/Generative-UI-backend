from sqlalchemy import create_engine, MetaData
import urllib.parse
from tables import BaseClass
import os
import sys

# SETTING THE DIR TO ROOT FOLDER TO IMPORT utils.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)
from utils import get_database_config

db_config = get_database_config()

safe_password = urllib.parse.quote_plus(db_config["password"])
dialect = db_config["dialect"]
driver = db_config["driver"]
username = db_config["username"]
server_name = "db" if db_config["env"] == "PRD" else "localhost"
port = db_config["port"]
db_name = db_config["database_name"]
conn_str = f"{dialect}+{driver}://{username}:{safe_password}@{server_name}:{port}/{db_name}"
engine = create_engine(conn_str)


BaseClass.metadata.create_all(engine)
print("Tables created!")