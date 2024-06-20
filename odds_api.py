import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

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

def fetch_odds(sport, regions='us,us2', markets='h2h,spreads,totals', odds_format='decimal', date_format='iso', bookmakers: str = ''):
    # Adjust markets for outrights if necessary
    if 'championship_winner' in sport:
        markets = 'outrights'
    
    params = {
        'api_key': API_KEY,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
        'bookmakers': bookmakers
    }
    odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params=params)
    if odds_response.status_code == 200:
        odds_data = odds_response.json()
        print(f"Successfully fetched odds data for {sport}. Markets: {markets}")  # Debug message
        return odds_data
    else:
        error_message = f"Error fetching odds: {odds_response.status_code}, Response: {odds_response.json().get('message', '')}"
        log_error(error_message)
        print(error_message)  # Debug message
        return None

def present_data(odds_data, selected_sports, selected_markets):
    print("Debug: Entering present_data function")
    print(f"Debug: Selected sports: {selected_sports}")
    print(f"Debug: Selected markets: {selected_markets}")
    print(f"Debug: Odds data keys: {odds_data.keys()}")

    all_data = []

    for sport in selected_sports:
        print(f"Debug: Processing sport: {sport}")
        if sport not in odds_data:
            print(f"Debug: No data for sport {sport}")
            continue

        for event in odds_data[sport]:
            print(f"Debug: Processing event: {event['id']}")
            event_data = {
                'sport': sport,
                'event_id': event['id'],
                'home_team': event['home_team'],
                'away_team': event['away_team'],
                'commence_time': event['commence_time']
            }

            for bookmaker in event['bookmakers']:
                for market in bookmaker['markets']:
                    if market['key'] in selected_markets:
                        for outcome in market['outcomes']:
                            key = f"{bookmaker['key']}_{market['key']}_{outcome['name']}"
                            event_data[key] = outcome.get('price')
                            if 'point' in outcome:
                                event_data[f"{key}_point"] = outcome['point']

            all_data.append(event_data)

    df = pd.DataFrame(all_data)
    print(f"Debug: Number of processed events: {len(df)}")
    print("Debug: DataFrame columns", df.columns)
    print("Debug: DataFrame shape", df.shape)
    print("Debug: DataFrame head")
    print(df.head())

    return df

# If you want to run this file independently, you can add a main function:
if __name__ == "__main__":
    # Example usage
    sport = "basketball_nba"
    odds_data = fetch_odds(sport)
    if odds_data:
        df = present_data({sport: odds_data}, [sport], ['h2h', 'spreads', 'totals'])
        print(df)