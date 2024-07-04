import matplotlib.pyplot as plt

plt.plot(data['date'], data['GDP_growth'], label='Actual GDP Growth')
plt.plot(data['date'].iloc[X_test.index], y_pred, label='Predicted GDP Growth')
plt.legend()
plt.show()
