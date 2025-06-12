# Steam Games Scraper

This script fetches metadata and review summaries for the top N Steam games and saves the results to a CSV file. It uses the SteamSpy “all” endpoint to build a pool of game IDs, sorts by owner count, and then pulls details from the official Steam Store API.


# File Structure
``` text
scraper/
├── fetch_games.py         # Main script
├── README.md              # This file

After running, you will have:
data/
└── steam_games.csv        # Output CSV with the scraped data
``` 
# Installation

Make sure you have Python 3.7+ and install the `requests` library:
