from pydantic import BaseModel


class CategoryModel(BaseModel):
    name: str
    category_id: int