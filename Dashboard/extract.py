import pandas as pd

# ---------------
# Extraction Part
# ---------------
def extract():
    basket_df = pd.read_csv("data/raw/basket_details.csv")
    customer_df = pd.read_csv("data/raw/customer_details.csv")
    return basket_df, customer_df
