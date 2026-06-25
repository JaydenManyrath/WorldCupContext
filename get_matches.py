import requests
import os
import re
from datetime import date
from database import get_connection
from dotenv import load_dotenv

API_KEY = os.getenv("SPORTSAPI")
BASE_URL = "https://v3.football.api-sports.io/fixtures"
WORLD_CUP_LEAGUE_ID = 1
SEASON = 2026

def normalize_team_name(name):
  return re.sub(r"[^a-z]", "", name.lower())

def find_team_by_name(cursor, api_team_name):
  normalized_api_name = normalize_team_name(api_team_name)
  cursor.execute("SELECT id, name FROM teams")
  teams = cursor.fetchall()
  for team in teams:
    if normalize_team_name(team["name"]) == normalized_api_name:
            return team["id"]
  return None

def update_team_api(cursor, local_team_id, api_football_id):
  cursor.execute(
    """
    UPDATE teams
    SET api_football_id = ?
    WHERE id = ?
    """,
    (api_football_id, local_team_id)
  )

def fetch_matches(match_date=None):
  if match_date is None:
    match_date = date.today().isoformat()

  headers = {"x-apisports-key": API_KEY}
  params = {
    "date": match_date,
    "timezone": "America/New_York"
  }

  response = requests.get(BASE_URL, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()

  if data.get("errors"):
    print("API Errors: ", data["errors"])

  all_matches = data["response"]

  world_cup_matches = [
    match for match in all_matches
    if match["league"]["id"] == WORLD_CUP_LEAGUE_ID
    and match["league"]["season"] == SEASON
  ]

  return world_cup_matches

def sync_api_ids(cursor, matches):
  for match in matches:
    home = match["teams"]["home"]
    away = match["teams"]["away"]
    home_team_id = find_team_by_name(cursor, home["name"])
    away_team_id = find_team_by_name(cursor, away["name"])
    if home_team_id is None or away_team_id is None:
      print(
          f"Could not match teams: "
          f"{home['name']} vs {away['name']}"
      )
      continue
    # only fill api_football_id if missing
    cursor.execute(
      """
      UPDATE teams
      SET api_football_id = ?
      WHERE id = ?
      AND api_football_id IS NULL
      """,
      (home["id"], home_team_id)
    )
    cursor.execute(
      """
      UPDATE teams
      SET api_football_id = ?
      WHERE id = ?
      AND api_football_id IS NULL
      """,
      (away["id"], away_team_id)
    )
    cursor.execute(
      """
      UPDATE matches
      SET fixture_id = ?
      WHERE home_team_id = ?
      AND away_team_id = ?
      """,
      (
          match["fixture"]["id"],
          home_team_id,
          away_team_id
      )
    )

def get_matches():
  matches = fetch_matches()
  with get_connection() as conn:
    cursor = conn.cursor()
    sync_api_ids(cursor, matches)
    conn.commit()
  return matches