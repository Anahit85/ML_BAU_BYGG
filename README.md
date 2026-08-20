# ML_BAU_BYGG

# 🏢 Swedish Housing Stock Forecast (ML_BAU_BYGG)

Eine Machine-Learning-Analyse zur Prognose des Wohnungsbestands in Schweden bis 2030 auf Basis historischer Daten der Statistiska centralbyrån (SCB).

---

## 📊 Projektübersicht

Dieses Projekt analysiert die Entwicklung des schwedischen Wohnungsbestands von 2013 bis 2025 und nutzt Regressionen zur Vorhersage der Bautrends für die Jahre 2026 bis 2030.

* **Datenquelle:** Statistiska centralbyrån (SCB)
* **Ziel:** Prognose des künftigen Wohnungsbestands und Visualisierung von Wachstumstrends

---

## 📈 Ergebnisse & Modellvergleich

Zur Bestimmung des besten Trends wurden zwei Regressionsmodelle auf den historischen Daten evaluiert:

* **Lineare Regression:**
  * $R^2$-Score: `0.9965`
  * Mean Absolute Error (MAE): `10.371 Wohnungen`
* **Polynomielle Regression (Grad 2):**
  * $R^2$-Score: `0.9975`
  * Mean Absolute Error (MAE): `8.170 Wohnungen`

**Fazit:** Das polynomielle Modell (Grad 2) bildet den leicht abgeflachten Bautrend der letzten Jahre präziser ab und liefert die verlässlichere Prognose bis 2030.

---

## 📁 Projektstruktur

```text
ML_BAU_BYGG/
├── data/
│   └── housing_data.csv       # Extrahierte Datensätze der SCB
├── 01_eda_housing.ipynb       # Notebook mit EDA, Visualisierungen & ML-Modellen
├── fetch_housing_data.py      # Skript zum Datenabruf
├── FORTSCHRITT.md             # Projekt-Dokumentation & Meilensteine
└── README.md                  # Projektbeschreibung
