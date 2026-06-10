from src.model.category_model import CategoryModel
from src.repository.category_repository import CategoryRepository


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
    ):
        self.category_repository: CategoryRepository = category_repository

    def get_all_categories(self) -> list[CategoryModel]:
        return self.category_repository.select_all()