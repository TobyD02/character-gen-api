from src.model.character_special_ability_model import CharacterSpecialAbilityModel
from src.process.build_character_special_ability_from_generated_process import \
    BuildCharacterSpecialAbilityFromGeneratedProcess
from src.model.character_model import CharacterModel
from src.model.ollama_character_model import OllamaCharacterDefinitionModel, OllamaSpecialAbilityModel
from src.model.character_power_scale_model import CharacterPowerScaleModel
from src.process.extract_domainant_colour_from_image_url_process import ExtractDominantColourFromImageUrlProcess
from src.repository.character_special_ability_repository import CharacterSpecialAbilityRepository
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
from src.model.character_response_model import CharacterResponseModel


class CharacterService(ServiceAbstract):
    def __init__(
            self,
            extract_dominant_colour_from_image_url_process: ExtractDominantColourFromImageUrlProcess,
            build_character_special_ability_from_generated_process: BuildCharacterSpecialAbilityFromGeneratedProcess,
            character_special_ability_repository: CharacterSpecialAbilityRepository,
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
        self.extract_dominant_colour_from_image_url_process: ExtractDominantColourFromImageUrlProcess = \
            extract_dominant_colour_from_image_url_process
        self.build_character_special_ability_from_generated_process: BuildCharacterSpecialAbilityFromGeneratedProcess = \
            build_character_special_ability_from_generated_process
        self.character_special_ability_repository: CharacterSpecialAbilityRepository = character_special_ability_repository
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

    def get_or_generate_character(self, character_id: int) -> CharacterResponseModel:
        try:
            character = self.character_repository.select(character_id)
        except Exception as e:
            raise e

        # Check if character profile exists, in which case return it.30259
        try:
            return self.full_character_model_repository.select(character)
        except Exception as e:
            print(f"Failed to find exising character profile, generating new one: {e}", flush=True)
            pass

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

        # Generate special abilities and description
        # @todo: Filter character categories, and use select categories to inform special abilities
        try:
            ollama_result = self.ollama_generate_character_process.execute(description, model_with_tags.categories)
        except Exception as e:
            raise e

        special_ability_models = self.build_character_special_ability_from_generated_process.execute([
            ollama_result.special_ability_1,
            ollama_result.special_ability_2,
            ollama_result.special_ability_3,
            ollama_result.special_ability_4,
        ])

        color_palette = self.extract_dominant_colour_from_image_url_process.execute(model_with_tags.image_url)

        # generate character model
        character_profile = self.create_character_for_db_insert_process.execute(
            character.character_id,
            model_with_tags.image_url,
            powerscaling,
            model_with_tags.categories,
            ollama_result,
            color_palette
        )

        return self._insert_character(character, character_profile, powerscaling, model_with_tags, ollama_result, special_ability_models)


    def get_random_generated(self, count: int):
        ids = self.character_profile_repository.select_random_character_ids(count)

        cards = []
        for character_id in ids:
            cards.append(self.get_or_generate_character(character_id))

        return cards

    def get_all_characters(self):
        ids = self.character_profile_repository.select_all_character_ids()
        cards = []
        for character_id in ids:
            cards.append(self.get_or_generate_character(character_id))

        return cards

    def get_by_category(self, category_id: int):
        ids = self.character_profile_repository.get_by_category(category_id)

        print(f"Found {len(ids)} characters", flush=True)
        cards = []
        for character_id in ids:
            cards.append(self.get_or_generate_character(character_id))

        return cards

    def search_by_category(self, query: str):
        ids = self.character_profile_repository.search_by_category(query)

        print(f"Found {len(ids)} characters", flush=True)
        cards = []
        for character_id in ids:
            cards.append(self.get_or_generate_character(character_id))

        return cards

    def _insert_character(
            self,
            character: CharacterModel,
            character_profile: CharacterProfileModel,
            powerscaling: CharacterPowerScaleModel,
            model_with_tags: DeathBattleFandomQueryResponseModel,
            ollama_character_definition: OllamaCharacterDefinitionModel,
            special_abilities: list[CharacterSpecialAbilityModel]
    ) -> CharacterResponseModel:
        # 1. Resolve powerscale
        powerscale = self.powerscale_repository.get_by_label(powerscaling.label)

        if not powerscale:
            self.powerscale_repository.insert(
                powerscaling.tier,
                powerscaling.label,
                powerscaling.name
            )
            powerscale = self.powerscale_repository.get_by_label(powerscaling.label)

        character_profile.powerscale_id = powerscale.powerscale_id

        # 2. Insert character
        character_profile_id = self.character_profile_repository.insert(character_profile)

        # 3. Insert categories
        self.character_category_repository.insert_many(character.character_id, model_with_tags.categories)

        self.character_special_ability_repository.insert_character_special_abilities(character.character_id, special_abilities)


        character_profile.character_profile_id = character_profile_id
        character_profile.powerscale_id = powerscale.powerscale_id

        return CharacterResponseModel(
            character=character,
            character_profile=character_profile,
            categories=model_with_tags.categories,
            powerscale=powerscale,
            special_abilities=special_abilities
        )
