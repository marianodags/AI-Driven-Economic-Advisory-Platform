"""
Zamboanga del Norte Economic Analytics Dictionary Constants
"""

PROVINCE_METADATA = {
    'name': 'Province of Zamboanga del Norte',
    'region': 'Zamboanga Peninsula (Region IX)',
    'capital': 'Dipolog City',
    'base_year': '2018 Constant Prices',
    'unit': 'In thousand Philippine Pesos (PHP 000)',
    'latest_data_year': 2024,
    'source': 'Philippine Statistics Authority (PSA) - Provincial Product Accounts (PPA)'
}

SECTORS = ['Agriculture', 'Industry', 'Services']

def get_sample_data():
    from Data_Collection import load_data
    return load_data()

if __name__ == '__main__':
    print("Province Metadata:", PROVINCE_METADATA)
