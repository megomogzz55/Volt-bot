import requests
import boto3
import time
from config import Config

class Publisher:
    def __init__(self):
        self.s3 = boto3.client('s3',
            endpoint_url=Config.R2_ENDPOINT,
            aws_access_key_id=Config.R2_ACCESS_KEY,
            aws_secret_access_key=Config.R2_SECRET_KEY
        )

    def upload_to_r2(self, local_path, player_name):
        """رفع الصورة وتوليد رابط CDN دائم"""
        file_key = f"volt/{player_name.replace(' ', '_')}_{int(time.time())}.png"
        try:
            self.s3.upload_file(local_path, Config.R2_BUCKET, file_key)
            return f"{Config.CDN_URL}/{file_key}"
        except: return None

    def post_fantasy(self, text, image_url=None):
        """النشر على صفحة الفانتازي"""
        url = f"https://graph.facebook.com/v19.0/{Config.FB_PAGE_ID}/photos" if image_url else f"https://graph.facebook.com/v19.0/{Config.FB_PAGE_ID}/feed"
        payload = {'access_token': Config.FB_ACCESS_TOKEN, 'message' if not image_url else 'caption': text}
        if image_url: payload['url'] = image_url
        
        r = requests.post(url, data=payload)
        return "id" in r.json()
        
