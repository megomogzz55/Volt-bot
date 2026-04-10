import random
import time
from gradio_client import Client
from config import Config

class ImageGenerator:
    def __init__(self):
        self.tokens = Config.HF_TOKENS
        self.current_token_idx = 0

    def get_client(self):
        token = self.tokens[self.current_token_idx]
        return Client("PrithivMLmods/FireRed-Image-Edit-1.0-Fast", hf_token=token)

    def generate_ai_image(self, original_url, player_name):
        """توليد الكارتون مع تبديل التوكنز آلياً عند انتهاء الكوتا"""
        for _ in range(len(self.tokens)):
            try:
                client = self.get_client()
                random_seed = random.randint(0, 2**32 - 1) # لضمان نتيجة مختلفة كل مرة
                
                print(f"🎨 رسم {player_name} بتوكن رقم {self.current_token_idx + 1}...")
                result = client.predict(
                    image=original_url,
                    prompt=Config.MUSE_PROMPT,
                    seed=random_seed,
                    api_name="/infer"
                )
                return result[0]['path'] if isinstance(result[0], dict) else result[0]
            except Exception as e:
                print(f"⚠️ التوكن {self.current_token_idx + 1} مجهد، بنبدل...")
                self.current_token_idx = (self.current_token_idx + 1) % len(self.tokens)
                time.sleep(2)
        return None
