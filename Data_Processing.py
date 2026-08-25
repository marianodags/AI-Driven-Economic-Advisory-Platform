import pandas as pd
import numpy as np

def process_data(df):
    """
    Processes Zamboanga del Norte industry dataset.
    Calculates total GDP per year, sector breakdowns (Agriculture, Industry, Services),
    growth rates, and industry percentage contributions.
    """
    df = df.copy()
    years = [str(y) for y in range(2018, 2025) if str(y) in df.columns]

    # Yearly total GDP
    total_gdp = {y: df[y].sum() for y in years}

    # Yearly sector totals
    sector_gdp = {}
    for cat in ['Agriculture', 'Industry', 'Services']:
        cat_df = df[df['category'] == cat]
        sector_gdp[cat] = {y: cat_df[y].sum() for y in years}

    # Yearly growth rates
    yearly_df = pd.DataFrame({'year': [int(y) for y in years], 'gdp': [total_gdp[y] for y in years]})
    yearly_df['gdp_growth'] = yearly_df['gdp'].pct_change() * 100

    # Industry level summary for 2024
    df['share_2024'] = (df['2024'] / total_gdp['2024']) * 100
    df['growth_2023_2024'] = ((df['2024'] - df['2023']) / df['2023']) * 100

    return {
        'raw_df': df,
        'years': years,
        'total_gdp': total_gdp,
        'sector_gdp': sector_gdp,
        'yearly_df': yearly_df,
        'latest_gdp_2024': total_gdp['2024'],
        'latest_growth_2024': yearly_df.loc[yearly_df['year'] == 2024, 'gdp_growth'].values[0]
    }

if __name__ == '__main__':
    from Data_Collection import load_data
    data = load_data()
    processed = process_data(data)
    print("Processed Yearly GDP:", processed['total_gdp'])
