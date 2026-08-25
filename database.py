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

        cursor.execute("SELECT COUNT(*) FROM gdp_by_industry WHERE code = ?", (code,))
        exists = cursor.fetchone()[0] > 0

        if not exists:
            cursor.execute("INSERT INTO gdp_by_industry (code, industry, category) VALUES (?, ?, ?)", (code, industry, category))

        for col in df_cols:
            if col in ['code', 'industry', 'category']:
                continue
            val = row[col]
            if pd.notna(val):
                cursor.execute(f'UPDATE gdp_by_industry SET "{col}" = ? WHERE code = ?', (float(val) if str(col).isdigit() else str(val), code))

    conn.commit()
    conn.close()

def create_industry(code, industry, category, year_values=None, db_path=DB_PATH):
    """
    CREATE: Adds a new industry record to the database.
    """
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Dynamic year columns check
    if year_values:
        cursor.execute("PRAGMA table_info(gdp_by_industry)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        for yr in year_values.keys():
            yr_str = str(yr)
            if yr_str not in existing_cols and yr_str.isdigit():
                cursor.execute(f'ALTER TABLE gdp_by_industry ADD COLUMN "{yr_str}" REAL')
        conn.commit()

    cursor.execute("INSERT INTO gdp_by_industry (code, industry, category) VALUES (?, ?, ?)", (code, industry, category))

    if year_values:
        for yr, val in year_values.items():
            if str(yr).isdigit():
                cursor.execute(f'UPDATE gdp_by_industry SET "{yr}" = ? WHERE code = ?', (float(val) if val is not None else None, code))

    conn.commit()
    conn.close()
    return True

def get_industry_by_code(code, db_path=DB_PATH):
    """
    READ: Retrieves a single industry record by code.
    """
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gdp_by_industry WHERE code = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_industry(code, industry=None, category=None, year_values=None, db_path=DB_PATH):
    """
    UPDATE: Updates an existing industry record details and yearly GDP figures.
    """
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if industry is not None:
        cursor.execute("UPDATE gdp_by_industry SET industry = ? WHERE code = ?", (industry, code))
    if category is not None:
        cursor.execute("UPDATE gdp_by_industry SET category = ? WHERE code = ?", (category, code))

    if year_values:
        cursor.execute("PRAGMA table_info(gdp_by_industry)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        for yr in year_values.keys():
            yr_str = str(yr)
            if yr_str not in existing_cols and yr_str.isdigit():
                cursor.execute(f'ALTER TABLE gdp_by_industry ADD COLUMN "{yr_str}" REAL')
        conn.commit()

        for yr, val in year_values.items():
            if str(yr).isdigit():
                cursor.execute(f'UPDATE gdp_by_industry SET "{yr}" = ? WHERE code = ?', (float(val) if val is not None else None, code))

    conn.commit()
    conn.close()
    return True

def delete_industry(code, db_path=DB_PATH):
    """
    DELETE: Removes an industry record by code.
    """
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gdp_by_industry WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return True

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
