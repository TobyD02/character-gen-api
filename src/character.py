import json

import requests

query = '''
query ($search: String) {
  Page(page: 1, perPage: 1000) {
    characters(search: $search) {
      id
      name {
        full
        native
        alternative
      }
      image {
        medium
      }
      description(asHtml: false)
      gender
    }
  }
}
'''

variables = {
    "search": "deku"
}

response = requests.post(
    "https://graphql.anilist.co",
    json={"query": query, "variables": variables}
)

with open("./character.json", "a") as f:
    f.write(json.dumps(response.json(), indent=4))