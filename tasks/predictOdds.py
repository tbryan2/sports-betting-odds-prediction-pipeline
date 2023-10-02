from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd

def predict_odds(odds_path, model_path, prediction_path):
    """
    Generates predicted odds for each matchup in the DataFrame using a model.
    For this example, we'll load a dummy model from an .h5 file.
    """

    df = pd.read_csv(odds_path)

    # Load the saved model
    model = load_model(model_path)

    # Generate random features for prediction (since the model is a dummy)
    # Ensuring that each row has a different random feature
    random_features = np.random.rand(df.shape[0], 1)

    print("Random features: ", random_features)
    # Get raw predicted odds from the model
    # This should output a 2D array (number of samples x 2)
    predicted_odds_raw = model.predict(random_features)

    # Normalize the odds so they sum up to 100 for each match
    total_odds = np.sum(predicted_odds_raw, axis=1)
    normalized_odds_home = (predicted_odds_raw[:, 0] / total_odds) * 100
    normalized_odds_away = (predicted_odds_raw[:, 1] / total_odds) * 100

    # Assign the normalized, predicted odds to the dataframe
    df['home_team_predicted_odds'] = normalized_odds_home
    df['away_team_predicted_odds'] = normalized_odds_away

    df.to_csv(prediction_path, index=False)
