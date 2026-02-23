import feedparser
import hashlib
from supabase import create_client

print("🚀 Spouštím stahování zpráv...")

SUPABASE_URL = "https://ncxcpeeocknrotbzmfde.supabase.co"
SUPABASE_KEY = "sb_publishable_L1AIP3X0SS5_-S5SbX0M7Q_KMWjfCLj"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS_URL = "https://ct24.ceskatelevize.cz/rss/hlavni-zpravy"

feed = feedparser.parse(RSS_URL)

print("Nalezeno článků:", len(feed.entries))

for entry in feed.entries:
    title = entry.title
    url = entry.link
    content = entry.summary if "summary" in entry else ""

    # vytvoření hash pro kontrolu duplicity
    hash_value = hashlib.sha256((title + content).encode("utf-8")).hexdigest()

    # kontrola, zda už existuje
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

    try:
        supabase.table("articles").insert(data).execute()
        print("✅ Uloženo:", title)
    except Exception as e:
        print("❌ Chyba při ukládání:", e)

print("🎯 Hotovo")