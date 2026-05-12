from sqlalchemy import create_engine, select, outerjoin, join, or_, and_
from sqlalchemy.orm import Session

from database.relational.crud import DBEngine
from database.relational.tables import ProjectDetails, PageLayout, ProjectMaster, ProjectUsers
from utils import log_error

def start_engine():
    try:
        db_engine = DBEngine()
        return db_engine.engine
    except Exception as err:
        log_error(str(err))

def approve_page(page_name: str, layout: dict, project_id: int) -> bool:
    """
    Enter the project detail and save the page layout
    Args:
        page_name: Name of the page
        layout: JSON layout
        project_id: associated project id

    Returns: bool: Acknowledgement

    """
    engine = start_engine()
    if not engine:
        return False

    with Session(engine) as session:
        try:
            new_page_layout = PageLayout()
            new_page_layout.PageName = page_name
            new_page_layout.Layout = layout
            session.add(new_page_layout)

            session.flush() # push to db without inserting

            new_project_dtl = ProjectDetails()
            new_project_dtl.PageID = new_page_layout.PageID # depends on the above insert
            new_project_dtl.ProjectID = project_id
            session.add(new_project_dtl)

            session.commit()
            return True
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False

def create_project_with_manager(user_id: int, proj_name: str, proj_desc: str) -> bool:
    engine = start_engine()
    if not engine:
        return False

    with Session(engine) as session:
        try:
            new_proj = ProjectMaster()
            new_proj.ManagerID = user_id
            new_proj.Name = proj_name
            new_proj.Description = proj_desc
            session.add(new_proj)

            session.flush()

            new_proj_user = ProjectUsers()
            new_proj_user.ProjectID = new_proj.ProjectID # above inserted
            new_proj_user.UserID = user_id
            session.add(new_proj_user)

            session.commit()
            return True
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False



