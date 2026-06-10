from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from src.controller.index_controller import IndexController

def register_routes(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/api/search/{character_name}")
    async def get_search(character_name: str):
        return IndexController().get_search(character_name)

    @app.get("/api/character/{character_id}")
    async def post_character(character_id: int):
        return IndexController().post_character(character_id)

    @app.get("/api/characters/random")
    async def post_character():
        return IndexController().get_random_characters()

    @app.get("/api/characters/all")
    async def post_character():
        return IndexController().get_all_characters()

    @app.get("/api/characters/category/{category_id}")
    async def post_character(category_id: int):
        return IndexController().get_by_category(category_id)

    @app.get("/api/search/category/{query}")
    async def post_character(query: str):
        return IndexController().search_by_category(query)

    @app.get("/character/{character_id}")
    async def get_character(request: Request, character_id: int):
        return IndexController().render_character(request, character_id)

    @app.get("/characters")
    async def get_character(request: Request):
        return IndexController().render_characters(request)

    @app.get("/characters/roster")
    async def get_character(request: Request):
        return IndexController().render_character_roster(request)

    @app.get("/api/categories")
    async def get_categories():
        return IndexController().get_all_categories()