from datetime import datetime, timedelta
import pandas as pd
import requests

def get_odds(sport, api_key, regions, bookmakers, odds_format):
    '''
    Pull latest odds from The Odds API,
    by default this pulls h2h odds assuming that it's Tuesday
    and we're pulling odds for the upcoming Thursday to Monday
    '''
    # Calculate commenceTimeFrom and commenceTimeTo
    now = datetime.utcnow()
    next_thursday = now + timedelta((3 - now.weekday() + 7) % 7)  # 3 represents Thursday
    next_monday = next_thursday + timedelta(days=4)  # 4 days after Thursday is Monday

    commence_time_from = next_thursday.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    commence_time_to = next_monday.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions={regions}&bookmakers={bookmakers}&oddsFormat={odds_format}&commenceTimeFrom={commence_time_from}&commenceTimeTo={commence_time_to}"

    response = requests.get(url, timeout=60)

    odds = response.json()

    odds_df = pd.json_normalize(odds,
                        sep='_',
                        record_path=['bookmakers', 'markets', 'outcomes'],
                        meta=[['id'],
                            ['sport_key'],
                            ['sport_title'],
                            ['commence_time'],
                            ['home_team'],
                            ['away_team'],
                            ['bookmakers', 'key'],
                            ['bookmakers', 'title'],
                            ['bookmakers', 'markets', 'key']]
                        )

    odds_df = odds_df[['name', 'price', 'commence_time', 'home_team', 'away_team']]

    return odds_df
