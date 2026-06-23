import os 
import requests
import google.generativeai as genai
from dotenv import load_dotenv

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
 #TBD 

def load_favorites():
    conn = get_db()
    rows = conn.execute("""
        SELECT teams.name FROM favorites
        JOIN teams ON favorites.team_id = teams.id
    """).fetchall()
    conn.close()
    return [row[0] for row in rows]

def promptForFavorites():
  print("Enter your favorite national teams. Type 'DONE' when finished.")
  while True:
    team_input = input("> ").strip()
    if(team_input.upper() == "DONE"):
      break
    if team_input:
      saveTeam(team_input)
      print(f"Added {team_input}")

  # Takes match/matches from getMatches and prompts LLM for match contextualization. 
def getMatchHype(team1, team2, h2h_data, prediction_data):
    # Format the last 5 H2H results into a readable string
    h2h_summary = ""
    for match in h2h_data[:5]:
        date = match["date"]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        home_score = match["goals"]["home"]
        away_score = match["goals"]["away"]
      h2h_summary += f"\n- {date}: {home} {home_score}-{away_score} {away}"

    home_win = prediction_data["percent"]["home"]
    draw = prediction_data["percent"]["draw"]
    away_win = prediction_data["percent"]["away"]

    prompt = f"""You are a football pundit. Write a hype paragraph or two for the upcoming World Cup match between {team1} and {team2}.

    Their last 5 meetings:
    {h2h_summary}

    Current predictions: {team1} win {home_win}, Draw {draw}, {team2} win {away_win}.

  Include historical rivalry context from the results above, current stakes, and players to watch. Do not contradict the statistics provided."""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response

  #Uses youtube API to find previous match highlights 
  #def getPreviousMatches(team1, team2):

if __name__ == "__main__":
