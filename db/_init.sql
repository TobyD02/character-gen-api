CREATE TABLE IF NOT EXISTS character
(
    character_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    page_id      INTEGER UNIQUE,
    name         TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS powerscale
(
    powerscale_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tier          REAL,
    label         TEXT UNIQUE,
    name          TEXT
);

CREATE TABLE IF NOT EXISTS character_profile
(
    character_profile_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    character_id         INTEGER NOT NULL UNIQUE REFERENCES character (character_id),
    image_url               TEXT,
    description          TEXT,
    powerscale_id        INTEGER,
    html_colour_hex      TEXT
);

CREATE TABLE IF NOT EXISTS category
(
    category_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name        TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS character_category
(
    character_id INTEGER NOT NULL,
    category_id  INTEGER NOT NULL,

    PRIMARY KEY (character_id, category_id),

    FOREIGN KEY (character_id)
        REFERENCES character (character_id)
        ON DELETE CASCADE,

    FOREIGN KEY (category_id)
        REFERENCES category (category_id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS character_special_ability
(
    character_id INTEGER NOT NULL REFERENCES character(character_id),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    special_ability_emoji TEXT NOT NULL,

    CONSTRAINT uq_character_special_ability_character_name
    UNIQUE(character_id, name)
);