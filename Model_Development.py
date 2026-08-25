import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_and_forecast(processed_data, forecast_years=[2025, 2026, 2027]):
    """
    Fits ML regression models on historic Zamboanga del Norte GDP data (2018-2024)
    and forecasts total GDP, sector GDP, and industry GDP for future years.
    """
    yearly_df = processed_data['yearly_df']
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
        y_cat = [sector_gdp[cat][str(y)] for y in yearly_df['year']]
        cat_model = LinearRegression()
        cat_model.fit(X_hist, y_cat)
        cat_preds = cat_model.predict(X_future)
        sector_forecasts[cat] = {yr: round(float(p), 2) for yr, p in zip(forecast_years, cat_preds)}

    # Industry-level forecasts
    raw_df = processed_data['raw_df']
    years_str = processed_data['years']
    industry_forecasts = []

    for idx, row in raw_df.iterrows():
        y_ind = [row[y] for y in years_str]
        ind_model = LinearRegression()
        ind_model.fit(X_hist, y_ind)
        ind_preds = ind_model.predict(X_future)

        ind_fc_dict = {
            'code': row['code'],
            'industry': row['industry'],
            'category': row['category'],
            '2024_actual': float(row['2024'])
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
    print("Forecast Total GDP (2025-2027):", results['forecast_total'])
