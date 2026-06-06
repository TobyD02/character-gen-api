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
from src.repository.full_character_model_repository import FullCharacterModelRepository
from src.repository.powerscale_repository import PowerScaleRepository
from src.service.service_abstract import ServiceAbstract
from src.repository.character_search_repository import CharacterSearchRepository
from src.repository.character_repository import CharacterRepository

class CharacterService(ServiceAbstract):
    def __init__(
        self,
        character_repository: CharacterRepository,
        character_search_repository: CharacterSearchRepository,
        full_character_model_repository: FullCharacterModelRepository,
        character_profile_repository: CharacterProfileRepository,
        character_category_repository: CharacterCategoryRepository,
        powerscale_repository: PowerScaleRepository,
        ollama_generate_character_process: OllamaGenerateCharacterProcess,
        create_character_for_db_insert_process: CreateCharacterForDbInsertProcess,
        search_death_battle_fandom_wiki_process: SearchDeathBattleFandomWikiProcess,
        fetch_and_parse_search_death_battle_fandom_wiki_process: FetchAndParseDeathBattleFandomWikiPageContentProcess,
        extract_powerscaling_from_death_battle_query_response_process: ExtractPowerscalingFromDeathBattleQueryResponseProcess,
    ):
        self.character_repository: CharacterRepository = character_repository
        self.character_search_repository: CharacterSearchRepository = character_search_repository
        self.full_character_model_repository: FullCharacterModelRepository = full_character_model_repository
        self.character_profile_repository: CharacterProfileRepository = character_profile_repository
        self.character_category_repository: CharacterCategoryRepository = character_category_repository
        self.powerscale_repository: PowerScaleRepository = powerscale_repository
        self.ollama_generate_character_process: OllamaGenerateCharacterProcess = ollama_generate_character_process
        self.create_character_for_db_insert_process: CreateCharacterForDbInsertProcess = create_character_for_db_insert_process
        self.search_death_battle_fandom_wiki_process: SearchDeathBattleFandomWikiProcess = search_death_battle_fandom_wiki_process
        self.fetch_and_parse_search_death_battle_fandom_wiki_process: FetchAndParseDeathBattleFandomWikiPageContentProcess = \
            fetch_and_parse_search_death_battle_fandom_wiki_process

        self.extract_powerscaling_from_death_battle_query_response_process: ExtractPowerscalingFromDeathBattleQueryResponseProcess = \
            extract_powerscaling_from_death_battle_query_response_process

    def search_death_battle_fandom(self, character_name: str) -> list[DeathBattleFandomQueryResponseModel]:
        # try:
        #     return self.search_death_battle_fandom_wiki_process.execute(character_name)
        # except Exception as e:
        #     raise e

        try:
            return self.character_search_repository.search(character_name)
        except Exception as e:
            raise e

        ## Should create

    def search_death_battle_fandom_with_page_id(self, page_id: int) -> DeathBattleFandomQueryResponseModel:
        try:
            return self.search_death_battle_fandom_wiki_process.execute_from_page_id(page_id)
        except Exception as e:
            raise e

    def generate_new_character(self, character_id: int) -> CharacterProfileModel:
        try:
            character = self.character_repository.select(character_id)
        except Exception as e:
            raise e

        try:
            model_with_tags = self.search_death_battle_fandom_with_page_id(character.page_id)
        except Exception as e:
            raise e

        # Get the description
        try:
            description = self.fetch_and_parse_search_death_battle_fandom_wiki_process.execute(character.page_id)
        except Exception as e:
            raise e

        # Get the powerscaling
        try:
            powerscaling = self.extract_powerscaling_from_death_battle_query_response_process.execute(
                model_with_tags
            )
        except Exception as e:
            raise e

        try:
            ollama_result = self.ollama_generate_character_process.execute(description)
        except Exception as e:
            raise e

        # generate character model
        character_profile =  self.create_character_for_db_insert_process.execute(
            character.character_id,
            model_with_tags.image_url,
            powerscaling,
            model_with_tags.categories,
            ollama_result
        )

        character_profile = self._insert_character(character_profile)

        return character_profile

    def _insert_character(self, character: CharacterProfileModel):
        # 1. Resolve powerscale
        ps = self.powerscale_repository.get_by_label(character.powerscale.label)

        if not ps:
            self.powerscale_repository.insert(
                character.powerscale.tier,
                character.powerscale.label,
                character.powerscale.name
            )
            ps = self.powerscale_repository.get_by_label(character.powerscale.label)

        powerscale_id = ps.powerscale_id

        # 2. Insert character
        character_id = self.character_profile_repository.insert(character, powerscale_id)

        # 3. Insert categories
        self.character_category_repository.insert_many(character_id, character.categories)

        character.id = character_id
        return character


    def get_character(self, character_id: int):
        return self.full_character_model_repository.select(character_id)