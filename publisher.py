import requests
import boto3
import time
from config import Config

class Publisher:
    def __init__(self):
        # إعداد مخزن R2 لضمان روابط صور لا تموت
        self.s3 = boto3.client('s3',
            endpoint_url=Config.R2_ENDPOINT,
            aws_access_key_id=Config.R2_ACCESS_KEY,
            aws_secret_access_key=Config.R2_SECRET_KEY
        )

    def upload_to_r2(self, file_path, player_name):
        """رفع الصورة وتوليد رابط CDN دائم للفيسبوك"""
        file_key = f"volt/{player_name}_{int(time.time())}.png"
        self.s3.upload_file(file_path, Config.R2_BUCKET, file_key)
        return f"{Config.CDN_URL}/{file_key}"

    def send_to_fb(self, text, img_url, target="fantasy"):
        """نشر على فيسبوك (فانتازي أو أخبار)"""
        page_id = Config.FB_FANTASY_PAGE_ID if target == "fantasy" else Config.FB_NEWS_PAGE_ID
        token = Config.FB_FANTASY_ACCESS_TOKEN if target == "fantasy" else Config.FB_NEWS_ACCESS_TOKEN
        
        url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
        payload = {'url': img_url, 'caption': text, 'access_token': token}
        return requests.post(url, data=payload).json()

    def send_to_tg(self, text, img_url, target="fantasy"):
        """نشر على قنوات تليجرام"""
        channel = Config.TG_FANTASY_CHANNEL if target == "fantasy" else Config.TG_NEWS_CHANNEL
        url = f"https://api.telegram.org/bot{Config.TG_BOT_TOKEN}/sendPhoto"
        payload = {'chat_id': channel, 'photo': img_url, 'caption': text, 'parse_mode': 'HTML'}
        return requests.post(url, data=payload).json()
