import pandas as pd

# ---------------
# Extraktion
# ---------------
def extract():
    basket_df = pd.read_csv("Dashboard/data/basket_details.csv", sep=",", encoding="utf-8")
    customer_df = pd.read_csv("Dashboard/data/customer_details.csv", sep=",", encoding="utf-8")

    basket_df["customer_id"] = basket_df["customer_id"].astype(str).str.strip() 
    customer_df["customer_id"] = customer_df["customer_id"].astype(str).str.strip()
    
    return basket_df, customer_df

#----------------
# Transformation
#----------------

def transform(customer_df, basket_df):
    
    # Setzen von Datentypen
    customer_df["customer_age"] = pd.to_numeric(customer_df["customer_age"], errors="coerce") 
    customer_df["tenure"] = pd.to_numeric(customer_df["tenure"], errors="coerce") 
    basket_df["basket_count"] = pd.to_numeric(basket_df["basket_count"], errors="coerce")

    # Datum umwandeln (YYYY-MM-DD)
    basket_df["basket_date"] = pd.to_datetime(basket_df["basket_date"], errors="coerce")

    # Entferung von Dublikaten
    customer_df = customer_df.drop_duplicates(subset=["customer_id"])
    basket_df = basket_df.drop_duplicates()

    # Behandlung fehlender Werte
    customer_df["customer_age"] = customer_df["customer_age"].fillna(customer_df["customer_age"].median())
    customer_df["tenure"] = customer_df["tenure"].fillna(customer_df["tenure"].median())
    basket_df["basket_count"] = basket_df["basket_count"].fillna(0)

    # 'sex' bereinigen und harmonisieren
    customer_df["sex"] = customer_df["sex"].fillna("UNKNOWN")
    customer_df["sex"] = customer_df["sex"].astype(str).str.upper().str.strip()
    customer_df["sex"] = customer_df["sex"].replace({
        "FEMALE": "F",
        "MALE": "M",     
    })
    customer_df["sex"] = customer_df["sex"].fillna("UNKNOWN")

    # Erweiterung der Datumspalten
    basket_df["basket_year"] = basket_df["basket_date"].dt.year 
    basket_df["basket_month"] = basket_df["basket_date"].dt.month 
    basket_df["basket_weekday"] = basket_df["basket_date"].dt.weekday

    # Customer-Level Aggregationen auf Basis von basket_details
    agg_features = (basket_df.groupby("customer_id").agg(
        total_baskets=("basket_date", "nunique"),                        # Anzahl untersch. Einkaufstage
        total_items=("basket_count", "sum"),                            # Summe gekaufter Artikel   
        avg_basket_size=("basket_count", "mean"),                       # durschnittl. Warenkorbgröße
        distinct_products=("product_id", "nunique"),                     # Anzahl versch. Produkte
        last_basket_date=("basket_date", "max")                         # Datum letzter Einkauf
        )
        .reset_index()
    )

    agg_features["customer_id"] = agg_features["customer_id"].astype(str).str.strip()

    # Berechnung Tage seit letztem Kauf
    max_date = basket_df["basket_date"].max()
    agg_features["days_since_last_basket"] = (max_date - agg_features["last_basket_date"]).dt.days

    # Altersgruppen und Gruppen nach Kundenbeziehung (Tenure) bilden 
    bins_age = [0, 24, 34, 44, 120] 
    labels_age = ["<25", "25-34", "35-44", "45+"] 
    customer_df["age_group"] = pd.cut( customer_df["customer_age"], bins=bins_age, labels=labels_age, right=True )

    bins_tenure = [0, 12, 36, 120] 
    labels_tenure = ["neu", "mittel", "lang"] 
    customer_df["tenure_group"] = pd.cut( customer_df["tenure"], bins=bins_tenure, labels=labels_tenure, right=True )

    # Join (Aggregierte Daten aus Basket & Kundendaten)
    for df in [customer_df, basket_df]: df["customer_id"] = df["customer_id"].astype(str).str.strip() 
    
    agg_features["customer_id"] = agg_features["customer_id"].astype(str).str.strip()
    
    final_df = customer_df.merge(agg_features, on="customer_id", how="left")

    print("Anzahl Kunden:", len(customer_df)) 
    print("Anzahl gemergter Kunden:", len(final_df[final_df['total_baskets'] > 0])) 
    print("Beispiel gemergt:", final_df[final_df['total_baskets'] > 0].head())

    # Kunden ohne Käufe fangen (Fehlende Basket Werte)
    final_df["sex"] = final_df["sex"].fillna("UNKNOWN") 
    final_df["customer_age"] = pd.to_numeric(final_df["customer_age"], errors="coerce") 
    final_df["tenure"] = pd.to_numeric(final_df["tenure"], errors="coerce") 
    
    for col in ["total_baskets", "total_items", "avg_basket_size", "distinct_products"]: final_df[col] = final_df[col].fillna(0) 
    
    final_df["last_basket_date"] = pd.to_datetime(final_df["last_basket_date"], errors="coerce") 
    final_df["days_since_last_basket"] = (pd.Timestamp("2023-12-31") - final_df["last_basket_date"]).dt.days
    final_df["days_since_last_basket"] = final_df["days_since_last_basket"].fillna(-1).astype(int)

    return final_df

#----------------
# Laden
#----------------

def load(final_df):
    final_df.to_csv("customer_basket_ready.csv", index=False)

#----------------
# Pipeline Runner   Ausführung ETL-Prozess
#----------------

def run_pipeline():
    basket_df, customer_df = extract()
    final_df = transform(customer_df, basket_df)
    load(final_df)

if __name__ == "__main__":
    run_pipeline()