def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    return (1 / odds_a + 1 / odds_b) * 100

def find_arbitrage_opportunities(odds_data):
    opportunities = []
    
    for event in odds_data:
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
        
        # Initialize a dictionary for spreads data
        spreads_data = {}
        
        # Collect spreads data
        for bookmaker in event.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market['key'] == 'spreads':
                    for outcome in market.get('outcomes', []):
                        outcome_data = {
                            'bookmaker': bookmaker['title'],
                            'odds': outcome['price'],
                            'team': outcome['name'],
                            'point': outcome['point']
                        }
                        # Key by point spread to group similar spreads together
                        spreads_key = outcome['point']
                        spreads_data.setdefault(spreads_key, []).append(outcome_data)
        
        # Find arbitrage opportunities in spreads
        for spread, outcomes in spreads_data.items():
            if len(outcomes) < 2: continue  # Need at least two different bookmakers for comparison
            
            # Attempt to find pairs of outcomes from different bookmakers for arbitrage calculation
            for i, outcome_i in enumerate(outcomes):
                for outcome_j in outcomes[i+1:]:
                    # Check if outcomes are from different bookmakers and involve different teams
                    if outcome_i['bookmaker'] != outcome_j['bookmaker'] and outcome_i['team'] != outcome_j['team']:
                        arb_percentage = calculate_arbitrage_percentage(outcome_i['odds'], outcome_j['odds'])
                        if arb_percentage < 100:
                            opportunities.append({
                                'event_name': event_name,
                                'market_type': 'spreads',
                                'outcome_name': f"{outcome_i['team']} vs {outcome_j['team']}",
                                'point': spread,
                                'bookmaker': outcome_i['bookmaker'],
                                'odds': outcome_i['odds'],
                                'comparison_bookmaker': outcome_j['bookmaker'],
                                'comparison_odds': outcome_j['odds'],
                                'arb_percentage': arb_percentage
                            })

    return opportunities
