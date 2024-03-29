def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    return (1 / odds_a + 1 / odds_b) * 100

def find_arbitrage_opportunities(odds_data):
    opportunities = []
    
    for event in odds_data:
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"
        
        # Separate market data by type for logical comparisons
        h2h_data, spreads_data, totals_data = {}, {}, {}
        
        # Collect data
        for bookmaker in event.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                for outcome in market.get('outcomes', []):
                    outcome_data = {
                        'bookmaker': bookmaker['title'],
                        'odds': outcome['price'],
                        'name': outcome.get('name', 'N/A'),
                        'point': outcome.get('point')
                    }
                    if market['key'] == 'h2h':
                        if event.get('home_team') == outcome['name']:
                            h2h_data.setdefault('home', []).append(outcome_data)
                        else:
                            h2h_data.setdefault('away', []).append(outcome_data)
                    elif market['key'] == 'spreads':
                       # Note: For spreads, we differentiate by the team's name and the point spread
                        spread_key = (outcome['name'], outcome['point'])
                        spreads_data.setdefault(spread_key, []).append(outcome_data)
                    elif market['key'] == 'totals':
                        totals_data.setdefault(outcome['point'], []).append(outcome_data)
        
        # Process h2h
        for home_outcome in h2h_data.get('home', []):
            for away_outcome in h2h_data.get('away', []):
                if home_outcome['bookmaker'] != away_outcome['bookmaker']:  # Ensure different bookmakers
                    arb_percentage = calculate_arbitrage_percentage(home_outcome['odds'], away_outcome['odds'])
                    if arb_percentage < 100:
                        opportunities.append({
                            'event_name': event_name,
                            'market_type': 'h2h',
                            'outcome_name': f"{home_outcome['name']} vs {away_outcome['name']}",
                            'point': 'N/A',
                            'bookmaker': home_outcome['bookmaker'],
                            'odds': home_outcome['odds'],
                            'comparison_bookmaker': away_outcome['bookmaker'],
                            'comparison_odds': away_outcome['odds'],
                            'arb_percentage': arb_percentage
                        })
        
        # Process totals - simplified example
        for point, outcomes in totals_data.items():
            if len(outcomes) >= 2:  # Need at least two outcomes to compare, e.g., Over vs Under
                # Simplified, assuming first two outcomes are Over and Under for demonstration
                first_outcome = outcomes[0]
                second_outcome = outcomes[1]
                arb_percentage = calculate_arbitrage_percentage(first_outcome['odds'], second_outcome['odds'])
                if arb_percentage < 100:
                    opportunities.append({
                        'event_name': event_name,
                        'market_type': 'totals',
                        'outcome_name': f"Over/Under {point}",
                        'point': point,
                        'bookmaker': first_outcome['bookmaker'],
                        'odds': first_outcome['odds'],
                        'comparison_bookmaker': second_outcome['bookmaker'],
                        'comparison_odds': second_outcome['odds'],
                        'arb_percentage': arb_percentage
                    })
                    
        # Process spreads
        for (team_name, point), outcomes in spreads_data.items():
            if len(outcomes) >= 2:
                # Compare odds for the same team and point spread from different bookmakers
                for i in range(len(outcomes)):
                    for j in range(i + 1, len(outcomes)):
                        arb_percentage = calculate_arbitrage_percentage(outcomes[i]['odds'], outcomes[j]['odds'])
                        if arb_percentage < 100:
                            opportunities.append({
                                'event_name': event_name,
                                'market_type': 'spreads',
                                'outcome_name': f"{team_name} {point}",
                                'point': point,
                                'bookmaker': outcomes[i]['bookmaker'],
                                'odds': outcomes[i]['odds'],
                                'comparison_bookmaker': outcomes[j]['bookmaker'],
                                'comparison_odds': outcomes[j]['odds'],
                                'arb_percentage': arb_percentage
                            })

    return opportunities
