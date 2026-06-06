import os

from src.repository.repository_abstract import RepositoryAbstract


class PowerScaleRepository(RepositoryAbstract):
    def __init__(self):
        super().__init__("powerscale")

    def get_by_label(self, label: str):
        self.cursor.execute(
            "SELECT * FROM powerscale WHERE label = ?",
            (label,)
        )
        return self.cursor.fetchone()

    def insert(self, tier: float, label: str, name: str):
        self.cursor.execute("""
            INSERT OR IGNORE INTO powerscale (tier, label, name)
            VALUES (?, ?, ?)
        """, (tier, label, name))

        self.connection.commit()