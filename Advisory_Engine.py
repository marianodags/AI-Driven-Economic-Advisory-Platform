def generate_economic_advisory(processed_data, forecast_data):
    """
    Generates AI economic advisory, policy feedback, performance evaluation,
    and strategic recommendations tailored exclusively for Zamboanga del Norte.
    """
    total_2024 = processed_data['latest_gdp_2024']
    growth_2024 = processed_data['latest_growth_2024']
    sector_gdp = processed_data['sector_gdp']

    agri_2024 = sector_gdp['Agriculture']['2024']
    ind_2024 = sector_gdp['Industry']['2024']
    serv_2024 = sector_gdp['Services']['2024']

    services_share = (serv_2024 / total_2024) * 100
    industry_share = (ind_2024 / total_2024) * 100
    agri_share = (agri_2024 / total_2024) * 100

    fc_2025 = forecast_data['forecast_total'][2025]
    fc_2027 = forecast_data['forecast_total'][2027]
    projected_growth_2025 = ((fc_2025 - total_2024) / total_2024) * 100

    executive_summary = (
        f"Zamboanga del Norte recorded a total Gross Domestic Product (GDP) of PHP {total_2024:,.0f} thousand in 2024, "
        f"representing a growth rate of {growth_2024:.2f}%. The economy is heavily service-driven ({services_share:.1f}% share), "
        f"followed by Industry ({industry_share:.1f}% share) and Agriculture, Forestry, and Fishing ({agri_share:.1f}% share). "
        f"AI econometric forecasting projects GDP to reach PHP {fc_2025:,.0f} thousand in 2025 ({projected_growth_2025:.2f}% YoY growth) "
        f"and PHP {fc_2027:,.0f} thousand by 2027."
    )

    key_insights = [
        {
            'title': 'Services Sector Dominance & Retail Expansion',
            'status': 'Strong Growth',
            'detail': f"Services contributes PHP {serv_2024:,.0f} thousand ({services_share:.1f}% of total economy). Wholesale and retail trade, repair of motor vehicles, and education are key drivers."
        },
        {
            'title': 'Manufacturing & Construction Resurgence',
            'status': 'Expanding',
            'detail': f"Industry accounts for PHP {ind_2024:,.0f} thousand ({industry_share:.1f}% share). Manufacturing recovered to PHP 22.3B in 2024, supported by robust public and private construction activities (PHP 20.2B)."
        },
        {
            'title': 'Agricultural Output Stabilization',
            'status': 'Needs Modernization',
            'detail': f"Agriculture, forestry, and fishing generated PHP {agri_2024:,.0f} thousand ({agri_share:.1f}% share). While a critical employer, output contracted slightly (-1.86% in 2024), highlighting climate and supply chain risks."
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
