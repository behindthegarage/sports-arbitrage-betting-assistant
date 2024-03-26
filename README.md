
# Sports Arbitrage Bot

## Description
This Sports Arbitrage Bot is designed to identify positive arbitrage opportunities across multiple bookmakers for various sports. It fetches odds data from the Odds API, analyzes potential arbitrage situations, and reports any found opportunities, aiming to aid in sports betting strategies.

## Installation

To get started with this bot, follow these steps:

1. Clone the repository to your local machine.
   ```
   git clone https://github.com/yourusername/sports-arbitrage-bot.git
   ```
2. Navigate to the cloned directory.
   ```
   cd sports-arbitrage-bot
   ```
3. Install the required Python packages.
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the bot by executing the main script:
```
python main.py
```

Ensure you have set your Odds API key in the `.env` file before running the bot.

## To-Do List
- [ ] Clear the `error_log.txt` file at the start of each script run.
- [ ] Implement functionality to analyze more complex arbitrage opportunities.
- [ ] Add more detailed logging for debugging purposes.
- [ ] Create a more user-friendly interface or dashboard for monitoring.

For more information on the Odds API and configuring your API key, visit [The Odds API documentation](https://the-odds-api.com/).
