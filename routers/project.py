from fastapi import FastAPI, APIRouter, status, HTTPException

from models.models import ProjectMasterModel, ProjectUserModel, ProjectDetailModel, PageLayoutModel
from database.relational.crud import ProjectMasterCrud, ProjectUserCrud, ProjectDetailsCrud, PageLayoutCrud
from utils import log_info

router = APIRouter(prefix="/api/project")

@router.get("/", status_code=status.HTTP_200_OK)
def get_project(project_id: int = 0):
    obj = ProjectMasterCrud()
    return obj.read(project_id)

@router.post("/create_project/", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectMasterModel):
    obj = ProjectMasterCrud()
    success = obj.create(project.manager_id, project.name, project.description)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project creation failed")
    return {"message": "Project creation successful"}

@router.post("/update_project/", status_code=status.HTTP_200_OK)
def update_project(project: ProjectMasterModel):
    obj = ProjectMasterCrud()
    success = obj.update(project.project_id, project.manager_id, project.name, project.description, project.is_active)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project updation failed")
    return {"message": "Project updation successful"}

@router.post("/delete_project/", status_code=status.HTTP_200_OK)
def delete_project(project: ProjectMasterModel):
    obj = ProjectMasterCrud()
    success = obj.delete(project.project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project deletion failed")
    return {"message": "Project deletion successful"}

# PROJECT USER
@router.post("/add_project_user/", status_code=status.HTTP_201_CREATED)
def add_project_user(project: ProjectUserModel):
    obj = ProjectUserCrud()
    success = obj.create(project.project_id,project.user_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project user creation failed")
    return {"message": "Project user creation successful"}

@router.post("/delete_project_user/", status_code=status.HTTP_200_OK)
def delete_project_user(project: ProjectUserModel):
    obj = ProjectUserCrud()
    success = obj.delete(project.proj_user_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project user deletion failed")
    return {"message": "Project user deletion successful"}

# PROJECT LAYOUT
@router.post("/save_page_layout/", status_code=status.HTTP_201_CREATED)
def save_page_layout(project: PageLayoutModel):
    obj = PageLayoutCrud()
    success = obj.create(layout = project.layout)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project layout creation failed")
    return {"message": "Project layout saved successful"}

@router.post("/replace_page_layout/", status_code=status.HTTP_200_OK)
def replace_page_layout(project: PageLayoutModel):
    obj = PageLayoutCrud()
    log_info(str(project.page_id))
    success = obj.update(page_id = project.page_id, layout = project.layout)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project layout creation failed")
    return {"message": "Project layout saved successful"}