from app.database.connection import SessionLocal
from app.models.task import Task

db = SessionLocal()

tasks = db.query(Task).all()

for task in tasks:
    print(
        "ID:", task.id,
        "Title:", task.title,
        "User ID:", task.user_id
    )

db.close()