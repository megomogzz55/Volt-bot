"""
image_generator.py — Fantasy Volt Image Generator
بيستخدم Pillow فقط — بدون Playwright، بدون timeout
"""

import os
import base64
import requests
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ══════════════════════════════════════════
# 1. تحميل اللوجو
# ══════════════════════════════════════════
def load_logo(logo_path: str = "logo.png", size: int = 60) -> Image.Image | None:
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((size, size), Image.LANCZOS)
        return logo
    except Exception as e:
        print(f"⚠️ logo.png مش موجود: {e}")
        return None


def load_logo_base64(logo_path: str = "logo.png") -> str:
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return ""


# ══════════════════════════════════════════
# 2. Muse Style — Gemini
# ══════════════════════════════════════════
MUSE_PROMPT = (
    "Convert this football player photo into a Muse State flat cartoon illustration. "
    "Flat vector art, bold black outlines (4px), solid flat colors only, "
    "zero gradients, zero shading. Clean minimal cartoon face. "
    "White background. Upper body portrait centered. "
    "Same jersey colors as in the photo. High quality sharp edges."
)

GEMINI_MODEL = "gemini-2.0-flash-preview-image-generation"


def muse_style_gemini(image_url: str, gemini_key: str) -> bytes | None:
    try:
        print("📥 تحميل صورة اللاعب...")
        resp = requests.get(image_url, timeout=15)
        if resp.status_code != 200:
            return None
        img_b64 = base64.b64encode(resp.content).decode("utf-8")
        print(f"✅ الصورة اتحملت ({len(resp.content)} bytes)")

        print(f"🤖 Gemini {GEMINI_MODEL}...")
        api_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent?key={gemini_key}"
        )
        payload = {
            "contents": [{"parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
                {"text": MUSE_PROMPT}
            ]}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "temperature": 1}
        }
        r = requests.post(api_url, json=payload, timeout=60)
        if r.status_code == 429:
            print("⚠️ Gemini 429 — quota")
            return None
        if r.status_code != 200:
            print(f"❌ Gemini {r.status_code}: {r.text[:200]}")
            return None

        data = r.json()
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
                print("✅ Gemini رجّع كارتون!")
                return base64.b64decode(part["inlineData"]["data"])
        return None
    except Exception as e:
        print(f"❌ Gemini: {e}")
        return None


def muse_style_pollinations(player_name: str) -> bytes | None:
    try:
        print("🎨 Pollinations flux...")
        prompt = (
            f"flat cartoon football player {player_name}, "
            "Muse State style, flat vector, bold outlines, solid colors, white background"
        )
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=512&height=600&nologo=true"
        r = requests.get(url, timeout=45)
        if r.status_code == 200 and len(r.content) > 5000:
            print(f"✅ Pollinations نجح ({len(r.content)} bytes)")
            return r.content
        print(f"⚠️ Pollinations {r.status_code} ({len(r.content)} bytes)")
        return None
    except Exception as e:
        print(f"❌ Pollinations: {e}")
        return None


def fetch_player_image(url: str) -> Image.Image | None:
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return Image.open(BytesIO(r.content)).convert("RGBA")
    except Exception as e:
        print(f"❌ فشل تحميل صورة: {e}")
    return None


def upload_to_catbox(img_bytes: bytes) -> str | None:
    try:
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": ("card.png", img_bytes, "image/png")},
            timeout=30
        )
        if r.status_code == 200 and r.text.startswith("https://"):
            return r.text.strip()
    except:
        pass
    return None


# ══════════════════════════════════════════
# 3. رسم الكارت بـ Pillow
# ══════════════════════════════════════════

def hex_to_rgb(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)


def get_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """يجرب يحمّل فونت عربي، لو ما لقاش يستخدم default"""
    fonts_to_try = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    ]
    for f in fonts_to_try:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass
    return ImageFont.load_default()


