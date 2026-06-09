from fastapi import FastAPI, Request

from src.controller.index_controller import IndexController
from src.model.death_battle_fandom_query_response_model import DeathBattleFandomQueryResponseModel


def register_routes(app: FastAPI):
    @app.get("/api/search/{character_name}")
    async def get_search(character_name: str):
        return IndexController().get_search(character_name)

    @app.get("/api/character/{character_id}")
    async def post_character(character_id: int):
        return IndexController().post_character(character_id)

    @app.get("/character/{character_id}")
    async def get_character(request: Request, character_id: int):
        return IndexController().render_character(request, character_id)

    @app.get("/characters")
    async def get_character(request: Request):
        return IndexController().render_characters(request)
