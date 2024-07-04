import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Step 1: Data Loading and Preprocessing
data_dict = {
    'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01'],
    'GDP': [1000000, 1010000, 1020500, 1031500],
    'establishment_revenue': [50000, 51000, 52000, 53000],
    'employment_rate': [60, 61, 62, 63]
}
data = pd.DataFrame(data_dict)

# Step 2: Feature Selection
X = data[['establishment_revenue', 'employment_rate']]
y = data['GDP'].pct_change().fillna(0)  # Example: Using percent change of GDP as target variable

# Step 3: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Model Development
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Step 6: Visualization
plt.plot(data['date'].iloc[X_test.index], y_test, label='Actual GDP Growth')
plt.plot(data['date'].iloc[X_test.index], y_pred, label='Predicted GDP Growth')
plt.legend()
plt.title('Actual vs Predicted GDP Growth')
plt.xlabel('Date')
plt.ylabel('GDP Growth')
plt.show()

# Step 7: Deployment (Flask example)
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict(pd.DataFrame(data))
    return jsonify(prediction.tolist())

if __name__ == '__main__':
    app.run(debug=True)
"""
