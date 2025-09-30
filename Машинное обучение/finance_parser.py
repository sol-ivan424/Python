import io
import requests
import pandas as pd

API_KEY = "UILINXK5WN59E5Y4" 
SYMBOL  = "IBM"          
OUTPUT  = f"{SYMBOL.lower()}_series.csv"

url = "https://www.alphavantage.co/query"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": SYMBOL,
    "apikey": API_KEY,
    "datatype": "csv",         
    "outputsize": "compact"    
}

r = requests.get(url, params=params, timeout=30)
text = r.text

if text.startswith("timestamp,open,high,low,close,volume"):
    df = pd.read_csv(io.StringIO(text), parse_dates=["timestamp"])
    df = df[["timestamp", "close"]].rename(columns={"timestamp": "date", "close": "value"})
    df = df.sort_values("date") 
    df.to_csv(OUTPUT, index=False)
    print(f"OK: сохранён временной ряд {SYMBOL} → {OUTPUT} (колонки: date,value). Строк: {len(df)}")
else:
   
    print("API вернул сообщение. Первые 500 символов ответа ниже:\n")
    print(text[:500])
