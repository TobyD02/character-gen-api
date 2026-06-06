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

