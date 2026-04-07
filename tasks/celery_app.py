from celery import Celery


celery = Celery(
    "tasks",
    broker="redis://:Try1moretime@localhost:6379/0",
    backend="redis://:Try1moretime@localhost:6379/0",  # ← обязательно
    include=["tasks.tasks"],
)
