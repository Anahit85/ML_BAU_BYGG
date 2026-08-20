"""
Schritt 1a: SCB API erkunden.
 
Die SCB Statistikdatenbank ist wie ein Ordnerbaum aufgebaut. Man startet
oben und klickt sich (per API-Aufruf) durch die Ordner, bis man bei einer
konkreten Tabelle ankommt.
 
Ausführen mit:
    python src/explore_scb.py
und dann dem Pfad folgen, den das Skript ausgibt (siehe Kommentare unten).
"""
import requests
import json
 
BASE_URL = "https://api.scb.se/OV0104/v1/doris/sv/ssd"
 
 
def list_folder(path=""):
    """Zeigt an, was sich in einem Ordner der SCB-Datenbank befindet."""
    url = f"{BASE_URL}/{path}" if path else BASE_URL
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    items = resp.json()
 
    print(f"\n=== Inhalt von: {path or '(Start)'} ===")
    for item in items:
        typ = "ORDNER" if item.get("type") == "l" else "TABELLE"
        print(f"  [{typ}] {item['id']}  –  {item['text']}")
    return items
 
 
def show_table_metadata(path):
    """Zeigt die Variablen einer konkreten Tabelle (z.B. welche Regionen,
    Jahre, etc. verfügbar sind), bevor wir die Daten selbst abrufen."""
    url = f"{BASE_URL}/{path}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    meta = resp.json()
 
    print(f"\n=== Variablen der Tabelle: {path} ===")
    for var in meta.get("variables", []):
        print(f"\n  Variable: {var['text']}  (code: {var['code']})")
        # Zeig nur die ersten 5 Werte, sonst wird's unübersichtlich
        values = list(zip(var["values"], var["valueTexts"]))
        for val_code, val_text in values[:5]:
            print(f"     {val_code}  –  {val_text}")
        if len(values) > 5:
            print(f"     ... ({len(values)} Werte insgesamt)")
    return meta
 
 
def find_stockholm_regions_and_total_income_code(path):
    """Filtert die Regionsliste auf Stockholm (Kommun-Code 0180) und zeigt
    die komplette Liste der Einkommenskomponenten, damit wir den Code für
    'Gesamteinkommen' finden."""
    url = f"{BASE_URL}/{path}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    meta = resp.json()
 
    for var in meta.get("variables", []):
        if var["code"] == "Region":
            print("\n=== Stockholm-Regionen (Kommun-Code 0180) ===")
            stockholm = [
                (c, t) for c, t in zip(var["values"], var["valueTexts"])
                if c.startswith("0180")
            ]
            print(f"Gefunden: {len(stockholm)} Einträge")
            for c, t in stockholm[:15]:
                print(f"  {c}  –  {t}")
            if len(stockholm) > 15:
                print(f"  ... und {len(stockholm) - 15} weitere")
 
        if var["code"] == "Inkomstkomponenter":
            print("\n=== ALLE Einkommenskomponenten ===")
            for c, t in zip(var["values"], var["valueTexts"]):
                print(f"  {c}  –  {t}")
 
        if var["code"] == "Tid":
            print(f"\n=== Verfügbare Jahre ===")
            print(f"  Neuestes Jahr: {var['values'][-1]}")
 
 
if __name__ == "__main__":
    find_stockholm_regions_and_total_income_code(
        "HE/HE0110/HE0110I/Tab2InkDesoRegso"
    )