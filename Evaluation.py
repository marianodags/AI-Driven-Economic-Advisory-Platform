from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_model(model, X_hist, y_hist):
    """
    Evaluates forecasting model performance metrics.
    """
    y_pred = model.predict(X_hist)
    mse = mean_squared_error(y_hist, y_pred)
    mae = mean_absolute_error(y_hist, y_pred)
    r2 = r2_score(y_hist, y_pred)
    return {
        'mse': float(mse),
        'rmse': float(mse ** 0.5),
        'mae': float(mae),
        'r2': float(r2),
        'y_pred': y_pred.tolist()
    }

if __name__ == '__main__':
    from Data_Collection import load_data
    from Data_Processing import process_data
    from Model_Development import train_and_forecast
    pdata = process_data(load_data())
    res = train_and_forecast(pdata)
    metrics = evaluate_model(res['model'], res['X_hist'], res['y_hist'])
    print("Evaluation Metrics:", metrics)
