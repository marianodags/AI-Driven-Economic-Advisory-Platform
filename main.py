# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

# Step 1: Data Collection
app = Flask(__name__)
data = pd.read_csv('economic_data.csv')

# Step 2: Data Processing
data = data.dropna()
data['GDP_growth'] = data['GDP'].pct_change()

# Step 3: Model Development
X = data[['establishment_revenue', 'employment_rate']]
y = data['GDP_growth']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Step 4: Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Step 5: Visualization
plt.plot(data['date'], data['GDP_growth'], label='Actual GDP Growth')
plt.plot(data['date'].iloc[X_test.index], y_pred, label='Predicted GDP Growth')
plt.legend()
plt.title('Actual vs Predicted GDP Growth')
plt.xlabel('Date')
plt.ylabel('GDP Growth')
plt.show()

# Step 6: Deployment
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict(pd.DataFrame(data))
    return jsonify(prediction.tolist())

if __name__ == '__main__':
    app.run(debug=True)
