import os 
from google 
import genai from google.genai 
import types 
my_api_key = os.getenv('GOOGLEAPI') 
genai.api_key = my_api_key 
football_key = os.getenv('FOOTBALLAPI') 
youtube_key = os.getenv('YOUTUBEAPI') 

print(football_key)
 print(youtube_key) 
 print(google_key) 
 
 # Take input from user for favorite teams, saves it to database, and then prompts for specific match date while(input() is not None): 
 favorite_team = input() 
 
 # Gets all matches from match data compares it to listed favorites. If none, then all matches are given to LLM. 
 def getMatches(date): 
  
  # Takes match/matches from getMatches and prompts LLM for match contextualization. 
  def getMatchHype(List teams): 
    
  #Uses youtube API to find previous match highlights 
  def getPreviousMatches(team1, team2):