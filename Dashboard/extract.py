import pandas as pd

# ---------------
# Extraktion
# ---------------
def extract():
    basket_df = pd.read_csv("data/raw/basket_details.csv")
    customer_df = pd.read_csv("data/raw/customer_details.csv")
    return basket_df, customer_df

#----------------
# Transformation
#----------------

def transform(customer_df, basket_df):
    
    # Setzen von Datentypen








#----------------
# Laden
#----------------

def load(return von transform):