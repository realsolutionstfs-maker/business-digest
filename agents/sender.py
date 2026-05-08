import re
import json
import requests
from datetime import datetime
from .config import logger, BASE_DIR, BRAND, HAS_BUTTONDOWN

BUTTONDOWN_API = "https://api.buttondown.email/v1/emails"


def _headers():
    from .config import API_KEYS
    key = API_KEYS.get("buttondown", "")
    if not key:
        return {}
    return {"Authorization": f"Token {key}", "Content-Type": "application/json"}


def _is_duplicate(resp):
    try:
        body = resp.json()
        return body.get("code") == "email_duplicate"
    except Exception:
        return "email_duplicate" in resp.text


def _mark_safe(headers):
    return {**headers, "X-Buttondown-Live-Dangerously": "1", "X-Buttondown-Confirm-Duplicate": "1"}


def send(newsletter_html: str, subject: str = "") -> bool:
    if not HAS_BUTTONDOWN:
        logger.warning("No Buttondown API key — newsletter not sent")
        return False

    if not subject:
        subject = f"{BRAND['name']} — {datetime.now().strftime('%d %B %Y')}"

    headers = _headers()
    if not headers:
        logger.warning("Buttondown API key not configured")
        return False

    payload = {"subject": subject, "body": newsletter_html, "status": "draft"}

    def _post_and_send(hdrs, pld):
        resp = requests.post(BUTTONDOWN_API, headers=hdrs, json=pld, timeout=30)
        if resp.status_code not in (200, 201):
            return None, resp
        eid = resp.json().get("id", "")
        eurl = resp.json().get("absolute_url", "")
        sresp = requests.patch(
            f"{BUTTONDOWN_API}/{eid}",
            headers=_mark_safe(hdrs),
            json={"status": "about_to_send"},
            timeout=60,
        )
        return (eid, eurl, sresp), resp

    for attempt in range(3):
        try:
            created, raw = _post_and_send(headers, payload)

            if created and created[2].status_code == 200:
                logger.info(f"Buttondown: sent! — {created[1]}")
                return True

            dup = False
            if created:
                dup = _is_duplicate(created[2])
            if not dup and raw.status_code not in (200, 201):
                dup = _is_duplicate(raw)
            if not dup:
                err = created[2] if created else raw
                logger.error(f"Buttondown error: {err.status_code} — {err.text[:200]}")
                return False

            logger.info(f"Buttondown: duplicate, retrying with unique content marker")
            marker = f"<!--{datetime.now().strftime('%Y%m%d%H%M%S%f')}-->"
            pld2 = {**payload, "body": newsletter_html + marker, "subject": f"{subject} ({datetime.now().strftime('%H%M%S')})"}
            c2, _ = _post_and_send(headers, pld2)
            if c2 and c2[2].status_code == 200:
                logger.info(f"Buttondown: sent! (unique marker) — {c2[1]}")
                return True
            logger.error(f"Buttondown: all strategies failed")
            return False

        except requests.exceptions.Timeout:
            logger.error(f"Buttondown timeout (attempt {attempt + 1}/3)")
            continue
        except Exception as e:
            logger.error(f"Buttondown request failed: {e}")
            return False

    logger.error("Buttondown: all 3 attempts failed")
    return False


def _wrap_template(body: str) -> str:
    tmpl_path = BASE_DIR / "templates" / "newsletter.html"
    if not tmpl_path.exists():
        return body
    tmpl = tmpl_path.read_text(encoding="utf-8")
    body_html = body.replace("\n", "<br>\n")
    for section in ["THE SYSTEM", "THE TOOL", "THE MOVE"]:
        body_html = body_html.replace(f"## {section}", f'<h2>{section}</h2>')
    body_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", body_html)
    body_html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", body_html, flags=re.MULTILINE)
    body_html = re.sub(r"^(\d+)\. ", r"<br>\1. ", body_html, flags=re.MULTILINE)
    return tmpl.replace("{{content}}", body_html).replace("{{unsubscribe_url}}", "{{ unsubscribe_url }}").replace("{{archive_url}}", "{{ archive_url }}")


def send_latest() -> bool:
    newsletters_dir = BASE_DIR / "output" / "newsletters"
    if not newsletters_dir.exists():
        logger.error("No newsletters directory")
        return False

    files = sorted(newsletters_dir.glob("*.html"))
    if not files:
        logger.error("No newsletter files found")
        return False

    latest = files[-1]
    raw = latest.read_text(encoding="utf-8")
    html = _wrap_template(raw)
    date_str = latest.stem.replace("weekly_", "")
    try:
        parsed = datetime.strptime(date_str, "%Y%m%d")
        subject = f"{BRAND['name']} — {parsed.strftime('%d %B %Y')}"
    except ValueError:
        subject = f"{BRAND['name']} — Weekly Brief"

    logger.info(f"Sending: {latest.name}")
    return send(html, subject)
