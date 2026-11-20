from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import Base, engine
from app.models.task import Task
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.tasks import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="Backend API for managing personal tasks",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Task Management API is running"
    }
