import pytest
import os
import io
import pandas as pd
from database import (
    init_db, fetch_gdp_by_industry_db, export_db_to_csv, import_df_to_db,
    create_industry, get_industry_by_code, update_industry, delete_industry
)
from Data_Collection import load_data
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Evaluation import evaluate_model
from Advisory_Engine import generate_economic_advisory
from Deployment import create_app

TEST_DB_PATH = 'test_gdp_database.db'

@pytest.fixture(autouse=True)
def setup_test_database():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    init_db(db_path=TEST_DB_PATH)
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_sqlite_database():
    df = fetch_gdp_by_industry_db(db_path=TEST_DB_PATH)
    assert not df.empty
    assert len(df) >= 16
    assert 'code' in df.columns
    assert '2024' in df.columns

def test_database_crud_operations():
    test_code = 'TEST_Z'

    # 1. CREATE
    created = create_industry(test_code, 'Test Sector Z', 'Services', {'2024': 500000.0, '2025': 550000.0}, db_path=TEST_DB_PATH)
    assert created

    # 2. READ
    record = get_industry_by_code(test_code, db_path=TEST_DB_PATH)
    assert record is not None
    assert record['industry'] == 'Test Sector Z'
    assert record['2024'] == 500000.0

    # 3. UPDATE
    updated = update_industry(test_code, industry='Test Sector Z Updated', year_values={'2025': 600000.0}, db_path=TEST_DB_PATH)
    assert updated
    record_updated = get_industry_by_code(test_code, db_path=TEST_DB_PATH)
    assert record_updated['industry'] == 'Test Sector Z Updated'
    assert record_updated['2025'] == 600000.0

    # 4. DELETE
    deleted = delete_industry(test_code, db_path=TEST_DB_PATH)
    assert deleted
    assert get_industry_by_code(test_code, db_path=TEST_DB_PATH) is None

def test_database_export_and_import():
    csv_str = export_db_to_csv(db_path=TEST_DB_PATH)
    assert 'Agriculture, forestry, and fishing' in csv_str

    # Test importing DataFrame with 2025 column
    test_df = pd.DataFrame([
        {'code': 'A', 'industry': 'Agriculture, forestry, and fishing', 'category': 'Agriculture', '2025': 19500000.0}
    ])
    import_df_to_db(test_df, db_path=TEST_DB_PATH)
    df_after = fetch_gdp_by_industry_db(db_path=TEST_DB_PATH)
    assert '2025' in df_after.columns
    val_2025 = df_after.loc[df_after['code'] == 'A', '2025'].values[0]
    assert val_2025 == 19500000.0

def test_data_collection():
    df = load_data(db_path=TEST_DB_PATH)
    assert not df.empty
    assert 'code' in df.columns
    assert 'category' in df.columns

def test_data_processing():
    raw_df = load_data(db_path=TEST_DB_PATH)
    processed = process_data(raw_df)
    assert 'total_gdp' in processed
    assert 'sector_gdp' in processed
    assert 'major_analytics' in processed
    assert 'all_ind_analytics' in processed
    assert processed['latest_gdp_2024'] > 0
    assert len(processed['years']) >= 7

def test_model_development_and_forecasting():
    raw_df = load_data(db_path=TEST_DB_PATH)
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    assert 2026 in forecast['forecast_total']
    assert forecast['forecast_total'][2026] > 0
    assert len(forecast['industry_forecasts']) == len(raw_df)

def test_evaluation():
    raw_df = load_data(db_path=TEST_DB_PATH)
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    metrics = evaluate_model(forecast['model'], forecast['X_hist'], forecast['y_hist'])
    assert 'r2' in metrics
    assert 'mse' in metrics
    assert metrics['r2'] <= 1.0

def test_advisory_engine():
    raw_df = load_data(db_path=TEST_DB_PATH)
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    advisory = generate_economic_advisory(processed, forecast)
    assert 'Zamboanga del Norte' in advisory['executive_summary']
    assert len(advisory['key_insights']) > 0

def test_flask_crud_and_analytics_endpoints():
    app = create_app()
    client = app.test_client()

    # Index page
    res_index = client.get('/')
    assert res_index.status_code == 200
    assert b'Zamboanga Del Norte' in res_index.data

    # Data API with year filter
    res_data = client.get('/api/data?year=2024')
    assert res_data.status_code == 200
    json_data = res_data.get_json()
    assert json_data['metadata']['name'] == 'Province of Zamboanga del Norte'
    assert 'major_analytics' in json_data['processed']
    assert 'all_ind_analytics' in json_data['processed']

    # Predict API
    res_pred = client.post('/api/predict', json={'year': 2030})
    assert res_pred.status_code == 200
    assert res_pred.get_json()['year'] == 2030

def test_seed_forecaster_insights_scripts():
    from seed import seed_database
    from forecaster import run_forecaster
    from insights import generate_insights

    df_seeded = seed_database(db_path=TEST_DB_PATH)
    assert not df_seeded.empty
    assert '2025' in df_seeded.columns

    forecast_results = run_forecaster(db_path=TEST_DB_PATH)
    assert 2026 in forecast_results['forecast_total']

    advisory_insights = generate_insights(db_path=TEST_DB_PATH)
    assert 'executive_summary' in advisory_insights
    assert len(advisory_insights['strategic_recommendations']) > 0
