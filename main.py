from typing import Dict

from fastapi import FastAPI, HTTPException, status

from schemas import CreateTaskSchema, UpdateTaskSchema, ResponseTaskSchema

app = FastAPI()

id_count = 0
db: Dict[int, dict] = {}

@app.get(
    "/tasks",
    response_model=list[ResponseTaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Gives as the entire list of tasks"
)
def get_tasks():
    return list(db.values())

@app.post(
    "/tasks",
    response_model=ResponseTaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task"
)
def create_task(task: CreateTaskSchema):
    global id_count
    id_count += 1
    new_task = {"id": id_count, **task.model_dump()}
    db[id_count] = new_task
    return new_task
