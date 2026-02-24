import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🧹 Mažu všechny články ze Supabase...")

response = supabase.table("articles") \
    .delete() \
    .gt("created_at", "2000-01-01") \
    .execute()

print("Smazáno řádků:", len(response.data) if response.data else 0)
print("✅ Reset hotov")