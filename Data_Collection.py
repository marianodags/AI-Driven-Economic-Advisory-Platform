import pandas as pd
import os
from database import fetch_gdp_by_industry_db, init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'gdp_database.db')
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, 'data', 'zamboanga_gdp.csv')
DEFAULT_ECONOMIC_CSV_PATH = os.path.join(BASE_DIR, 'data', 'economic_data.csv')

def load_data(db_path=DEFAULT_DB_PATH, csv_path=DEFAULT_CSV_PATH):
    """
    Loads Zamboanga del Norte PPA GDP dataset from SQLite database.
    Falls back to CSV if database connection or fetch fails.
    """
    try:
        init_db(db_path=db_path, csv_path=csv_path)
        df = fetch_gdp_by_industry_db(db_path=db_path)
        if not df.empty:
            return df
    except Exception as e:
        print(f"Database load warning: {e}. Falling back to CSV.")

    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    elif os.path.exists(DEFAULT_ECONOMIC_CSV_PATH):
        return pd.read_csv(DEFAULT_ECONOMIC_CSV_PATH)
    else:
        raise FileNotFoundError("Neither database nor CSV files could be loaded.")

if __name__ == '__main__':
    df = load_data()
    print("Loaded Data Shape from DB:", df.shape)
    print(df.head())
