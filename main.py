from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, project, inference
from utils import get_database_config

app = FastAPI()
app.include_router(users.router)
app.include_router(project.router)
app.include_router(inference.router)

config = get_database_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173"] if config["env"] == "PRD" else ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def root():
    return "Server is running!"