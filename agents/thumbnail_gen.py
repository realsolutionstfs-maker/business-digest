"""Generate thumbnail images for YouTube and Instagram."""
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from .config import logger, BASE_DIR


def generate_thumbnail(title: str, output_path: str = None) -> str:
    """Create a simple dark-themed thumbnail with title text."""
    w, h = 1280, 720
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = (15, 15, 26)  # Dark navy

    # Red accent line
    img[60:64, :] = (233, 69, 96)
    img[h-64:h-60, :] = (233, 69, 96)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "BUSINESS DIGEST", (60, 160), font, 0.5, (233, 69, 96), 1)

    # Wrap title text
    words = title.split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        if len(test) > 30:
            lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)

    y = 280
    for line in lines[:5]:
        cv2.putText(img, line.upper(), (60, y), font, 1.2, (255, 255, 255), 2)
        y += 70

    if not output_path:
        output_path = str(BASE_DIR / "output" / "thumbnails" / f"thumb_{datetime.now().strftime('%Y%m%d')}.jpg")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(output_path, img)
    logger.info(f"  Thumbnail saved to {output_path}")
    return output_path


def generate_ig_story(title: str) -> str:
    """Generate Instagram story-sized image (1080x1920)."""
    w, h = 1080, 1920
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = (15, 15, 26)

    cv2.putText(img, "BUSINESS DIGEST", (60, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (233, 69, 96), 1)

    words = title.split()
    lines = []
    current = ""
    for w in words:
        test = current + " " + w if current else w
        if len(test) > 25:
            lines.append(current)
            current = w
        else:
            current = test
    if current:
        lines.append(current)

    y = 500
    for line in lines[:8]:
        cv2.putText(img, line.upper(), (80, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        y += 120

    out = str(BASE_DIR / "output" / "thumbnails" / f"ig_{datetime.now().strftime('%Y%m%d')}.jpg")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(out, img)
    logger.info(f"  IG story saved to {out}")
    return out
