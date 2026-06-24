import os 
import requests
import google.generativeai as genai
import sqlite3
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
  conn = get_db
  row = conn.execute("SELECT id FROM teams WHERE LOWER(name) = LOWER(?)", (team_name,)).fetchone()
  if row:
    conn.execute("INSERT OR IGNORE INTO favorites (team_id) VALUES (?)," (row[0],))
    conn.commit()
    conn.close()
    return True
  else:
    conn.close()
    return False

def getMatches():
 


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
      found = saveTeam(team_input)
      if found:
        print(f"Added {team_input}")
      else:
        print(f" x {team_input} not found in World Cup teams. Check spelling.")

  # Takes match/matches from getMatches and prompts LLM for match contextualization. 
def getMatchHype(match):
  team1 = match["home_team_name"]
  team2 = match["away_team_name"]
    # Format the last 5 H2H results into a readable string
    h2h_summary = ""
   

    home_win = 
    draw = 
    away_win = 

    prompt = f"""You are a football pundit. Write a hype paragraph or two for the upcoming World Cup match between {team1} and {team2}.

    Their last 5 meetings:
    {h2h_summary}

    Current predictions: {team1} win {home_win}, Draw {draw}, {team2} win {away_win}.

  Include historical rivalry context from the results above, current stakes, and players to watch. Do not contradict the statistics provided."""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response

def getMatchsHype(teams):

  team_list = ", ".join([f"{m['home_team_name']} vs {m['away_team_name']}" for m in matches])

  prompt = f"""You are a football pundit. From this list of today's World Cup matches, pick the most exciting one and explain why it's the must-watch game of the day. Then write a hype paragraph for it.

  Matches: {team_list}"""

  model = genai.GenerativeModel('gemini-2.5-flash')
  response = model.generate_content(prompt)
  print("\n" + response.text)


  #Uses youtube API to find previous match highlights 
  #def getPreviousMatches(team1, team2):

if __name__ == "__main__":
  spotlightMatch = []
  if(dbIsEmpty()):
    promptForFavorites()

  favorites = load_favorites()

  for(match in getMatches()):
    if(match["home_team_id"] in favorites or match["away_team_id"] in favorites)
      spotlightMatch.append(match)

  if(len(spotlightMatch) == 0): #No favorites playing, let LLM pick 
    print("No favorites playing today, letting the AI pick the best match.\n")
    getMatchesHype(getMatches())

  elif(len(spotlightMatch) == 1): #Favorite team is playing
    getMatchHype(spotlightMatch[0])

  elif(len(spotlightMatch) > 1):
    print("\nMultiple matches with your favorite teams today. Pick one:\n")
    for i, match in enumerate(spotlightMatch):
      home = match["home_team_name"]
      away = match["away_team_name"]
      time = match["utc_date"]
      print(f"  [{i + 1}] {home} vs {away}  —  {time}")
    while True:
      try:
        choice = int(input("\n Enter a number for the game you would like to spotlight."))
        if(1 <= choice  len(spotlightMatch)):
          getMatchHype(spotlightMatch[choice - 1])
        else:
          print(f" Please enter a number between 1 and {len(spotlightMatch)}")
      except ValueError:
        print("Invalid input, please enter a number")
  

