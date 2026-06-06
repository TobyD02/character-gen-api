from fastapi import FastAPI

from src.controller.index_controller import IndexController
from src.model.death_battle_fandom_query_response_model import DeathBattleFandomQueryResponseModel


def register_routes(app: FastAPI):
    @app.get("/{character_name}")
    async def get_search(character_name: str):
        return IndexController().get_search(character_name)

    @app.get("/character/{page_id}")
    async def post_character(page_id: int):
        return IndexController().post_character(page_id)