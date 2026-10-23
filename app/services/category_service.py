from sqlalchemy.orm import Session

from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSсhema

class CategoryNotFound(Exception):
    pass


class CategoryService:
    def __init__(self, db:Session):
        self.db = db
        self.category_repository = CategoryRepository(db=db)


    def get_list_categories(self)->list[CategorySchema]:
        category_orm = self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in category_orm]

    def create_category(self,payload:CategoryCreateSchema )-> CategorySchema:
        category = self.category_repository.create(payload.name)
        self.db.commit()
        return CategorySchema.model_validate(category)

    def update_category(self,category_id:str, payload: CategoryUpdateSсhema)->CategorySchema:
        category_for_update = self.category_repository.get_by_id(category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        if payload.name:
            category_for_update.name = payload.name

        self.db.commit()

        return CategorySchema.model_validate(category_for_update)

    def delete_category(self,category_id:str)->None:
        category_for_delete = self.category_repository.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")

        self.category_repository.delete(category_for_delete)
        self.db.commit()
