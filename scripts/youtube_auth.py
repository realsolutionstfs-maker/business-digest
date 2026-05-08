#!/usr/bin/env python3
"""YouTube OAuth setup — genera link, tu autorizzi, io salvo token."""
import sys, json, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

CLIENT_SECRET_PATH = Path(__file__).parent.parent / "data" / "youtube_client_secret.json"
TOKEN_PATH = Path(__file__).parent.parent / "data" / "youtube_token.json"

print("=" * 60)
print("YOUTUBE SETUP")
print("=" * 60)
print()
print("SERVE UN PROGETTO GOOGLE CLOUD CON YOUTUBE DATA API V3 ATTIVO.")
print()
print("1. Vai su https://console.cloud.google.com/")
print("2. Crea progetto (o usane uno esistente)")
print("3. API & Services → Library → cerca 'YouTube Data API v3' → ATTIVA")
print("4. API & Services → Credentials → Create Credentials → OAuth 2.0 Client ID")
print("5. Application Type: Desktop app")
print("6. Scarica il JSON e SALVALO come:")
print()
print(f"   {CLIENT_SECRET_PATH}")
print()
print("7. Poi esegui QUESTO COMANDO:")
print()
print("   python3 scripts/youtube_auth.py --exchange")
print()

# Check if client secret exists and do OAuth flow
if len(sys.argv) > 1 and sys.argv[1] == "--exchange":
    if not CLIENT_SECRET_PATH.exists():
        print("ERRORE: youtube_client_secret.json non trovato")
        print(f"       Salvalo in {CLIENT_SECRET_PATH}")
        sys.exit(1)

    from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_PATH), SCOPES)
    creds = flow.run_local_server(port=0)

    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    TOKEN_PATH.write_text(json.dumps(token_data, indent=2))
    print()
    print(f"Token salvato in {TOKEN_PATH}")
    print("YouTube publishing pronto!")
else:
    print()
    print("DOPO aver salvato il JSON, esegui:")
    print("   python3 scripts/youtube_auth.py --exchange")
