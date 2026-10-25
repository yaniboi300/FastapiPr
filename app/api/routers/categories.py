from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies import get_category_service
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSсhema,
)
from app.services.category_service import CategoryNotFound, CategoryService

router = APIRouter(prefix="/categories")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service),
) -> CategorySchema:

    return category_service.create_category(payload)


@router.get("")
def get_categories(
    category_service: CategoryService = Depends(get_category_service),
) -> list[CategorySchema]:
    return category_service.get_list_categories()


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdateSсhema,
    category_service: CategoryService = Depends(get_category_service),
) -> CategorySchema:

    try:
        return category_service.update_category(category_id, payload)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service),
) -> None:

    try:
        return category_service.delete_category(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
