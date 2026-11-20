from sqlalchemy.orm import Session
from sqlalchemy import case
from app.models.task import Task
from datetime import datetime, timezone

def create_task(db: Session, task_data, user_id: int):

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# GET ALL TASKS

# GET ALL USERS' TASKS
def get_all_tasks(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 5,
    status_filter: str = None,
    priority_filter: str = None
):

    # Fetch tasks from ALL users
    query = db.query(Task)

    # Status Filter
    if status_filter:
        query = query.filter(
            Task.status == status_filter
        )

    # Priority Filter
    if priority_filter:
        query = query.filter(
            Task.priority == priority_filter
        )

    total_tasks = query.count()

    skip = (page - 1) * limit

    priority_order = case(
        (Task.priority == "high", 1),
        (Task.priority == "medium", 2),
        (Task.priority == "low", 3),
        else_=4
    )

    tasks = query.order_by(
        priority_order,
        Task.id.desc()
    ).offset(skip).limit(limit).all()

    total_pages = (total_tasks + limit - 1) // limit

    return {
        "total_tasks": total_tasks,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "tasks": tasks
    }
 
# GET SINGLE TASK
def get_task_by_id(db: Session, task_id: int, user_id: int):

    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

# UPDATE TASK
def update_task(db: Session, task, task_data):

    update_data = task_data.model_dump(exclude_unset=True)

    if "status" in update_data:

        new_status = update_data["status"]
        current_status = task.status

        allowed_transitions = {
            "pending": ["in_progress"],
            "in_progress": ["completed"],
            "completed": []
        }

        if new_status is None:
            raise ValueError("Status cannot be null")
        if new_status != current_status:
            if new_status not in allowed_transitions[current_status]:
                raise ValueError(
                    f"Invalid status transition: {current_status} to {new_status}"
                )
        if new_status == "completed":
            task.completed_at = datetime.now(timezone.utc)
    for key, value in update_data.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

# DELETE TASK
def delete_task(db: Session, task):
    db.delete(task)
    db.commit()
    return True

# GET TASK SUMMARY
def get_task_summary(db: Session, user_id: int):
    total_tasks = db.query(Task).filter(
        Task.user_id == user_id
    ).count()
    pending_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status == "pending"
    ).count()
    completed_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status == "completed"
    ).count()
    in_progress_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status == "in_progress"
    ).count()

    return {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks
    }
