import os
print(os.path.abspath("worldcup.db"))
import json
import requests
from database import get_connection

url = "https://api.football-data.org/v4/competitions/WC/teams"

def fetch_teams():
  api_key = os.getenv("FOOTBALLAPI")
  headers = {
      "X-Auth-Token": api_key
  }
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.json()["teams"]

def save_teams(teams):
    with get_connection() as conn:
        cursor = conn.cursor()
        for team in teams:
            cursor.execute(

                """
                INSERT OR REPLACE INTO teams (id, name, tla)
                VALUES (?, ?, ?)
                """,
                (team["id"], team["name"], team.get("tla"))
            )
        conn.commit()

teams = fetch_teams()
save_teams(teams)

print(f"Saved {len(teams)} teams.")