from pydantic import BaseModel, ConfigDict


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSсhema(BaseModel):
    name: str | None = None
