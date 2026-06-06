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
    character_id         INTEGER REFERENCES character (character_id),
    image                TEXT,
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
