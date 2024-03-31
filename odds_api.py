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


def fetch_sports(key: str) -> set[str]:
    sports_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports',
        params={'api_key': key}
    )
    if sports_response.status_code == 200:
        sports_data = sports_response.json()
        
        
        # Filter out sports with 'soccer' in their 'key'
        return {sport['key'] for sport in sports_data if 'soccer' not in sport['key'] and 'boxing' not in sport['key']}
    else:
        error_message = f"Error fetching odds: {sports_response.status_code}, Response: {sports_response.json()['message']}"
        log_error(error_message)
        # print(error_message)  # Optionally, you can still print it out or remove this line.
        return set()

def fetch_odds(sport, regions='us,us2', markets='h2h,spreads,totals', odds_format='decimal', date_format='iso', bookmakers: str = ''): # ,spreads,totals for testing
    params = {
        'api_key': API_KEY,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
        'bookmakers': bookmakers  # Include the bookmakers parameter here
    }
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params=params
    )
    if odds_response.status_code == 200:
        odds_data = odds_response.json()
        # Print fetched data for debugging and verification
        # print("Fetched data:")
        # print(odds_data)
        return odds_data
    else:
        error_message = f"Error fetching odds: {odds_response.status_code}, Response: {odds_response.json()['message']}"
        log_error(error_message)
        # print(error_message)  # Optionally, you can still print it out or remove this line.
        return None


