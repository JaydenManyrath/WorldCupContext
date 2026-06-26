# MatchDay ⚽

An AI-powered CLI dashboard that acts as your personal pundit for the 2026 World Cup. Run it before a watch party and walk in sounding like a seasoned fan.

---

## Features

- **Favorite team selection** — On first run, presents an interactive checklist of all 48 World Cup teams. Your choices are saved to a local SQLite database and remembered on every future run.
- **Today's matches dashboard** — Automatically pulls and displays all of today's World Cup fixtures with kickoff times, venues, and live status.
- **Favorite team tracker** — Shows your favorites' previous result and next upcoming match at a glance.
- **Smart spotlight selection** — If one of your favorites is playing today, it's auto-selected. If multiple are playing, you choose. If none are playing, Gemini picks the most interesting match for you.
- **AI match hype** — Uses Google Gemini to generate a pundit-style pre-match breakdown with rivalry context, current stakes, win probabilities, and players to watch.
- **Win predictions** — Surfaces real win/draw/loss percentages for the spotlight match.
- **YouTube highlights** — Finds a highlight video of the two teams' most recent encounter via the YouTube Data API.
- **Local SQLite database** — Stores teams, matches, and favorites locally to minimize redundant API calls.

---

## Tech Stack

- **Python 3**
- **SQLite** — local database for teams, matches, and favorites
- **[Football-Data.org API](https://www.football-data.org/)** — tournament structure, team roster, and match ingestion
- **[API-Sports](https://www.api-football.com/)** — live match schedules and win predictions
- **Google Gemini API** — AI match contextualization and hype generation
- **YouTube Data API v3** — highlight video search

---

## Project Structure

```
MatchDay/
├── worldcup.py          # Main entry point
├── display.py           # Dashboard rendering and CLI output
├── spotlight.py         # Spotlight match selection logic
├── favorites.py         # Favorite team selection and storage
├── get_matches.py       # API-Sports live match fetching
├── head_to_head.py      # H2H history fetching
├── prediction.py        # Win prediction fetching
├── api_youtube.py       # YouTube highlight search
├── database.py          # SQLite connection and helpers
├── ingest_teams.py      # One-time team data ingestion
├── ingest_matches.py    # One-time match schedule ingestion
├── refresh_matches.py   # Updates match scores in DB
├── sync_api_ids.py      # Bridges Football-Data and API-Sports team IDs
├── Schema.sql           # SQLite schema
├── test_worldcup.py     # Unit tests
└── .env                 # API keys (not committed)
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/JaydenManyrath/WorldCupContext.git
cd WorldCupContext
```

### 2. Install dependencies

```bash
pip install requests google-generativeai python-dotenv questionary
```

### 3. Configure API keys

Create a `.env` file in the project root:

```
GOOGLEAPI=your_google_gemini_api_key
FOOTBALLAPI=your_football_data_org_api_key
SPORTSAPI=your_api_sports_key
YOUTUBEAPI=your_youtube_data_api_v3_key
```

- **Google Gemini** — [Google AI Studio](https://aistudio.google.com/)
- **Football-Data.org** — [football-data.org](https://www.football-data.org/client/register)
- **API-Sports** — [api-football.com](https://www.api-football.com/)
- **YouTube Data API v3** — [Google Cloud Console](https://console.cloud.google.com/)

### 4. Initialize and populate the database

```bash
sqlite3 worldcup.db < Schema.sql
python ingest_teams.py
python ingest_matches.py
python sync_api_ids.py
```

### 5. Run

```bash
python3 worldcup.py
```

---

## Usage

On first run you'll see an interactive checklist of all 48 World Cup teams:

```
? Select your favorite national teams (space to select, enter to confirm)
 ○ Argentina
 ○ Belgium
 ● Brazil
 ○ England
 ...
```

The dashboard then displays automatically:

```
TODAY'S WORLD CUP MATCHES
------------------------------------------------------------
2:00 PM  Norway    vs   France      [NS]  Hard Rock Stadium, Miami
7:00 PM  Uruguay   vs   Spain       [NS]  MetLife Stadium, New York

FAVORITE TEAM MATCHES
------------------------------------------------------------
France
  Previous: Jun 22, 5:00 PM | France 3-0 Iraq
  Next:     Jun 26, 2:00 PM | Norway vs France

SPOTLIGHT MATCH
------------------------------------------------------------
2:00 PM | Norway vs France — Hard Rock Stadium, Miami

Prediction
------------------------------------------------------------
Norway: 22%   Draw: 28%   France: 50%

Why it matters
------------------------------------------------------------
Get ready for a fascinating encounter as France (50%) clash
with an ambitious Norway looking to cause an upset...

YOUTUBE HIGHLIGHT
------------------------------------------------------------
Watch: Norway vs France Highlights
https://www.youtube.com/watch?v=...
```

---

## Running Tests

```bash
python -m unittest test_worldcup.py
```

Covers `saveTeam` (valid and invalid), and all three paths through `findSpotlightMatch` (one favorite, no favorites, multiple favorites).

---

## Built By

Jayden Manyrath & Andrew Manoni — Project #1, CLI & APIs
