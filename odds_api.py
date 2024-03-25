import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('ODDS_API_KEY')

def fetch_sports(key: str) -> set[str]:
    sports_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports',
        params={'api_key': key}
    )
    if sports_response.status_code == 200:
        sports_data = sports_response.json()
        # Directly iterate over sports_data as it's already a list
        return {sport['key'] for sport in sports_data}
    else:
        print(f"Error fetching sports: {sports_response.status_code}")
        return set()

def fetch_odds(sport, regions='us,us2', markets='h2h', odds_format='decimal', date_format='iso', bookmakers: str = ''):
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
        response_content = odds_response.text  # or odds_response.json() if the response is JSON
        print(f"Error fetching odds: {odds_response.status_code}, Response: {response_content}")

