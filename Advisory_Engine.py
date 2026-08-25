def generate_economic_advisory(processed_data, forecast_data):
    """
    Generates AI economic advisory, policy feedback, performance evaluation,
    and strategic recommendations tailored exclusively for Zamboanga del Norte.
    """
    total_latest = processed_data['latest_gdp_2024']
    growth_latest = processed_data['latest_growth_2024']
    latest_year = processed_data['latest_year']
    sector_gdp = processed_data['sector_gdp']

    agri_latest = sector_gdp['Agriculture'][latest_year]
    ind_latest = sector_gdp['Industry'][latest_year]
    serv_latest = sector_gdp['Services'][latest_year]

    services_share = (serv_latest / total_latest) * 100 if total_latest > 0 else 0
    industry_share = (ind_latest / total_latest) * 100 if total_latest > 0 else 0
    agri_share = (agri_latest / total_latest) * 100 if total_latest > 0 else 0

    forecast_dict = forecast_data.get('forecast_total', {})
    fc_years = sorted(list(forecast_dict.keys()))
    first_fc_year = fc_years[0] if fc_years else 2026
    last_fc_year = fc_years[-1] if fc_years else 2030

    fc_first_val = forecast_dict.get(first_fc_year, total_latest * 1.04)
    fc_last_val = forecast_dict.get(last_fc_year, total_latest * 1.20)
    projected_growth = ((fc_first_val - total_latest) / total_latest) * 100 if total_latest > 0 else 0

    executive_summary = (
        f"Zamboanga del Norte recorded a total Gross Domestic Product (GDP) of PHP {total_latest:,.0f} thousand in {latest_year}, "
        f"representing a growth rate of {growth_latest:.2f}%. The economy is heavily service-driven ({services_share:.1f}% share), "
        f"followed by Industry ({industry_share:.1f}% share) and Agriculture, Forestry, and Fishing ({agri_share:.1f}% share). "
        f"AI econometric forecasting projects GDP to reach PHP {fc_first_val:,.0f} thousand in {first_fc_year} ({projected_growth:.2f}% growth) "
        f"and PHP {fc_last_val:,.0f} thousand by {last_fc_year}."
    )

    key_insights = [
        {
            'title': 'Services Sector Dominance & Retail Expansion',
            'status': 'Strong Growth',
            'detail': f"Services contributes PHP {serv_latest:,.0f} thousand ({services_share:.1f}% of total economy). Wholesale and retail trade, repair of motor vehicles, and education are key drivers."
        },
        {
            'title': 'Manufacturing & Construction Resurgence',
            'status': 'Expanding',
            'detail': f"Industry accounts for PHP {ind_latest:,.0f} thousand ({industry_share:.1f}% share). Manufacturing recovered strongly, supported by robust public and private construction activities."
        },
        {
            'title': 'Agricultural Output Stabilization',
            'status': 'Needs Modernization',
            'detail': f"Agriculture, forestry, and fishing generated PHP {agri_latest:,.0f} thousand ({agri_share:.1f}% share). While a critical employer, output requires climate resilience and supply chain modernization."
        }
    ]

    strategic_recommendations = [
        {
            'sector': 'Agriculture & Agri-Business',
            'action': 'Agri-Processing & Climate Resilience',
            'description': 'Establish coconut, rubber, and seaweeds value-added processing hubs in Dipolog and Dapitan to shift from raw exports to high-value processed goods.'
        },
        {
            'sector': 'Industry & Logistics',
            'action': 'Infrastructure & Port Enhancements',
            'description': 'Expand port capacity at Galas Port (Dipolog) and Pulauan Port (Dapitan) to reduce shipping costs and boost intra-regional trade across Mindanao.'
        },
        {
            'sector': 'Services & Tourism',
            'action': 'Eco-Tourism & Digital Commerce',
            'description': 'Capitalize on Dapitan City\'s historical heritage and coastal tourism while incentivizing MSME digital adoption and financial inclusion.'
        },
        {
            'sector': 'Human Capital & Education',
            'action': 'Skills Alignment & Healthcare Investment',
            'description': 'Align vocational programs (TESDA/JRMSU) with light manufacturing, IT-BPO, and modern agri-tech, expanding public health facilities across rural municipalities.'
        }
    ]

    return {
        'executive_summary': executive_summary,
        'key_insights': key_insights,
        'strategic_recommendations': strategic_recommendations
    }
