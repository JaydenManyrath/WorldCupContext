import os
import requests
from database import get_connection

API_KEY = os.getenv("SPORTSAPI")
BASE_URL = "https://v3.football.api-sports.io/fixtures/headtohead"
headers = {"x-apisports-key": API_KEY}

def get_team_api_ids_for_fixture(fixture_id):
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            home.api_football_id,
            away.api_football_id,
            home.name,
            away.name
        FROM matches
        JOIN teams AS home ON matches.home_team_id = home.id
        JOIN teams AS away ON matches.away_team_id = away.id
        WHERE matches.fixture_id = ?
        """,
        (fixture_id,)
    )
    row = cursor.fetchone()

  if row is None:
    return None

  home_api_id, away_api_id, home_name, away_name = row
  if home_api_id is None or away_api_id is None:
    return None

  return {
    "home_team_id": home_api_id,
    "away_team_id": away_api_id,
    "home_team": home_name,
    "away_team": away_name
  }

def get_head_to_head(fixture_id, last=5):
  teams = get_team_api_ids_for_fixture(fixture_id)
  if teams is None:
      return None

  params = {
    "h2h": f"{teams['home_team_id']}-{teams['away_team_id']}",
    "last": last
  }

  response = requests.get(BASE_URL, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()

  if data["results"] == 0 or not data["response"]:
    return {
        "fixture_id": fixture_id,
        "home_team": teams["home_team"],
        "away_team": teams["away_team"],
        "total_h2h_matches": 0,
        "matches": []
    }

  return {
    "fixture_id": fixture_id,
    "home_team": teams["home_team"],
    "away_team": teams["away_team"],
    "total_h2h_matches": data["results"],
    "matches": [
        {
            "date": match["fixture"]["date"],
            "home_team": match["teams"]["home"]["name"],
            "away_team": match["teams"]["away"]["name"],
            "home_goals": match["goals"]["home"],
            "away_goals": match["goals"]["away"],
            "status": match["fixture"]["status"]["short"]
        }
        for match in data["response"]
    ]
  }



if __name__ == "__main__":
  h2h = get_head_to_head(1489408)
  print(h2h)
  h2h = get_head_to_head(1539009)
  print(h2h)
  h2h = get_head_to_head(1489406)
  print(h2h)
  h2h = get_head_to_head(1489405)
  print(h2h)
  h2h = get_head_to_head(1539010)
  print(h2h)
  h2h = get_head_to_head(1489407)
  print(h2h)