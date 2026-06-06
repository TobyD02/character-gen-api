## Todo
- [ ] Update special ability generation
  - Special abilities should be extracted and linked to certain combative tags that are explicitly defined.
  - This way - combat tags can be linked to gameplay features.
  - i.e. some defensive tag could be linked to defensive special ability, etc...

## Running

- **This has been updated - now ollama exists in the docker compose. It may be quicker to run locally and set ollama_url
  to host.docker.internal instead.**

```shell
ollama pull gemma4:e4b
ollama serve
```

```shell
docker compose up --build
```

## Todo

- [ ] Gather all character page ID's from the wiki
    ```aiignore
    ## Link to pages about characters. 
    https://vsbattles.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:Characters&cmlimit=max&format=json
  
    ## To request next page, set the "cmcontinue" query param to that which the json provides
    ```
    - For each, literally just serialise a character name and page id. Once all have been fetched, all queries happen
      via the database - and character models are generated on when and if they are needed.
    - Will require updating the database - since on a search, nothing is serialised into the database.
        - Perhaps a basic model that is just "Character" -> (id, pageid, name).
        - This then links to a character profile etc....