def create_goal_card_pillow(
    player_name: str,
    assist: str,
    minute: int,
    score: str,
    player_img: Image.Image,
    logo: Image.Image | None,
    output_path: str
) -> bool:
    W, H = 500, 600
    BLUE = hex_to_rgb("#00AFCC")
    DARK = hex_to_rgb("#0d1f3c")
    DARKER = hex_to_rgb("#0a0e1a")
    RED = hex_to_rgb("#E85555")
    WHITE = (255, 255, 255)

    card = Image.new("RGB", (W, H), DARKER)
    draw = ImageDraw.Draw(card)

    # خلفية تدرج يدوي
    for y in range(H):
        ratio = y / H
        r = int(DARK[0] * (1 - ratio) + DARKER[0] * ratio)
        g = int(DARK[1] * (1 - ratio) + DARKER[1] * ratio)
        b = int(DARK[2] * (1 - ratio) + DARKER[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Header أزرق
    for y in range(65):
        ratio = y / 65
        r = int(BLUE[0] * (1 - ratio * 0.3))
        g = int(BLUE[1] * (1 - ratio * 0.3))
        b = int(BLUE[2] * (1 - ratio * 0.3))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # نص GOAL!
    f_goal = get_font(32, bold=True)
    draw.text((W//2, 32), "⚽  GOAL!", font=f_goal, fill=WHITE, anchor="mm")

    # badge الدقيقة
    draw_rounded_rect(draw, (12, 75, 90, 100), 12, (0, 0, 0, 180))
    draw.rectangle([12, 75, 90, 100], fill=(20, 20, 40))
    draw.rounded_rectangle([12, 75, 90, 100], radius=12, outline=BLUE, width=1)
    f_min = get_font(14, bold=True)
    draw.text((51, 87), f"⏱ {minute}'", font=f_min, fill=BLUE, anchor="mm")

    # صورة اللاعب
    try:
        img_h = 310
        img_w = int(player_img.width * img_h / player_img.height)
        player_resized = player_img.resize((img_w, img_h), Image.LANCZOS)
        x_offset = (W - img_w) // 2
        if player_img.mode == "RGBA":
            card.paste(player_resized, (x_offset, 55), player_resized.split()[3])
        else:
            card.paste(player_resized, (x_offset, 55))
    except Exception as e:
        print(f"⚠️ مشكلة في صورة اللاعب: {e}")

    # خط فاصل
    draw.line([(30, 358), (W - 30, 358)], fill=BLUE, width=2)

    # اسم اللاعب
    f_name = get_font(30, bold=True)
    draw.text((W//2, 378), player_name, font=f_name, fill=WHITE, anchor="mm")

    # القسم الكورالي (تحت)
    for y in range(415, H):
        ratio = (y - 415) / (H - 415)
        r = int(RED[0] * (1 - ratio * 0.3))
        g = int(RED[1] * (1 - ratio * 0.3))
        b = int(RED[2] * (1 - ratio * 0.3))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # ركنين مستديرين للقسم الأحمر
    draw.rounded_rectangle([0, 415, W, H], radius=20, fill=RED)
    draw.rectangle([0, 435, W, H], fill=RED)

    f_info = get_font(16, bold=True)
    f_val = get_font(17, bold=True)

    # أسيست
    y_pos = 430
    if assist and assist.lower() not in ["none", "-", ""]:
        draw_rounded_rect(draw, (20, y_pos, W - 20, y_pos + 36), 8, (255, 255, 255, 30))
        draw.rounded_rectangle([20, y_pos, W - 20, y_pos + 36], radius=8,
                                 fill=(255, 255, 255, 40))
        draw.text((35, y_pos + 18), "🅰️", font=f_info, fill=WHITE, anchor="lm")
        draw.text((65, y_pos + 18), "أسيست", font=f_info, fill=(255, 255, 255, 180), anchor="lm")
        draw.text((W - 30, y_pos + 18), assist, font=f_val, fill=WHITE, anchor="rm")
        y_pos += 46

    # النتيجة
    draw.rounded_rectangle([20, y_pos, W - 20, y_pos + 36], radius=8,
                             fill=(255, 255, 255, 40))
    draw.text((35, y_pos + 18), "🏆", font=f_info, fill=WHITE, anchor="lm")
    draw.text((65, y_pos + 18), "النتيجة", font=f_info, fill=(255, 255, 255, 180), anchor="lm")
    draw.text((W - 30, y_pos + 18), score, font=f_val, fill=(255, 230, 50), anchor="rm")

    # اللوجو
    if logo:
        # تحويل اللوجو لأبيض
        logo_white = logo.copy()
        r2, g2, b2, a2 = logo_white.split()
        logo_white = Image.merge("RGBA", (
            Image.new("L", logo_white.size, 255),
            Image.new("L", logo_white.size, 255),
            Image.new("L", logo_white.size, 255),
            a2
        ))
        card.paste(logo_white, (14, H - 60), logo_white.split()[3])

    card.save(output_path, "PNG", quality=95)
    print(f"✅ الكارت اتحفظ: {output_path}")
    return True


# ══════════════════════════════════════════
# 4. الدالة الرئيسية
# ══════════════════════════════════════════
def generate_goal_card(player_name: str, assist: str, minute: int,
                        score: str, player_img_url: str,
                        output_path: str = "/tmp/goal_card.png") -> str | None:
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    logo = load_logo("logo.png", size=55)

    # محاولة Muse Style
    cartoon_bytes = None
    if gemini_key:
        cartoon_bytes = muse_style_gemini(player_img_url, gemini_key)
        if not cartoon_bytes:
            time.sleep(2)
            cartoon_bytes = muse_style_pollinations(player_name)
    else:
        cartoon_bytes = muse_style_pollinations(player_name)

    # تحميل الصورة
    if cartoon_bytes:
        player_img = Image.open(BytesIO(cartoon_bytes)).convert("RGBA")
        print("🎨 استخدام كارتون Muse Style")
    else:
        print("📸 استخدام صورة حقيقية")
        player_img = fetch_player_image(player_img_url)
        if not player_img:
            print("❌ فشل تحميل صورة اللاعب")
            return None

    # رسم الكارت
    success = create_goal_card_pillow(
        player_name=player_name,
        assist=assist,
        minute=minute,
        score=score,
        player_img=player_img,
        logo=logo,
        output_path=output_path
    )
    return output_path if success else None


# ══════════════════════════════════════════
# 5. كروت FPL الأخرى
# ══════════════════════════════════════════
def price_card(player_name: str, old_price: float, new_price: float,
               output_path: str = "/tmp/price_card.png") -> str | None:
    try:
        W, H = 500, 350
        is_up = new_price > old_price
        COLOR = hex_to_rgb("#00a86b") if is_up else hex_to_rgb("#E85555")
        DARK = hex_to_rgb("#0d1f3c")
        DARKER = hex_to_rgb("#0a0e1a")
        WHITE = (255, 255, 255)

        card = Image.new("RGB", (W, H), DARKER)
        draw = ImageDraw.Draw(card)

        for y in range(H):
            ratio = y / H
            r = int(DARK[0] * (1-ratio) + DARKER[0] * ratio)
            g = int(DARK[1] * (1-ratio) + DARKER[1] * ratio)
            b = int(DARK[2] * (1-ratio) + DARKER[2] * ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        # Header
        for y in range(60):
            draw.line([(0, y), (W, y)], fill=COLOR)

        f_h = get_font(24, bold=True)
        draw.text((W//2, 30), "💰  تغيير سعر", font=f_h, fill=WHITE, anchor="mm")

        f_name = get_font(28, bold=True)
        draw.text((W//2, 110), player_name, font=f_name, fill=WHITE, anchor="mm")

        arrow = "📈" if is_up else "📉"
        f_price = get_font(32, bold=True)
        f_old = get_font(22)
        draw.text((120, 190), f"{old_price:.1f}م", font=f_old, fill=(150, 150, 150), anchor="mm")
        draw.text((250, 190), arrow, font=f_price, fill=WHITE, anchor="mm")
        draw.text((380, 190), f"{new_price:.1f}م", font=f_price, fill=COLOR, anchor="mm")

        # لوجو
        logo = load_logo("logo.png", 45)
        if logo:
            r2, g2, b2, a2 = logo.split()
            logo_w = Image.merge("RGBA", (Image.new("L", logo.size, 255),
                                           Image.new("L", logo.size, 255),
                                           Image.new("L", logo.size, 255), a2))
            card.paste(logo_w, (14, H - 55), logo_w.split()[3])

        card.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"❌ price_card: {e}")
        return None


def captain_card(player_name: str, price: float, form: float,
                  ownership: float, fixture: str,
                  output_path: str = "/tmp/captain_card.png") -> str | None:
    try:
        W, H = 500, 400
        BLUE = hex_to_rgb("#00AFCC")
        DARK = hex_to_rgb("#0d1f3c")
        DARKER = hex_to_rgb("#0a0e1a")
        WHITE = (255, 255, 255)

        card = Image.new("RGB", (W, H), DARKER)
        draw = ImageDraw.Draw(card)

        for y in range(H):
            ratio = y / H
            r = int(DARK[0]*(1-ratio)+DARKER[0]*ratio)
            g = int(DARK[1]*(1-ratio)+DARKER[1]*ratio)
            b = int(DARK[2]*(1-ratio)+DARKER[2]*ratio)
            draw.line([(0, y), (W, y)], fill=(r, g, b))

        for y in range(60):
            draw.line([(0, y), (W, y)], fill=BLUE)

        f_h = get_font(22, bold=True)
        draw.text((W//2, 30), "©  توصية الكابتن", font=f_h, fill=WHITE, anchor="mm")

        f_name = get_font(30, bold=True)
        draw.text((W//2, 105), player_name, font=f_name, fill=WHITE, anchor="mm")

        # Stats boxes
        stats = [(f"{price:.1f}م", "السعر"), (str(form), "الفورم"), (f"{ownership:.1f}%", "الملكية")]
        for i, (val, lbl) in enumerate(stats):
            x = 80 + i * 140
            draw.rounded_rectangle([x-55, 140, x+55, 210], radius=12,
                                     fill=(255,255,255,25))
            draw.rectangle([x-55, 155, x+55, 210], fill=(30, 50, 80))
            draw.rounded_rectangle([x-55, 140, x+55, 210], radius=12,
                                     outline=(255,255,255,30), width=1)
            f_val = get_font(20, bold=True)
            f_lbl = get_font(12)
            draw.text((x, 168), val, font=f_val, fill=BLUE, anchor="mm")
            draw.text((x, 198), lbl, font=f_lbl, fill=(150,150,150), anchor="mm")

        f_fix = get_font(16, bold=True)
        draw.text((W//2, 260), f"⚽  {fixture}", font=f_fix, fill=(255, 230, 50), anchor="mm")

        logo = load_logo("logo.png", 45)
        if logo:
            r2,g2,b2,a2 = logo.split()
            lw = Image.merge("RGBA",(Image.new("L",logo.size,255),Image.new("L",logo.size,255),
                                      Image.new("L",logo.size,255),a2))
            card.paste(lw,(14,H-55),lw.split()[3])

        card.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"❌ captain_card: {e}")
        return None


def injury_card(player_name: str, chance: int, news: str,
                 output_path: str = "/tmp/injury_card.png") -> str | None:
    try:
        W, H = 500, 330
        RED = hex_to_rgb("#E85555")
        DARK = hex_to_rgb("#1a0a0a")
        DARKER = hex_to_rgb("#0a0e1a")
        WHITE = (255, 255, 255)

        card = Image.new("RGB", (W, H), DARKER)
        draw = ImageDraw.Draw(card)

        for y in range(H):
            ratio = y/H
            r=int(DARK[0]*(1-ratio)+DARKER[0]*ratio)
            g=int(DARK[1]*(1-ratio)+DARKER[1]*ratio)
            b=int(DARK[2]*(1-ratio)+DARKER[2]*ratio)
            draw.line([(0,y),(W,y)],fill=(r,g,b))

        for y in range(60):
            draw.line([(0,y),(W,y)],fill=RED)

        f_h = get_font(22, bold=True)
        draw.text((W//2, 30), "🚑  تحديث إصابة", font=f_h, fill=WHITE, anchor="mm")

        f_name = get_font(28, bold=True)
        draw.text((W//2, 95), player_name, font=f_name, fill=WHITE, anchor="mm")

        f_chance = get_font(38, bold=True)
        draw.text((W//2, 160), f"{chance}% للمشاركة", font=f_chance, fill=RED, anchor="mm")

        f_news = get_font(14)
        # تقسيم النص لو طويل
        words = news.split()
        lines, line = [], []
        for w in words:
            line.append(w)
            if len(" ".join(line)) > 45:
                lines.append(" ".join(line[:-1]))
                line = [w]
        if line:
            lines.append(" ".join(line))
        for i, l in enumerate(lines[:3]):
            draw.text((W//2, 210 + i*22), l, font=f_news, fill=(180,180,180), anchor="mm")

        logo = load_logo("logo.png", 45)
        if logo:
            r2,g2,b2,a2=logo.split()
            lw=Image.merge("RGBA",(Image.new("L",logo.size,255),Image.new("L",logo.size,255),
                                    Image.new("L",logo.size,255),a2))
            card.paste(lw,(14,H-55),lw.split()[3])

        card.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"❌ injury_card: {e}")
        return None


def transfers_card(bought: list, sold: list,
                    output_path: str = "/tmp/transfers_card.png") -> str | None:
    try:
        W, H = 500, 480
        BLUE = hex_to_rgb("#00AFCC")
        GREEN = hex_to_rgb("#00a86b")
        RED = hex_to_rgb("#E85555")
        DARK = hex_to_rgb("#0d1f3c")
        DARKER = hex_to_rgb("#0a0e1a")
        WHITE = (255, 255, 255)

        card = Image.new("RGB", (W, H), DARKER)
        draw = ImageDraw.Draw(card)

        for y in range(H):
            ratio = y/H
            r=int(DARK[0]*(1-ratio)+DARKER[0]*ratio)
            g=int(DARK[1]*(1-ratio)+DARKER[1]*ratio)
            b=int(DARK[2]*(1-ratio)+DARKER[2]*ratio)
            draw.line([(0,y),(W,y)],fill=(r,g,b))

        for y in range(60):
            draw.line([(0,y),(W,y)],fill=BLUE)

        f_h = get_font(22, bold=True)
        draw.text((W//2, 30), "🔄  أكتر التحويلات", font=f_h, fill=WHITE, anchor="mm")

        f_sec = get_font(14, bold=True)
        f_row = get_font(14)
        f_num = get_font(13)

        # الأكتر دخولاً
        draw.text((W-30, 75), "الأكتر دخولاً", font=f_sec, fill=GREEN, anchor="rm")
        for i, p in enumerate(bought[:4]):
            y = 98 + i * 42
            draw.rounded_rectangle([15, y, W-15, y+34], radius=8, fill=(255,255,255,15))
            draw.rectangle([15, y+8, W-15, y+34], fill=(20,40,30,150))
            draw.rounded_rectangle([15, y, W-15, y+34], radius=8, fill=(20,40,30))
            draw.text((30, y+17), "▲", font=f_row, fill=GREEN, anchor="lm")
            draw.text((50, y+17), p.get("name",""), font=f_row, fill=WHITE, anchor="lm")
            draw.text((W-25, y+17), f'+{p.get("transfers_in",0):,}', font=f_num,
                      fill=(150,150,150), anchor="rm")

        # الأكتر خروجاً
        y_sec = 270
        draw.text((W-30, y_sec), "الأكتر خروجاً", font=f_sec, fill=RED, anchor="rm")
        for i, p in enumerate(sold[:4]):
            y = y_sec + 23 + i * 42
            draw.rounded_rectangle([15, y, W-15, y+34], radius=8, fill=(40,15,15))
            draw.text((30, y+17), "▼", font=f_row, fill=RED, anchor="lm")
            draw.text((50, y+17), p.get("name",""), font=f_row, fill=WHITE, anchor="lm")
            draw.text((W-25, y+17), f'-{p.get("transfers_out",0):,}', font=f_num,
                      fill=(150,150,150), anchor="rm")

        logo = load_logo("logo.png", 45)
        if logo:
            r2,g2,b2,a2=logo.split()
            lw=Image.merge("RGBA",(Image.new("L",logo.size,255),Image.new("L",logo.size,255),
                                    Image.new("L",logo.size,255),a2))
            card.paste(lw,(14,H-55),lw.split()[3])

        card.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"❌ transfers_card: {e}")
        return None


# ══════════════════════════════════════════
# اختبار محلي
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("🧪 اختبار...")
    r = generate_goal_card(
        player_name="محمد صلاح",
        assist="ترينت",
        minute=67,
        score="ليفربول 2 - 0 بورنموث",
        player_img_url="https://r2.thesportsdb.com/images/media/player/cutout/3blc581757088735.png",
        output_path="/tmp/test_goal_card.png"
    )
    print(f"{'✅' if r else '❌'}: {r}")
