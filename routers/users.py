from fastapi import FastAPI, APIRouter, status, HTTPException

from database.relational import transact, joins
from database.relational.crud import UserMasterCrud
from models.models import UserModel

router = APIRouter(
    prefix="/api/user"
)

@router.get("/")
def root():
    return "Routing is working!"

@router.get("/get_user/", status_code=status.HTTP_200_OK)
def get_user(user_id: int = 0, email: str = "", password: str = ""):
    obj = UserMasterCrud()
    return obj.read(user_id, email, password)


@router.post("/login_user/", status_code = status.HTTP_200_OK)
def login_user(user: UserModel):
    # obj = UserMasterCrud()
    # return obj.read(0, user.email, user.password)
    return joins.login_user(email=user.email, password=user.password)

@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserModel):
    # obj = UserMasterCrud()
    # success = obj.create(first_name = user.first_name, last_name = user.last_name, email = user.email, password = user.password)

    success = transact.create_user(first_name = user.first_name, last_name = user.last_name, email = user.email, password = user.password)
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
