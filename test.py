import pandas as pd

df = pd.read_csv("customer_details.csv", sep=",")
print(df.head())