from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

class CategorySchema(BaseModel):
    id: str
    name:str

class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSсhema(BaseModel):
    name: str | None = None

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreateSchema(BaseModel):
    title:str

class TaskUpdateSchema(BaseModel):
    title:str | None = None
    completed:bool | None = None

tasks: list[TaskSchema] = []




@app.get("/tasks")
def read_tasks()->list[TaskSchema]:
    return tasks

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreateSchema)->TaskSchema:

    new_task = TaskSchema(id=str(uuid4()), title=payload.title, completed=False)

    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed

            return tasks


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


categories: list[CategorySchema] = []


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(category)
    return category


@app.get("/categories")
def get_categories() -> list[CategorySchema]:
    return categories


@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryUpdateSсhema):
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category

    raise HTTPException(status_code=404, detail="Category not found")


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return  

    raise HTTPException(status_code=404, detail="Category not found")
