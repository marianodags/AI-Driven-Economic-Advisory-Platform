import pandas as pd
import os
from database import fetch_gdp_by_industry_db, init_db

def load_data(db_path='gdp_database.db', csv_path='zamboanga_gdp.csv'):
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
    elif os.path.exists('economic_data.csv'):
        return pd.read_csv('economic_data.csv')
    else:
        raise FileNotFoundError("Neither database nor CSV files could be loaded.")

if __name__ == '__main__':
    df = load_data()
    print("Loaded Data Shape from DB:", df.shape)
    print(df.head())
