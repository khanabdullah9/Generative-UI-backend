from sqlalchemy import create_engine, select, outerjoin, join, or_, and_
from sqlalchemy.orm import Session

from database.relational.crud import DBEngine
from database.relational.tables import ProjectMaster, ProjectUsers, ProjectDetails, PageLayout
from utils import log_error


def start_engine():
    try:
        db_engine = DBEngine()
        return db_engine.engine
    except Exception as err:
        log_error(str(err))

def get_all_projects(user_id):
    engine = start_engine()
    if not engine:
        return []

    try:
        with Session(engine) as session:
            statement = (
                select(
                    ProjectMaster.ProjectID,
                    ProjectMaster.ManagerID,
                    ProjectMaster.Name
                )
                .distinct()
                .outerjoin(ProjectUsers)
                .where(
                    or_(ProjectMaster.ManagerID == user_id, ProjectUsers.UserID == user_id),
                    and_(ProjectMaster.IsActive == 1, ProjectUsers.IsActive == 1)
                )
            )
            results = session.execute(statement)
            if results:
                return results.fetchall()
        return []
    except Exception as err:
        log_error(str(err))
        return []

def get_projects(project_id, user_id):
    """
    get projects for specific user
    :param project_id:
    :param user_id:
    :return: list of projects
    """
    engine = start_engine()
    if not engine:
        return []

    try:
        with Session(engine) as session:
            statement = (
                select(
                    ProjectMaster.ProjectID,
                    ProjectMaster.ManagerID,
                    ProjectMaster.Name
                ).outerjoin(ProjectUsers)
                .where(
                    ProjectMaster.ProjectID == project_id,
                    or_(ProjectUsers.UserID == user_id, ProjectMaster.ManagerID == user_id),
                    and_(ProjectMaster.IsActive == 1, ProjectUsers.IsActive == 1)
                )
            )
            results = session.execute(statement)
            if results:
                return results.fetchall()
        return []
    except Exception as err:
        log_error(str(err))
        return []

def get_project_pages(project_id: int = 0):
    engine = start_engine()
    if not engine:
        return []

    try:
        with Session(engine) as session:
            statement = (
                select(
                    PageLayout.PageID,
                    PageLayout.PageName
                )
                .join(ProjectDetails, ProjectDetails.PageID == PageLayout.PageID)
                .where(
                    and_(
                        ProjectDetails.ProjectID == project_id,
                        ProjectDetails.IsActive == 1,
                        PageLayout.IsActive == 1
                    )
                )
            )
            result = session.execute(statement)
            if result:
                return result.fetchall()
            return []
    except Exception as err:
        log_error(str(err))
        return []