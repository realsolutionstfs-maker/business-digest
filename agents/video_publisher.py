import os
import json
from datetime import datetime
from pathlib import Path
from .config import logger, BASE_DIR

# YouTube
YT_CRED_PATH = BASE_DIR / "data" / "youtube_token.json"
YT_CLIENT_SECRET_PATH = BASE_DIR / "data" / "youtube_client_secret.json"

# Instagram
IG_TOKEN_PATH = BASE_DIR / "data" / "instagram_token.json"


def generate_video(script_path: str, output_path: str = None) -> bool:
    """Generate video from voiceover script using gTTS + opencv."""
    try:
        from gtts import gTTS
        import cv2
        import numpy as np
    except ImportError:
        logger.error("gTTS or opencv not installed")
        return False

    script = Path(script_path).read_text()

    # Generate audio
    audio_path = str(Path(output_path).with_suffix(".mp3")) if output_path else "/tmp/voice.mp3"
    tts = gTTS(text=script[:500], lang="en", slow=False)
    tts.save(audio_path)
    logger.info(f"  Audio saved to {audio_path}")

    # Create simple video with text overlay
    if output_path and str(output_path).endswith(".mp4"):
        video_path = output_path
    else:
        video_path = str(Path(audio_path).with_suffix(".mp4"))

    img = np.zeros((720, 1280, 3), dtype=np.uint8)
    img[:] = (15, 15, 26)  # Dark navy background

    font = cv2.FONT_HERSHEY_SIMPLEX
    lines = script.split("\n")[:5]
    y = 200
    for line in lines:
        if line.strip() and not line.startswith("["):
            cv2.putText(img, line[:60], (100, y), font, 0.7, (233, 69, 96), 1)
            y += 60

    fps = 1
    duration = max(10, min(60, len(script) // 10))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, fps, (1280, 720))

    for _ in range(fps * duration):
        out.write(img)
    out.release()

    logger.info(f"  Video saved to {video_path}")

    # Try to mux audio + video with ffmpeg (if available)
    import subprocess, shutil
    ffmpeg = shutil.which("ffmpeg") or shutil.which("ffmpeg.exe")
    if ffmpeg:
        final_path = video_path.replace(".mp4", "_final.mp4")
        cmd = [ffmpeg, "-i", video_path, "-i", audio_path,
               "-c:v", "copy", "-c:a", "aac", "-shortest", final_path, "-y"]
        subprocess.run(cmd, capture_output=True)
        if Path(final_path).exists():
            os.replace(final_path, video_path)
            logger.info(f"  Audio muxed into video")
    else:
        logger.info("  ffmpeg not found — video without audio")

    return True


def upload_youtube(video_path: str, title: str = "", description: str = "") -> bool:
    """Upload video to YouTube via Data API v3."""
    if not YT_CRED_PATH.exists():
        logger.error("YouTube not authorized — run setup_youtube() first")
        return False

    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        logger.error("google-api-python-client not installed")
        return False

    creds = Credentials.from_authorized_user_file(str(YT_CRED_PATH))
    youtube = build("youtube", "v3", credentials=creds)

    if not title:
        title = f"Business Digest — {datetime.now().strftime('%d %B %Y')}"
    if not description:
        description = "Weekly business narrative analysis. One story, one framework, one move."

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": ["business", "startup", "strategy", "entrepreneurship"],
            "categoryId": "22",
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    logger.info(f"YouTube uploaded: https://youtu.be/{response['id']}")
    return True


def post_instagram(image_path: str, caption: str = "") -> bool:
    """Post to Instagram via Graph API (Business/Creator account required)."""
    if not IG_TOKEN_PATH.exists():
        logger.error("Instagram not authorized")
        return False

    try:
        import requests
    except ImportError:
        return False

    token = json.loads(IG_TOKEN_PATH.read_text()).get("access_token")
    ig_user_id = json.loads(IG_TOKEN_PATH.read_text()).get("user_id")

    if not token or not ig_user_id:
        logger.error("Instagram token or user_id missing")
        return False

    # Step 1: Create media container
    url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
    params = {
        "image_url": image_path,
        "caption": caption[:2200],
        "access_token": token,
    }
    resp = requests.post(url, params=params, timeout=15)
    if resp.status_code != 200:
        logger.error(f"Instagram container failed: {resp.text[:200]}")
        return False

    container_id = resp.json().get("id")

    # Step 2: Publish
    pub_url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media_publish"
    pub_params = {"creation_id": container_id, "access_token": token}
    pub_resp = requests.post(pub_url, params=pub_params, timeout=15)
    if pub_resp.status_code == 200:
        logger.info(f"Instagram posted: {pub_resp.json().get('id', '')}")
        return True

    logger.error(f"Instagram publish failed: {pub_resp.text[:200]}")
    return False


def publish_video_to_youtube():
    """Find latest voiceover and publish to YouTube."""
    voices = sorted((BASE_DIR / "output" / "voiceovers").glob("voice_*.txt"))
    if not voices:
        logger.info("No voiceover files found")
        return False

    latest = voices[-1]
    video_path = str(latest).replace("voiceovers", "videos").replace(".txt", ".mp4")
    Path(video_path).parent.mkdir(parents=True, exist_ok=True)

    if not generate_video(str(latest), video_path):
        return False

    return upload_youtube(video_path)
