import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from odds_api import fetch_odds, log_error
from arbitrage_finder import find_arbitrage_opportunities
from sports_selection import fetch_sports
import json

# Load environment variables
load_dotenv()
API_KEY = os.getenv('ODDS_API_KEY')

def present_data(odds_data, selected_sports, selected_markets):
    flattened_data = []

    st.write("Debug: Entering present_data function")
    st.write(f"Debug: Selected sports: {selected_sports}")
    st.write(f"Debug: Selected markets: {selected_markets}")
    st.write(f"Debug: Odds data keys: {odds_data.keys()}")

    for sport_key in selected_sports:
        st.write(f"Debug: Processing sport: {sport_key}")
        for event in odds_data.get(sport_key, []):
            st.write(f"Debug: Processing event: {event.get('id')}")
            event_id = event.get('id')
            event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
            for bookmaker in event.get('bookmakers', []):
                bookmaker_name = bookmaker.get('title')
                for market in bookmaker.get('markets', []):
                    market_key = market.get('key')
                    if market_key in selected_markets:
                        st.write(f"Debug: Processing market: {market_key}")
                        for outcome in market.get('outcomes', []):
                            data = {
                                'sport': sport_key,
                                'event_id': event_id,
                                'event_name': event_name,
                                'bookmaker': bookmaker_name,
                                'market_type': market_key,
                                'team': outcome.get('name'),
                                'price': outcome.get('price'),
                                'point': outcome.get('point')
                            }
                            if market_key == 'h2h':
                                data['point'] = None
                            elif market_key == 'spreads':
                                data['point'] = outcome.get('point')
                            elif market_key == 'totals':
                                data['point'] = f"{market.get('totals')} {outcome.get('name')}"
                            
                            flattened_data.append(data)

    st.write(f"Debug: Number of flattened data entries: {len(flattened_data)}")
    return pd.DataFrame(flattened_data)

def main():
    st.title("Sports Arbitrage Finder")

    # Fetch and categorize sports
    categorized_sports = fetch_sports()
    if not categorized_sports:
        st.error("Failed to fetch sports.")
        return

    # Sport selection
    st.header("Select Sports")
    selected_sports = []
    for category, sports in categorized_sports.items():
        st.subheader(category)
        for sport in sports:
            if st.checkbox(sport, key=sport):
                selected_sports.append(sport)

    if not selected_sports:
        st.warning("Please select at least one sport.")
        return

    st.write(f"Selected sports: {', '.join(selected_sports)}")

    # Market selection
    st.header("Select Markets")
    markets = st.multiselect("Choose markets", ['h2h', 'spreads', 'totals'], default=['h2h'])

    # Fetch odds button
    if st.button("Fetch Odds and Find Arbitrage Opportunities"):
        if not markets:
            st.warning("Please select at least one market type.")
            return

        combined_df = pd.DataFrame()
        all_opportunities = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, sport_key in enumerate(selected_sports):
            status_text.text(f"Fetching odds for {sport_key}...")

            regions = 'us,us2'
            odds_format = 'decimal'
            date_format = 'iso'
            bookmakers_list = "betmgm,draftkings,espnbet,fanduel,williamhill_us"

            odds_data = fetch_odds(sport=sport_key, regions=regions, markets=','.join(markets), odds_format=odds_format, date_format=date_format, bookmakers=bookmakers_list)

            st.write(f"Debug: Odds data for {sport_key}:")
            st.write(odds_data)

            if odds_data:
                sport_df = present_data({sport_key: odds_data}, [sport_key], markets)
                st.write(f"Debug: Sport DataFrame for {sport_key}:")
                st.write(sport_df)
                combined_df = pd.concat([combined_df, sport_df], ignore_index=True, sort=False)
                opportunities = find_arbitrage_opportunities(odds_data)
                all_opportunities.extend(opportunities)

            progress_bar.progress((i + 1) / len(selected_sports))

        status_text.text("Processing complete!")

        # Debug information
        # st.write("Debug: DataFrame columns", combined_df.columns)
        # st.write("Debug: DataFrame shape", combined_df.shape)
        # st.write("Debug: DataFrame head", combined_df.head())

        # Display odds data
        st.header("Odds Data")
        st.dataframe(combined_df)

        # Filter odds data
        st.header("Filter Odds Data")
        if 'market_type' in combined_df.columns:
            market_filter = st.multiselect("Filter by market type", markets, default=markets)
            filtered_df = combined_df[combined_df['market_type'].isin(market_filter)]
            st.dataframe(filtered_df)
        else:
            st.warning("Market type information is not available in the data.")
            st.dataframe(combined_df)

        # Save odds data to CSV
        csv = combined_df.to_csv(index=False)
        st.download_button(
            label="Download Odds Data as CSV",
            data=csv,
            file_name="odds_data.csv",
            mime="text/csv",
        )

        # Display arbitrage opportunities
        st.header("Arbitrage Opportunities")
        if all_opportunities:
            opp_df = pd.DataFrame(all_opportunities)
            opp_df['arb_percentage'] = opp_df['arb_percentage'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(opp_df)
        else:
            st.info("No arbitrage opportunities were found across all sports.")

if __name__ == "__main__":
    main()