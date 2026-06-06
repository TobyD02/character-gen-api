from src.model.character_profile_model import CharacterProfileModel
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


class IndexController:
    def __init__(self):
        self.character_service = CharacterService(
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

    def post_character(self, character_id: int) -> CharacterProfileModel|None:
        # model = self.character_service.search_death_battle_fandom_with_page_id(page_id)
        return self.character_service.generate_new_character(character_id)
