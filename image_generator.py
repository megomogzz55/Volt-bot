"""
image_generator.py — توليد كروت FPL بستايل Fantasy Volt
الألوان: أزرق #00AFCC (فوق) + كورالي #E85555 (تحت)
"""

import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai

# ══════════════════════════════════════════
# إعداد Gemini
# ══════════════════════════════════════════
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ══════════════════════════════════════════
# الألوان والإعدادات
# ══════════════════════════════════════════
TEAL   = (0, 175, 204)       # #00AFCC
CORAL  = (232, 85, 85)        # #E85555
YELLOW = (245, 197, 24)       # #F5C518
WHITE  = (255, 255, 255)
DARK   = (13, 13, 13)
CARD_W, CARD_H = 1080, 1080

# ══════════════════════════════════════════
# مساعد: تحميل فونت
# ══════════════════════════════════════════
def get_font(size, bold=False):
    """حمّل فونت — لو مش موجود استخدم الـ default"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()

# ══════════════════════════════════════════
# مساعد: كتابة نص في المنتصف
# ══════════════════════════════════════════
def draw_centered(draw, text, y, font, color=WHITE, width=CARD_W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (width - tw) // 2
    draw.text((x, y), text, font=font, fill=color)

# ══════════════════════════════════════════
# مساعد: خلفية Fantasy Volt
# ══════════════════════════════════════════
def make_base_card():
    """اعمل كارت بخلفية Fantasy Volt"""
    img = Image.new("RGB", (CARD_W, CARD_H), DARK)
    draw = ImageDraw.Draw(img)

    # الجزء العلوي — أزرق
    draw.rectangle([0, 0, CARD_W, CARD_H // 2], fill=TEAL)

    # الجزء السفلي — كورالي
    draw.rectangle([0, CARD_H // 2, CARD_W, CARD_H], fill=CORAL)

    # خطوط diagonal خفية
    for i in range(0, CARD_W + CARD_H, 40):
        draw.line([(i, 0), (0, i)], fill=(255, 255, 255, 15), width=1)

    # شريط أبيض في المنتصف
    draw.rectangle([0, CARD_H//2 - 6, CARD_W, CARD_H//2 + 6], fill=WHITE)

    return img, draw

# ══════════════════════════════════════════
# كارت تغيير السعر
# ══════════════════════════════════════════
def price_card(player_name, old_price, new_price, player_img_url=None):
    """كارت ارتفاع أو انخفاض السعر"""
    img, draw = make_base_card()

    rising = new_price > old_price
    arrow  = "▲" if rising else "▼"
    diff   = abs(new_price - old_price)
    label  = "ارتفع السعر! 💰" if rising else "انخفض السعر! 📉"

    f_big   = get_font(90, bold=True)
    f_med   = get_font(60, bold=True)
    f_small = get_font(45)
    f_label = get_font(50, bold=True)

    # الجزء العلوي
    draw_centered(draw, label,        80,  f_label)
    draw_centered(draw, player_name, 200,  f_big)
    draw_centered(draw, f"£{old_price}m  →  £{new_price}m", 340, f_med, YELLOW)

    # السهم في المنتصف
    arrow_color = (0, 230, 100) if rising else (255, 80, 80)
    draw_centered(draw, f"{arrow} {diff:.1f}m", CARD_H//2 - 50, f_big, arrow_color)

    # الجزء السفلي
    draw_centered(draw, "اشتريته؟ 🤔" if rising else "بعته؟ 🤔", 620, f_med)
    draw_centered(draw, "قولنا في الكومنتس 👇", 710, f_small)
    draw_centered(draw, "#فانتازي  #FPL", 850, f_small, YELLOW)

    # لوجو صغير
    draw_centered(draw, "⚽ VOLT FPL", 960, get_font(35), WHITE)

    path = f"/tmp/price_{player_name.replace(' ', '_')}.jpg"
    img.save(path, "JPEG", quality=95)
    print(f"✅ تم إنشاء كارت السعر: {path}")
    return path

# ══════════════════════════════════════════
# كارت الكابتن
# ══════════════════════════════════════════
def captain_card(player_name, price, form, ownership, fixture):
    """كارت توصية الكابتن"""
    img, draw = make_base_card()

    f_big   = get_font(85, bold=True)
    f_med   = get_font(55, bold=True)
    f_small = get_font(42)

    draw_centered(draw, "👑 CAPTAIN",      70,  get_font(70, bold=True), YELLOW)
    draw_centered(draw, "توصية الكابتن",  160,  f_med)
    draw_centered(draw, player_name,       290,  f_big)
    draw_centered(draw, f"£{price}m",      420,  f_med, YELLOW)

    draw_centered(draw, f"📈 فورم: {form}",     580, f_small)
    draw_centered(draw, f"👥 ملكية: {ownership}%", 660, f_small)
    draw_centered(draw, f"⚽ {fixture}",          740, f_small)

    draw_centered(draw, "موافق؟ 👇",       870,  f_med)
    draw_centered(draw, "#كابتن  #FPL",   970,  f_small, YELLOW)

    path = f"/tmp/captain_{player_name.replace(' ', '_')}.jpg"
    img.save(path, "JPEG", quality=95)
    print(f"✅ تم إنشاء كارت الكابتن: {path}")
    return path

# ══════════════════════════════════════════
# كارت الإصابة
# ══════════════════════════════════════════
def injury_card(player_name, chance, news):
    """كارت تحذير إصابة"""
    img, draw = make_base_card()

    # غيّر ألوان الكارت لأحمر داكن
    draw.rectangle([0, 0, CARD_W, CARD_H//2], fill=(180, 30, 30))

    f_big   = get_font(85, bold=True)
    f_med   = get_font(55, bold=True)
    f_small = get_font(42)

    status = "🔴 غايب" if chance == 0 else f"🟡 {chance}% يلعب"

    draw_centered(draw, "🚑 تحذير إصابة",  70,  get_font(65, bold=True), YELLOW)
    draw_centered(draw, player_name,        220, f_big)
    draw_centered(draw, status,             360, f_med, YELLOW)

    # الخبر — قسّمه لو طويل
    words = news.split()
    lines, line = [], []
    for w in words:
        line.append(w)
        if len(" ".join(line)) > 30:
            lines.append(" ".join(line))
            line = []
    if line:
        lines.append(" ".join(line))

    y = 560
    for l in lines[:3]:
        draw_centered(draw, l, y, f_small)
        y += 60

    draw_centered(draw, "لو معاك فكّر في بديل 🤔", 800, f_med)
    draw_centered(draw, "#إصابة  #FPL",             930, f_small, YELLOW)

    path = f"/tmp/injury_{player_name.replace(' ', '_')}.jpg"
    img.save(path, "JPEG", quality=95)
    print(f"✅ تم إنشاء كارت الإصابة: {path}")
    return path

# ══════════════════════════════════════════
# كارت التحويلات
# ══════════════════════════════════════════
def transfers_card(bought_list, sold_list):
    """كارت حركة التحويلات"""
    img, draw = make_base_card()

    f_big   = get_font(65, bold=True)
    f_med   = get_font(48, bold=True)
    f_small = get_font(38)

    draw_centered(draw, "🔄 حركة التحويلات", 60, f_big, YELLOW)

    # أكتر اتشتروا
    draw_centered(draw, "📈 أكتر اتشتروا", 170, f_med)
    y = 240
    for p in bought_list[:3]:
        draw_centered(draw, f"↑ {p['name']}  £{p['price']}m", y, f_small, (150, 255, 150))
        y += 65

    # أكتر اتبيعوا
    draw_centered(draw, "📉 أكتر اتبيعوا", CARD_H//2 + 30, f_med)
    y = CARD_H//2 + 110
    for p in sold_list[:3]:
        draw_centered(draw, f"↓ {p['name']}  £{p['price']}m", y, f_small, (255, 150, 150))
        y += 65

    draw_centered(draw, "إيه رأيك؟ 👇", 890, f_med)
    draw_centered(draw, "#تحويلات  #FPL", 970, f_small, YELLOW)

    path = "/tmp/transfers_card.jpg"
    img.save(path, "JPEG", quality=95)
    print(f"✅ تم إنشاء كارت التحويلات: {path}")
    return path

# ══════════════════════════════════════════
# كارت كارتون اللاعب بـ Gemini (Muse Style)
# ══════════════════════════════════════════
def player_cartoon(image_url_or_path):
    """حوّل صورة لاعب لكارتون Muse Style بـ Gemini"""
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY مش موجود")
        return None

    try:
        # تحميل الصورة
        if image_url_or_path.startswith("http"):
            r = requests.get(image_url_or_path, timeout=10)
            img_data = r.content
        else:
            with open(image_url_or_path, "rb") as f:
                img_data = f.read()

        img = Image.open(io.BytesIO(img_data))

        model = genai.GenerativeModel("gemini-2.0-flash-exp")

        prompt = """Convert this football player photo into a Muse State flat cartoon illustration.
Flat vector art, bold black outlines (4px), solid flat colors only,
zero gradients, zero shading.
Clean minimal cartoon face — recognizable but simplified.
White background. Upper body portrait centered.
Same jersey colors as in the photo. High quality sharp edges."""

        response = model.generate_content([prompt, img])

        # استخرج الصورة من الرد
        for part in response.parts:
            if hasattr(part, "inline_data"):
                cartoon_data = part.inline_data.data
                path = "/tmp/player_cartoon.jpg"
                with open(path, "wb") as f:
                    f.write(cartoon_data)
                print(f"✅ تم إنشاء الكارتون: {path}")
                return path

    except Exception as e:
        print(f"❌ خطأ في Gemini: {e}")
        return None


# ══════════════════════════════════════════
# تجربة
# ══════════════════════════════════════════
if __name__ == "__main__":
    # اختبار كارت السعر
    path = price_card("محمد صلاح", 13.0, 13.2)
    print(f"الكارت محفوظ في: {path}")

    # اختبار كارت الكابتن
    path = captain_card("إيرلينج هالاند", 15.0, "8.5", 65.3, "مان سيتي vs ويست هام")
    print(f"الكارت محفوظ في: {path}")
