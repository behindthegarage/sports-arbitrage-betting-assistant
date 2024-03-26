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

def present_data(odds_data, sport, combined_df):
    # Initialize an empty list to hold the flattened data
    flattened_data = []

    # Iterate over each event in the fetched odds data
    for event in odds_data:
        event_id = event.get('id')
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"  # Construct event name
        # Extract data from each bookmaker within the event
        for bookmaker in event.get('bookmakers', []):
            bookmaker_name = bookmaker.get('title')
            # And now extract and handle each market within the bookmaker data
            for market in bookmaker.get('markets', []):
                if market.get('key') == 'h2h':  # Assuming we're interested in 'h2h' markets
                    for outcome in market.get('outcomes', []):
                        # Here, you might want to handle how you present the odds and outcomes
                        flattened_data.append({
                            'sport': sport,
                            'event_id': event_id,
                            'event_name': event_name,
                            'bookmaker': bookmaker_name,
                            'team': outcome.get('name'),
                            'price': outcome.get('price')
                        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(flattened_data)

    # Append this DataFrame to the combined DataFrame
    combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

def present_opportunities(opportunities):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(opportunities)
    
    # Specify the order of columns, now including 'bookmaker_a' and 'bookmaker_b'
    columns_order = ['event_name', 'bookmaker_a', 'odds_a', 'bookmaker_b', 'odds_b', 'arb_percentage']
    df = df[columns_order]

    # Format the 'arb_percentage' to two decimal places
    df['arb_percentage'] = df['arb_percentage'].apply(lambda x: f"{x:.2f}%")

    # Correct way to fill NaN values in 'event_name' without triggering a warning
    df['event_name'] = df['event_name'].fillna('N/A')

    # Print the DataFrame
    print(df.to_string(index=False))

def main():
    # Fetch list of all available sports
    available_sports = fetch_sports(API_KEY)
    
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
        markets = 'h2h'  # Markets
        odds_format = 'decimal'  # Using decimal format for odds
        date_format = 'iso'  # ISO date format
        # Bookmakers lists
        
        # Max bookmakers (limit 40)
        # bookmakers_list = "betfair_sb_uk,betmgm,betonlineag,betparx,betrivers,betus,betvictor,betway,bovada,boylesports,casumo,coral,draftkings,espnbet,everygame,fanduel,fliff,grosvenor,hardrockbet,ladbrokes_uk,leovegas,livescorebet,lowvig,marathonbet,matchbook,mybookieag,nordicbet,onexbet,paddypower,pointsbetus,sisportsbook,skybet,sport888,superbook,suprabets,tipico_us,virginbet,williamhill_us,windcreek,wynnbet"
        
        # Michigan legal bookmakers
        # bookmakers_list = "betmgm,betrivers,draftkings,fanduel,wynnbet,espnbet,sisportsbook,williamhill_us,pointsbetus,betparx"
        
        # Current user funded bookmakers
        bookmakers_list = "betmgm,draftkings,fanduel" # Seeded bookmakers (odds-api token usage = 66)
 
        odds_data = fetch_odds(sport, regions, markets, odds_format, date_format, bookmakers_list)
        
        if odds_data:
            # print(f"Fetched odds data for {sport}.")
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
    combined_df.to_csv('all_sports_odds_data.csv', index=False)
    print("All sports data has been written to all_sports_odds_data.csv")
    
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
