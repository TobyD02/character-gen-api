import os

import ollama

from src.model.ollama_character_model import OllamaCharacterDefinitionModel
from src.process.process_abstract import ProcessAbstract

test_data = {
    "name": "Monkey D. Luffy",
    "description": "Monkey D. Luffy is the captain of the Straw Hat Pirates and a powerful fighter who gained rubber-like abilities after eating a Devil Fruit.",
    "special_abilities": [
        {
            "name": "Gomu Gomu no Pistol",
            "description": "Luffy stretches his arm and launches a high-speed punch.",
            "special_ability_emoji": "👊"
        },
        {
            "name": "Gear Second",
            "description": "Enhances speed and strength by accelerating blood flow.",
            "special_ability_emoji": "💨"
        },
        {
            "name": "Haki",
            "description": "A spiritual power allowing Luffy to overpower enemies.",
            "special_ability_emoji": "⚡"
        }
    ],
}

test_data_fixed = {
    "name": "Monkey D. Luffy",
    "description": "...",
    "special_ability_1": test_data["special_abilities"][0],
    "special_ability_2": test_data["special_abilities"][1],
    "special_ability_3": test_data["special_abilities"][2],
    "special_ability_4": {
        "name": "Empty",
        "description": "N/A",
        "special_ability_emoji": "❌"
    },
    "html_colour_hex": "#ff0000"
}


class OllamaGenerateCharacterProcess(ProcessAbstract):
    def __init__(self):
        self.PROMPT_PREFIX = '''
        You are generating a fictional character profile from metadata.

        You must return a JSON object matching the schema exactly.

        STYLE RULES:
        - Write concise, in-universe narration.
        - Do not mention anime, metadata, JSON or the prompt.
        - special_ability must reflect the most iconic ability.
        - Do not invent unrelated abilities.
        
        SPECIAL_ABILITY GENERATION RULES:
        - target: Choose "self" if the ability boosts/heals the user, "other" for a single enemy or ally, or "multi" if it strikes/buffs multiple targets simultaneously.
        - range: Define how far the ability can reach (0 for melee/self/aura, up to 10 for massive intergalactic or long-range sniper distance). If target is "self", range MUST be 0.
        - area_of_effect: Define the splash/blast radius centered on the target. 0 means it hits exactly one point/person. Higher numbers (up to 10) represent massive zone-wide or planet-level crossfire.
        - health_add: Set between -10 (devastating lethal damage) and 10 (supreme healing/regeneration). 0 means no direct health change.
        - defense_add: Set between -10 (completely shattering armor/shields) and 10 (becoming near-indestructible). 
        - movement_add: Set between -10 (stunning, paralyzing, or freezing in place) and 10 (extreme hypersonic or light-speed travel).
        - attack_power_add: Set between -10 (reduces the targets attack power to the minimum) and 10 (increases the targets attack power to the maximum)
        - will_stun: True if the attack is intended to be used to stun the opponent, or in some way prevent them from taking their next turn. 
        - Narrative Alignment: Ensure the mechanical numbers logically match your written description (e.g., if a Viltrumite punches a hole through a planet, health_add should be deeply negative, range should be 0, and area_of_effect should reflect the collateral damage).
        
        CRITICAL RULE: NO DEAD ABILITIES
        - Every single ability MUST have at least one non-zero effect value. Never return 0 for all effect fields.
        - If an ability is purely psychological, tactical, or a utility skill (like perception, analyzing, or a passive trait), you MUST translate it into your existing combat stats:
          * High perception/analysis means predicting attacks -> give a positive `defense_add` or `damage_buff_mult` to `self`.
          * Pulling or drawing in targets means disrupting their position -> give a negative `movement_add` to the `other`.
        - Check your target! If target is `SELF`, the values must be positive buffs (+health, +defense, +movement, or +damage_buff_mult). If target is `OTHER` or `MULTI`, negative values represent a powerful attack or debuff.
        
        RULES FOR SPECIAL ABILITIES 1-4:
        - special_ability_1 must be an attacking move. This means it must (in some way) apply negative defense, health or both to its target.
        - special_ability_2 must be a defensive/healing move. This means it must (in some way) apply positive effects to its target.
        - special_ability_3 can be any type of move - whether that be attacking, defensive/healing, buff/debuff, etc...
        - special_ability_4 can be any type of move - whether that be attacking, defensive/healing, buff/debuff, etc...
        
        When selecting abilities from the source material, prioritise how iconic/recognisable they are for that
        individual character, as well as diversifying the effects of their abilities. If the source material is heavily 
        weighted towards offense/defense/buff then it is fine to produce all abilities inline with that. Adherence 
        to the source is very important.
        
        When generating special ability descriptions, avoid using the characters name. Instead, use neutral
        placeholders such as "they", "the user", etc...

        OUTPUT:
        Return ONLY valid JSON matching schema.
        '''

        host = os.getenv("OLLAMA_URL")
        if not host:
            host = "http://localhost:11434"

        self.client = ollama.Client(host)

        model = os.getenv("OLLAMA_MODEL")
        if not model:
            model = "gemma4:e4b"

        self.model = model

    def execute(self, description: str, categories: list[str]) -> OllamaCharacterDefinitionModel:
        completed_prompt = self.PROMPT_PREFIX + description  # + f"categories: [{','.join(categories)}]"
        print("Generating...", flush=True)
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    'role': 'user',
                    'content': completed_prompt
                }
            ],
            think=False,
            options={
                "num_ctx": 4096 * 2
            },
            format=OllamaCharacterDefinitionModel.model_json_schema(),
        )

        return OllamaCharacterDefinitionModel.model_validate_json(response.message.content)

    def execute_test(self, description):
        return OllamaCharacterDefinitionModel.model_validate(test_data_fixed)
