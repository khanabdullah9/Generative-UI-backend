from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime

class BaseClass(DeclarativeBase):
    pass

class UserMaster(BaseClass):
    __tablename__  = "UserMaster"

    UserID: Mapped[int] = mapped_column(primary_key=True)
    FirstName: Mapped[str]
    LastName: Mapped[str]
    Email: Mapped[str]
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1) 

class ProjectMaster(BaseClass):
    __tablename__  = "ProjectMaster"

    ProjectID: Mapped[int] = mapped_column(primary_key=True)
    ManagerID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    Name: Mapped[str]
    Description: Mapped[str]
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class ProjectDetails(BaseClass):
    __tablename__ = "ProjectDetails"

    DetailID: Mapped[int] = mapped_column(primary_key=True)
    ProjectID: Mapped[int] = mapped_column(ForeignKey("ProjectMaster.ProjectID"))
    PageID: Mapped[int] # PageID will come from NoSQL database
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class ProjectUsers(BaseClass):
    __tablename__ = "ProjectUsers"

    ProjUserID: Mapped[int] = mapped_column(primary_key=True)
    ProjectID: Mapped[int] = mapped_column(ForeignKey("ProjectMaster.ProjectID"))
    UserID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)