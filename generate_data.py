import pandas as pd
import numpy as np
import random
import os

os.makedirs('reports', exist_ok=True)

np.random.seed(42)
n_rows = 1000

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Sports', 'Books']
regions = ['North', 'South', 'East', 'West']

data = {
    'TransactionID': range(1, n_rows + 1),
    'Date': pd.date_range(start='2025-01-01', periods=n_rows, freq='h'),
    'Category': np.random.choice(categories, n_rows),
    'Region': np.random.choice(regions, n_rows),
    'Quantity': np.random.randint(1, 15, n_rows),
    'Price': np.random.uniform(10.0, 500.0, n_rows),
    'CustomerAge': np.random.randint(18, 70, n_rows)
}

df = pd.DataFrame(data)

df.loc[np.random.choice(n_rows, 50, replace=False), 'Category'] = np.nan
df.loc[np.random.choice(n_rows, 75, replace=False), 'Price'] = np.nan
df.loc[np.random.choice(n_rows, 40, replace=False), 'CustomerAge'] = np.nan

df.loc[np.random.choice(n_rows, 10, replace=False), 'Price'] = np.random.uniform(2000.0, 5000.0, 10)
df.loc[np.random.choice(n_rows, 5, replace=False), 'Quantity'] = np.random.randint(100, 500, 5)

duplicates = df.sample(n=50, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('raw_data.csv', index=False)
