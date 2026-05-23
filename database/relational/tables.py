from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class BaseClass(DeclarativeBase):
    pass

class UserMaster(BaseClass):
    __tablename__  = "UserMaster"

    UserID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    FirstName: Mapped[str]
    LastName: Mapped[str]
    Email: Mapped[str]
    Password: Mapped[str]
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1) 

class ProjectMaster(BaseClass):
    __tablename__  = "ProjectMaster"

    ProjectID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    ManagerID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    Name: Mapped[str]
    Description: Mapped[str]
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class ProjectDetails(BaseClass):
    __tablename__ = "ProjectDetails"

    DetailID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    ProjectID: Mapped[int] = mapped_column(ForeignKey("ProjectMaster.ProjectID"))
    PageID: Mapped[int] = mapped_column(ForeignKey("PageLayout.PageID"))
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class ProjectUsers(BaseClass):
    __tablename__ = "ProjectUsers"

    ProjUserID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    ProjectID: Mapped[int] = mapped_column(ForeignKey("ProjectMaster.ProjectID"))
    UserID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class PageLayout(BaseClass):
    __tablename__ = "PageLayout"

    PageID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    PageName: Mapped[str]
    Layout: Mapped[dict] = mapped_column(JSONB)
    # Prompt: Mapped[str]
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class PageData(BaseClass):
    __tablename__ = "PageData"

    PageDataID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    ProjDetailID: Mapped[int] = mapped_column(ForeignKey("ProjectDetails.DetailID"))
    Data: Mapped[dict] = mapped_column(JSONB)
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class Usage(BaseClass):
    __tablename__ = "Usage"

    UsageID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    UserID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    UsageCount: Mapped[int] = mapped_column(default=0)
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)

class Prompt(BaseClass):
    __tablename__ = "Prompt"

    PromptID: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    Prompt: Mapped[str]
    UserID: Mapped[int] = mapped_column(ForeignKey("UserMaster.UserID"))
    CreatedDate: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    ModifiedDate: Mapped[datetime] = mapped_column(insert_default=datetime.utcnow(), onupdate=datetime.utcnow())
    IsActive: Mapped[int] = mapped_column(default=1)
