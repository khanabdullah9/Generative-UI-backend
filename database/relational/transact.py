from sqlalchemy import create_engine, select, outerjoin, join, or_, and_
from sqlalchemy.orm import Session

from database.relational.crud import DBEngine
from database.relational.tables import ProjectDetails, PageLayout
from utils import log_error

def start_engine():
    try:
        db_engine = DBEngine()
        return db_engine.engine
    except Exception as err:
        log_error(str(err))

def approve_page(page_name: str, layout: dict, project_id: int):
    engine = start_engine()
    if not engine:
        return []

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
            session.rollback()
            return False
