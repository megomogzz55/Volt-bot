"""
Telegram Notifier & Remote Control — Free Hybrid Notification & Control Layer
Sends instant photo & text alerts to your Telegram when posts are published,
and alerts on any system errors.
"""

import json
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


def _get_config():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
    return cfg


from typing import Optional

def send_telegram_alert(message: str, image_path: Optional[str] = None) -> bool:
    """
    Sends an alert message and optional photo to the owner's Telegram.
    Gracefully skips if Telegram credentials are not yet configured.
    """
    cfg = _get_config()
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or cfg.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        return False
        
    try:
        if image_path and os.path.exists(image_path):
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(image_path, "rb") as photo_file:
                payload = {"chat_id": chat_id, "caption": message[:1024]}
                files = {"photo": photo_file}
                r = requests.post(url, data=payload, files=files, timeout=20)
                return r.status_code == 200
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            r = requests.post(url, json=payload, timeout=15)
            return r.status_code == 200
    except Exception as e:
        print(f"Telegram alert skipped ({e})")
        return False
