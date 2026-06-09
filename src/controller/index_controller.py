from src.process.build_character_special_ability_from_generated_process import \
    BuildCharacterSpecialAbilityFromGeneratedProcess
from src.process.extract_domainant_colour_from_image_url_process import ExtractDominantColourFromImageUrlProcess
from src.repository.character_special_ability_repository import CharacterSpecialAbilityRepository
from src.model.character_response_model import CharacterResponseModel
from src.model.death_battle_fandom_query_response_model import DeathBattleFandomQueryResponseModel
from src.process.create_character_for_db_insert_process import CreateCharacterForDbInsertProcess
from src.process.extract_powerscaling_from_death_battle_query_response_process import \
    ExtractPowerscalingFromDeathBattleQueryResponseProcess
from src.process.fetch_and_parse_death_battle_fandom_wiki_page_content_process import \
    FetchAndParseDeathBattleFandomWikiPageContentProcess
from src.process.ollama_generate_character_process import OllamaGenerateCharacterProcess
from src.process.search_death_battle_fandom_wiki_process import SearchDeathBattleFandomWikiProcess
from src.repository.character_category_repository import CharacterCategoryRepository
from src.repository.character_profile_repository import CharacterProfileRepository
from src.repository.character_search_repository import CharacterSearchRepository
from src.repository.full_character_model_repository import FullCharacterModelRepository
from src.repository.powerscale_repository import PowerScaleRepository
from src.service.character_service import CharacterService
from src.repository.character_repository import CharacterRepository

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")


class IndexController:
    def __init__(self):
        self.character_service = CharacterService(
            ExtractDominantColourFromImageUrlProcess(),
            BuildCharacterSpecialAbilityFromGeneratedProcess(),
            CharacterSpecialAbilityRepository(),
            CharacterRepository(),
            CharacterSearchRepository(),
            FullCharacterModelRepository(),
            CharacterProfileRepository(),
            CharacterCategoryRepository(),
            PowerScaleRepository(),
            OllamaGenerateCharacterProcess(),
            CreateCharacterForDbInsertProcess(),
            SearchDeathBattleFandomWikiProcess(),
            FetchAndParseDeathBattleFandomWikiPageContentProcess(),
            ExtractPowerscalingFromDeathBattleQueryResponseProcess(),
        )

    def get_search(self, character_name: str) -> list[DeathBattleFandomQueryResponseModel] | None:

        if character_name == '':
            return None

        return self.character_service.search_death_battle_fandom(character_name)

    def post_character(self, character_id: int) -> CharacterResponseModel:
        # model = self.character_service.search_death_battle_fandom_with_page_id(page_id)
        return self.character_service.get_or_generate_character(character_id)

    def get_random_characters(self):
        return self.character_service.get_random_generated(50)

    def get_all_characters(self):
        return self.character_service.get_all_characters()

    def get_by_category(self, category_id: int):
        return self.character_service.get_by_category(category_id)

    def search_by_category(self, query: str):
        return self.character_service.search_by_category(query)

    def render_characters(self, request: Request):
        characters = self.character_service.get_all_characters()
        return templates.TemplateResponse(
            request=request, name="cards.html.j2", context={ "characters": [{
                "character": i.character,
                "character_profile": i.character_profile,
                "special_abilities": i.special_abilities,
                "categories": i.categories,
                "powerscale": i.powerscale,
            } for i in characters]}
        )

    def render_character(self, request: Request, character_id: int):
        character = self.character_service.get_or_generate_character(character_id)
        return templates.TemplateResponse(
            request=request, name="card.html.j2", context={
                "character": character.character,
                "character_profile": character.character_profile,
                "special_abilities": character.special_abilities,
                "categories": character.categories,
                "powerscale": character.powerscale,
            }
        )

