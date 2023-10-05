from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Initialize a Sequential model
model = Sequential()

# Add a Dense layer with 2 output units
model.add(Dense(2, input_dim=1))

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Save the model
model.save('models/dummy_model.h5')
 
