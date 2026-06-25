CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY, -- FOOTBALL DATA ID
    api_football_id INTEGER, -- API FOOTBALL ID
    name TEXT NOT NULL,
    tla TEXT
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY, -- FOOTBALL DATA ID
    fixture_id INTEGER UNIQUE, -- API-FOOTBALL ID

    utc_date TEXT NOT NULL,
    status TEXT NOT NULL,

    home_team_id INTEGER,
    away_team_id INTEGER,

    home_team_score INTEGER,
    away_team_score INTEGER,
    winner_team_id INTEGER,

    stage TEXT,
    group_name TEXT,

    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(id)
);

CREATE TABLE IF NOT EXISTS favorites (
    team_id INTEGER PRIMARY KEY,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);