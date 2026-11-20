from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.database.connection import get_db
from app.services.task_service import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    get_task_summary
)

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# CREATE TASK API
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(
        db,
        task_data,
        user_id=current_user.id
    )

# GET ALL TASKS API
@router.get("/")
def read_all_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    status_filter: str = Query(None, alias="status"),
    priority_filter: str = Query(None, alias="priority"),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_all_tasks(
        db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        status_filter=status_filter,
        priority_filter=priority_filter
    )

# GET TASK SUMMARY API
@router.get("/summary")
def task_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_task_summary(
        db,
        user_id=current_user.id
    )

# GET SINGLE TASK API
@router.get("/{task_id}")
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(
        db,
        task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task

# UPDATE TASK API
@router.patch("/{task_id}", response_model=TaskResponse)
def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(
        db,
        task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    try:
        return update_task(db, task, task_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# DELETE TASK API
@router.delete("/{task_id}")
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_by_id(
        db,
        task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    delete_task(db, task)
    return {"message": "Task deleted successfully"}
