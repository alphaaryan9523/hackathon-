import numpy as np
from sklearn.linear_model import LinearRegression

# Simple predictive model based on historical data
def predict_demand(historical_data):
    # Convert data to numpy array and reshape for sklearn
    data = np.array(historical_data).reshape(-1, 1)
    X = np.arange(len(data)).reshape(-1, 1)  # Time steps
    y = data.ravel()  # Stock levels

    # Train simple linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future demand (e.g., next 5 time steps)
    future_steps = np.arange(len(data), len(data) + 5).reshape(-1, 1)
    future_demand = model.predict(future_steps)

    return future_demand.tolist()
