from src.model.character_power_scale_model import character_power_scale_data, CharacterPowerScaleModel
from src.model.death_battle_fandom_query_response_model import DeathBattleFandomQueryResponseModel
from src.process.process_abstract import ProcessAbstract

class ExtractPowerscalingFromDeathBattleQueryResponseProcess(ProcessAbstract):
    def __init__(self):
        pass

    def execute(self, model: DeathBattleFandomQueryResponseModel) -> CharacterPowerScaleModel:

        # Build lookup once if you do this frequently
        powerscale_lookup = {
            p["label"]: p
            for p in character_power_scale_data
        }

        matches = []

        for category in model.categories:
            power = powerscale_lookup.get(category)

            if power:
                matches.append(power)

        power_scale = max(matches, key=lambda p: float(p["tier"]))
        return CharacterPowerScaleModel(
            tier=power_scale["tier"],
            label=power_scale["label"],
            name=power_scale["name"],
        )
