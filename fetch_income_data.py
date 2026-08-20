"""
Schritt 2 (angepasst): Einkommensdaten für ALLE Kommunen im Großraum
Stockholm abrufen (Stockholms län) - nicht nur innerhalb Stockholm-Stadt.

Warum die Änderung? SCB veröffentlicht Durchschnitts-/Quartilseinkommen
aus Datenschutzgründen nur ab Kommun-Ebene, nicht für kleinere Stadtteile.
Das ist aber kein Problem für uns: Google/Meta Ads lässt sich ohnehin
meist nur auf Kommun- oder Postleitzahlenebene gezielt schalten - ein
Vergleich zwischen z.B. Danderyd, Nacka, Täby, Solna, Stockholm ist also
genau die richtige Granularität fürs Marketing-Targeting.

Ausführen mit:
    python fetch_income_data.py
"""
import requests
import pandas as pd

BASE_URL = "https://api.scb.se/OV0104/v1/doris/sv/ssd"
TABLE_PATH = "HE/HE0110/HE0110I/Tab1InkDesoRegso"


def get_stockholms_lan_kommun_codes():
    """Holt sich alle Kommun-Codes in Stockholms län (Region-Code beginnt
    mit '01' und ist 4-stellig, z.B. 0180 = Stockholm, 0162 = Danderyd)."""
    url = f"{BASE_URL}/{TABLE_PATH}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    meta = resp.json()
    for var in meta["variables"]:
        if var["code"] == "Region":
            codes = [
                (c, t) for c, t in zip(var["values"], var["valueTexts"])
                if c.startswith("01") and len(c) == 4
            ]
            return codes
    return []


def fetch_income_data():
    kommun_codes = get_stockholms_lan_kommun_codes()
    print(f"Anzahl Kommunen in Stockholms län gefunden: {len(kommun_codes)}")
    for c, t in kommun_codes[:10]:
        print(f"  {c} – {t}")

    codes_only = [c for c, t in kommun_codes]
    names_lookup = {c: t for c, t in kommun_codes}

    query = {
        "query": [
            {"code": "Region", "selection": {"filter": "item", "values": codes_only}},
            {"code": "InkomstTyp", "selection": {"filter": "item", "values": ["NeInk"]}},
            {"code": "Kon", "selection": {"filter": "item", "values": ["1+2"]}},
            {"code": "ContentsCode", "selection": {"filter": "item", "values": ["0000089S"]}},
            {"code": "Tid", "selection": {"filter": "item", "values": ["2024"]}},
        ],
        "response": {"format": "json"},
    }
    url = f"{BASE_URL}/{TABLE_PATH}"
    resp = requests.post(url, json=query, timeout=30)

    if resp.status_code != 200:
        print(f"FEHLER {resp.status_code}: {resp.text[:500]}")
        return None

    data = resp.json()
    rows = []
    for item in data["data"]:
        code = item["key"][0]
        rows.append({
            "kommun_code": code,
            "kommun_name": names_lookup.get(code, ""),
            "andel_hoechstes_einkommensquartil_pct": item["values"][0],
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(
        "andel_hoechstes_einkommensquartil_pct", ascending=False
    )
    df.to_csv("data/stockholm_lan_inkomst_2024.csv", index=False)
    print(f"\nFertig! {len(df)} Zeilen gespeichert in data/stockholm_lan_inkomst_2024.csv")
    print(df.to_string(index=False))
    return df


if __name__ == "__main__":
    fetch_income_data()
