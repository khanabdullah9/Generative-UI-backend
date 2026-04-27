from fastapi import FastAPI, APIRouter

from database import project
from models.models import user_model

router = APIRouter(
    prefix="/api/user"
)

@router.get("/")
def root():
    return "Routing is working!"

@router.post("/create_user/")
def create_user(user: user_model):
    result = project.add_user(user_name = user.user_name, email = user.email)
    return result
    
@router.post("/replace_user/")
def replace_user(user: user_model):
    return project.replace_user(id = user.id, user_name = user.user_name,
                                    email = user.email, password = user.password)