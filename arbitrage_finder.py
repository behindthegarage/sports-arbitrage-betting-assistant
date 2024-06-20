def find_arbitrage_opportunities(odds_data):
    opportunities = []
    
    for event in odds_data:
        event_name = f"{event.get('home_team')} vs {event.get('away_team')}"

        for market_type in ['h2h', 'spreads', 'totals']:
            best_odds = {}

            for bookmaker in event.get('bookmakers', []):
                for market in bookmaker.get('markets', []):
                    if market['key'] == market_type:
                        for outcome in market.get('outcomes', []):
                            key = (outcome['name'], outcome.get('point'))
                            odds = outcome['price']
                            if key not in best_odds or odds > best_odds[key]['odds']:
                                best_odds[key] = {
                                    'bookmaker': bookmaker['title'],
                                    'odds': odds,
                                    'point': outcome.get('point')
                                }

            if market_type == 'h2h' and len(best_odds) == 2:
                opportunities.extend(check_arbitrage(event_name, market_type, best_odds))
            elif market_type in ['spreads', 'totals'] and len(best_odds) >= 2:
                opportunities.extend(check_arbitrage(event_name, market_type, best_odds))

    return opportunities

def check_arbitrage(event_name, market_type, best_odds):
    opportunities = []
    odds_list = list(best_odds.values())

    if market_type == 'h2h':
        arb_percentage = calculate_arbitrage_percentage(odds_list[0]['odds'], odds_list[1]['odds'])
        if arb_percentage < 100:
            opportunities.append(create_opportunity(event_name, market_type, best_odds, arb_percentage))
    else:  # spreads or totals
        for i in range(len(odds_list)):
            for j in range(i + 1, len(odds_list)):
                if odds_list[i]['point'] != odds_list[j]['point']:
                    arb_percentage = calculate_arbitrage_percentage(odds_list[i]['odds'], odds_list[j]['odds'])
                    if arb_percentage < 100:
                        opportunities.append(create_opportunity(event_name, market_type, 
                                                                {k: v for k, v in best_odds.items() if v in [odds_list[i], odds_list[j]]}, 
                                                                arb_percentage))

    return opportunities

def create_opportunity(event_name, market_type, odds_data, arb_percentage):
    outcomes = list(odds_data.keys())
    return {
        'event_name': event_name,
        'market_type': market_type,
        'outcome_name': f"{outcomes[0][0]} vs {outcomes[1][0]}",
        'point': f"{outcomes[0][1]} / {outcomes[1][1]}",
        'bookmaker': odds_data[outcomes[0]]['bookmaker'],
        'odds': odds_data[outcomes[0]]['odds'],
        'comparison_bookmaker': odds_data[outcomes[1]]['bookmaker'],
        'comparison_odds': odds_data[outcomes[1]]['odds'],
        'arb_percentage': arb_percentage
    }

def calculate_arbitrage_percentage(odds_a, odds_b):
    """Calculate the arbitrage percentage of two outcomes."""
    return (1 / odds_a + 1 / odds_b) * 100

# If you want to run this file independently, you can add a main function:
if __name__ == "__main__":
    # Example usage
    sample_odds_data = [
        {
            "home_team": "Team A",
            "away_team": "Team B",
            "bookmakers": [
                {
                    "title": "Bookmaker 1",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "Team A", "price": 2.0},
                                {"name": "Team B", "price": 2.1}
                            ]
                        }
                    ]
                },
                {
                    "title": "Bookmaker 2",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "Team A", "price": 1.95},
                                {"name": "Team B", "price": 2.15}
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    opportunities = find_arbitrage_opportunities(sample_odds_data)
    for opp in opportunities:
        print(opp)