from pydantic import BaseModel, ConfigDict

from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.model.ollama_character_model import OllamaSpecialAbilityModel



class CharacterProfileModel(BaseModel):
    character_profile_id: int | None = None
    character_id: int
    image_url: str
    description: str = ""
    powerscale_id: int|None

    colour_primary: str|None
    colour_secondary: str|None
    colour_tertiary: str|None

