import requests
import json
from datetime import datetime
from .config import logger, BASE_DIR

import os
from .config import API_KEYS, BASE_DIR, logger

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_REDIRECT = "https://realsolutionstfs-maker.github.io/business-digest/"

TOKEN_PATH = BASE_DIR / "data" / "linkedin_token.json"


def get_auth_url():
    return (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={LINKEDIN_REDIRECT}"
        "&scope=w_member_social"
    )


def exchange_code(auth_code):
    resp = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data={
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "redirect_uri": LINKEDIN_REDIRECT,
    })
    if resp.status_code != 200:
        logger.error(f"LinkedIn token exchange failed: {resp.text[:200]}")
        return None
    data = resp.json()
    TOKEN_PATH.write_text(json.dumps(data, indent=2))
    logger.info("LinkedIn token saved")
    return data.get("access_token")


def get_user_id(token):
    # Try OpenID userinfo endpoint (works with w_member_social)
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code == 200:
        sub = resp.json().get("sub", "")
        if sub:
            return sub
    logger.warning(f"LinkedIn userinfo failed: {resp.text[:100]}")
    return None


def post_linkedin(token, content):
    user_id = get_user_id(token)
    if not user_id:
        logger.error("Cannot get LinkedIn user ID")
        return False

    payload = {
        "author": f"urn:li:person:{user_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content[:1300]},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        json=payload,
    )

    if resp.status_code == 201:
        logger.info(f"LinkedIn: posted! — {resp.json().get('id', '')}")
        return True
    logger.error(f"LinkedIn post failed: {resp.status_code} — {resp.text[:200]}")
    return False


def publish_daily():
    if not TOKEN_PATH.exists():
        logger.info("No LinkedIn token found at data/linkedin_token.json")
        return False

    data = json.loads(TOKEN_PATH.read_text())
    token = data.get("access_token")
    if not token:
        logger.info("No access_token in linkedin_token.json")
        return False

    social_dir = BASE_DIR / "output" / "social"
    today = datetime.now().strftime("%Y%m%d")
    linkedin_files = sorted(social_dir.glob(f"linkedin_{today}*"))
    if not linkedin_files:
        logger.info(f"No LinkedIn content for {today}")
        return False

    content = linkedin_files[-1].read_text()
    return post_linkedin(token, content)
