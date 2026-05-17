from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, project, inference

app = FastAPI()
app.include_router(users.router)
app.include_router(project.router)
app.include_router(inference.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def root():
    return "Server is running!"