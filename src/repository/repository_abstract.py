import os
import sqlite3
from abc import ABC
from pathlib import Path


class RepositoryAbstract(ABC):
    def __init__(
        self,
        table_name: str = None,
    ):
        if table_name:
            self.table_name = table_name

        database_path = os.getenv("SQLITE_PATH")
        if not database_path:
            database_path = "./db.sqlite3"

        self.database_path = database_path
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()
