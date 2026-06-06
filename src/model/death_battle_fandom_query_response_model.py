from pydantic import BaseModel


class DeathBattleFandomQueryResponseModel(BaseModel):
    page_id: int
    name: str
    image_url: str
    categories: list[str]
