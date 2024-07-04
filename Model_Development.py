from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

X = data[['establishment_revenue', 'employment_rate']]
y = data['GDP_growth']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)
