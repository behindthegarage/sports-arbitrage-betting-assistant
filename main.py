from dotenv import load_dotenv
import os
from odds_api import fetch_odds, fetch_sports, log_error
from arbitrage_finder import find_arbitrage_opportunities
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access the API key
API_KEY = os.getenv('ODDS_API_KEY')

# Clear the error.log file before running the script
with open('error.log', 'w') as file:
    file.write('')
    
# Clear the odds_data.csv file before running the script
with open('odds_data.csv', 'w') as file:
    file.write('')

def present_data(odds_data, sport, combined_df):
    flattened_data = []

    for event in odds_data:
        event_id = event.get('id')
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
        for bookmaker in event.get('bookmakers', []):
            bookmaker_name = bookmaker.get('title')
            for market in bookmaker.get('markets', []):
                market_key = market.get('key')
                if market_key in ['h2h', 'spreads', 'totals']:
                    for outcome in market.get('outcomes', []):
                        data = {
                            'sport': sport,
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

    # If combined_df is empty, directly assign df to it. Otherwise, concatenate.
    if combined_df.empty:
        combined_df = df.copy()
    else:
        # Concatenate df with combined_df without reindexing, ensuring all columns in df are included
        # Using 'sort=False' to avoid alphabetically sorting columns
        combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)

    return combined_df

def present_opportunities(opportunities):
    if not opportunities:
        print("No arbitrage opportunities found.")
        return

    # Convert the list of opportunity dictionaries to a DataFrame
    df = pd.DataFrame(opportunities)
    
    # Convert arb_percentage to a formatted string only when displaying it
    if not df.empty:
        df['arb_percentage'] = df['arb_percentage'].apply(lambda x: f"{x:.2f}%")

    # Ensure all expected columns are present, adding defaults for any that might be missing
    for column in ['event_name', 'market_type', 'outcome_name', 'point', 'bookmaker', 'odds', 'comparison_bookmaker', 'comparison_odds', 'arb_percentage']:
        if column not in df.columns:
            df[column] = 'N/A'  # Use an appropriate default value

    # Handle potential missing values in 'point' column for h2h markets
    df['point'] = df['point'].fillna('N/A')

    # Define the order of columns for display
    columns_order = ['event_name', 'market_type', 'outcome_name', 'point', 'bookmaker', 'odds', 'comparison_bookmaker', 'comparison_odds', 'arb_percentage']

    # Reorder the DataFrame according to 'columns_order', ensuring it matches our desired output structure
    df = df[columns_order]

    # Convert DataFrame to a string and print it for presentation
    print(df.to_string(index=False))

# Example usage (assuming 'opportunities' is populated with arbitrage opportunities according to the new structure)
# present_opportunities(opportunities)

def main():
    # Fetch list of all available sports
    # available_sports = fetch_sports(API_KEY)
    available_sports = fetch_sports(API_KEY) # For testing purposes, limit to ['basketball_nba']
    
    # Initialize an empty DataFrame to hold data for all sports
    combined_df = pd.DataFrame()
    
    # List to store all found arbitrage opportunities
    all_opportunities = []
    
    # Dictionary to track arbitrage opportunities count per sport
    opportunities_summary = {}
    
    # Iterate over each available sport
    for sport in available_sports:
        # print(f"Fetching odds for {sport}...")
        regions = 'us,us2'  # Focusing on US region
        markets = 'h2h,spreads,totals' # ,spreads,totals'  # Markets
        odds_format = 'decimal'  # Using decimal format for odds
        date_format = 'iso'  # ISO date format
        # Bookmakers lists
        
        # Max bookmakers (limit 40)
        # bookmakers_list = "betfair_sb_uk,betmgm,betonlineag,betparx,betrivers,betus,betvictor,betway,bovada,boylesports,casumo,coral,draftkings,espnbet,everygame,fanduel,fliff,grosvenor,hardrockbet,ladbrokes_uk,leovegas,livescorebet,lowvig,marathonbet,matchbook,mybookieag,nordicbet,onexbet,paddypower,pointsbetus,sisportsbook,skybet,sport888,superbook,suprabets,tipico_us,virginbet,williamhill_us,windcreek,wynnbet"
        
        # Michigan legal bookmakers
        # bookmakers_list = "betmgm,betrivers,draftkings,fanduel,wynnbet,espnbet,sisportsbook,williamhill_us,pointsbetus,betparx"
        
        # Current user funded bookmakers
        bookmakers_list = "betmgm,draftkings,fanduel,williamhill_us" ## betparx,betrivers,espnbet to be added
 
        # markets='h2h,spreads,totals' for testing
        odds_data = fetch_odds(sport=sport, regions=regions, markets='h2h,spreads,totals', odds_format=odds_format, date_format=date_format, bookmakers=bookmakers_list)
        
        if odds_data:
            print(f"Fetched odds data for {sport}.")
            combined_df = present_data(odds_data, sport, combined_df)
            opportunities = find_arbitrage_opportunities(odds_data)
            if opportunities:
                print(f"Arbitrage Opportunities Found for {sport}:")
                present_opportunities(opportunities)
                any_opportunities_found = True  # Update the flag since opportunities were found
                
                # Store opportunities for later display
                all_opportunities.extend(opportunities)
 
                 # Update the summary dictionary
                opportunities_summary[sport] = len(opportunities)
                               
            else:
                print(f"No arbitrage opportunities found for {sport}.")
        else:
            error_message = f"Failed to fetch odds data for {sport}."
            log_error(error_message)  # Log the error instead of printing
            # print(error_message)  # Optionally, you can still print it out or remove this line.

    # Write the combined DataFrame to a single CSV file after processing all sports
    print (combined_df)
    combined_df.to_csv('odds_data.csv', index=False)
    print("All sports data has been written to odds_data.csv")
    
    # Display all arbitrage opportunities found
    if all_opportunities:
        print("\nArbitrage Opportunities Found:")
        present_opportunities(all_opportunities)

        # Display the summary of arbitrage opportunities found
        print("\nSummary of Arbitrage Opportunities Found:")
        for sport, count in opportunities_summary.items():
            print(f"{sport}: {count} opportunities")
    else:
        print("No arbitrage opportunities were found across all sports.")
    
if __name__ == "__main__":
    main()
