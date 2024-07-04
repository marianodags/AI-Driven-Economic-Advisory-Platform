# Cleaning and preprocessing data
data = data.dropna()
data['GDP_growth'] = data['GDP'].pct_change()
