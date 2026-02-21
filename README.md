# ETL Pipeline – Customer & Basket Data (Python / Pandas)

## Projektüberblick
Dieses Projekt implementiert einen vollständigen ETL-Prozess (Extract, Transform, Load) in Python.
Ziel ist es, zwei CSV-Datenquellen (Kundendaten und Warenkorb-/Einkaufsdaten) zu bereinigen, zu harmonisieren,
auf Kundenebene zu aggregieren und als Analyse-Datensatz zu exportieren.

Der Schwerpunkt des Projekts liegt auf einem komplexen ETL-Prozess (mehrere Datenquellen, Cleaning, Typisierung,
Missing-Values-Strategie, Feature Engineering und Aggregationen). Damit ist keine zusätzliche Graphdatenbank erforderlich,
wenn der ETL-Prozess ausreichend umfangreich ist (siehe Modulvorgaben).

## Datenquellen
- `customer_details.csv` (Kundenstammdaten)
- `basket_details.csv` (Transaktions-/Warenkorbdaten)

Hinweis: In den gelieferten Tabellen gibt es nur eine geringe Überschneidung der `customer_id` zwischen beiden Quellen.
Das wird im Projekt als Ergebnis/Limitierung dokumentiert (Datenqualität/Schlüsselinkonsistenz), der ETL-Prozess selbst
behandelt Nicht-Matches korrekt (Left-Join, Nullwerte werden zu 0/-1).

## ETL-Schritte (Kurzbeschreibung)
### Extract
- Einlesen der CSV-Dateien (UTF-8)
- Harmonisierung der Schlüsselspalte `customer_id`

### Transform
- Typkonvertierungen (numeric, datetime)
- Duplikate entfernen
- Missing Values behandeln (Median/0/UNKNOWN)
- Feature Engineering: Zeitfeatures, Kundengruppen (Age/Tenure)
- Customer-Level Aggregationen aus Basket-Daten:
  - Anzahl Einkaufstage (`total_baskets`)
  - Gesamtmenge gekaufter Items (`total_items`)
  - Durchschnittliche Korbgröße (`avg_basket_size`)
  - Anzahl unterschiedlicher Produkte (`distinct_products`)
  - Datum letzter Einkauf & Recency (`days_since_last_basket`)
- Zusammenführen (Left-Join) von Kundendaten + Aggregationen

### Load
- Export als `customer_basket_ready.csv`

## Voraussetzungen
- Python 3.10+ empfohlen
- Pakete: siehe `requirements.txt`

## Installation
```bash
pip install -r requirements.txt