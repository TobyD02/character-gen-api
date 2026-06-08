## Todo
- [ ] Combat Ideas
  - Cannot guarantee that abilities be generated properly - i.e. attacks dont buff enemies, etc...
  - Instead - what if characters have base attack, and abilities that buff their base stats
    - i.e. boost attack damage, defense, recover hp
    - These could be either buff or debuff - with debuff targetting foes and buff targetting allies
    - for debuff - if target is set to self (for some reason) change to other
    - all values are scalar - debuff implies negative, buff implies positive.
  - Alternatively, could define enums for types of abilities
    - i.e. heal, damage, buff, stun, slow, etc...
    - Perhaps moves could be linked to an array of these (with a maximum number)
    - Then - moves are given a base power which informs how powerful they are
      - Perhaps the final cost is this power * number of effects they inflict
  - Powerscale could be a buff for generate attack power/base stats etc...
    - Could also inform the amount of 'mana' - i.e. how many points they can spend on moves per turn.
 
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