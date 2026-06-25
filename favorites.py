from database import get_connection
from datetime import datetime
from zoneinfo import ZoneInfo
import questionary

NY = ZoneInfo("America/New_York")

def favorites_is_empty():
  with get_connection() as conn:
    cursor = conn.execute("SELECT COUNT(*) FROM favorites")
    count = cursor.fetchone()[0]
  return count == 0

def load_all_teams():
  with get_connection() as conn:
    cursor = conn.execute("""
      SELECT id, name
      FROM teams
      ORDER BY name
    """)
    teams = cursor.fetchall()
  return teams

def select_favorite_teams():
  teams = load_all_teams()
  if not teams:
    print("No teams found in database. Run the team ingestion script first")
    return []
  choices = []
  for team in teams:
    choices.append(
      questionary.Choice(
        title=team["name"],
        value=team["id"]
      )
    )
  selected_team_ids = questionary.checkbox(
    "Select your favorite World Cup teams (Space = Select, Enter = Confirm)",
    choices = choices
  ).ask()
  return selected_team_ids or []

def save_favorites(team_ids):
  with get_connection() as conn:
    cursor = conn.cursor()
    for team_id in team_ids:
      cursor.execute("""
        INSERT OR IGNORE INTO favorites (team_id)
        VALUES (?)
        """,
        (team_id,)
      )
    conn.commit()

def load_favorites():
  with get_connection() as conn:
    cursor = conn.execute("""
      SELECT team_id
      FROM favorites
    """)
    favorites = [row["team_id"] for row in cursor.fetchall()]
  return favorites

def load_team_matches(team_id):
  with get_connection() as conn:
    cursor = conn.execute("""
      SELECT *
      FROM matches
      WHERE home_team_id = ?
      OR away_team_id = ?
      ORDER BY utc_date
      """,
      (team_id, team_id)
    )
    return cursor.fetchall()

def get_previous_match(team_id):
  matches = load_team_matches(team_id)
  now = datetime.now(NY)
  previous = None
  for match in matches:
    match_time = datetime.fromisoformat(
      match["utc_date"].replace("Z", "+00:00")
    ).astimezone(NY)
    if match_time <= now: previous = match
    else: break
  return previous 

def get_next_match(team_id):
  matches = load_team_matches(team_id)
  now = datetime.now(NY)
  for match in matches:
    match_time = datetime.fromisoformat(
      match["utc_date"].replace("Z", "+00:00")
    ).astimezone(NY)
    if match_time > now: return match
  return None

def get_favorite_summary(team_id):
  with get_connection() as conn:
    cursor = conn.execute(
      """
      SELECT name
      FROM teams
      WHERE id = ?
      """,
      (team_id,)
    )
    team = cursor.fetchone()

  return {
    "team_id": team_id,
    "team_name": team["name"] if team else "Unknown Team",
    "previous_match": get_previous_match(team_id),
    "next_match": get_next_match(team_id)
  }

def load_favorite_summaries():
  favorite_ids = load_favorites()
  summaries = []
  for team_id in favorite_ids:
    summaries.append(
      get_favorite_summary(team_id)
    )
  return summaries

if __name__ == "__main__":

    print("Testing favorites workflow...\n")
    print("Favorites empty:", favorites_is_empty())

    selected = select_favorite_teams()
    print("\nSelected team IDs:", selected)

    if selected:
        save_favorites(selected)
        print("Favorites saved.")

    print("\nFavorites currently in database:")
    print(load_favorites())
  
