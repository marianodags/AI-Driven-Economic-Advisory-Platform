import pandas as pd
import numpy as np

def process_data(df):
    """
    Processes Zamboanga del Norte industry dataset.
    Calculates total GDP per year, sector breakdowns (Agriculture, Industry, Services),
    growth rates, industry percentage contributions, and all 8 Economic Analytics Matrices.
    Dynamically adapts to available year columns in the database (e.g., 2018 through 2025+).
    Identifies complete years for baseline executive metrics to avoid partial import distortions.
    """
    df = df.copy()
    all_year_cols = [c for c in df.columns if str(c).isdigit()]
    years = sorted(all_year_cols, key=lambda x: int(x))

    # Yearly total GDP
    total_gdp = {y: float(df[y].fillna(0).sum()) for y in years}

    # Yearly sector totals
    sector_gdp = {}
    for cat in ['Agriculture', 'Industry', 'Services']:
        cat_df = df[df['category'] == cat]
        sector_gdp[cat] = {y: float(cat_df[y].fillna(0).sum()) for y in years}

    # Identify complete years where all industry sectors have valid non-zero figures
    complete_years = []
    for y in years:
        non_zero_count = (df[y].fillna(0) > 0).sum()
        if non_zero_count == len(df) and total_gdp[y] > 0:
            complete_years.append(y)

    latest_year = complete_years[-1] if complete_years else years[-1]
    prev_year = complete_years[-2] if len(complete_years) > 1 else (years[-2] if len(years) > 1 else years[0])

    # Yearly growth rates for overall pipeline
    yearly_df = pd.DataFrame({'year': [int(y) for y in years], 'gdp': [total_gdp[y] for y in years]})
    yearly_df['gdp_growth'] = yearly_df['gdp'].pct_change() * 100

    # Latest complete growth calculation
    latest_growth = 0.0
    if latest_year in total_gdp and prev_year in total_gdp and total_gdp[prev_year] > 0:
        latest_growth = ((total_gdp[latest_year] - total_gdp[prev_year]) / total_gdp[prev_year]) * 100

    # Build 8 Economic Analytics Matrices
    major_analytics = {}
    sector_names = {
        'Agriculture': 'Agriculture Sector',
        'Industry': 'Industry Sector',
        'Services': 'Services Sector',
        'All Industries': 'All Industries (Total GDP)'
    }

    for cat_key, display_name in sector_names.items():
        growth_rate = {}
        share_in_gdp = {}
        contribution = {}
        pct_share = {}

        for i, y in enumerate(years):
            curr_val = total_gdp[y] if cat_key == 'All Industries' else sector_gdp[cat_key][y]
            tot_gdp = total_gdp[y]

            sh = (curr_val / tot_gdp * 100) if tot_gdp else 0.0
            share_in_gdp[y] = sh
            pct_share[y] = sh

            if i == 0:
                growth_rate[y] = None
                contribution[y] = None
            else:
                py = years[i - 1]
                prev_val = total_gdp[py] if cat_key == 'All Industries' else sector_gdp[cat_key][py]
                prev_tot_gdp = total_gdp[py]

                gr = (((curr_val - prev_val) / prev_val) * 100) if prev_val else 0.0
                growth_rate[y] = gr

                contrib = (((curr_val - prev_val) / prev_tot_gdp) * 100) if prev_tot_gdp else 0.0
                contribution[y] = contrib

        major_analytics[display_name] = {
            'growth_rate': growth_rate,
            'share_in_gdp': share_in_gdp,
            'contribution_to_growth': contribution,
            'percentage_share': pct_share
        }

    # All Industries Analytics Matrix
    all_ind_analytics = {}
    for _, row in df.iterrows():
        code = str(row['code'])
        ind_name = str(row['industry'])
        cat = str(row['category'])

        growth_rate = {}
        share_in_gdp = {}
        contribution = {}
        pct_share = {}

        for i, y in enumerate(years):
            curr_val = float(row[y]) if pd.notna(row[y]) else 0.0
            tot_gdp = total_gdp[y]

            sh = (curr_val / tot_gdp * 100) if tot_gdp else 0.0
            share_in_gdp[y] = sh
            pct_share[y] = sh

            if i == 0:
                growth_rate[y] = None
                contribution[y] = None
            else:
                py = years[i - 1]
                prev_val = float(row[py]) if pd.notna(row[py]) else 0.0
                prev_tot_gdp = total_gdp[py]

                gr = (((curr_val - prev_val) / prev_val) * 100) if prev_val else 0.0
                growth_rate[y] = gr

                contrib = (((curr_val - prev_val) / prev_tot_gdp) * 100) if prev_tot_gdp else 0.0
                contribution[y] = contrib

        all_ind_analytics[code] = {
            'industry': ind_name,
            'category': cat,
            'growth_rate': growth_rate,
            'share_in_gdp': share_in_gdp,
            'contribution_to_growth': contribution,
            'percentage_share': pct_share
        }

    return {
        'raw_df': df,
        'years': years,
        'complete_years': complete_years,
        'latest_year': latest_year,
        'prev_year': prev_year,
        'total_gdp': total_gdp,
        'sector_gdp': sector_gdp,
        'yearly_df': yearly_df,
        'latest_gdp_2024': total_gdp[latest_year],
        'latest_growth_2024': float(latest_growth),
        'major_analytics': major_analytics,
        'all_ind_analytics': all_ind_analytics
    }

if __name__ == '__main__':
    from Data_Collection import load_data
    data = load_data()
    processed = process_data(data)
    print("Processed Yearly GDP:", processed['total_gdp'])
