from sqlalchemy import create_engine, select, and_
from sqlalchemy.orm import Session
import urllib.parse
from utils import get_database_config, log_error, log_info
from database.relational.tables import *

class DBEngine():
    def __init__(self):
        db_config = get_database_config()
        if not db_config:
            return
        
        safe_password = urllib.parse.quote_plus(db_config["password"])
        dialect = db_config["dialect"]
        driver = db_config["driver"]
        username = db_config["username"]
        server_name = "db" if db_config["env"] == "PRD" else "localhost"
        port = db_config["port"]
        db_name = db_config["database_name"]
        conn_str = f"{dialect}+{driver}://{username}:{safe_password}@{server_name}:{port}/{db_name}"

        self.engine = create_engine(conn_str)

    def test_connection(self):
        pass

class UserMasterCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, first_name, last_name, email, password):
        try:
            with Session(self.engine) as session:
                new_user = UserMaster()
                new_user.FirstName = first_name
                new_user.LastName = last_name
                new_user.Email = email
                new_user.Password = password
                
                session.add(new_user)
                session.commit()
            return True
        except Exception as err:
            session.rollback()
            log_error(str(err))
            return False

    def read(self, user_id:int = 0,  email: str = "", password: str = ""):
        statement = select(UserMaster.UserID, UserMaster.FirstName, UserMaster.LastName)
        if user_id > 0:
            statement = statement.where(
                and_(UserMaster.UserID == user_id, UserMaster.IsActive == 1)
            )
        if email and password:
            statement = statement.where(
                and_(UserMaster.Email == email, UserMaster.Password == password, UserMaster.IsActive == 1)
            )
        if email and not password:
            statement = statement.where(UserMaster.Email == email)

        try:
            with Session(self.engine) as session:
                result = session.execute(statement)
                return result.mappings().all()
        except Exception as err:
            log_error(str(err))

        return []
    
    def update(self, id: int = None, first_name = "", last_name = "", email = "", is_active = 1):
            try:
                with Session(self.engine) as session:
                    user = session.get(UserMaster, id)
                    if user:
                        if first_name:
                            user.FirstName = first_name
                        if last_name:
                            user.LastName = last_name
                        if email:
                            user.Email = email
                        if is_active == 0:
                            user.IsActive = 0
                        session.commit()
                        return True
            except Exception as err:
                log_error(str(err))
                return False
            return False

    def delete(self, id):
        return self.update(id = id, is_active = 0) # simply set the user inactive

class ProjectMasterCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, manager_id, name, description):
        try:
            with Session(self.engine) as session:
                new_project = ProjectMaster()
                new_project.ManagerID = manager_id
                new_project.Name = name
                new_project.Description = description
                session.add(new_project)
                session.commit()
                return True, new_project.ProjectID
        except Exception as err:
            log_error(str(err))
            return False,0

    def read(self, project_id = 0):
        statement = select(ProjectMaster)
        if project_id > 0:
            statement = select(ProjectMaster).where(
                and_(ProjectMaster.ProjectID == project_id, ProjectMaster.IsActive == 1)
            )

        try:
            with Session(self.engine) as session:
                return session.execute(statement).mappings().all()
        except Exception as err:
            log_error(str(err))
            return []

    def update(self, project_id: int, manager_id: int = 0, name: str = "", description: str = "", is_active: int = 1):
        try:
            with Session(self.engine) as session:
                project = session.get(ProjectMaster, project_id)
                if not project:
                    return False

                if manager_id:
                    project.ManagerID = manager_id
                if name:
                    project.Name = name
                if description:
                    project.Description = description
                if is_active == 0:
                    project.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, project_id):
        return self.update(project_id = project_id, is_active = 0)

class ProjectUserCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, project_id, user_id):
        try:
            with Session(self.engine) as session:
                new_project_user = ProjectUsers()
                new_project_user.ProjectID = project_id
                new_project_user.UserID = user_id
                session.add(new_project_user)
                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def read(self, project_user_id:int):
        statement = select(ProjectUsers)
        if project_user_id > 0:
            statement = select(ProjectUsers).where(
                and_(ProjectUsers.ProjUserID == project_user_id, ProjectUsers.IsActive == 1)
            )

        try:
            with Session(self.engine) as session:
                return session.execute(statement).scalars().all()
        except Exception as err:
            log_error(str(err))
        return []

    def update(self, project_user_id:int, project_id: int = None, user_id: int = None, is_active: int = 1):
        try:
            with Session(self.engine) as session:
                project_user = session.get(ProjectUsers, project_user_id)
                if not project_user:
                    print(f"Could not find user for id={project_user_id}")
                    return False

                if project_id:
                    project_user.ProjectID = project_id
                if user_id:
                    project_user.UserID = user_id
                if is_active == 0:
                    project_user.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, project_user_id:int):
        return self.update(project_user_id = project_user_id, is_active = 0)

class ProjectDetailsCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, project_id: int, page_id: int):
        try:
            with Session(self.engine) as session:
                new_project = ProjectDetails()
                new_project.ProjectID = project_id
                new_project.PageID = page_id
                session.add(new_project)
                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def read(self, detail_id:int = 0, project_id: int = 0):
        statement = select(ProjectDetails)
        if detail_id > 0:
            statement = select(ProjectDetails).where(
                and_(ProjectDetails.DetailID == detail_id, ProjectDetails.IsActive == 1)
            )
        if project_id > 0:
            statement = select(ProjectDetails).where(
                and_(ProjectDetails.ProjectID == project_id, ProjectDetails.IsActive == 1)
            )

        try:
            with Session(self.engine) as session:
                return session.execute(statement).mappings().all()
        except Exception as err:
            log_error(str(err))
        return []

    def update(self, detail_id: int, project_id: int = None, page_id: int = None, is_active: int = 1):
        try:
            with Session(self.engine) as session:
                project_details = session.get(ProjectDetails, detail_id)
                if not project_details:
                    return False

                if project_id:
                    project_details.ProjectID = project_id
                if page_id:
                    project_details.PageID = page_id
                if is_active == 0:
                    project_details.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, detail_id: int):
        return self.update(detail_id = detail_id, is_active = 0)

class PageLayoutCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, page_name: str, layout: dict):
        try:
            with Session(self.engine) as session:
                new_page_layout = PageLayout()
                new_page_layout.PageName = page_name
                new_page_layout.Layout = layout

                session.add(new_page_layout)
                session.commit()
                return True, new_page_layout.PageID
        except Exception as err:
            log_error(str(err))
            return False, 0

    def read(self, page_id:int = 0):
        statement = select(PageLayout.Layout)
        if page_id > 0:
            statement = select(PageLayout.Layout).where(
                and_(PageLayout.PageID == page_id, PageLayout.IsActive == 1)
            )
        with Session(self.engine) as session:
            return session.execute(statement).mappings().all()

    def update(self, page_id: int, page_name: str = "", layout: dict = None, is_active: int = 1):
        try:
            with Session(self.engine) as session:
                page_layout = session.get(PageLayout, page_id)
                if not page_layout:
                    return False

                if page_name:
                    page_layout.PageName = page_name
                if layout:
                    page_layout.Layout = layout
                if is_active == 0:
                    page_layout.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, page_id: int):
        return self.update(page_id = page_id, is_active = 0)

class PageDataCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, proj_detail_id: int, page_data: dict):
        try:
            with Session(self.engine) as session:
                new_page_data = PageData()
                new_page_data.ProjDetailID = proj_detail_id
                new_page_data.Data = page_data
                session.add(new_page_data)
                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def read(self, page_data_id: int = 0):
        statement = select(PageData)
        if page_data_id > 0:
            statement = select(PageData).where(
                and_(PageData.PageDataID == page_data_id, PageData.IsActive == 1)
            )
        with Session(self.engine) as session:
            return session.execute(statement).scalars().all()

    def read_for_report(self, page_id: int):
        try:
            proj_dtl_id = (
                select(ProjectDetails.DetailID)
                .distinct()
                .where(
                    and_(ProjectDetails.PageID == page_id, ProjectDetails.IsActive == 1)
                )
                .scalar_subquery()
            )
            statement = select(PageData.Data).where(
                and_(PageData.ProjDetailID == proj_dtl_id, PageData.IsActive == 1)
            )
            with Session(self.engine) as session:
                return session.execute(statement).mappings().all()
        except Exception as err:
            log_error(str(err))
            return []

    def update(self, page_data_id: int, page_data: dict, is_active: int = 1):
        try:
            with Session(self.engine) as session:
                page_data_obj = session.get(PageData, page_data_id)
                if not page_data_obj:
                    return False

                if page_data:
                    page_data_obj.Data = page_data
                if is_active == 0:
                    page_data_obj.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, page_data_id: int):
        return self.update(page_data_id = page_data_id, page_data = {}, is_active = 0)

class UsageCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, user_id: int):
        try:
            with Session(self.engine) as session:
                new_usage = Usage()
                new_usage.UserID = user_id

                session.add(new_usage)
                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def read(self, user_id: int):
        statement = select(Usage.UsageCount).where(
            and_(Usage.UserID == user_id, Usage.IsActive == 1)
        )
        with Session(self.engine) as session:
            return session.execute(statement).mappings().all()

    def update(self, user_id:int, is_active: int = 1):
        try:
            with Session(self.engine) as session:
                # usage_obj = session.get(Usage, user_id)
                usage_lst = session.query(Usage).filter(and_(Usage.UserID == user_id, Usage.IsActive == 1)).all()
                if not usage_lst:
                    return False

                usage_obj = usage_lst[0]

                usage_obj.UsageCount += 1

                if is_active == 0:
                    usage_obj.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, user_id: int):
        return self.update(user_id = user_id, is_active = 0)

class PromptCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, user_id: int, prompt: str):
        try:
            with Session(self.engine) as session:
                new_prompt = Prompt
                new_prompt.Prompt = prompt
                new_prompt.UserID = user_id

                session.add(new_prompt)
                session.commit()

                return True
        except Exception as err:
            log_error(str(err))
            return False

    def read(self, user_id: int):
        statement = select(Prompt.Prompt).where(
            and_(Prompt.UserID == user_id, Prompt.IsActive == 1)
        )
        with Session(self.engine) as session:
            return session.execute(statement).mappings().all()

    def update(self, user_id:int, prompt: str = "", is_active: int = 1):
        try:
            with Session(self.engine) as session:
                prompt_obj = session.get(Prompt, user_id)
                if not prompt_obj:
                    return False

                prompt_obj.Prompt = prompt

                if is_active == 0:
                    prompt_obj.IsActive = 0

                session.commit()
                return True
        except Exception as err:
            log_error(str(err))
            return False

    def delete(self, user_id: int):
        return self.update(user_id = user_id, is_active = 0)
