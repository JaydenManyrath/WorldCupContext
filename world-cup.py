import os 
import requests
#import google.generativeai as genai
from dotenv import load_dotenv
from database import initialize_database, fetch_all, get_connection
from datetime import date

initialize_database()
tables = fetch_all("SELECT name FROM sqlite_master WHERE type ='table';")
print(tables)

# returns upcoming matches for a given date
def show_todays_matches():
  today = date.today().isoformat()



#load_dotenv() 

google_key = os.getenv('GOOGLEAPI') 
football_key = os.getenv('FOOTBALLAPI') 
youtube_key = os.getenv('YOUTUBEAPI') 
genai.configure(api_key=google_key)

 ## If database is empty ask user for favorite teams and populate 
 ## If not load database 
 ## Prompt for match date in interest
 ## Check if match date is already in database, if so return previous results to save API calls
 ## Check if match is past or future 
 ## Else check if favorite teams are playing
  ##  If one return contextualization of that match
  ## If multiple then make user choose one of the matches that their favorites are playing in
  ## If none then LLM chooses best match to watch
  ## Return most recent faceoff highlights 
 
print("Welcome to the World Cup Hype Engine!")
print("Enter your favorite national teams. Type 'DONE' when finished.")
 # Take input from user for favorite teams, saves it to database, and then prompts for specific match date while(input() is not None): 
#while True:
  #team_input = input("> ").strip()
 # Gets all matches from match data compares it to listed favorites. If none, then all matches are given to LLM. 
 #def getMatches(date): 
  
  # Takes match/matches from getMatches and prompts LLM for match contextualization. 
def getMatchHype(team1, team2): 
  model = genai.GenerativeModel('gemini-2.5-flash')
  prompt = f"You are a football pundit. Write a hype paragraph or two summary for the upcoming World Cup match between {team1} and {team2}. Include any background information, historical rivalry, current stakes, or players to watch."
  response = model.generate_content(prompt)
  return response

  #Uses youtube API to find previous match highlights 
  #def getPreviousMatches(team1, team2):

#if __name__ == "__main__":