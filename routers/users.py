from fastapi import FastAPI, APIRouter

from database.relational.crud import UserMasterCrud
from models.models import user_model

router = APIRouter(
    prefix="/api/user"
)

@router.get("/")
def root():
    return "Routing is working!"

@router.get("/get_user/{user_id}")
def get_user(user_id: int):
    obj = UserMasterCrud()
    return obj.read(id = user_id)

@router.post("/create_user/")
def create_user(user: user_model):
    obj = UserMasterCrud()
    return obj.create(first_name = user.first_name, last_name = user.last_name, email = user.email)
    
@router.post("/update_user/")
def update_user(user: user_model):
    obj = UserMasterCrud()
    return obj.update(id = user.user_id, first_name = user.first_name, last_name = user.last_name, email = user.email)

@router.post("/set_user_inactive/")
def delete_user(user: user_model):
    pass


@router.post("/replace_user/")
def replace_user(user: user_model):
    pass