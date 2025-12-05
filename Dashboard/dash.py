
import os
print("Arbeitsverzeichnis:", os.getcwd())
print("Dateien im Ordner:", os.listdir())


import pandas as pd
df = pd.read_csv("Dashboard/gaming_sales_data.csv", sep=";")
print(df.head())
