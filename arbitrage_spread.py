def find_spread_arbitrage_opportunities(odds_data):
    opportunities = []
    
    for event in odds_data:
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"

        # Dictionary to store the best odds for each team spread across all bookmakers
        best_spread_odds_per_team = {}

        # Collect 'spreads' data and determine the best odds offered for each team spread
        for bookmaker in event.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market['key'] == 'spreads':
                    for outcome in market.get('outcomes', []):
                        team = outcome['name']
                        odds = outcome['price']
                        spread = outcome['point']  # Assuming 'point' holds the spread value
                        if team not in best_spread_odds_per_team or odds > best_spread_odds_per_team[team]['odds']:
                            best_spread_odds_per_team[team] = {
                                'bookmaker': bookmaker['title'], 
                                'odds': odds, 
                                'spread': spread
                            }

        # If we have best odds for both teams, calculate arbitrage opportunity
        if len(best_spread_odds_per_team) == 2:
            teams = list(best_spread_odds_per_team.keys())
            odds_a = best_spread_odds_per_team[teams[0]]['odds']
            odds_b = best_spread_odds_per_team[teams[1]]['odds']
            spread_a = best_spread_odds_per_team[teams[0]]['spread']
            spread_b = best_spread_odds_per_team[teams[1]]['spread']
            bookmaker_a = best_spread_odds_per_team[teams[0]]['bookmaker']
            bookmaker_b = best_spread_odds_per_team[teams[1]]['bookmaker']
            
            arb_percentage = calculate_arbitrage_percentage(odds_a, odds_b)
            
            if arb_percentage < 100:
                opportunities.append({
                    'event_name': event_name,
                    'market_type': 'spreads',
                    'outcome_name': f"{teams[0]} ({spread_a}) vs {teams[1]} ({spread_b})",
                    'point': f"{spread_a} vs {spread_b}",
                    'bookmaker': bookmaker_a,
                    'odds': odds_a,
                    'comparison_bookmaker': bookmaker_b,
                    'comparison_odds': odds_b,
                    'arb_percentage': arb_percentage
                })

    return opportunities


def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    # Print the odds being used for calculation
    print(f"Calculating arbitrage percentage using odds: {odds_a} and {odds_b}")
    
    return (1 / odds_a + 1 / odds_b) * 100
