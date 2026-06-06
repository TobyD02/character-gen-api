from pydantic import BaseModel, ConfigDict

from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.model.ollama_character_model import OllamaSpecialAbilityModel



class CharacterProfileModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int | None = None

    page_id: int

    name: str
    image_url: str

    categories: list[str]

    description: str = ""

    # Generated enrichment
    special_abilities: list[OllamaSpecialAbilityModel]
    powerscale: CharacterPowerScaleModel
    html_colour_hex: str
