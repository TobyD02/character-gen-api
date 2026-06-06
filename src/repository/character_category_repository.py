import os

from src.repository.repository_abstract import RepositoryAbstract


class CharacterCategoryRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character_category")

    def insert_many(self, character_id: int, categories: list[str]):
        category_map = self._ensure_categories_exist(categories)

        print(category_map)

        self.cursor.executemany(
            """
            INSERT INTO character_category (character_id, category_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """, [
                (character_id, category_map[c])
                for c in categories
            ])

        self.connection.commit()

    def _ensure_categories_exist(self, categories: list[str]) -> dict[str, int]:
        self.cursor.executemany(
            """
            INSERT INTO category (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
            """, [(c,) for c in categories])

        self.connection.commit()

        self.cursor.execute(
            """
            SELECT category_id, name
            FROM category
            WHERE name = ANY (%s)
            """, (categories,))

        rows = self.cursor.fetchall()

        return {row["name"]: row["category_id"] for row in rows}
