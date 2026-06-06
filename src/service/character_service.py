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
from src.repository.character_repository import CharacterRepository
from src.repository.full_character_model_repository import FullCharacterModelRepository
from src.repository.powerscale_repository import PowerScaleRepository
from src.service.service_abstract import ServiceAbstract

class CharacterService(ServiceAbstract):
    def __init__(
        self,
        full_character_model_repository: FullCharacterModelRepository,
        character_repository: CharacterRepository,
        character_category_repository: CharacterCategoryRepository,
        powerscale_repository: PowerScaleRepository,
        ollama_generate_character_process: OllamaGenerateCharacterProcess,
        create_character_for_db_insert_process: CreateCharacterForDbInsertProcess,
        search_death_battle_fandom_wiki_process: SearchDeathBattleFandomWikiProcess,
        fetch_and_parse_search_death_battle_fandom_wiki_process: FetchAndParseDeathBattleFandomWikiPageContentProcess,
        extract_powerscaling_from_death_battle_query_response_process: ExtractPowerscalingFromDeathBattleQueryResponseProcess,
    ):
        self.full_character_model_repository: FullCharacterModelRepository = full_character_model_repository
        self.character_repository: CharacterRepository = character_repository
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
        try:
            return self.search_death_battle_fandom_wiki_process.execute(character_name)
        except Exception as e:
            raise e

    def search_death_battle_fandom_with_page_id(self, page_id: int) -> DeathBattleFandomQueryResponseModel:
        try:
            return self.search_death_battle_fandom_wiki_process.execute_from_page_id(page_id)
        except Exception as e:
            raise e

    def generate_new_character(self, death_battle_fandom_wiki_query_response_model: DeathBattleFandomQueryResponseModel) -> CharacterProfileModel:

        # Check if character entry already exists
        try:
            id = self.character_repository.select_by_name(death_battle_fandom_wiki_query_response_model.name)
            print(id)
            if id is not None:
                return self.get_character(id)

            id = self.character_repository.select_by_page_id(death_battle_fandom_wiki_query_response_model.page_id)
            if id is not None:
                return self.get_character(id)

        except Exception as e:
            raise e

        # Get the description
        try:
            description = self.fetch_and_parse_search_death_battle_fandom_wiki_process.execute(death_battle_fandom_wiki_query_response_model.page_id)
        except Exception as e:
            raise e

        # Get the powerscaling
        try:
            powerscaling = self.extract_powerscaling_from_death_battle_query_response_process.execute(
                death_battle_fandom_wiki_query_response_model
            )
        except Exception as e:
            raise e

        try:
            ollama_result = self.ollama_generate_character_process.execute(description)
        except Exception as e:
            raise e

        # generate character model
        character_profile =  self.create_character_for_db_insert_process.execute(
            death_battle_fandom_wiki_query_response_model.name,
            death_battle_fandom_wiki_query_response_model.image_url,
            powerscaling,
            death_battle_fandom_wiki_query_response_model.page_id,
            death_battle_fandom_wiki_query_response_model.categories,
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

        powerscale_id = ps["id"]

        # 2. Insert character
        character_id = self.character_repository.insert(character, powerscale_id)

        # 3. Insert categories
        self.character_category_repository.insert_many(character_id, character.categories)

        character.id = character_id
        return character


    def get_character(self, character_id: int):
        return self.full_character_model_repository.select(character_id)