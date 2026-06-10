from src.repository.repository_abstract import RepositoryAbstract
from src.model.category_model import CategoryModel


class CategoryRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__()

    def select_all(self) -> list[CategoryModel]:
        self.cursor.execute(
            """
            SELECT category_id, name
            FROM category
            """)

        return [CategoryModel(name=i["name"], category_id=i["category_id"]) for i in self.cursor.fetchall()]
