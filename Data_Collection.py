import pandas as pd
import os

def load_data(filepath='zamboanga_gdp.csv'):
    """
    Loads Zamboanga del Norte PPA GDP dataset.
    """
    if not os.path.exists(filepath):
        filepath = 'economic_data.csv'
    return pd.read_csv(filepath)

if __name__ == '__main__':
    df = load_data()
    print("Loaded Data Shape:", df.shape)
    print(df.head())
