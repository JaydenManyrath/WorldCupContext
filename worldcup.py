from get_matches import get_matches
from favorites import (
  favorites_is_empty,
  select_favorite_teams,
  save_favorites,
  load_favorite_summaries
)
from spotlight import get_spotlight
from display import display_matches, display_spotlight, display_favorites
import time

def onboard_favorites_if_needed():
  if favorites_is_empty():
    selected_team_ids = select_favorite_teams()
    if selected_team_ids:
      save_favorites(selected_team_ids)

def main():
  onboard_favorites_if_needed()
  matches = get_matches() # api call
  display_matches(matches)
  time.sleep(60)
  spotlight = get_spotlight(matches) # api call
  display_spotlight(spotlight)
  favorite_summaries = load_favorite_summaries()
  display_favorites(favorite_summaries)

if __name__ == "__main__":
  main()
