# Fortschritt: BAU BYGG AB – Marketing-Targeting-Modell

Projekt: ML-Modell zur Identifikation der besten Zielgebiete für
Marketing (Bad-/Villa-Renovierung) im Großraum Stockholm.


## Ziel des Projekts

Herausfinden, in welchen Kommunen/Gebieten im Großraum Stockholm die
höchste Wahrscheinlichkeit besteht, dass Haushalte in eine
Bad-/Villa-Renovierung investieren - damit das Marketing (Google Ads,
Meta Ads, Flyer) gezielt dorthin ausgerichtet werden kann.

Da BAU BYGG AB noch keine eigenen strukturierten Kundendaten hat, nutzen
wir öffentliche (offene) Daten von Statistiska centralbyrån (SCB) als
Grundlage, statt eines klassischen Lead-Scoring-Modells.


## Was bisher gemacht wurde

### 1. Projekt-Setup
- Lokales Python-Projekt in VS Code aufgesetzt (`ML Project BAUBYGG`)
- Virtuelle Umgebung (venv) erstellt
- Pakete installiert: `requests`, `pandas`

### 2. SCB-API erkundet
- Die SCB Statistikdatenbank (api.scb.se) ist wie ein Ordnerbaum
  aufgebaut. Wir haben uns durchnavigiert:
  Start -> HE (Hushållens ekonomi) -> HE0110 (Inkomster och skatter)
  -> HE0110I (Regionale Statistik unterhalb Kommun-Ebene)
- Skript `explore_scb.py` erstellt, um Ordnerinhalte und
  Tabellen-Variablen der API anzuzeigen

### 3. Erste Datenabfrage (mit Hindernissen)
- Versuch: Durchschnittseinkommen pro kleinem Stadtteil (DeSO/RegSO)
  in Stockholm abzurufen
- Problem: SCB unterdrückt aus Datenschutzgründen alle Werte
  unterhalb der Kommun-Ebene für dieses Merkmal (Ergebnis war
  durchgehend ".." statt echter Zahlen) - das gilt sowohl für DeSO
  (671 kleine Gebiete) als auch RegSO (127 größere Gebiete)
- Getestet und bestätigt: Auf Kommun-Ebene (z.B. "0180" = Stockholm)
  funktioniert die Abfrage einwandfrei (Beispielwert: 467,7 tkr)

### 4. Datensatz erfolgreich erstellt ✅
- Strategie angepasst: Vergleich auf **Kommun-Ebene** statt
  Stadtteil-Ebene (passt ohnehin besser zu Google/Meta Ads
  Geo-Targeting, das meist nur Kommun-/PLZ-genau funktioniert)
- Skript `fetch_income_data.py` ruft für alle 26 Kommunen im
  Großraum Stockholm (Stockholms län) den Anteil der Bevölkerung im
  höchsten Einkommensquartil ab
- Ergebnis gespeichert in: `data/stockholm_lan_inkomst_2024.csv`

**Top-Ergebnisse (Anteil Top-Einkommensverdiener pro Kommun, 2024):**

| Kommun     | Anteil oberstes Einkommensquartil |
|------------|-----------------------------------|
| Danderyd   | 55 %                              |
| Täby       | 48 %                              |
| Lidingö    | 46 %                              |
| Nacka      | 44 %                              |
| Vaxholm    | 43 %                              |
| Ekerö      | 41 %                              |
| Solna      | 41 %                              |

-> Diese Kommunen sind laut Einkommensdaten die vielversprechendsten
   Zielgebiete für Bad-/Villa-Renovierungs-Marketing.


## Wichtige technische Lernpunkte

- SCB PxWebApi: GET-Request zum Navigieren/Erkunden, POST-Request mit
  einer genauen Variablen-Auswahl (Region, Jahr, Merkmal, Geschlecht,
  etc.) für den eigentlichen Datenabruf
- Datenschutz bei kleinräumigen Statistiken: SCB veröffentlicht
  bestimmte Merkmale (v.a. Durchschnitts-/Quartilseinkommen) nicht für
  sehr kleine Gebiete, um Rückschlüsse auf Einzelpersonen zu verhindern
- Lösung bei fehlenden Daten: eine Ebene höher gehen (gröbere
  Regionsebene) und/oder ein anderes Merkmal wählen (Prozentanteile
  statt absolute Durchschnittswerte)


## Nächste Schritte (geplant)

1. Zweite Datenquelle hinzufügen: Immobilien-/Gebäudedaten pro Kommun
   (Baujahr, Immobilienpreise, Anteil Einfamilienhäuser/Villen) aus dem
   SCB-Bereich "BO" (Boende, byggande och bebyggelse)
2. Datensätze zusammenführen (Einkommen + Immobiliendaten pro Kommun)
3. Feature Engineering: eigenen "Renovierungs-Potenzial-Score" pro
   Kommun berechnen
4. Modellierung: Clustering (z.B. KMeans) zur Segmentierung der
   Kommunen nach Marketing-Priorität
5. Ergebnis nutzen: Ranking-Liste als Grundlage für Google/Meta Ads
   Geo-Targeting
6. Parallel: BAU BYGG AB sollte eigene Anfragedaten sammeln (Datum,
   PLZ des Kunden, Projekttyp, Angebotssumme, gewonnen/verloren) für
   ein späteres echtes Lead-Scoring-Modell


## Erreichte Meilensteine

- [x] Daten via SCB-Skript geladen (`housing_data.csv`)
- [x] Explorative Datenanalyse (EDA) im Notebook `01_eda_housing.ipynb`
- [x] Visualisierung des Wohnungsbestands (Balken- & Trend-Diagramme)
- [x] Machine Learning Modelle trainiert:
  - Lineare Regression (R² = 0.9965, MAE = 10.371)
  - Polynomielle Regression Grad 2 (R² = 0.9975, MAE = 8.170)
- [x] Prognose für 2026–2030 erstellt