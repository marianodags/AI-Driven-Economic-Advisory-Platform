import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_and_forecast(processed_data, forecast_years=None):
    """
    Fits ML regression models on historic Zamboanga del Norte GDP data (e.g. 2018-2024 or 2018-2025)
    and forecasts total GDP, sector GDP, and industry GDP for future years (2026-2030).
    Handles missing/NaN values gracefully if partial row data is provided.
    """
    yearly_df = processed_data['yearly_df']
    years = processed_data['years']

    if forecast_years is None:
        latest_y = int(processed_data['latest_year'])
        forecast_years = list(range(max(2026, latest_y + 1), max(2031, latest_y + 6)))

    X_hist = yearly_df[['year']].values
    y_hist = yearly_df['gdp'].values

    # Total GDP forecast model
    model = LinearRegression()
    model.fit(X_hist, y_hist)

    X_future = np.array(forecast_years).reshape(-1, 1)
    y_future_pred = model.predict(X_future)

    forecast_total = {}
    for yr, pred in zip(forecast_years, y_future_pred):
        forecast_total[yr] = round(float(pred), 2)

    # Sector forecasts
    sector_gdp = processed_data['sector_gdp']
    sector_forecasts = {}
    for cat in ['Agriculture', 'Industry', 'Services']:
        y_cat = [sector_gdp[cat][str(y)] for y in years]
        cat_model = LinearRegression()
        cat_model.fit(X_hist, y_cat)
        cat_preds = cat_model.predict(X_future)
        sector_forecasts[cat] = {yr: round(float(p), 2) for yr, p in zip(forecast_years, cat_preds)}

    # Industry-level forecasts
    raw_df = processed_data['raw_df']
    industry_forecasts = []

    for idx, row in raw_df.iterrows():
        # Clean NaNs in row for training
        valid_pairs = [(int(y), row[y]) for y in years if y in row and pd.notna(row[y])]
        if len(valid_pairs) >= 2:
            X_ind = np.array([p[0] for p in valid_pairs]).reshape(-1, 1)
            y_ind = np.array([p[1] for p in valid_pairs], dtype=float)
            ind_model = LinearRegression()
            ind_model.fit(X_ind, y_ind)
            ind_preds = ind_model.predict(X_future)
        else:
            ind_preds = [0.0] * len(forecast_years)

        latest_y_str = processed_data['latest_year']
        latest_val = float(row[latest_y_str]) if latest_y_str in row and pd.notna(row[latest_y_str]) else 0.0

        ind_fc_dict = {
            'code': str(row['code']),
            'industry': str(row['industry']),
            'category': str(row['category']),
            'latest_actual': latest_val
        }
        for yr, p in zip(forecast_years, ind_preds):
            ind_fc_dict[str(yr)] = round(float(p), 2)
        industry_forecasts.append(ind_fc_dict)

    return {
        'model': model,
        'X_hist': X_hist,
        'y_hist': y_hist,
        'forecast_total': forecast_total,
        'sector_forecasts': sector_forecasts,
        'industry_forecasts': industry_forecasts
    }

if __name__ == '__main__':
    from Data_Collection import load_data
    from Data_Processing import process_data
    df = load_data()
    pdata = process_data(df)
    results = train_and_forecast(pdata)
    print("Forecast Total GDP:", results['forecast_total'])
