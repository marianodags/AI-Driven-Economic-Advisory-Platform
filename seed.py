import pandas as pd
import sqlite3
import os
from database import init_db, import_df_to_db, fetch_gdp_by_industry_db, DB_PATH

def seed_database(db_path=DB_PATH):
    """
    Seeds the SQLite database with Region IX / Zamboanga del Norte economic data.
    Loads 2018–2024 official published PSA baseline figures, adds a preliminary 2025
    projection column (until real 2025 PSA data is uploaded/imported), and imports into gdp_database.db.
    """
    init_db(db_path=db_path)

    csv_path = 'zamboanga_gdp.csv'
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = fetch_gdp_by_industry_db(db_path=db_path)

    # Check if 2025 column already exists, if not calculate preliminary 2025 projections until official 2025 PSA dataset is uploaded
    if '2025' not in df.columns or df['2025'].isnull().all():
        vals_2025 = []
        for idx, row in df.iterrows():
            val_2023 = float(row['2023']) if '2023' in row and pd.notna(row['2023']) else 0.0
            val_2024 = float(row['2024']) if '2024' in row and pd.notna(row['2024']) else 0.0

            if val_2023 > 0:
                growth_rate = (val_2024 - val_2023) / val_2023
            else:
                growth_rate = 0.05

            clamped_rate = max(-0.02, min(0.08, growth_rate))
            val_2025 = round(val_2024 * (1.0 + clamped_rate), 2)
            vals_2025.append(val_2025)

        df['2025'] = vals_2025

    import_df_to_db(df, db_path=db_path)
    print(f"Successfully seeded database at {db_path} with 2018–2024 PSA baseline data + preliminary 2025 column (ready for official 2025 upload).")
    return df

if __name__ == '__main__':
    seed_database()
