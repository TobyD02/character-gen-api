import os

import ollama

from src.model.ollama_character_model import OllamaCharacterDefinitionModel
from src.process.process_abstract import ProcessAbstract

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
        - type: Buff it it has positive influence over the target (i.e. increasing their stats), debuff if it has negative effects (decreasing their stats)
        - health_impact_factor: Represents if the ability will affect the targets hp - in the case of a buff this would heal, in the case of a debuff this would damage.
        - defense_impact_factor: Represents if the ability will affect the target's defense. In the case of a buff this would increase defense, in the case of a debuff this would reduce defense.
        - movement_impact_factor: Represents if the ability will affect the target's movement. In the case of a buff this would increase movement speed or mobility, in the case of a debuff this would reduce movement speed or mobility.
        - attack_power_impact_factor: Represents if the ability will affect the target's attack power. In the case of a buff this would increase attack power, in the case of a debuff this would reduce attack power.
        - will_stun: True if the attack is intended to be used to stun the opponent, or in some way prevent them from taking their next turn. 
        - Narrative Alignment: Ensure the mechanical numbers logically match your written description (e.g., if a Viltrumite punches a hole through a planet, health_add should be deeply negative, range should be 0, and area_of_effect should reflect the collateral damage).
        
        CRITICAL RULE: NO DEAD ABILITIES
        - Every single ability MUST have at least one non-zero effect value. Never return 0 for all effect fields.
        - If an ability is purely psychological, tactical, or a utility skill (like perception, analyzing, or a passive trait), you MUST translate it into your existing combat stats:
          * High perception/analysis means predicting attacks -> give a positive `defense_add` or `damage_buff_mult` to `self`.
          * Pulling or drawing in targets means disrupting their position -> give a negative `movement_add` to the `other`.
        - Check your target! If target is `SELF`, the values must be positive buffs (+health, +defense, +movement, or +damage_buff_mult). If target is `OTHER` or `MULTI`, negative values represent a powerful attack or debuff.
        
        
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