import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve API key from environment variables
API_KEY = os.getenv('ODDS_API_KEY')

def fetch_sports():
    """Fetch and categorize available sports from the Odds API."""
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports',
        params={'api_key': API_KEY}
    )
    if sports_response.status_code == 200:
        sports_data = sports_response.json()
        print(sports_data)
        # Example categorization (further refinement needed based on actual API response structure)
        categorized_sports = categorize_sports(sports_data)
        return categorized_sports
    else:
        print(f"Error fetching sports: {sports_response.status_code}")
        return None

def categorize_sports(sports_data):
    """Categorize sports data into groups (e.g., by type)."""
    categories = {
        'Football': [],
        'Basketball': [],
        'Baseball': [],
        'Hockey': [],
        'Soccer': [],
        # Add other categories as needed
    }
    for sport in sports_data:
        # Example categorization logic (adjust based on the API response structure and desired categories)
        if 'football' in sport['key'].lower():
            categories['Football'].append(sport['key'])
        elif 'basketball' in sport['key'].lower():
            categories['Basketball'].append(sport['key'])
        elif 'baseball' in sport['key'].lower():
            categories['Baseball'].append(sport['key'])
        elif 'hockey' in sport['key'].lower():
            categories['Hockey'].append(sport['key'])
        elif 'soccer' in sport['key'].lower():
            categories['Soccer'].append(sport['key'])
        # Repeat for other categories
    
    return categories

def user_select_sports(categorized_sports):
    """Prompt user to select sports for odds fetching."""
    print("Available Sports Categories:")
    for category, sports in categorized_sports.items():
        print(f"{category}: {len(sports)} sports")
    
    selected_category = input("Enter a category to fetch odds for: ")
    # You can extend this logic to allow selection of multiple categories or specific sports within a category
    
    return categorized_sports.get(selected_category, [])

