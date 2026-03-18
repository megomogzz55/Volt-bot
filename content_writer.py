import requests
from config import GROQ_API_KEY

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def write_arabic(prompt, max_tokens=300):
    """اكتب محتوى عربي مصري بـ Groq"""
    if not GROQ_API_KEY:
        # لو مفيش Groq key — اكتب template بسيط
        return None

    try:
        r = requests.post(GROQ_URL, headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }, json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": """أنت مسؤول محتوى صفحة فانتازي كرة قدم عربية.
اكتب بالعربي المصري الطبيعي — مش فصحى.
الأسلوب: ودود، ذكي، أحياناً ساخر.
مختصر ومباشر. استخدم emoji بذكاء."""
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.8
        }, timeout=15)

        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
        return None


# ══════════════════════════════════════════
# Templates جاهزة لو مفيش AI
# ══════════════════════════════════════════

def price_rise_text(player_name, old_price, new_price):
    ai = write_arabic(
        f"لاعب الفانتازي {player_name} ارتفع سعره من {old_price}m لـ {new_price}m. "
        f"اكتب بوست قصير وجذاب عن ده مع نصيحة هل يستاهل الاشتراء."
    )
    if ai:
        return ai
    change = new_price - old_price
    return f"""💰 سعر جديد!

{player_name}
{old_price}m ← {new_price}m
▲ +{change:.1f}m

اشتريته؟ قولنا في الكومنتس 👇

#فانتازي #FPL"""


def price_fall_text(player_name, old_price, new_price):
    ai = write_arabic(
        f"لاعب الفانتازي {player_name} انخفض سعره من {old_price}m لـ {new_price}m. "
        f"اكتب بوست قصير تحذيري."
    )
    if ai:
        return ai
    change = old_price - new_price
    return f"""📉 انتبه!

{player_name} بيرخص
{old_price}m ← {new_price}m
▼ -{change:.1f}m

لو معاك فكّر تبيعه دلوقتي 🤔

#فانتازي #FPL"""


def captain_text(players):
    names = ", ".join([p["name"] for p in players[:3]])
    ai = write_arabic(
        f"أفضل خيارات الكابتن للجولة الجاية في FPL: {names}. "
        f"اكتب توصية كابتن بأسلوب مصري ومسلي."
    )
    if ai:
        return ai
    top = players[0]
    return f"""👑 كابتنك الجولة دي؟

⭐ {top['name']}
💰 {top['price']}m
📈 فورم: {top['form']}
👥 ملكية: {top['ownership']}%

إيه رأيك؟ 👇

#فانتازي #FPL #كابتن"""


def top_transfers_text(bought, sold):
    ai = write_arabic(
        f"أكتر لاعبين اتشتروا في FPL النهارده: {', '.join([p['name'] for p in bought[:3]])}. "
        f"وأكتر اتبيعوا: {', '.join([p['name'] for p in sold[:3]])}. "
        f"اكتب ملخص بأسلوب مصري."
    )
    if ai:
        return ai

    bought_text = "\n".join([
        f"  +{p['transfers_in']:,} | {p['name']} £{p['price']}m"
        for p in bought[:3]
    ])
    sold_text = "\n".join([
        f"  -{p['transfers_out']:,} | {p['name']} £{p['price']}m"
        for p in sold[:3]
    ])
    return f"""🔄 حركة التحويلات النهارده

📈 أكتر اتشتروا:
{bought_text}

📉 أكتر اتبيعوا:
{sold_text}

إيه رأيك في الحركة دي؟ 👇

#فانتازي #FPL #تحويلات"""


def injury_text(player):
    chance = player['chance']
    status_emoji = "🔴" if chance == 0 else "🟡" if chance < 75 else "🟠"
    ai = write_arabic(
        f"لاعب FPL {player['name']} نسبة لعبه {chance}%. الخبر: {player['news']}. "
        f"اكتب تحذير قصير بالعربي المصري."
    )
    if ai:
        return ai
    return f"""{status_emoji} تحذير إصابة!

👤 {player['name']}
⚽ نسبة اللعب: {chance}%
📋 {player['news']}

لو معاك فكّر في بديل 🤔

#فانتازي #FPL #إصابة"""


def fixtures_text(fixtures):
    if not fixtures:
        return None
    lines = "\n".join([
        f"  ⚽ {f['home']} vs {f['away']}"
        for f in fixtures[:5]
    ])
    ai = write_arabic(
        f"مباريات الجولة القادمة في البريميرليج: {lines}. "
        f"اكتب بوست جذاب عن الجولة."
    )
    if ai:
        return ai
    return f"""📅 مباريات الجولة الجاية

{lines}

مين هتكبّل كابتنك؟ 👇

#فانتازي #FPL #بريميرليج"""
