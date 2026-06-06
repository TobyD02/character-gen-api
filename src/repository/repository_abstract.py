import os
from abc import ABC

import psycopg2
from psycopg2.extras import RealDictCursor


class RepositoryAbstract(ABC):
    def __init__(
        self,
        table_name: str = None,
    ):
        if table_name:
            self.table_name = table_name

        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL is not set")

        self.connection = psycopg2.connect(
            database_url,
        )

        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def close(self) -> None:
        self.connection.close()
