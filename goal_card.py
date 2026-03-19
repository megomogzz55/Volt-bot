"""
goal_card.py - كارت الهدف
1. صورة اللاعب من FPL API
2. Gemini يحوّلها لكارتون Muse Style
3. إضافة لوجو Fantasy Volt
4. caption بالعربي المصري
"""

import os
import io
import requests
from PIL import Image, ImageDraw
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BASE_DIR  = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"

# ══════════════════════════════════════════
# 1. جيب صورة اللاعب
# ══════════════════════════════════════════
def get_player_image(player_code):
    url = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{player_code}.png"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            print(f"✅ صورة اللاعب اتحملت ({len(r.content)} bytes)")
            return r.content
        else:
            print(f"⚠️ FPL API رجع {r.status_code}")
    except Exception as e:
        print(f"⚠️ فشل تحميل صورة اللاعب: {e}")
    return None

# ══════════════════════════════════════════
# 2. حوّل لكارتون Muse Style
# ══════════════════════════════════════════
def to_muse_style(image_bytes):
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY مش موجود")
        return None
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = """Convert this football player photo into a Muse State flat cartoon illustration.
Flat vector art, bold black outlines (4px), solid flat colors only,
zero gradients, zero shading.
Clean minimal cartoon face — recognizable but simplified.
White background. Upper body portrait centered.
Same jersey colors as in the photo. High quality sharp edges."""

        # صور FPL بتيجي PNG
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                print("✅ Gemini نجح في توليد الكارتون!")
                return part.inline_data.data

        print("⚠️ Gemini ما رجعش صورة")
        return None

    except Exception as e:
        print(f"❌ خطأ في Gemini: {e}")
        return None

# ══════════════════════════════════════════
# 3. أضف اللوجو
# ══════════════════════════════════════════
def add_logo(image_bytes, logo_size=120):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        img = img.resize((1080, 1080), Image.LANCZOS)

        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            x = img.width - logo_size - 20
            y = img.height - logo_size - 20
            img.paste(logo, (x, y), mask=logo)
        else:
            print("⚠️ logo.png مش موجود في الريبو")

        output = io.BytesIO()
        img.convert("RGB").save(output, "JPEG", quality=95)
        return output.getvalue()

    except Exception as e:
        print(f"❌ خطأ في إضافة اللوجو: {e}")
        return image_bytes

# ══════════════════════════════════════════
# 4. Caption
# ══════════════════════════════════════════
def make_goal_caption(scorer, assist, minute, home_team, away_team,
                       home_score, away_score):
    assist_line = f"🅰️ أسيست: {assist}" if assist else "🅰️ بدون أسيست"
    return f"""⚽ هـــدف! {scorer}
{assist_line}
⏱️ الدقيقة: {minute}'
🆚 {home_team} {home_score} - {away_score} {away_team}

#فانتازي #FPL #بريميرليج"""

# ══════════════════════════════════════════
# 5. الدالة الرئيسية
# ══════════════════════════════════════════
def create_goal_card(player_code, scorer_name, assist_name,
                     minute, home_team, away_team,
                     home_score, away_score):
    print(f"🎨 بنعمل كارت هدف لـ {scorer_name}...")

    # 1. صورة اللاعب
    image_bytes = get_player_image(player_code)
    if not image_bytes:
        print("⚠️ مفيش صورة من FPL")
        caption = make_goal_caption(scorer_name, assist_name, minute,
                                    home_team, away_team, home_score, away_score)
        return None, caption

    # 2. Gemini Muse Style
    print("🤖 Gemini بيحوّل لكارتون...")
    muse_bytes = to_muse_style(image_bytes)

    if muse_bytes:
        print("✅ الكارتون جاهز!")
        final_bytes = muse_bytes
    else:
        print("⚠️ Gemini فشل — هنستخدم الصورة الحقيقية")
        final_bytes = image_bytes

    # 3. أضف اللوجو
    final_bytes = add_logo(final_bytes)

    # 4. احفظ
    path = f"/tmp/goal_{scorer_name.replace(' ', '_')}.jpg"
    with open(path, "wb") as f:
        f.write(final_bytes)
    print(f"✅ الصورة: {path}")

    caption = make_goal_caption(scorer_name, assist_name, minute,
                                home_team, away_team, home_score, away_score)
    return path, caption

if __name__ == "__main__":
    path, caption = create_goal_card(
        player_code=118748,
        scorer_name="محمد صلاح",
        assist_name="ترينت",
        minute=67,
        home_team="ليفربول",
        away_team="بورنموث",
        home_score=2,
        away_score=0
    )
    print(caption)
