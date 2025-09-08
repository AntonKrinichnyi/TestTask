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

@app.put(
    "/tasks/{id}",
    response_model=ResponseTaskSchema,
    status_code=status.HTTP_200_OK,
    summary="Upadte task by id"
)
def update_task(id: int, update: UpdateTaskSchema):
    if id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found")
    task = db[id]
    data = update.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(task, key, value)
    
    return task

@app.delete(
    "/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task by id"
)
def delete_task(id: int):
    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task not found")
    del db[id]
    return {"message": "Deleted successfuly"}
