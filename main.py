from config import Config
from publisher import Publisher
from image_generator import ImageGenerator
import requests

def get_ai_caption(event_data):
    """استخدام Groq (Llama 3.3) لكتابة كابشن مصري طبيعي"""
    headers = {"Authorization": f"Bearer {Config.GROQ_API_KEY}"}
    prompt = f"اكتب كابشن فيسبوك قصير ومرح بلهجة مصرية عن: {event_data}. استخدم إيموجيز."
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
    return res.json()['choices'][0]['message']['content']

def check_espn_news():
    """مراقبة الأهداف والأخبار في كل الدوريات"""
    pub = Publisher()
    gen = ImageGenerator()
    
    for league_id, league_name in Config.ESPN_LEAGUES.items():
        # سحب البيانات من ESPN Hidden API
        url = f"{Config.ESPN_BASE}/{league_id}/scoreboard"
        events = requests.get(url).json().get('events', [])
        
        for event in events:
            # منطق اكتشاف الأهداف أو الأخبار العاجلة هنا
            # ... 
            # لو فيه هدف:
            caption = get_ai_caption(f"هدف في دوري {league_name}")
            # توليد صورة كارتون بستايل Muse
            img_path = gen.generate_cartoon(original_url, "player_name")
            cdn_link = pub.upload_to_r2(img_path, "player")
            
            # النشر المزدوج (فيس + تليجرام)
            pub.send_to_fb(caption, cdn_link, target="news")
            pub.send_to_tg(caption, cdn_link, target="news")

if __name__ == "__main__":
    check_espn_news()
