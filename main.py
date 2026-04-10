import os
import json
import datetime
import time
import random
from fpl_data import get_bootstrap, get_price_changes, get_injured_players, get_fixtures
from content_writer import price_text, injury_text, quiz_text, news_text
from publisher import post_fantasy, upload_to_r2
from image_generator import ImageGenerator

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try: return json.load(open(STATE_FILE))
        except: pass
    return {"posted_prices": [], "posted_injuries": [], "last_quiz": None, "last_news": None}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), ensure_ascii=False, indent=2)

def main():
    print(f"🤖 Volt-bot Active — {datetime.datetime.utcnow()}")
    state = load_state()
    data = get_bootstrap() # FPL API
    gen = ImageGenerator()
    
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=2) # توقيت مصر
    hour, minute = now.hour, now.minute

    # --- 1. الأخبار العاجلة (ESPN API) ---
    if hour % 3 == 0 and minute < 10: # كل 3 ساعات
        news = news_text() # بيجيب من ESPN Hidden API
        if news != state["last_news"]:
            if post_fantasy(news):
                state["last_news"] = news
                print("✅ تم نشر خبر عاجل")

    # --- 2. تغييرات الأسعار (8 صباحاً) ---
    if hour == 8 and minute < 10:
        changes = get_price_changes(data)
        for p in changes[:3]:
            if p['id'] not in state["posted_prices"]:
                path = gen.generate_ai_image(p['photo'], p['name'])
                cdn_url = upload_to_r2(path, p['name']) # الرفع لـ Cloudflare R2
                if post_fantasy(price_text(p), cdn_url):
                    state["posted_prices"].append(p['id'])
                    time.sleep(15)

    # --- 3. التحديات والاختبارات (12 ظهراً) ---
    if hour == 12 and minute < 10:
        if state["last_quiz"] != str(datetime.date.today()):
            if post_fantasy(quiz_text()):
                state["last_quiz"] = str(datetime.date.today())
                print("✅ تم نشر التحدي اليومي")

    # --- 4. الجداول والترتيب (أيام الجولة) ---
    if hour == 22 and minute < 10:
        fixtures = get_fixtures(data) # من football-data.org
        post_fantasy(f"📊 جدول ترتيب الدوري بعد ماتشات النهاردة:\n{fixtures}")

    # --- 5. مراقبة الإصابات (مستمر) ---
    injured = get_injured_players(data)
    for p in injured:
        if float(p['ownership']) > 15 and p['id'] not in state["posted_injuries"]:
            path = gen.generate_ai_image(p['photo'], p['name'])
            cdn_url = upload_to_r2(path, p['name'])
            if post_fantasy(injury_text(p), cdn_url):
                state["posted_injuries"].append(p['id'])
                break

    save_state(state)
    print("✅ تم إنهاء كل المهام المجدولة")

if __name__ == "__main__":
    main()
