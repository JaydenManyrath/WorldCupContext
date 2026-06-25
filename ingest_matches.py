import os
import requests
from database import get_connection
from dotenv import load_dotenv
load_dotenv()

URL = "https://api.football-data.org/v4/competitions/WC/matches?season=2026"

def fetch_matches():
    api_key = os.getenv("FOOTBALLAPI")
    headers = {
        "X-Auth-Token": api_key
    }
    response = requests.get(URL, headers=headers)
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

def save_matches(matches):
    saved_count = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        for match in matches:
          home_team_id = match["homeTeam"].get("id")
          away_team_id = match["awayTeam"].get("id")
          full_time_score = match["score"]["fullTime"]
          cursor.execute(
              """
              INSERT OR REPLACE INTO matches (
                  id, utc_date, status,
                  home_team_id, away_team_id,
                  home_team_score, away_team_score,
                  winner_team_id, stage, group_name
              )
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              """,
              (
                match["id"],
                match["utcDate"],
                match["status"],
                home_team_id,
                away_team_id,
                full_time_score["home"],
                full_time_score["away"],
                get_winner_team_id(match),
                match.get("stage"),
                match.get("group")
              )
          )
          saved_count += 1
        conn.commit()
    return saved_count

matches = fetch_matches()
saved_count = save_matches(matches)

print(f"Saved {saved_count} out of {len(matches)} matches.")