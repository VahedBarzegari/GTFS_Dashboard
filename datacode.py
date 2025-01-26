import pandas as pd

from pathlib import Path

infile = Path(__file__).parent / "sales.csv"
df1 = pd.read_csv(infile)
df1['order_date'] = pd.to_datetime(df1['order_date'])
df1['month'] = df1['order_date'].dt.month_name()
df1['hour'] = df1['order_date'].dt.hour
df1['value ($)'] = df1['quantity_ordered'] * df1['price_each']