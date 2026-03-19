"""
goal_card.py
بيعمل كارت الهدف:
1. يجيب صورة اللاعب من FPL API
2. يحوّلها لكارتون Muse Style بـ Gemini
3. يضيف لوجو Fantasy Volt
4. يرجع الصورة + الـ caption
"""

import os
import io
import requests
from PIL import Image, ImageDraw
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"

# ══════════════════════════════════════════
# 1. جيب صورة اللاعب من FPL
# ══════════════════════════════════════════
def get_player_image(player_code):
    """
    player_code = الكود من FPL API (مثلاً صلاح = 118748)
    """
    url = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{player_code}.png"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        print(f"⚠️ فشل تحميل صورة اللاعب: {e}")
    return None

# ══════════════════════════════════════════
# 2. حوّل الصورة لكارتون Muse Style
# ══════════════════════════════════════════
def to_muse_style(image_bytes):
    """بيحوّل صورة اللاعب لكارتون Muse Style بـ Gemini"""
    if not GEMINI_API_KEY:
        print("⚠️ GEMINI_API_KEY مش موجود")
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)

        img = Image.open(io.BytesIO(image_bytes))

        model = genai.GenerativeModel("gemini-2.0-flash-exp")

        prompt = """Convert this football player photo into a Muse State flat cartoon illustration.
Flat vector art, bold black outlines (4px), solid flat colors only,
zero gradients, zero shading.
Clean minimal cartoon face — recognizable but simplified.
White or transparent background. Upper body portrait centered.
Same jersey colors as in the photo. High quality sharp edges."""

        response = model.generate_content([prompt, img])

        for part in response.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                return part.inline_data.data

        print("⚠️ Gemini ما رجعش صورة")
        return None

    except Exception as e:
        print(f"❌ خطأ في Gemini: {e}")
        return None

# ══════════════════════════════════════════
# 3. أضف اللوجو على الصورة
# ══════════════════════════════════════════
def add_logo(image_bytes, logo_size=120):
    """يضيف لوجو Fantasy Volt على الصورة"""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

        # حجم ثابت للصورة
        img = img.resize((1080, 1080), Image.LANCZOS)

        # حمّل اللوجو
        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # ضع اللوجو في أسفل اليمين
            x = img.width - logo_size - 20
            y = img.height - logo_size - 20
            img.paste(logo, (x, y), mask=logo)

        # احفظ
        output = io.BytesIO()
        img.convert("RGB").save(output, "JPEG", quality=95)
        return output.getvalue()

    except Exception as e:
        print(f"❌ خطأ في إضافة اللوجو: {e}")
        return image_bytes

# ══════════════════════════════════════════
# 4. اعمل الـ Caption
# ══════════════════════════════════════════
def make_goal_caption(scorer, assist, minute, home_team, away_team,
                       home_score, away_score):
    """يعمل caption الهدف بالعربي المصري"""
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
    """
    بترجع (image_path, caption)
    """
    print(f"🎨 بنعمل كارت هدف لـ {scorer_name}...")

    # 1. جيب صورة اللاعب
    image_bytes = get_player_image(player_code)
    if not image_bytes:
        print("⚠️ مفيش صورة — هنستخدم placeholder")
        # placeholder بسيط
        img = Image.new("RGB", (1080, 1080), (0, 175, 204))
        draw = ImageDraw.Draw(img)
        output = io.BytesIO()
        img.save(output, "JPEG")
        image_bytes = output.getvalue()

    # 2. حوّل لكارتون Muse Style
    print("🤖 Gemini بيحوّل لكارتون...")
    muse_bytes = to_muse_style(image_bytes)

    if muse_bytes:
        print("✅ الكارتون جاهز!")
        final_bytes = muse_bytes
    else:
        print("⚠️ Gemini فشل — هنستخدم الصورة الأصلية")
        final_bytes = image_bytes

    # 3. أضف اللوجو
    final_bytes = add_logo(final_bytes)

    # 4. احفظ الصورة
    path = f"/tmp/goal_{scorer_name.replace(' ', '_')}.jpg"
    with open(path, "wb") as f:
        f.write(final_bytes)
    print(f"✅ الصورة محفوظة: {path}")

    # 5. اعمل الـ caption
    caption = make_goal_caption(
        scorer_name, assist_name, minute,
        home_team, away_team, home_score, away_score
    )

    return path, caption


# ══════════════════════════════════════════
# اختبار
# ══════════════════════════════════════════
if __name__ == "__main__":
    path, caption = create_goal_card(
        player_code=118748,      # كود صلاح في FPL
        scorer_name="محمد صلاح",
        assist_name="ترينت",
        minute=67,
        home_team="ليفربول",
        away_team="بورنموث",
        home_score=2,
        away_score=0
    )
    print("\n📝 الـ Caption:")
    print(caption)
    print(f"\n🖼️ الصورة: {path}")
