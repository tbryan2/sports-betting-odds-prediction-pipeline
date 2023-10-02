import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Create a simple model
model = Sequential([
    Dense(5, input_shape=(5,), activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy')

# Generate some random data
X = np.random.rand(100, 5)
y = np.random.randint(0, 2, 100)

# Fit the model
model.fit(X, y, epochs=3)

# Save the model
model.save('models/dummy_model.h5')