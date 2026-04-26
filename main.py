from fastapi import FastAPI

from models import save_data_model, user_model
from database.crud import CRUD
from utils import log_info
from database import project

app = FastAPI()

@app.get("/")
def root():
    return "Server is running!"

@app.post("/api/create_project")
def create_project():
    pass

@app.post("/api/save_data/")
def save_data(data: save_data_model) -> bool:
    if data.form_data in [None, {}]:
        return False

    crud_obj = CRUD(data.db_name, data.collection_name)
    match data.mode:
        case 1:
            crud_obj.create(data.form_data)
        case 3:
            crud_obj.replace(data.form_data)

    return True

@app.post("/api/user/create_user/")
def create_user(user: user_model):
    result = project.add_user(user_name = user.user_name, email = user.email)
    return result
    
@app.post("/api/user/replace_user/")
def replace_user(user: user_model):
    return project.replace_user(id = user.id, user_name = user.user_name,
                                    email = user.email, password = user.password)