import boto3
from .config import Config
import time

def upload_to_r2(file_path, player_name):
    """رفع الصورة لـ Cloudflare R2 والحصول على رابط CDN"""
    s3 = boto3.client(
        's3',
        endpoint_url=Config.R2_ENDPOINT,
        aws_access_key_id=Config.R2_ACCESS_KEY,
        aws_secret_access_key=Config.R2_SECRET_KEY
    )
    
    # اسم فريد لكل نسخة عشان "التنوع"
    file_key = f"players/{player_name}_{int(time.time())}.png"
    
    try:
        s3.upload_file(file_path, Config.R2_BUCKET, file_key)
        return f"{Config.CDN_URL}/{file_key}"
    except Exception as e:
        print(f"❌ خطأ في الرفع لـ R2: {e}")
        return None
      
