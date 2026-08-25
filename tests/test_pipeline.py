import pytest
import os
import io
import pandas as pd
from database import init_db, fetch_gdp_by_industry_db, export_db_to_csv, import_df_to_db
from Data_Collection import load_data
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Evaluation import evaluate_model
from Advisory_Engine import generate_economic_advisory
from Deployment import create_app

def test_sqlite_database():
    init_db()
    df = fetch_gdp_by_industry_db()
    assert not df.empty
    assert len(df) == 16
    assert 'code' in df.columns
    assert '2024' in df.columns

def test_database_export_and_import():
    init_db()
    csv_str = export_db_to_csv()
    assert 'Agriculture, forestry, and fishing' in csv_str

    # Test importing DataFrame with 2025 column
    test_df = pd.DataFrame([
        {'code': 'A', 'industry': 'Agriculture, forestry, and fishing', 'category': 'Agriculture', '2025': 19500000.0}
    ])
    import_df_to_db(test_df)
    df_after = fetch_gdp_by_industry_db()
    assert '2025' in df_after.columns
    val_2025 = df_after.loc[df_after['code'] == 'A', '2025'].values[0]
    assert val_2025 == 19500000.0

def test_data_collection():
    df = load_data()
    assert not df.empty
    assert 'code' in df.columns
    assert 'category' in df.columns

def test_data_processing():
    raw_df = load_data()
    processed = process_data(raw_df)
    assert 'total_gdp' in processed
    assert 'sector_gdp' in processed
    assert processed['latest_gdp_2024'] > 0
    assert len(processed['years']) >= 7

def test_model_development_and_forecasting():
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    assert 2026 in forecast['forecast_total']
    assert forecast['forecast_total'][2026] > 0
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
    assert 'industry_rows' in json_data['processed']
    assert len(json_data['processed']['industry_rows']) == 16

    # Export API
    res_export = client.get('/api/export?format=csv')
    assert res_export.status_code == 200
    assert b'code,industry,category' in res_export.data

    # Upload API via JSON
    res_upload = client.post('/api/upload', json=[
        {'code': 'B', 'industry': 'Mining and quarrying', 'category': 'Industry', '2025': 210000.0}
    ])
    assert res_upload.status_code == 200
    assert res_upload.get_json()['rows_imported'] == 1

    # Predict API
    res_pred = client.post('/api/predict', json={'year': 2030})
    assert res_pred.status_code == 200
    assert res_pred.get_json()['year'] == 2030
