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
def get_player_image(player_name):
    """
    يجيب صورة وجه اللاعب من الأمام من TheSportsDB
    strCutout = صورة وجه من الأمام على خلفية شفافة ✅
    """
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={requests.utils.quote(player_name)}"
        r = requests.get(url, timeout=10)
        data = r.json()

        if not data.get("player"):
            print(f"⚠️ مفيش لاعب بالاسم: {player_name}")
            return None

        player = data["player"][0]

        # strCutout = صورة وجه من الأمام ✅
        # strThumb = صورة action من الجانب ❌
        img_url = player.get("strCutout") or player.get("strThumb")

        if not img_url:
            print("⚠️ مفيش صورة في TheSportsDB")
            return None

        print(f"✅ لقينا صورة اللاعب: {img_url}")
        img_r = requests.get(img_url, timeout=10)
        if img_r.status_code == 200:
            print(f"✅ الصورة اتحملت ({len(img_r.content)} bytes)")
            return img_r.content

        print(f"⚠️ فشل تحميل الصورة: {img_r.status_code}")
        return None

    except Exception as e:
        print(f"⚠️ خطأ في تحميل الصورة: {e}")
        return None

# ══════════════════════════════════════════
# 2. حوّل لكارتون Muse Style
# ══════════════════════════════════════════
def upload_image_temp(image_bytes):
    """
    يرفع الصورة على imgbb بدون API key
    ويرجع URL مؤقت
    """
    # الطريقة 1 — imgbb بدون key
    try:
        import base64
        b64 = base64.b64encode(image_bytes).decode()
        r = requests.post(
            "https://imgbb.com/json",
            data={
                "source": b64,
                "type": "base64",
                "action": "upload",
            },
            timeout=30
        )
        data = r.json()
        if data.get("image", {}).get("url"):
            url = data["image"]["url"]
            print(f"✅ imgbb: {url}")
            return url
    except Exception as e:
        print(f"⚠️ imgbb فشل: {e}")

    # الطريقة 2 — catbox.moe بدون key
    try:
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload", "userhash": ""},
            files={"fileToUpload": ("player.png", image_bytes, "image/png")},
            timeout=30
        )
        if r.status_code == 200 and r.text.startswith("https"):
            print(f"✅ catbox: {r.text.strip()}")
            return r.text.strip()
    except Exception as e:
        print(f"⚠️ catbox فشل: {e}")

    print("⚠️ فشل رفع الصورة")
    return None


def to_muse_style(image_bytes):
    """
    بيحوّل صورة اللاعب لكارتون Muse Style
    الترتيب:
    1. Pollinations nanobanana (مجاني — reference image)
    2. Gemini (لو عنده quota)
    """

    # ══════════════════════════════════════════
    # الحل 1 — Pollinations nanobanana
    # ══════════════════════════════════════════
    try:
        from urllib.parse import quote

        print("🎨 بنرفع الصورة على 0x0.st...")
        image_url = upload_image_temp(image_bytes)

        if image_url:
            print("🎨 بنجرب Pollinations nanobanana...")

            prompt = "Convert this football player photo into a Muse State flat cartoon illustration. Flat vector art, bold black outlines, solid flat colors only, zero gradients, clean minimal cartoon face recognizable but simplified, white background, upper body portrait centered, same jersey colors"

            params = {
                "model": "nanobanana",
                "image": image_url,
                "width": 1024,
                "height": 1024,
                "nologo": "true",
                "seed": 42
            }

            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
            r = requests.get(url, params=params, timeout=120)

            if r.status_code == 200 and len(r.content) > 10000:
                print("✅ Pollinations نجح!")
                return r.content
            else:
                print(f"⚠️ Pollinations رجع {r.status_code} ({len(r.content)} bytes)")

    except Exception as e:
        print(f"⚠️ Pollinations فشل: {e}")

    # ══════════════════════════════════════════
    # الحل 2 — Gemini (لو عنده quota)
    # ══════════════════════════════════════════
    if GEMINI_API_KEY:
        try:
            from google import genai
            from google.genai import types

            print("🤖 بنجرب Gemini...")
            client = genai.Client(api_key=GEMINI_API_KEY)

            prompt = """Convert this football player photo into a Muse State flat cartoon illustration.
Flat vector art, bold black outlines (4px), solid flat colors only,
zero gradients, zero shading.
Clean minimal cartoon face — recognizable but simplified.
White background. Upper body portrait centered.
Same jersey colors as in the photo. High quality sharp edges."""

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
                    print("✅ Gemini نجح!")
                    return part.inline_data.data

        except Exception as e:
            print(f"⚠️ Gemini فشل: {e}")

    print("⚠️ كل الطرق فشلت — هنستخدم الصورة الحقيقية")
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

    # 1. صورة اللاعب من TheSportsDB باسمه الإنجليزي
    # player_code هنا هيبقى الاسم الإنجليزي مثلاً "Mohamed Salah"
    player_english_name = str(player_code)
    image_bytes = get_player_image(player_english_name)
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
