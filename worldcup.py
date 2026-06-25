import os
import sqlite3
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import date

load_dotenv()

google_key = os.getenv('GOOGLEAPI')
football_key = os.getenv('FOOTBALLAPI')
youtube_key = os.getenv('YOUTUBEAPI')
genai.configure(api_key=google_key)

DB_PATH = "worldcup.db"

def getDB():
  return sqlite3.connect(DB_PATH)

def dbIsEmpty():
  conn = getDB()
  cursor = conn.execute("SELECT COUNT(*) FROM favorites")
  count = cursor.fetchone()[0]
  conn.close()
  return count == 0

def saveTeam(team_name):
  conn = getDB()
  row = conn.execute("SELECT id FROM teams WHERE LOWER(name) = LOWER(?)", (team_name,)).fetchone()
  if row:
      conn.execute("INSERT OR IGNORE INTO favorites (team_id) VALUES (?)", (row[0],))
      conn.commit()
      conn.close()
      return True
  else:
      conn.close()
      return False

def getMatches():
  from get_matches import get_matches as fetch
  return get_matches()

def load_favorites():
  conn = getDB()
  rows = conn.execute("""
      SELECT teams.id FROM favorites
      JOIN teams ON favorites.team_id = teams.id
  """).fetchall()
  conn.close()
  return [row[0] for row in rows]

def promptForFavorites():
  print("Enter your favorite national teams. Type 'DONE' when finished.")
  while True:
      team_input = input("> ").strip()
      if team_input.upper() == "DONE":
          break
      if team_input:
          found = saveTeam(team_input)
          if found:
              print(f"  ✓ Added {team_input}")
          else:
              print(f"  ✗ '{team_input}' not found in World Cup teams. Check spelling.")

def getMatchHype(match):
  from prediction import get_match_prediction

  team1 = match["home_team_name"]
  team2 = match["away_team_name"]
  fixture_id = match["id"]
  if fixture_id:  
    prediction = get_match_prediction(fixture_id)
  else:
    prediction = None

  pred_text = ""
  if prediction:
    pred_text = f"{team1} win {prediction['home_win_percent']}, Draw {prediction['draw_percent']}, {team2} win {prediction['away_win_percent']}. {prediction['advice']}"
  else:
    pred_text = "No prediction available."

  prompt = f"""You are a football pundit. Write a hype paragraph or two for the upcoming World Cup match between {team1} and {team2}.

  Their last 5 meetings:

  Prediction: {pred_text}

  Include historical rivalry context, current stakes, and players to watch. Do not contradict the statistics provided."""

  model = genai.GenerativeModel('gemini-2.5-flash')
  response = model.generate_content(prompt)
  return response.text, prediction

def getMatchesHype(matches):
  team_list = ", ".join([f"{m['home_team_name']} vs {m['away_team_name']}" for m in matches])

  prompt = f"""You are a football pundit. From this list of today's World Cup matches, pick the most exciting one and explain why it's the must-watch game of the day. Then write a hype paragraph for it.

  Matches: {team_list}"""

  model = genai.GenerativeModel('gemini-2.5-flash')
  response = model.generate_content(prompt)
  return response.text

def findSpotlightMatch(matches, favorites):
  spotlightMatches = []

  for match in matches:
      if match["home_team_id"] in favorites or match["away_team_id"] in favorites:
          spotlightMatches.append(match)

  if len(spotlightMatches) == 0:
      print("No favorites playing today — letting the AI pick the best match.\n")
      hype = getMatchesHype(matches)
      return hype, None, None

  elif len(spotlightMatches) == 1:
      return getMatchHype(spotlightMatches[0])

  else:
      print("\nMultiple matches with your favorite teams today. Pick one:\n")
      for i, match in enumerate(spotlightMatches):
          print(f"  [{i + 1}] {match['home_team_name']} vs {match['away_team_name']}  —  {match['utc_date']}")

      while True:
        try:
          choice = int(input("\nEnter a number: ").strip())
          if 1 <= choice <= len(spotlightMatches):
              return getMatchHype(spotlightMatches[choice - 1])
          else:
            print(f"  Please enter a number between 1 and {len(spotlightMatches)}")
        except ValueError:
          print("  Invalid input, please enter a number")

def displayDash(hype_text, matches, favorites, prediction):
  print("=" * 45)
  print("       WORLD CUP 2026 DASHBOARD")
  print("=" * 45)

  print("\nUPCOMING MATCHES TODAY")
  print("-" * 45)
  for match in matches:
      print(f"{match['utc_date']}   {match['home_team_name']} vs {match['away_team_name']}")

  print("\nFAVORITE TEAM MATCHES")
  print("-" * 45)
  conn = getDB()
  if favorites:
    for team_id in favorites:
      team_name = conn.execute("SELECT name FROM teams WHERE id = ?", (team_id,)).fetchone()
      next_match = conn.execute("""
      SELECT m.utc_date, ht.name, at.name
      FROM matches m 
      JOIN teams ht ON m.home_team_id = ht.id
      JOIN teams at ON m.away_team_id = at.id
      WHERE (m.home_team_id = ? OR m.away_team_id = ?)
      AND m.status = 'NS'
      ORDER BY m.utc_date ASC
      LIMIT 1
      """, (team_id, team_id)).fetchone()

      if team_name:
        print(f"\n{team_name[0]}")
      if next_match:
        print(f"Next Match: {next_match[1]} vs {next_match[2]}")
        print(f"Kickoff: {next_match[0]}")
      else:
        print("No upcoming matches found.")
  else:
    print("No favorites found")
  conn.close()
  
  print("\n SPOTLIGHT MATCHUP")
  print("-" * 45)

  if prediction:
    print(f"\n{prediction['home_team']} vs {prediction['away_team']}")
    print(f"\nPrediction")
    print(f"{prediction['home_team']} Win:  {prediction['home_win_percent']}")
    print(f"Draw:          {prediction['draw_percent']}")
    print(f"{prediction['away_team']} Win:  {prediction['away_win_percent']}")
    print(f"\nPredicted Result: {prediction['predicted_winner']}")
    print(f"Advice: {prediction['advice']}")

  print(hype_text)

if __name__ == "__main__":
  try:
    if dbIsEmpty():
        promptForFavorites()

    favorites = load_favorites()
    matches = getMatches()

    if not matches:
        print("No World Cup matches today.")
    else:
        hype, prediction = findSpotlightMatch(matches, favorites)
        displayDash(hype, matches, favorites, prediction)
  except Exception as e:
    print(f"\n Something went wrong: {e}")