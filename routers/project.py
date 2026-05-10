from fastapi import APIRouter, status, HTTPException
import json

from models.models import UserModel, ProjectMasterModel, ProjectUserModel, ProjectDetailModel, PageLayoutModel, PageDataModel, ListProjectModel, ListProjectPagesModel
from database.relational.crud import UserMasterCrud, ProjectMasterCrud, ProjectUserCrud, ProjectDetailsCrud, PageLayoutCrud, PageDataCrud
from database.relational import joins
from utils import log_info

router = APIRouter(prefix="/api/project")

@router.get("/", status_code=status.HTTP_200_OK)
def get_project(project_id: int = 0):
    obj = ProjectMasterCrud()
    return obj.read(project_id)

@router.get("/get_all_projects/", status_code=status.HTTP_200_OK)
def get_all_projects(user_id: int):
    results = joins.get_all_projects(user_id)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return results

@router.post("/create_project/", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectMasterModel):
    obj = ProjectMasterCrud()
    success, inserted_id = obj.create(project.manager_id, project.name, project.description)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project creation failed")
    return {"message": "Project creation successful","project_id": inserted_id}

@router.post("/create_project_only/", status_code=status.HTTP_201_CREATED)
def create_project_only(project: ProjectMasterModel):
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

# USER MASTER
@router.get("/get_user/", status_code = status.HTTP_200_OK)
def get_user(user_id: int):
    obj = UserMasterCrud()
    results = obj.read(user_id)
    return results

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
    success = obj.create(page_name = project.page_name, layout = project.layout)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project layout creation failed")
    return {"message": "Project layout saved successful"}

@router.post("/replace_page_layout/", status_code=status.HTTP_200_OK)
def replace_page_layout(project: PageLayoutModel):
    obj = PageLayoutCrud()
    success = obj.update(page_id = project.page_id, page_name = project.page_name, layout = project.layout)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project layout creation failed")
    return {"message": "Project layout saved successful"}

#PROJECT DETAILS
@router.get("/get_project_details/", status_code = status.HTTP_200_OK)
def get_project_details(detail_id:int, project_id: int):
    obj = ProjectDetailsCrud()
    result = obj.read(detail_id, project_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "No match for requested detail id")

    return result

@router.get("/get_project_pages/", status_code = status.HTTP_200_OK)
def get_project_pages(project_id: int):
    """Get Project Pages list

    Args:
        project (ProjectDetailModel): Pydantic input data

    Raises:
        HTTPException: if no match for the data

    Returns:
        list[ListProjectPagesModel]: Pydantic rep.. of project pages
    """
    results = joins.get_project_pages(project_id)

    return results

@router.post("/create_project_detail/", status_code=status.HTTP_201_CREATED)
def create_project_detail(project: ProjectDetailModel):
    obj = ProjectDetailsCrud()
    success = obj.create(project.project_id, project.page_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project detail creation failed")
    return {"message": "Project detail creation successful"}

@router.post("/update_project_detail/", status_code=status.HTTP_200_OK)
def update_project_detail(project: ProjectDetailModel):
    obj = ProjectDetailsCrud()
    success = obj.update(project.detail_id,project.project_id, project.page_id, project.is_active)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project detail updation failed")
    return {"message": "Project detail updation successful"}

@router.post("/delete_project_detail/", status_code=status.HTTP_200_OK)
def delete_project_detail(project: ProjectDetailModel):
    obj = ProjectDetailsCrud()
    success = obj.delete(project.detail_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project detail deletion failed")
    return {"message": "Project detail deletion successful"}

# PAGE DATA
@router.post("/save_page_data/", status_code=status.HTTP_201_CREATED)
def save_page_data(project: PageDataModel):
    obj = PageDataCrud()
    success = obj.create(project.proj_detail_id, project.data)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page data save failed")
    return {"message": "Page data saved successful"}

@router.post("/replace_page_data/", status_code=status.HTTP_201_CREATED)
def replace_page_data(project: PageDataModel):
    obj = PageDataCrud()
    success = obj.update(project.page_data_id, project.data)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page data replace failed")
    return {"message": "Page data replace successful"}

@router.post("/delete_page_data/", status_code=status.HTTP_200_OK)
def delete_page_data(project: PageDataModel):
    obj = PageDataCrud()
    success = obj.delete(project.page_data_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page data deletion failed")
    return {"message": "Page data deletion successful"}