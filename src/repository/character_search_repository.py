from src.model.character_model import CharacterModel
from src.repository.repository_abstract import RepositoryAbstract


class CharacterSearchRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("character")

    def search(self, query: str):
        self.cursor.execute("""
            SELECT character_id, page_id, name
            FROM character
            WHERE name ILIKE %s
            ORDER BY name
            LIMIT 10
        """, (f"%{query}%",))

        results = self.cursor.fetchall()

        return [CharacterModel.model_validate(i) for i in results]