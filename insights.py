from database import fetch_gdp_by_industry_db, DB_PATH
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Advisory_Engine import generate_economic_advisory

def generate_insights(db_path=DB_PATH):
    """
    Generates AI executive narrative insights and strategic policy recommendations
    for Zamboanga del Norte based on database PPA trends and ML forecasting results.
    """
    df = fetch_gdp_by_industry_db(db_path=db_path)
    processed = process_data(df)
    forecast = train_and_forecast(processed)

    advisory = generate_economic_advisory(processed, forecast)

    print("=== AI Executive Economic Summary ===")
    print(advisory['executive_summary'])

    print("\n=== Key Sectoral Insights ===")
    for insight in advisory['key_insights']:
        print(f"• [{insight['status']}] {insight['title']}: {insight['detail']}")

    print("\n=== Strategic Policy Recommendations ===")
    for rec in advisory['strategic_recommendations']:
        print(f"• Sector: {rec['sector']} | Action: {rec['action']}")
        print(f"  {rec['description']}")

    return advisory

if __name__ == '__main__':
    generate_insights()
