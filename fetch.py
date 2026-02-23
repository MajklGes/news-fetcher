import os
import feedparser
import hashlib
from supabase import create_client

print("🚀 Spouštím stahování zpráv...")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS_URL = "https://ct24.ceskatelevize.cz/rss/hlavni-zpravy"

feed = feedparser.parse(RSS_URL)

print("Nalezeno článků:", len(feed.entries))

for entry in feed.entries:
    title = entry.title
    url = entry.link
    content = entry.summary if "summary" in entry else ""

    hash_value = hashlib.sha256((title + content).encode("utf-8")).hexdigest()

    existing = supabase.table("articles") \
        .select("id") \
        .or_(f"url.eq.{url},hash.eq.{hash_value}") \
        .execute()

    if existing.data:
        print("⛔ Už existuje:", title)
        continue

    data = {
        "title": title,
        "url": url,
        "content": content,
        "source": "ct24",
        "hash": hash_value
    }

    supabase.table("articles").insert(data).execute()
    print("✅ Uloženo:", title)

print("🎯 Hotovo")