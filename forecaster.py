import json
from database import fetch_gdp_by_industry_db, DB_PATH
from Data_Processing import process_data
from Model_Development import train_and_forecast

def run_forecaster(db_path=DB_PATH, forecast_years=None):
    """
    Loads historic GDP dataset from SQLite database, processes economic analytics,
    fits ML regression models, and outputs 2026–2030 predictions for total GDP,
    sectors, and individual industries.
    """
    if forecast_years is None:
        forecast_years = [2026, 2027, 2028, 2029, 2030]

    df = fetch_gdp_by_industry_db(db_path=db_path)
    processed = process_data(df)
    results = train_and_forecast(processed, forecast_years=forecast_years)

    print("=== Zamboanga del Norte Macroeconomic Forecast (2026–2030) ===")
    print("Projected Total GDP (in '000 PHP):")
    for yr, val in results['forecast_total'].items():
        print(f"  {yr}: ₱{val:,.2f} thousand")

    print("\nProjected Sectoral Breakdown (in '000 PHP):")
    for cat, fc_dict in results['sector_forecasts'].items():
        print(f"  {cat}:")
        for yr, val in fc_dict.items():
            print(f"    {yr}: ₱{val:,.2f} thousand")

    return results

if __name__ == '__main__':
    run_forecaster()
