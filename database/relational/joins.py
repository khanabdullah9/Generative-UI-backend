from sqlalchemy import create_engine, select, outerjoin, or_, and_
from sqlalchemy.orm import Session

from database.relational.crud import DBEngine
from database.relational.tables import ProjectMaster, ProjectUsers

def start_engine():
    db_engine = DBEngine()
    return db_engine.engine

def get_all_projects(user_id):
    engine = start_engine()

    with Session(engine) as session:
        statement = (
            select(
                ProjectMaster.ProjectID,
                ProjectMaster.ManagerID,
                ProjectMaster.Name
            )
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

def get_projects(project_id, user_id):
    """
    get projects for specific user
    :param project_id:
    :param user_id:
    :return: list of projects
    """
    engine = start_engine()

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
