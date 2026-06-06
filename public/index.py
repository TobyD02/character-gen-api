from fastapi import FastAPI

from src.routes import register_routes
from util.init_sqlite_db import init_db

app = FastAPI()

init_db()
register_routes(app)