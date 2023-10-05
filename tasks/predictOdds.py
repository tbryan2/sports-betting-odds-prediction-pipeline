from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import json


def predict_odds(model_path, **kwargs):
    """
    Generates predicted odds for each matchup in the DataFrame using a model.
    For this example, we'll load a dummy model from an .h5 file.
    """

    # Pull the odds DataFrame JSON from XCom
    ti = kwargs['ti']
    grouped_df_json = ti.xcom_pull(task_ids='get_odds', key='grouped_df')

    print(grouped_df_json)

    # Convert the JSON string back to a DataFrame
    df = pd.read_json(grouped_df_json, orient='split')

    # Load the saved model
    model = load_model(model_path)

    # Generate random features for prediction (since the model is a dummy)
    random_features = np.random.rand(df.shape[0], 1)

    # Get raw predicted odds from the model
    predicted_odds_raw = model.predict(random_features)

    # Normalize the odds so they sum up to 100 for each match
    total_odds = np.sum(predicted_odds_raw, axis=1)
    normalized_odds_home = (predicted_odds_raw[:, 0] / total_odds) * 100
    normalized_odds_away = (predicted_odds_raw[:, 1] / total_odds) * 100

    # Assign the normalized, predicted odds to the dataframe
    df['home_team_predicted_odds'] = normalized_odds_home
    df['away_team_predicted_odds'] = normalized_odds_away

    # Convert DataFrame to JSON and push to XCom for subsequent tasks
    predictions_json = df.to_json(orient="split")
    ti.xcom_push(key='predictions', value=predictions_json)
