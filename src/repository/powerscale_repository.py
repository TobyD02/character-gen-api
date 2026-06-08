import os

from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.repository.repository_abstract import RepositoryAbstract


class PowerScaleRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("powerscale")

    def get_by_label(self, label: str):
        self.cursor.execute(
            "SELECT * FROM powerscale WHERE label = %s",
            (label,)
        )
        result = self.cursor.fetchone()

        print(result, flush=True)

        if not result:
            return None

        return CharacterPowerScaleModel.model_validate(result)

    def insert(self, tier: float, label: str, name: str) -> int:
        self.cursor.execute("""
            INSERT INTO powerscale (tier, label, name)
            VALUES (%s, %s, %s)
            RETURNING powerscale_id
        """, (tier, label, name))

        self.connection.commit()

        return self.cursor.fetchone()["powerscale_id"]
