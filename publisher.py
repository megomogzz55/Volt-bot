import requests
import json
from config import (
    FB_FANTASY_PAGE_ID, FB_FANTASY_ACCESS_TOKEN,
    FB_NEWS_PAGE_ID, FB_NEWS_ACCESS_TOKEN
)

FB_API = "https://graph.facebook.com/v19.0"

def post_to_facebook(page_id, token, message, image_path=None):
    """نشر بوست على فيسبوك — نص أو نص + صورة"""
    try:
        if image_path:
            # بوست بصورة
            url = f"{FB_API}/{page_id}/photos"
            with open(image_path, "rb") as img:
                r = requests.post(url, data={
                    "caption": message,
                    "access_token": token
                }, files={"source": img}, timeout=30)
        else:
            # بوست نص فقط
            url = f"{FB_API}/{page_id}/feed"
            r = requests.post(url, data={
                "message": message,
                "access_token": token
            }, timeout=30)

        result = r.json()
        if "id" in result:
            print(f"✅ نُشر على فيسبوك: {result['id']}")
            return result["id"]
        else:
            print(f"❌ فشل النشر: {result}")
            return None
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None

def post_fantasy(message, image_path=None):
    """نشر على صفحة الفانتازي"""
    return post_to_facebook(
        FB_FANTASY_PAGE_ID,
        FB_FANTASY_ACCESS_TOKEN,
        message,
        image_path
    )

def post_news(message, image_path=None):
    """نشر على صفحة الأخبار"""
    return post_to_facebook(
        FB_NEWS_PAGE_ID,
        FB_NEWS_ACCESS_TOKEN,
        message,
        image_path
    )
