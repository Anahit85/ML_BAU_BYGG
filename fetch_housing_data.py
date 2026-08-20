import requests
import pandas as pd

def fetch_housing_data():
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/BO/BO0104/BO0104D/BO0104T01"
    
    # 1. Metadaten prüfen
    resp_meta = requests.get(url)
    resp_meta.raise_for_status()
    print("Metadaten erfolgreich abgerufen!")

    # 2. Daten abfragen
    query = {
        "query": [],
        "response": {"format": "json"}
    }
    
    resp_data = requests.post(url, json=query)
    resp_data.raise_for_status()
    
    raw_data = resp_data.json()
    print(f"Daten erfolgreich geladen! ({len(raw_data['data'])} Datensätze empfangen)")
    
    # 3. Dynamisches Umwandeln in ein DataFrame
    rows = []
    for item in raw_data['data']:
        # Kombiniert alle Key-Elemente und Values flexibel zu einer Liste
        rows.append(item['key'] + item['values'])
        
    df = pd.DataFrame(rows)
    
    # 4. Spaltennamen basierend auf der tatsächlichen Spaltenanzahl vergeben
    if df.shape[1] == 2:
        df.columns = ['Tid', 'Antal_Bostader']
    elif df.shape[1] == 3:
        df.columns = ['Hustyp', 'Tid', 'Antal_Bostader']
    elif df.shape[1] == 4:
        df.columns = ['Region', 'Hustyp', 'Tid', 'Antal_Bostader']
    
    # Als CSV speichern
    df.to_csv("housing_data.csv", index=False)
    print("Daten als 'housing_data.csv' gespeichert!")
    
    return df

if __name__ == "__main__":
    df = fetch_housing_data()
    print("\nErste Zeilen des DataFrames:")
    print(df.head())