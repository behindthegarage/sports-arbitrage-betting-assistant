def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    return (1/odds_a + 1/odds_b) * 100

def find_arbitrage_opportunities(odds_data):
    
    opportunities = []
    for event in odds_data:
        # Construct the event_name from home_team and away_team
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
        for bookmaker in event.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market['key'] == 'h2h' and len(market['outcomes']) == 2:
                    odds_a = market['outcomes'][0].get('price')
                    odds_b = market['outcomes'][1].get('price')
                    arb_percentage = calculate_arbitrage_percentage(odds_a, odds_b)
                    if arb_percentage < 100:
                        opportunities.append({
                            'event_id': event.get('id'),
                            'event_name': event_name,  # Use the constructed event name
                            'bookmaker': bookmaker.get('title'),
                            'odds_a': odds_a,
                            'odds_b': odds_b,
                            'arb_percentage': arb_percentage,
                        })
    return opportunities

