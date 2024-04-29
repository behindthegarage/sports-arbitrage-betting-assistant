import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('ODDS_API_KEY')

def log_error(message):
    # Get the current timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Format as desired

    # Construct the log message with the timestamp
    log_message = f"{timestamp} - {message}\n"

    # Append the log message to the file
    with open('error.log', 'a') as log_file:
        log_file.write(log_message)

def fetch_odds(sport, regions='us,us2', markets=['h2h', 'totals', 'spreads'], odds_format='decimal', date_format='iso', bookmakers: str = ''):
    # Example adjustment for market selection based on sport
    if 'championship_winner' in sport:
        markets = 'outrights'
    else:
        markets = ['h2h', 'totals', 'spreads'] # ,totals
        
    odds_results = {}
    for market in markets:
        params = {
            'api_key': API_KEY,
            'regions': regions,
            'markets': market,
            'oddsFormat': odds_format,
            'dateFormat': date_format,
            'bookmakers': bookmakers
        }
        odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params=params)
        if odds_response.status_code == 200:
            odds_data = odds_response.json()
            odds_results[market] = odds_data
            print(f"Successfully fetched {market} odds data for {sport}.")  # Debug message
        else:
            error_message = f"Error fetching {market} odds: {odds_response.status_code}, Response: {odds_response.json().get('message', '')}"
            log_error(error_message)
            print(error_message)  # Debug message
            odds_results[market] = None
    return odds_results



