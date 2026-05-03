from pydantic import BaseModel
from typing import Optional

class SaveDataModel(BaseModel):
    db_name: str
    collection_name: str
    form_data: dict
    mode: int # 1: create,2: read,3: update,4: delete

class UserModel(BaseModel):
    user_id: int | None = 0
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: int | None = 1

class ProjectMasterModel(BaseModel):
    project_id: int = 0
    manager_id: int = 0
    name: str = ""
    description: str = ""
    is_active: int = 1

class ProjectDetailModel(BaseModel):
    detail_id: int = 0
    project_id: int
    page_id: int    
    is_active: int = 1

class ProjectUserModel(BaseModel):
    proj_user_id: int = 0
    project_id: int = 0
    user_id: int = 0
    is_active: int  = 1

class PageLayoutModel(BaseModel):
    page_id: int = 0
    layout: dict
    is_active: int  = 1

class PageDataModel(BaseModel):
    page_data_id: int
    proj_detail_id: int
    data: dict
    is_active: int = 1
