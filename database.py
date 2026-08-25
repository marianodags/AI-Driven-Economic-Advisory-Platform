import sqlite3
import pandas as pd
import os
import io

DB_PATH = 'gdp_database.db'
CSV_PATH = 'zamboanga_gdp.csv'

def get_year_columns_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(gdp_by_industry)")
    columns = [row[1] for row in cursor.fetchall()]
    year_cols = [c for c in columns if c.isdigit()]
    return year_cols

def init_db(db_path=DB_PATH, csv_path=CSV_PATH):
    """
    Initializes SQLite database and seeds GDP by industry data from CSV if not exists or empty.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gdp_by_industry (
            code TEXT PRIMARY KEY,
            industry TEXT NOT NULL,
            category TEXT NOT NULL,
            "2018" REAL,
            "2019" REAL,
            "2020" REAL,
            "2021" REAL,
            "2022" REAL,
            "2023" REAL,
            "2024" REAL
        )
    ''')
    conn.commit()

    cursor.execute('SELECT COUNT(*) FROM gdp_by_industry')
    count = cursor.fetchone()[0]

    if count == 0 and os.path.exists(csv_path):
        df_csv = pd.read_csv(csv_path)
        import_df_to_db(df_csv, db_path=db_path)

    conn.close()

def import_df_to_db(df, db_path=DB_PATH):
    """
    Imports/upserts a DataFrame into the SQLite database table gdp_by_industry.
    Dynamically adds new year columns (e.g. '2025') if present in the DataFrame.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get existing table columns
    cursor.execute("PRAGMA table_info(gdp_by_industry)")
    existing_cols = [row[1] for row in cursor.fetchall()]

    # Check for new year columns in df
    df_cols = list(df.columns)
    for col in df_cols:
        col_str = str(col)
        if col_str not in existing_cols:
            if col_str.isdigit():
                cursor.execute(f'ALTER TABLE gdp_by_industry ADD COLUMN "{col_str}" REAL')
            else:
                cursor.execute(f'ALTER TABLE gdp_by_industry ADD COLUMN "{col_str}" TEXT')
    conn.commit()

    # Refresh columns after alter
    cursor.execute("PRAGMA table_info(gdp_by_industry)")
    updated_cols = [row[1] for row in cursor.fetchall()]

    # Upsert each row based on 'code'
    for _, row in df.iterrows():
        code = str(row['code'])
        industry = str(row['industry'])
        category = str(row['category'])

        # Check if code exists
        cursor.execute("SELECT COUNT(*) FROM gdp_by_industry WHERE code = ?", (code,))
        exists = cursor.fetchone()[0] > 0

        if not exists:
            cursor.execute("INSERT INTO gdp_by_industry (code, industry, category) VALUES (?, ?, ?)", (code, industry, category))

        # Update columns
        for col in df_cols:
            if col in ['code', 'industry', 'category']:
                continue
            val = row[col]
            if pd.notna(val):
                cursor.execute(f'UPDATE gdp_by_industry SET "{col}" = ? WHERE code = ?', (float(val) if str(col).isdigit() else str(val), code))

    conn.commit()
    conn.close()

def export_db_to_csv(db_path=DB_PATH):
    """
    Exports all records from SQLite database to a CSV formatted string.
    """
    df = fetch_gdp_by_industry_db(db_path=db_path)
    return df.to_csv(index=False)

def fetch_gdp_by_industry_db(db_path=DB_PATH):
    """
    Fetches GDP data by industry directly from SQLite database as a DataFrame.
    """
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(gdp_by_industry)")
    cols = [row[1] for row in cursor.fetchall()]
    col_selectors = [f'"{c}"' for c in cols]

    df = pd.read_sql_query(f'SELECT {", ".join(col_selectors)} FROM gdp_by_industry', conn)
    conn.close()
    return df

if __name__ == '__main__':
    init_db()
    df = fetch_gdp_by_industry_db()
    print("Database contents shape:", df.shape)
