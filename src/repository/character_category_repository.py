import os

from src.repository.repository_abstract import RepositoryAbstract


class CharacterCategoryRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_category")

    def insert_many(self, character_id: int, categories: list[str]):
        self.cursor.executemany("""
            INSERT OR IGNORE INTO character_category (character_id, category)
            VALUES (?, ?)
        """, [(character_id, c) for c in categories])

        self.connection.commit()