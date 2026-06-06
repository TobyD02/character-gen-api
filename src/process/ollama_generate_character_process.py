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
        - Do not mention anime, metadata, JSON, or the prompt.
        - special_ability must reflect the most iconic ability.
        - Do not invent unrelated abilities.

        OUTPUT:
        Return ONLY valid JSON matching schema.
        '''

        host = os.getenv("OLLAMA_URL")
        if not host:
            host = "http://localhost:11434"

        self.client = ollama.Client(host)

    def execute(self, description: str) -> OllamaCharacterDefinitionModel:
        response = self.client.chat(
            model='gemma4:e4b',
            messages=[
                {
                    'role': 'user',
                    'content': self.PROMPT_PREFIX + description
                }
            ],
            think=False,
            format=OllamaCharacterDefinitionModel.model_json_schema(),
        )

        return OllamaCharacterDefinitionModel.model_validate_json(response.message.content)

    def execute_test(self, description):
        return OllamaCharacterDefinitionModel.model_validate(test_data_fixed)


process = OllamaGenerateCharacterProcess()

print(process.execute_test("m"))