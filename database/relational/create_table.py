from sqlalchemy import create_engine, MetaData
import urllib.parse
from tables import BaseClass

safe_password = urllib.parse.quote_plus("root@1234")
engine = create_engine(f"postgresql+psycopg2://postgres:{safe_password}@localhost:5432/gen_ui", echo = True)

BaseClass.metadata.create_all(engine)
print("Tables created!")