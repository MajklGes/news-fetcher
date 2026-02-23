import os
import feedparser
import hashlib
from supabase import create_client

print("🚀 Spouštím stahování zpráv...")

SUPABASE_URL = os.getenv("https://ncxcpeeocknrotbzmfde.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_L1AIP3X0SS5_-S5SbX0M7Q_KMWjfCLj")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS_SOURCES = {
    "ct24": "https://ct24.ceskatelevize.cz/rss/hlavni-zpravy",
    "irozhlas": "https://www.irozhlas.cz/rss/irozhlas",
    "novinky": "https://www.novinky.cz/rss"
}

# Zakázaná slova
BANNED_WORDS = ["vražda", "vraždy", "vraždou", "vraždami", "vraždě", "vražd", "Ukrajina", "Ukrajině", "Ukrajinou", "Ukrajiny", "ukrajinci"]

for source_name, rss_url in RSS_SOURCES.items():
    print(f"\n🔎 Stahuji ze zdroje: {source_name}")

    feed = feedparser.parse(rss_url)

    print("Nalezeno článků:", len(feed.entries))

    for entry in feed.entries:
        title = entry.title
        url = entry.link
        content = entry.summary if "summary" in entry else ""

        text_to_check = (title + " " + content).lower()

        # ❌ blacklist
        if any(banned in text_to_check for banned in BANNED_WORDS):
            print("🚫 Zakázané slovo:", title)
            continue

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
            "source": source_name,
            "hash": hash_value
        }

        supabase.table("articles").insert(data).execute()
        print("✅ Uloženo:", title)

print("🎯 Hotovo")