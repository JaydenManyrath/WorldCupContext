import os
import requests
from datetime import date, timedelta
from database import get_connection

URL = "https://api.football-data.org/v4/competitions/WC/matches"

def fetch_todays_matches():
  api_key = os.getenv("SPORTSAPI")
  today = date.today()
  yesterday = (today - timedelta(days=1)).isoformat()
  tomorrow = (today + timedelta(days=1)).isoformat()

  headers = {"X-Auth-Token": api_key}
  params = {
    "dateFrom": yesterday,
    "dateTo": tomorrow,
    "season": 2026
  }

  response = requests.get(URL, headers=headers, params=params)
  response.raise_for_status()

  return response.json()["matches"]

def get_winner_team_id(match):
  winner = match["score"].get("winner")
  if winner == "HOME_TEAM":
    return match["homeTeam"]["id"]
  elif winner == "AWAY_TEAM":
    return match["awayTeam"]["id"]
  else:
    return None

def refresh_todays_matches():
  matches = fetch_todays_matches()
  print(f"API returned {len(matches)} matches.")
  updated_count = 0
  with get_connection() as conn:
    cursor = conn.cursor()
    for match in matches:
      home_id = match["homeTeam"].get("id")
      away_id = match["awayTeam"].get("id")
      if home_id is None or away_id is None:
        print("SKIPPED MATCH:")
        print("id:", match["id"])
        print("homeTeam:", match["homeTeam"])
        print("awayTeam:", match["awayTeam"])
        print("status:", match["status"])
        print()
        continue
      score = match["score"].get("fullTime") or {}
      home_score = score.get("home")
      away_score = score.get("away")
      cursor.execute (
        """
        INSERT OR REPLACE INTO matches (
          id, 
          utc_date,
          status,
          home_team_id,
          away_team_id,
          home_team_score,
          away_team_score,
          winner_team_id,
          stage,
          group_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
          match["id"],
          match["utcDate"],
          match["status"],
          home_id,
          away_id,
          home_score,
          away_score,
          get_winner_team_id(match),
          match.get("stage"),
          match.get("group")
        )
      )

      updated_count += 1
    conn.commit()
    return updated_count

if __name__ == "__main__":
  count = refresh_todays_matches()
  print(f"Updated {count} matches.")