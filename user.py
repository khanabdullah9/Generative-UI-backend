from fastapi import FastAPI

from models import user_model
from database import project
from utils import log_error

app = FastAPI()

@app.post("/api/user/create_user/")
def create_user(user: user_model):
    try:
        result = project.add_user(user_name = user.user_name, email = user.email)
        return result
    except Exception as err:
        log_error(str(err))
        return False
    
@app.post("/api/user/replace_user/")
def replace_user(user: user_model):
    try:
        return project.replace_user(id = user_model.id, user_name = user_model.user_name,
                                    email = user_model.email, password = user_model.password)
    except Exception as err:
        log_error(str(err))
        return False