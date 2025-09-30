

import requests, pandas as pd, json, time
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse

API_KEY     = "b8ad4f27fb94467690e30513da8058ab"
QUERY       = "экономика OR финансы"
LANGUAGE    = "ru"
DAYS_BACK   = 7
PAGE_SIZE   = 100
MAX_PAGES   = 5

OUT_FULL_CSV   = "news_full.csv"
OUT_FULL_JSON  = "news_full.json"
OUT_SERIES_CSV = "news_text_series.csv"
OUT_META_JSON  = "news_metadata.json"

ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_news(query, language, from_iso, to_iso, page_size=100, max_pages=5):
    headers = {"X-Api-Key": API_KEY}
    all_articles = []
    for page in range(1, max_pages + 1):
        params = {
            "q": query, "language": language,
            "from": from_iso, "to": to_iso,
            "sortBy": "publishedAt", "pageSize": page_size, "page": page
        }
        r = requests.get(ENDPOINT, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "ok":
            raise SystemExit(f"NewsAPI error: {data.get('message')}")
        arts = data.get("articles", [])
        if not arts: break
        all_articles.extend(arts)
        total = data.get("totalResults", 0)
        if page * page_size >= total: break
        time.sleep(0.7)
    return all_articles

def normalize_articles(articles):
    rows = []
    for a in articles:
        src = a.get("source") or {}
        try:
            dt = isoparse(a.get("publishedAt")).astimezone(timezone.utc)
        except Exception:
            dt = None
        rows.append({
            "published_at_utc": dt, 
            "source_id": src.get("id"),
            "source_name": src.get("name"),
            "author": a.get("author"),
            "title": a.get("title"),
            "description": a.get("description"),
            "content": a.get("content"),
            "url": a.get("url"),
            "urlToImage": a.get("urlToImage"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["published_at_utc"] = pd.to_datetime(df["published_at_utc"], errors="coerce", utc=True)
        df = df.sort_values("published_at_utc").reset_index(drop=True)
    return df

def build_text_series(df):
    if df.empty:
        return pd.DataFrame(columns=["date","text"])
    def mk(row):
        title = (row.get("title") or "").strip()
        desc  = (row.get("description") or "").strip()
        return f"{title} — {desc}" if title and desc else (title or desc)
    return pd.DataFrame({
        "date": df["published_at_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "text": df.apply(mk, axis=1)
    })

def main():
    to_dt   = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=DAYS_BACK)
    from_iso, to_iso = from_dt.isoformat(), to_dt.isoformat()

    arts = fetch_news(QUERY, LANGUAGE, from_iso, to_iso, PAGE_SIZE, MAX_PAGES)
    if not arts:
        raise SystemExit("Статей не найдено — поменяй запрос/интервал.")

    # Полный датасет
    df_full = normalize_articles(arts)
    df_full.to_csv(OUT_FULL_CSV, index=False)

    df_json = df_full.copy()
    if not df_json.empty:
        df_json["published_at_utc"] = df_json["published_at_utc"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUT_FULL_JSON, "w", encoding="utf-8") as f:
        json.dump(df_json.to_dict(orient="records"), f, ensure_ascii=False, indent=2)

    # «date,text»
    df_series = build_text_series(df_full)
    df_series.to_csv(OUT_SERIES_CSV, index=False)

    # Метаданные выгрузки
    meta = {
        "endpoint": ENDPOINT,
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "query": QUERY,
        "language": LANGUAGE,
        "from": from_iso,
        "to": to_iso,
        "page_size": PAGE_SIZE,
        "max_pages": MAX_PAGES,
        "total_saved": int(len(df_full)),
        "fields": list(df_full.columns),
        "note": "Полные ссылки на источники в поле 'url' файлов news_full.csv/json."
    }
    with open(OUT_META_JSON, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, default=str)

    print(f"[OK] {len(df_full)} статей сохранено")
    print(f" - {OUT_FULL_CSV} (полный CSV)")
    print(f" - {OUT_FULL_JSON} (полный JSON)")
    print(f" - {OUT_SERIES_CSV} (date,text)")
    print(f" - {OUT_META_JSON} (метаданные)")

if __name__ == "__main__":
    main()
