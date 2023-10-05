from datetime import datetime, timedelta
import pandas as pd
import requests


def get_odds(sport, regions, bookmakers, odds_format, csv_save_path, **kwargs):
    '''
    Pull latest odds from The Odds API,
    by default this pulls h2h odds assuming that it's Tuesday
    and we're pulling odds for the upcoming Thursday to Monday
    '''
    # Calculate commenceTimeFrom and commenceTimeTo
    now = datetime.utcnow()
    # 3 represents Thursday
    next_thursday = now + timedelta((3 - now.weekday() + 7) % 7)
    # 4 days after Thursday is Monday
    next_monday = next_thursday + timedelta(days=4)

    commence_time_from = next_thursday.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    commence_time_to = next_monday.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    secrets = kwargs['ti'].xcom_pull(task_ids='get_secrets')
    api_key = secrets['ODDS_API_KEY']

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions={regions}&bookmakers={bookmakers}&oddsFormat={odds_format}&commenceTimeFrom={commence_time_from}&commenceTimeTo={commence_time_to}"

    response = requests.get(url, timeout=60)
    odds = response.json()

    odds_df = pd.json_normalize(odds,
                                sep='_',
                                record_path=['bookmakers',
                                             'markets', 'outcomes'],
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

    odds_df = odds_df[['name', 'price',
                       'commence_time', 'home_team', 'away_team']]

    # Sort the DataFrame
    odds_df = odds_df.sort_values(['commence_time', 'home_team', 'away_team'])

    # Group by and aggregate to get one row per matchup
    def aggregate_rows(rows):
        home_row = rows[rows['home_team'] == rows['name']].iloc[0]
        away_row = rows[rows['away_team'] == rows['name']].iloc[0]

        return pd.Series({
            'home_team_odds': home_row['price'],
            'away_team_odds': away_row['price'],
            'commence_time': home_row['commence_time'],
            'home_team': home_row['home_team'],
            'away_team': home_row['away_team']
        })

    grouped_df = odds_df.groupby(['commence_time', 'home_team', 'away_team']).apply(
        aggregate_rows).reset_index(drop=True)

    grouped_df.to_csv(csv_save_path, index=False)
