import requests 
import os 
from dotenv import load_dotenv

load_dotenv() 

youtube_key = os.getenv('YOUTUBEAPI') 

def getHighlightVideo(match):
  team1 = match["teams"]["home"]["name"]
  team2 = match["teams"]["away"]["name"]
  searchQuery = f"{team1} vs {team2} World Cup Highlights"
  url = "https://www.googleapis.com/youtube/v3/search"
  params = {
        "part": "snippet",
        "q": searchQuery,
        "type": "video",       
        "maxResults": 1,       
        "key": youtube_key
    }
  response = requests.get(url, params=params)
  data = response.json()

  if("items" in data and len(data["items"]) > 0):
    video_id = data["items"][0]["id"]["videoId"]
    video_title = data["items"][0]["snippet"]["title"]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    return video_title, youtube_url
  else:
    return None, "No highlights found."

if __name__ == "__main__":
    title, link = getHighlightVideo("Argentina", "France")
    print(f"Watch {title}:")
    print(f"📺 {link}")