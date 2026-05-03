from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.models import SaveDataModel
from database.nosql.crud import CRUD
from utils import log_info
from database.nosql import project
from routers import users, project

app = FastAPI()
app.include_router(users.router)
app.include_router(project.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def root():
    return "Server is running!"

@app.post("/api/create_project")
def create_project():
    pass

@app.post("/api/save_data/")
def save_data(data: SaveDataModel) -> bool:
    if data.form_data in [None, {}]:
        return False

    crud_obj = CRUD(data.db_name, data.collection_name)
    match data.mode:
        case 1:
            crud_obj.create(data.form_data)
        case 3:
            crud_obj.replace(data.form_data)

    return True