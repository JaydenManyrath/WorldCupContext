import requests
import os

API_KEY = os.getenv("SPORTSAPI")
BASE_URL = "https://v3.football.api-sports.io/predictions"

headers = {"x-apisports-key": API_KEY}

def get_match_prediction(fixture_id):
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
  }

if __name__ == "__main__":
    prediction = get_match_prediction(1489406)

    print(prediction)