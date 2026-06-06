from fastapi import FastAPI

from src.routes import register_routes
from util.init_sqlite_db import init_db

app = FastAPI()

# init_db() # only needed for sqlite
register_routes(app)