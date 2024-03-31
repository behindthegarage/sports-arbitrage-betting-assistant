from dotenv import load_dotenv
import os
from odds_api import fetch_odds, log_error
from arbitrage_finder import find_arbitrage_opportunities
from sports_selection import fetch_sports, user_select_sports
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv('ODDS_API_KEY')

def present_data(odds_data, selected_sports, combined_df):
    flattened_data = []

    for sport_key in selected_sports:
        for event in odds_data.get(sport_key, []):
            event_id = event.get('id')
            event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
            for bookmaker in event.get('bookmakers', []):
                bookmaker_name = bookmaker.get('title')
                for market in bookmaker.get('markets', []):
                    market_key = market.get('key')
                    if market_key in ['h2h', 'spreads', 'totals']:
                        for outcome in market.get('outcomes', []):
                            data = {
                                'sport': sport_key,
                                'event_id': event_id,
                                'event_name': event_name,
                                'bookmaker': bookmaker_name,
                                'market_type': market_key,
                                'team': outcome.get('name'),
                                'price': outcome.get('price'),
                                'point': outcome.get('point', None)  # None if not applicable
                            }
                            flattened_data.append(data)

    df = pd.DataFrame(flattened_data)
    if combined_df.empty:
        combined_df = df.copy()
    else:
        combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
    return combined_df

def present_opportunities(opportunities):
    if not opportunities:
        print("No arbitrage opportunities found.")
        return
    df = pd.DataFrame(opportunities)
    if not df.empty:
        df['arb_percentage'] = df['arb_percentage'].apply(lambda x: f"{x:.2f}%")
    for column in ['event_name', 'market_type', 'outcome_name', 'point', 'bookmaker', 'odds', 'comparison_bookmaker', 'comparison_odds', 'arb_percentage']:
        if column not in df.columns:
            df[column] = 'N/A'
    df['point'] = df['point'].fillna('N/A')
    columns_order = ['event_name', 'market_type', 'outcome_name', 'point', 'bookmaker', 'odds', 'comparison_bookmaker', 'comparison_odds', 'arb_percentage']
    df = df[columns_order]
    print(df.to_string(index=False))

def main():
    # Clear the error.log and odds_data.csv file before running the script
    with open('error.log', 'w') as file:
        file.write('')
    with open('odds_data.csv', 'w') as file:
        file.write('')
    
    # Fetch and categorize sports
    categorized_sports = fetch_sports()
    if not categorized_sports:
        print("Failed to fetch sports.")
        return
    
    # Let the user select sports based on categories
    selected_sports = user_select_sports(categorized_sports)
    if not selected_sports:
        print("No sports selected for odds fetching.")
        return
    
    print(f"Selected sports for odds fetching: {selected_sports}")
    
    # Initialize an empty DataFrame to hold data for all sports
    combined_df = pd.DataFrame()
    
    # List to store all found arbitrage opportunities
    all_opportunities = []
    
    # Fetch odds for selected sports and find arbitrage opportunities
    for sport_key in selected_sports:
        print(f"Fetching odds for {sport_key}...")
        # define regions
        regions = 'us,us2'
        markets = 'h2h,spreads,totals'
        odds_format = 'decimal'
        date_format = 'iso'
        
        # Bookmakers lists
        # Max bookmakers (limit 40)
        # bookmakers_list = "betfair_sb_uk,betmgm,betonlineag,betparx,betrivers,betus,betvictor,betway,bovada,boylesports,casumo,coral,draftkings,espnbet,everygame,fanduel,fliff,grosvenor,hardrockbet,ladbrokes_uk,leovegas,livescorebet,lowvig,marathonbet,matchbook,mybookieag,nordicbet,onexbet,paddypower,pointsbetus,sisportsbook,skybet,sport888,superbook,suprabets,tipico_us,virginbet,williamhill_us,windcreek,wynnbet"
        
        # Michigan legal bookmakers
        # bookmakers_list = "betmgm,betrivers,draftkings,fanduel,wynnbet,espnbet,sisportsbook,williamhill_us,pointsbetus,betparx"
        
        # Current user funded bookmakers
        bookmakers_list = "betmgm,draftkings,fanduel,williamhill_us" ## betparx,betrivers,espnbet to be added
        
        # Fetch odds data
        odds_data = fetch_odds(sport=sport_key, regions=regions, markets='h2h,spreads,totals', odds_format=odds_format, date_format=date_format, bookmakers=bookmakers_list)
        # odds_data = fetch_odds(sport=sport_key)
        if odds_data:
            combined_df = present_data({sport_key: odds_data}, selected_sports, combined_df)
            opportunities = find_arbitrage_opportunities(odds_data)
            if opportunities:
                print(f"Arbitrage Opportunities Found for {sport_key}:")
                present_opportunities(opportunities)
                all_opportunities.extend(opportunities)
            else:
                print(f"No arbitrage opportunities found for {sport_key}.")
    
    # Write the combined DataFrame to a single CSV file after processing all sports
    combined_df.to_csv('odds_data.csv', index=False)
    print("All sports data has been written to odds_data.csv")
    
    # Display all arbitrage opportunities found
    if all_opportunities:
        print("\nArbitrage Opportunities Found:")
        present_opportunities(all_opportunities)
    else:
        print("No arbitrage opportunities were found across all sports.")

if __name__ == "__main__":
    main()
