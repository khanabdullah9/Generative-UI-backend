from fastapi import FastAPI, APIRouter, status, HTTPException

from models.models import ProjectMasterModel, ProjectUserModel, ProjectDetailModel
from database.relational.crud import ProjectMasterCrud
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


