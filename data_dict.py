import pandas as pd

# Sample economic data in dictionary format
data_dict = {
    'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01'],
    'GDP': [1000000, 1010000, 1020500, 1031500],
    'establishment_revenue': [50000, 51000, 52000, 53000],
    'employment_rate': [60, 61, 62, 63]
}

# Create DataFrame
data = pd.DataFrame(data_dict)

# Print the DataFrame to verify
print(data)
