#!/usr/bin/env python3
"""Instagram setup — usa le tue Facebook Developer credenziali."""
import sys, json
from pathlib import Path

TOKEN_PATH = Path(__file__).parent.parent / "data" / "instagram_token.json"
CLIENT_ID = "863hwbrm55axm1"  # Reuse LinkedIn App or create Facebook App

print("=" * 60)
print("INSTAGRAM SETUP")
print("=" * 60)
print()
print("PREREQUISITI:")
print("1. Account Facebook (già ce l'hai)")
print("2. Pagina Facebook")
print("3. Account Instagram Business o Creator collegato alla Pagina")
print()
print("PROCEDURA:")
print()
print("1. Vai su https://developers.facebook.com/")
print("2. Crea app → Business → nome: 'Business Digest Publisher'")
print("3. Aggiungi prodotto: 'Instagram Graph API'")
print("4. Vai su 'Instagram Graph API' → 'Generate Token'")
print("5. Seleziona Pagina Facebook + Account Instagram")
print("6. Copia l'ACCESS TOKEN")
print()
token = input("INCOLLA ACCESS TOKEN QUI: ").strip()
if not token:
    print("Nessun token")
    sys.exit(1)

# Get Instagram Business Account ID
import requests

resp = requests.get(
    "https://graph.facebook.com/v21.0/me/accounts",
    params={"access_token": token},
    timeout=10,
)
pages = resp.json().get("data", [])
if not pages:
    print("Nessuna Pagina Facebook trovata")
    sys.exit(1)

page_id = pages[0]["id"]
page_token = pages[0]["access_token"]

resp2 = requests.get(
    f"https://graph.facebook.com/v21.0/{page_id}",
    params={"fields": "instagram_business_account", "access_token": page_token},
    timeout=10,
)
ig_data = resp2.json().get("instagram_business_account", {})
if not ig_data:
    print("Nessun Instagram Business collegato alla Pagina")
    sys.exit(1)

ig_user_id = ig_data["id"]

# Exchange short token for long token
long_resp = requests.get(
    "https://graph.facebook.com/v21.0/oauth/access_token",
    params={
        "grant_type": "fb_exchange_token",
        "client_id": CLIENT_ID,
        "client_secret": "YOUR_APP_SECRET",
        "fb_exchange_token": token,
    },
    timeout=10,
)

data = {"access_token": token, "user_id": ig_user_id, "page_id": page_id}
TOKEN_PATH.write_text(json.dumps(data, indent=2))
print()
print(f"Instagram Business ID: {ig_user_id}")
print(f"Token salvato in {TOKEN_PATH}")
print("Instagram publishing pronto!")
