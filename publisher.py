import requests
from .config import Config

class Publisher:
    def __init__(self):
        self.page_id = Config.FB_PAGE_ID
        self.access_token = Config.FB_ACCESS_TOKEN

    def post_to_facebook(self, image_url, player_name):
        """نشر الصورة على فيسبوك باستخدام رابط الـ CDN"""
        url = f"https://graph.facebook.com/v19.0/{self.page_id}/photos"
        
        caption = f"كارتون النجم {player_name} بستايل جديد! ⚽🔥\n#Zamalek #Fantasy #VoltBot"
        
        payload = {
            'url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            result = response.json()
            if "id" in result:
                print(f"✅ تم النشر بنجاح! رابط البوست: https://fb.com/{result['id']}")
                return True
            else:
                print(f"❌ خطأ من فيسبوك: {result}")
                return False
        except Exception as e:
            print(f"❌ فشل الاتصال بفيسبوك: {e}")
            return False
