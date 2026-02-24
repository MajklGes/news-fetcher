import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🧹 Resetuji články...")

supabase.table("articles").update({
    "is_deleted": True,
    "is_saved": False,
    "custom_title": None
}).neq("id", "00000000-0000-0000-0000-000000000000").execute()

response = supabase.table("articles").update({
    "is_deleted": True,
    "is_saved": False,
    "custom_title": None
}).neq("id", "00000000-0000-0000-0000-000000000000").execute()

print(response)

print("✅ Reset hotov")