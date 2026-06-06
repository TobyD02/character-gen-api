from pydantic import BaseModel


class CharacterModel(BaseModel):
    character_id: int
    name: str
    page_id: int