import requests
import os

API_KEY = os.getenv("SPORTSAPI")
BASE_URL = "https://v3.football.api-sports.io/predictions"

headers = {"x-apisports-key": API_KEY}

"""def get_match_prediction(fixture_id):
  # make & store prediction API request
  params = {"fixture": fixture_id}
  response = requests.get(BASE_URL, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()

  if data["results"] == 0 or not data["response"]: return None
  prediction_data = data["response"][0]
  predictions = prediction_data["predictions"]
  teams = prediction_data["teams"]

  return {
        "fixture_id": fixture_id,
        "home_team": teams["home"]["name"],
        "away_team": teams["away"]["name"],
        "predicted_winner": predictions["winner"]["name"],
        "winner_comment": predictions["winner"]["comment"],
        "home_win_percent": predictions["percent"]["home"],
        "draw_percent": predictions["percent"]["draw"],
        "away_win_percent": predictions["percent"]["away"],
        "advice": predictions["advice"],
        "under_over": predictions["under_over"]
  }"""

def get_match_prediction(fixture_id):
    return {
        "fixture_id": fixture_id,
        "home_team": "Norway",
        "away_team": "France",
        "predicted_winner": "France",
        "winner_comment": "France are the stronger side on paper",
        "home_win_percent": "22%",
        "draw_percent": "28%",
        "away_win_percent": "50%",
        "advice": "France to win or draw",
        "under_over": "-0.5"
    }

if __name__ == "__main__":
    prediction = get_match_prediction(1489406)
    print(prediction)