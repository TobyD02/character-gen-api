import enum

import ollama
import pydantic
from pydantic import BaseModel

class PowerScale(enum.Enum):
  NEGLIGIBLE = "negligible"          # no meaningful combat ability

  HUMAN = "human"                    # peak human capability

  ENHANCED = "enhanced"              # superhuman strength/speed/reflexes

  STRUCTURAL = "structural"          # building to city-scale destruction

  REGIONAL = "regional"              # mountain / island / country-scale

  PLANETARY = "planetary"            # can threaten or destroy planets

  STELLAR = "stellar"                # star-level energy or system influence

  COSMIC = "cosmic"                  # galaxy-scale or space-time manipulation

  REALITY_BENDER = "reality_bender"  # dimensional, time, or universal laws affected

  TRANSCENDENT = "transcendent"      # beyond normal physics / scaling systems

class SpecialAbility(BaseModel):
  name: str
  description: str

class CharacterDefinition(BaseModel):
  name: str
  description: str
  special_ability: SpecialAbility
  powerscale: PowerScale

def test_ollama(prompt: str):

  response = ollama.chat(
    model='gemma4:e4b',
    messages=[
      {
        'role': 'user',
        'content': prompt
      }
    ],
    think=False,
    format=CharacterDefinition.model_json_schema()
  )

  return response

PROMPT_PREFIX = '''
You are generating a fictional character profile from metadata.

You must return a JSON object matching the schema exactly.

---

CORE RULE:
Powerscale is based on the character's overall combat and existential capability, not just physical destruction.

Think in terms of:
- What scale of reality the character can meaningfully affect or control
- Not just what they can destroy

---

SCALING GUIDE (internal reasoning only):

0. NEGLIGABLE SCALE
- weaker than a human, essentially incosequential

1. HUMAN SCALE
- no superhuman feats

2. STRUCTURAL SCALE (BUILDING → CITY)
- destroys buildings, streets, cities

3. REGIONAL SCALE (MOUNTAIN → COUNTRY)
- large natural or geographic destruction

4. PLANETARY SCALE (CONTINENT → PLANET)
- threatens or destroys planets

5. COSMIC SCALE (STAR → GALAXY)
- star-level energy manipulation or system-wide influence

6. REALITY SCALE (UNIVERSAL → MULTI_GALAXY)
- space-time, dimensional, or universal influence

7. TRANSCENDENT SCALE (OUTERVERSAL → BOUNDLESS)
- exists beyond normal physical reality or scaling systems

---

SELECTION RULES:
- Start from the TOP of the scale and move downward until a match is found.
- If the character has ANY of the following, they are at least REALITY SCALE:
  - time manipulation
  - dimensional travel or control
  - creation of pocket dimensions
  - divine/angelic status
- Do NOT underestimate abstract or non-physical beings.
- Choose the SINGLE closest enum value.

---

STYLE RULES:
- Write concise, in-universe narration.
- Do not mention anime, metadata, JSON, or the prompt.
- special_ability must reflect the most iconic ability.
- Do not invent unrelated abilities.

OUTPUT:
Return ONLY valid JSON matching schema.
'''

x = test_ollama(PROMPT_PREFIX + '''
  {
      "name":  "Izuku Midoriya",
      "description": "__Height:__ 166 cm (5'5\u00bc\")\n__Quirk:__ One For All\n\nStudent in Class 1-A at U.A High School.\n\nAlthough he was born without a Quirk, Izuku's innate heroism and strong sense of justice manages to catch the attention of the legendary hero [All Might](https://anilist.co/character/89224). Izuku has since become All Might's closest pupil.\n\nIzuku is a very timid, reserved, and polite boy. Although initially portrayed as insecure, tearful, and vulnerable, Izuku gradually matures into a more confident and braver person. His infectious leadership skills, combined with his passion and strategic abilities, have turned Izuku into a central figure of Class 1-A. He is caring and emotional, never hesitating to help or rescue someone in danger, even if he knows that he might not be strong or otherwise qualified enough to do it.\n\nIzuku is extremely (and sometimes scarily) enthusiastic about topics related to heroes. His dream drives him to write down notes about everything he learns about heroes' Quirks and fighting capabilities. Thanks to this practice, Izuku has developed a great analytical mind and can form complex battle plans in a few seconds, factoring in the best ways he can utilize the Quirks of allies and enemies alike for his own advantage.\n\nIzuku's Quirk \"One For All\" was transferred to him from All Might. His Quirk allows him to stockpile an enormous amount of raw power, allowing him to significantly enhance all of his physical abilities to various boundless levels. This results in unbelievable levels of strength, speed, stamina, agility, and durability. Izuku can focus the stockpiled power into a single body part, or spread it across his entire body evenly, though, focusing the power in a single part puts a greater strain on that part of his body.",
      "gender": "Male"
  },
''')

print(x.message.content)
