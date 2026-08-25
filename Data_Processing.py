import pandas as pd
import numpy as np

def process_data(df):
    """
    Processes Zamboanga del Norte industry dataset.
    Calculates total GDP per year, sector breakdowns (Agriculture, Industry, Services),
    growth rates, and industry percentage contributions.
    Dynamically adapts to available year columns in the database (e.g., 2018 through 2025+).
    """
    df = df.copy()
    all_year_cols = [c for c in df.columns if str(c).isdigit()]
    years = sorted(all_year_cols, key=lambda x: int(x))

    # Yearly total GDP
    total_gdp = {y: float(df[y].sum()) for y in years}

    # Yearly sector totals
    sector_gdp = {}
    for cat in ['Agriculture', 'Industry', 'Services']:
        cat_df = df[df['category'] == cat]
        sector_gdp[cat] = {y: float(cat_df[y].sum()) for y in years}

    # Yearly growth rates
    yearly_df = pd.DataFrame({'year': [int(y) for y in years], 'gdp': [total_gdp[y] for y in years]})
    yearly_df['gdp_growth'] = yearly_df['gdp'].pct_change() * 100

    latest_year = years[-1]
    prev_year = years[-2] if len(years) > 1 else years[0]

    # Industry level summary for latest year
    df[f'share_{latest_year}'] = (df[latest_year] / total_gdp[latest_year]) * 100
    df[f'growth_{prev_year}_{latest_year}'] = ((df[latest_year] - df[prev_year]) / df[prev_year]) * 100

    latest_growth = yearly_df.loc[yearly_df['year'] == int(latest_year), 'gdp_growth'].values[0]
    if pd.isna(latest_growth):
        latest_growth = 0.0

    return {
        'raw_df': df,
        'years': years,
        'latest_year': latest_year,
        'prev_year': prev_year,
        'total_gdp': total_gdp,
        'sector_gdp': sector_gdp,
        'yearly_df': yearly_df,
        'latest_gdp_2024': total_gdp[latest_year],
        'latest_growth_2024': float(latest_growth)
    }

if __name__ == '__main__':
    from Data_Collection import load_data
    data = load_data()
    processed = process_data(data)
    print("Processed Yearly GDP:", processed['total_gdp'])
