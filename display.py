from datetime import datetime
from get_matches import get_matches
from database import get_connection
from favorites import load_favorite_summaries
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

# displays todays games
def format_time(match):
  raw_date = match["fixture"]["date"]
  dt = datetime.fromisoformat(raw_date)
  return dt.strftime("%I:%M %p").lstrip("0")

def format_score(match):
  home_goals = match["goals"]["home"]
  away_goals = match["goals"]["away"]
  if home_goals is None or away_goals is None:
      return "vs"

  return f"{home_goals}-{away_goals}"

def display_matches(matches):
    print("\nTODAY'S WORLD CUP MATCHES")
    print("-" * 60)

    for match in matches:
      time = format_time(match)
      home = match["teams"]["home"]["name"]
      away = match["teams"]["away"]["name"]
      score = format_score(match)
      status = match["fixture"]["status"]["short"]
      venue = match["fixture"]["venue"]["name"]
      city = match["fixture"]["venue"]["city"]
      print(f"{time:<8} {home:<18} {score:^5} {away:<18} [{status}]")
      print(f"         {venue}, {city}")
      print()

def get_team_name(team_id):
  if team_id is None:
    return "TBD"
  with get_connection() as conn:
    row = conn.execute(
      "SELECT name FROM teams WHERE id = ?",
      (team_id,)
    ).fetchone()
  return row["name"] if row else "TBD"

def format_db_match(match):
  if match is None:
    return "No match found"
  home = get_team_name(match["home_team_id"])
  away = get_team_name(match["away_team_id"])
  home_score = match["home_team_score"]
  away_score = match["away_team_score"]
  if home_score is None or away_score is None:
    score = "vs"
  else:
    score = f"{home_score}-{away_score}"
  dt = datetime.fromisoformat(match["utc_date"].replace("Z", "+00:00")).astimezone(NY)
  time = dt.strftime("%b %d, %I:%M %p").replace(" 0", " ")
  return f"{time} | {home} {score} {away}"

def display_favorites(favorite_summaries):
  print("\nFAVORITE TEAM MATCHES")
  print("-" * 60)
  if not favorite_summaries:
    print("No favorite teams selected.")
    return
  for summary in favorite_summaries:
    print(f"\n{summary['team_name']}")
    print("  Previous:")
    print(f"    {format_db_match(summary['previous_match'])}")
    print("  Next:")
    print(f"    {format_db_match(summary['next_match'])}")
  

# display spotlight games

def format_spotlight_match(match):
  home = match["teams"]["home"]["name"]
  away = match["teams"]["away"]["name"]
  venue = match["fixture"]["venue"]["name"]
  city = match["fixture"]["venue"]["city"]
  time = format_time(match)
  return f"{time} | {home} vs {away} — {venue}, {city}"

def display_prediction(prediction):
  if not prediction:
    print("Prediction unavailable.")
    return
  print(f"{prediction['home_team']}: {prediction['home_win_percent']}")
  print(f"Draw: {prediction['draw_percent']}")
  print(f"{prediction['away_team']}: {prediction['away_win_percent']}")

def display_spotlight(spotlight):
  print("\nSPOTLIGHT MATCH")
  print("-" * 60)
  if not spotlight:
    print("No spotlight match available.")
    return
  match = spotlight["match"]
  prediction = spotlight["prediction"]
  hype = spotlight["hype"]
  print(format_spotlight_match(match))
  print("\nPrediction")
  print("-" * 60)
  display_prediction(prediction)
  print("\nWhy it matters")
  print("-" * 60)
  print(hype)


#display favorite team's upcoming & previous matches 

if __name__ == "__main__":
  favorite_summaries = load_favorite_summaries()
  display_favorites(favorite_summaries)