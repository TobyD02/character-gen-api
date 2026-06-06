from src.model.character_model import CharacterModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character")

    def insert(self, page_id: int, name: str) -> int:
        # 2. create stub record
        self.cursor.execute("""
            INSERT INTO character (
                page_id,
                name
            )
            VALUES (%s, %s)
            RETURNING character_id
        """, (page_id, name))

        self.connection.commit()
        return self.cursor.fetchone()[0]

    def select(self, character_id: int):
        # 1. try find
        self.cursor.execute("""
            SELECT *
            FROM character
            WHERE character_id = %s
            """, (character_id,))

        row = self.cursor.fetchone()
        if row:
            return CharacterModel.model_validate(row)

