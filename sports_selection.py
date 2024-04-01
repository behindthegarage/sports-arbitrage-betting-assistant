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
        # print(sports_data)
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
    """Prompt user to select multiple sports categories by numbers."""
    print("Available Sports Categories:")
    categories = list(categorized_sports.keys())
    
    # Display categories with corresponding numbers
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}: {len(categorized_sports[category])} sports")
    
    # Get user input
    selected_indices = input("Enter the numbers of the categories to fetch odds for (separated by commas): ")
    
    # Process user input
    selected_indices = [int(index.strip()) for index in selected_indices.split(',')]
    
    # Collect selected sports based on user input
    selected_sports = []
    for index in selected_indices:
        if 1 <= index <= len(categories):
            selected_sports.extend(categorized_sports[categories[index - 1]])
    
    return selected_sports


