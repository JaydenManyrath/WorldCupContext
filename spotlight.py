import os
import re
import questionary
import google.generativeai as genai
from dotenv import load_dotenv
from database import get_connection
from prediction import get_match_prediction

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLEAPI")

if GOOGLE_API_KEY:
  genai.configure(api_key=GOOGLE_API_KEY)

def get_favorite_api_ids():
  with get_connection() as conn:
    cursor = conn.execute("""
      SELECT teams.api_football_id
      FROM favorites
      JOIN teams ON favorites.team_id = teams.id
      WHERE teams.api_football_id IS NOT NULL
    """)
    return [row["api_football_id"] for row in cursor.fetchall()]

def get_favorite_matches_today(matches):
  favorite_api_ids = get_favorite_api_ids()
  favorite_matches = []
  for match in matches:
    home_id = match["teams"]["home"]["id"]
    away_id = match["teams"]["away"]["id"]
    if home_id in favorite_api_ids or away_id in favorite_api_ids:
      favorite_matches.append(match)
  return favorite_matches

def format_match_choice(match):
  home = match["teams"]["home"]["name"]
  away = match["teams"]["away"]["name"]
  kickoff = match["fixture"]["date"]
  return f"{home} vs {away} — {kickoff}"

def choose_favorite_match(matches):
  choices = []
  for match in matches:
    choices.append(
      questionary.Choice(
        title=format_match_choice(match),
        value=match
      )
    )
  return questionary.select(
    "Multiple favorite teams are playing today. Pick a spotlight match:",
    choices=choices
  ).ask()

def choose_ai_match(matches):
  if not GOOGLE_API_KEY:
    return matches[0]
  match_options = "\n".join([
    f"{match['fixture']['id']}: {match['teams']['home']['name']} vs {match['teams']['away']['name']}"
    for match in matches
  ])

  prompt = f"""
    You are a World Cup analyst.
    Choose the single most interesting match for a casual fan to watch today.
    Return ONLY the fixture id number.
    Matches:
    {match_options}
    """
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content(prompt)
  fixture_id_match = re.search(r"\d+", response.text)

  if not fixture_id_match:
    return matches[0]

  selected_fixture_id = int(fixture_id_match.group())
  for match in matches:
    if match["fixture"]["id"] == selected_fixture_id:
      return match
  return matches[0]

def build_prediction_text(prediction, home, away):
  if not prediction:
      return "No prediction available."

  return (
      f"{home}: {prediction['home_win_percent']}\n"
      f"Draw: {prediction['draw_percent']}\n"
      f"{away}: {prediction['away_win_percent']}"
  )


def select_spotlight_match(matches):
  favorite_matches = get_favorite_matches_today(matches)
  if len(favorite_matches) == 1:
    return favorite_matches[0]
  if len(favorite_matches) > 1:
    return choose_favorite_match(favorite_matches)
  return choose_ai_match(matches)

def generate_hype(match, prediction):
  home = match["teams"]["home"]["name"]
  away = match["teams"]["away"]["name"]
  prediction_text = build_prediction_text(prediction, home, away)
  if not GOOGLE_API_KEY:
    return f"{home} vs {away} is today's spotlight match.\n\nPrediction:\n{prediction_text}"
  prompt = f"""
  You are a football pundit writing for casual World Cup fans.
  Write one short hype paragraph for the match between {home} and {away}.
  Prediction context:
  {prediction_text}
  Explain why this match matters. Mention stakes, style matchup, key players to watch, and storylines to watch.
  Do not contradict the prediction context.
  """
  model = genai.GenerativeModel("gemini-2.5-flash")
  response = model.generate_content(prompt)
  return response.text

def get_spotlight(matches):
  if not matches:
    return None
  selected_match = select_spotlight_match(matches)
  if selected_match is None:
    return None
  fixture_id = selected_match["fixture"]["id"]
  try:
    prediction = get_match_prediction(fixture_id)
  except Exception:
    prediction = None
  hype = generate_hype(selected_match, prediction)
  return {
    "match": selected_match,
    "prediction": prediction,
    "hype": hype
  }