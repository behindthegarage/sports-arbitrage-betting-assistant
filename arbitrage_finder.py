def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    return (1/odds_a + 1/odds_b) * 100

def find_arbitrage_opportunities(odds_data):
    opportunities = []

    for event in odds_data:
        # Construct the event_name from home_team and away_team
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"

        # Extract all h2h markets from the bookmakers for this event
        h2h_markets = [bookmaker.get('markets', []) for bookmaker in event.get('bookmakers', []) if any(market['key'] == 'h2h' for market in bookmaker.get('markets', []))]

        # Iterate through each combination of bookmakers for the two outcomes
        for i, bookmaker_a in enumerate(event.get('bookmakers', [])):
            for market_a in bookmaker_a.get('markets', []):
                if market_a['key'] == 'h2h' and len(market_a['outcomes']) == 2:
                    odds_a = market_a['outcomes'][0].get('price')  # Odds for Team A from bookmaker_a

                    for j, bookmaker_b in enumerate(event.get('bookmakers', [])):
                        if i == j:  # Skip comparing the same bookmaker
                            continue

                        for market_b in bookmaker_b.get('markets', []):
                            if market_b['key'] == 'h2h' and len(market_b['outcomes']) == 2:
                                odds_b = market_b['outcomes'][1].get('price')  # Odds for Team B from bookmaker_b

                                # Calculate the arbitrage percentage for the current odds combination
                                arb_percentage = calculate_arbitrage_percentage(odds_a, odds_b)
                                if arb_percentage < 100:
                                    opportunities.append({
                                        'event_id': event.get('id'),
                                        'event_name': event_name,
                                        'bookmaker_a': bookmaker_a.get('title'),
                                        'odds_a': odds_a,
                                        'bookmaker_b': bookmaker_b.get('title'),
                                        'odds_b': odds_b,
                                        'arb_percentage': arb_percentage,
                                    })

    return opportunities


