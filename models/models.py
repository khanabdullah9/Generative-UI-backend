from pydantic import BaseModel
from typing import Optional

class save_data_model(BaseModel):
    db_name: str
    collection_name: str
    form_data: dict
    mode: int # 1: create,2: read,3: update,4: delete

class user_model(BaseModel):
    user_id: int | None = 0
    first_name: str
    last_name: str
    email: str
    password: str | None = ""
