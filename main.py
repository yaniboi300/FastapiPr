from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))



class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Запуск приложения")
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)


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



def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM)->TaskSchema:
    return TaskSchema(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

def category_orm_to_model(category_orm:CategoryORM) -> CategorySchema:
    return CategorySchema(id=category_orm.id, name=category_orm.name)

@app.get("/tasks")
def read_tasks(db:Session = Depends(get_db))->list[TaskSchema]:
    task = db.execute(select(TaskORM)).scalars().all()
    return [task_orm_to_model(t) for t in task]



@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload:TaskCreateSchema,db:Session = Depends(get_db))->TaskSchema:
    new_task = TaskORM( title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateSchema,db:Session = Depends(get_db))->TaskSchema:
     task_for_update = db.get(TaskORM, task_id)
     if payload.title:
         task_for_update.title = payload.title
     if payload.completed is not None:
        task_for_update.completed = payload.completed

     db.commit()

     return task_for_update

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str,db:Session = Depends(get_db))->None:
    task_for_delete = db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()



@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema,db:Session = Depends(get_db)) -> CategorySchema:
    category = CategoryORM(name=payload.name)
    db.add(category)
    db.commit()

    return category_orm_to_model(category)


@app.get("/categories")
def get_categories(db:Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.execute(select(CategoryORM)).scalars().all()
    return [category_orm_to_model(c) for c in categories]


@app.patch("/categories/{category_id}")
def update_category(
        category_id: str,
        payload: CategoryUpdateSсhema,
        db:Session = Depends(get_db)
):
    category = db.get(CategoryORM, category_id)

    if payload.name:
        category.name = payload.name

    db.commit()

    return category




@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str,db:Session = Depends(get_db)):
    category = db.get(CategoryORM, category_id)
    db.delete(category)
    db.commit()

