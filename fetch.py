import os
import feedparser
import hashlib
from supabase import create_client

print("🚀 Spouštím stahování zpráv...")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

RSS_SOURCES = {
    "idnesBrno": "https://servis.idnes.cz/rss.aspx?c=brnoh",
    "idnes": "https://servis.idnes.cz/rss.aspx?c=zpravodaj",
    "idnesSport": "https://servis.idnes.cz/rss.aspx?c=sport",
    "refresher": "https://refresher.cz/rss",
    "koktejl": "https://api-web.novinky.cz/v1/timelines/section_5ad5a5fcc25e64000bd6e7aa?xml=rss",
    "zahranicni": "https://api-web.novinky.cz/v1/timelines/section_5ad5a5fcc25e64000bd6e7a5?xml=rss",
    "domaci": "https://api-web.novinky.cz/v1/timelines/section_5ad5a5fcc25e64000bd6e7ab?xml=rss",
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
            "hash": hash_value,
            "is_deleted": False,
            "is_saved": False
        }

        supabase.table("articles").insert(data).execute()
        print("✅ Uloženo:", title)

print("🎯 Hotovo")