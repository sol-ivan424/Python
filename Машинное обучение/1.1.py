
import requests
import pandas as pd
from datetime import datetime
import time

API_KEY = "1cc3e142190a45b5bf8202034251809" 
CITIES  = ["Helsinki", "Moscow"]          
DAYS    = 3                                   
OUTPUT  = "weatherapi_multivariate.csv"

def fetch_forecast(city: str, days: int = DAYS) -> dict:
    url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": city,      
        "days": days,
        "aqi": "no",
        "alerts": "no",
        "lang": "ru",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def to_dataframe(payload: dict) -> pd.DataFrame:
    loc = payload["location"]
    rows = []
    for day in payload["forecast"]["forecastday"]:
        for h in day["hour"]:
            rows.append({
                "city": loc.get("name"),
                "region": loc.get("region"),
                "country": loc.get("country"),
                "lat": loc.get("lat"),
                "lon": loc.get("lon"),
                "tz_id": loc.get("tz_id"),
                "time_local": h["time"],
                "time_utc": datetime.utcfromtimestamp(h["time_epoch"]).isoformat(),
                "temp_c": h["temp_c"],
                "feelslike_c": h.get("feelslike_c"),
                "dewpoint_c": h.get("dewpoint_c"),
                "heatindex_c": h.get("heatindex_c"),
                "humidity": h.get("humidity"),
                "pressure_mb": h.get("pressure_mb"),
                "wind_kph": h.get("wind_kph"),
                "wind_mps": (h.get("wind_kph") or 0)/3.6,
                "wind_degree": h.get("wind_degree"),
                "wind_dir": h.get("wind_dir"),
                "cloud": h.get("cloud"),
                "precip_mm": h.get("precip_mm"),
                "uv": h.get("uv"),
                "vis_km": h.get("vis_km"),
                "gust_kph": h.get("gust_kph"),
                "will_it_rain": h.get("will_it_rain"),
                "chance_of_rain": h.get("chance_of_rain"),
                "will_it_snow": h.get("will_it_snow"),
                "chance_of_snow": h.get("chance_of_snow"),
                "condition": (h.get("condition") or {}).get("text"),
                "is_day": h.get("is_day"),
            })
    df = pd.DataFrame(rows)
    df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
    df = df.sort_values(["city", "time_utc"]).reset_index(drop=True)
    return df

def main():
    frames = []
    for city in CITIES:
        try:
            data = fetch_forecast(city, DAYS)
            df = to_dataframe(data)
            frames.append(df)
            print(f"[OK] {city}: {len(df)} строк")
            time.sleep(1.0)
        except Exception as e:
            print(f"[WARN] {city}: {e}")
    if not frames:
        raise SystemExit("Нет данных.")
    full = pd.concat(frames, ignore_index=True)
    full.to_csv(OUTPUT, index=False)
    print(f"[DONE] Сохранено {len(full)} строк → {OUTPUT}")

if __name__ == "__main__":
    main()
