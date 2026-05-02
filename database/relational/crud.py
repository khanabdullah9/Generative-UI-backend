from sqlalchemy import create_engine, select
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
        server_name = db_config["server_name"]
        port = db_config["port"]
        db_name = db_config["database_name"]
        conn_str = f"{dialect}+{driver}://{username}:{safe_password}@{server_name}:{port}/{db_name}"

        self.engine = create_engine(conn_str)

    def test_connection(self):
        pass

class UserMasterCrud(DBEngine):
    def __init__(self):
        super().__init__()

    def create(self, first_name, last_name, email):
        try:
            with Session(self.engine) as session:
                new_user = UserMaster()
                new_user.FirstName = first_name
                new_user.LastName = last_name
                new_user.Email = email
                
                session.add(new_user)
                session.commit()
            return True
        except Exception as err:
            session.rollback()
            log_error(str(err))
            return False

    def read(self, id = 0):
        statement = select(UserMaster)
        if id > 0:
            statement = select(UserMaster).where(UserMaster.UserID == id)
        
        try:
            with Session(self.engine) as session:
                return session.execute(statement).scalars().all()
        except Exception as err:
            log_error(str(err))
            return False

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
                        if is_active:
                            user.IsActive = is_active
                        session.commit()
                        return True
            except Exception as err:
                log_error(str(err))
                return False
            return False

    def delete(self, id):
        self.update(id = id, is_active = 0) # simply set the user inactive