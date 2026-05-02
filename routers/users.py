from http.client import HTTPException

from fastapi import FastAPI, APIRouter, status

from database.relational.crud import UserMasterCrud
from models.models import UserModel

router = APIRouter(
    prefix="/api/user"
)

@router.get("/")
def root():
    return "Routing is working!"

@router.get("/get_user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    obj = UserMasterCrud()
    return obj.read(id = user_id)

@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserModel):
    obj = UserMasterCrud()
    success = obj.create(first_name = user.first_name, last_name = user.last_name, email = user.email)
    if not success:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User creation failed")
    return {"message": "User created successfully"}
    
@router.post("/update_user/", status_code=status.HTTP_202_ACCEPTED)
def update_user(user: UserModel):
    obj = UserMasterCrud()
    success = obj.update(id = user.user_id, first_name = user.first_name, last_name = user.last_name, email = user.email, is_active = user.is_active)
    if not success:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User updation failed")
    return {"message": "User updated successfully"}

@router.post("/set_user_inactive/")
def delete_user(user: UserModel):
    pass


@router.post("/replace_user/")
def replace_user(user: user_model):
    pass