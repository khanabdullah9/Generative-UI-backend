from sqlalchemy import  select, insert, and_
from sqlalchemy.orm import Session

from database.relational.crud import DBEngine
from database.relational.tables import ProjectDetails, PageLayout, ProjectMaster, ProjectUsers, PageData, Usage, UserMaster, Prompt
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

def create_project_with_manager(user_id: int, proj_name: str, proj_desc: str) -> tuple[bool, int]:
    engine = start_engine()
    if not engine:
        return False, -1

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
            return True, new_proj.ProjectID
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False, -1

def save_page_data(page_id: int, form_data: dict) -> bool:
    """
    Save the form data
    Args:
        page_id: id of the page layout
        form_data: user form data

    Returns: bool: acknowledgement

    """
    engine = start_engine()
    if not engine:
        return False

    with Session(engine) as session:
        try:
            proj_dtl_id = (
                select(ProjectDetails.DetailID)
                .distinct() # to avoid multiple returns # HIGHLY unlikely
                .where(
                    and_(ProjectDetails.PageID == page_id, ProjectDetails.IsActive == 1)
                )
                .scalar_subquery()
            )

            new_page_data = PageData()
            new_page_data.Data = form_data
            new_page_data.ProjDetailID = proj_dtl_id
            session.add(new_page_data)

            session.commit()
            return True
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False

def create_user(first_name: str, last_name: str, email: str, password: str):
    """
    Insert new user (after sign-up) and start tracking their prompt usage
    Args:
        first_name:
        last_name:
        email:
        password:

    Returns:
        bool: acknowledgement
    """
    engine = start_engine()
    if not engine:
        return False

    with Session(engine) as session:
        try:
            new_user = UserMaster()
            new_user.FirstName = first_name
            new_user.LastName = last_name
            new_user.Email = email
            new_user.Password = password
            session.add(new_user)

            session.flush()

            new_usage = Usage()
            new_usage.UserID = new_user.UserID
            session.add(new_usage)

            session.commit()
            return True
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False

def pre_infer_processing(user_id: int, prompt: str):
    """
    Update the request usage and enter prompt
    Args:
        user_id: user id
        prompt: user prompt

    Returns: bool: Acknowledgement

    """
    engine = start_engine()
    if not engine:
        return False

    with Session(engine) as session:
        try:
            usage_lst = session.query(Usage).filter(and_(Usage.UserID == user_id, Usage.IsActive == 1)).all()
            if not usage_lst:
                return False

            usage_obj = usage_lst[0]
            usage_obj.UsageCount += 1

            session.add(usage_obj)
            session.flush()

            new_prompt = Prompt()
            new_prompt.Prompt = prompt
            new_prompt.UserID = user_id
            session.add(new_prompt)

            session.commit()
            return True
        except Exception as err:
            log_error(str(err))
            session.rollback()
            return False