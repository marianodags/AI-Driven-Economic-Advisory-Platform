import pytest
import os
import pandas as pd
from Data_Collection import load_data
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Evaluation import evaluate_model
from Advisory_Engine import generate_economic_advisory
from Deployment import create_app

def test_data_collection():
    df = load_data()
    assert not df.empty
    assert 'code' in df.columns
    assert '2024' in df.columns
    assert 'category' in df.columns

def test_data_processing():
    raw_df = load_data()
    processed = process_data(raw_df)
    assert 'total_gdp' in processed
    assert 'sector_gdp' in processed
    assert processed['latest_gdp_2024'] > 0
    assert len(processed['years']) == 7

def test_model_development_and_forecasting():
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    assert 2025 in forecast['forecast_total']
    assert forecast['forecast_total'][2025] > processed['latest_gdp_2024']
    assert len(forecast['industry_forecasts']) == len(raw_df)

def test_evaluation():
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    metrics = evaluate_model(forecast['model'], forecast['X_hist'], forecast['y_hist'])
    assert 'r2' in metrics
    assert 'mse' in metrics
    assert metrics['r2'] <= 1.0

def test_advisory_engine():
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    advisory = generate_economic_advisory(processed, forecast)
    assert 'Zamboanga del Norte' in advisory['executive_summary']
    assert len(advisory['key_insights']) > 0
    assert len(advisory['strategic_recommendations']) > 0

def test_flask_endpoints():
    app = create_app()
    client = app.test_client()

    # Index page
    res_index = client.get('/')
    assert res_index.status_code == 200
    assert b'Zamboanga Del Norte' in res_index.data

    # Data API
    res_data = client.get('/api/data')
    assert res_data.status_code == 200
    json_data = res_data.get_json()
    assert json_data['metadata']['name'] == 'Province of Zamboanga del Norte'

    # Forecast API
    res_fc = client.get('/api/forecast')
    assert res_fc.status_code == 200

    # Insights API
    res_ins = client.get('/api/insights')
    assert res_ins.status_code == 200

    # Predict API
    res_pred = client.post('/api/predict', json={'year': 2030})
    assert res_pred.status_code == 200
    json_pred = res_pred.get_json()
    assert json_pred['year'] == 2030
    assert json_pred['predicted_gdp'] > 0
