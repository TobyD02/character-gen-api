import requests
from bs4 import BeautifulSoup

from src.process.process_abstract import ProcessAbstract

class FetchAndParseDeathBattleFandomWikiPageContentProcess(ProcessAbstract):
    def __init__(self):
        self.base_url_template = "https://vsbattles.fandom.com/api.php?action=parse&pageid={page_id}&prop=text&format=json"
        self.base_url_template_with_info = "https://vsbattles.fandom.com/api.php?action=parse&pageid={page_id}&format=json&pageids=2405&prop=categories|pageimages&cllimit=max&pithumbsize=400&pilimit=max"

    def execute(self, page_id: int):
        response = requests.post(
            self.base_url_template.format(page_id=page_id),
            timeout=10
        )

        html_content = response.json()["parse"]["text"]["*"]
        # 2. Feed the string to the HTML parsing engine
        soup = BeautifulSoup(html_content, "html.parser")

        # 3. Clean up the tree by deleting known sidebar infoboxes, records, and styles
        for noisy_tag in soup(["aside", "table", "style", "script", "div.toc"]):
            noisy_tag.decompose()

        # 4. Extract text strictly from paragraph tags, discarding blank layout nodes
        descriptions = []
        for p in soup.find_all("p"):
            clean_text = p.get_text().strip()
            if clean_text:
                descriptions.append(clean_text)

        return ", ".join(descriptions)