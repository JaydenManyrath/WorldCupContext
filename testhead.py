import json
import requests

api_key = "d444d49baf78a9b6f78ded2a941af97e"

headers = {
    "x-apisports-key": api_key
}

fixture_id = 1489406

params = {
  "fixture": fixture_id
}

url = "https://v3.football.api-sports.io/predictions"

response = requests.get(
    url, headers=headers, params=params
)

data = response.json()

print(response.status_code)
print(json.dumps(response.json(), indent=2))