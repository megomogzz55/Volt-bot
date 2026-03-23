"""
goal_card.py - كارت الهدف
1. صورة اللاعب من FPL API الرسمي (بالكود المباشر)
2. Cloudflare FLUX يحوّلها لكارتون Muse Style
3. إضافة لوجو Fantasy Volt
4. caption بالعربي المصري
"""

import os
import io
import requests
from PIL import Image
from pathlib import Path

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
CF_ACCOUNT_ID  = os.environ.get("CF_ACCOUNT_ID", "")
CF_API_TOKEN   = os.environ.get("CF_API_TOKEN", "")
BASE_DIR  = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"

# ══════════════════════════════════════════════════════════════
# قاموس: اسم اللاعب (عربي أو إنجليزي) → FPL photo code
# المصدر: fantasy.premierleague.com/api/bootstrap-static/
# ══════════════════════════════════════════════════════════════
FPL_CODES = {
    # ليفربول
    "Mohamed Salah": 118748, "محمد صلاح": 118748, "صلاح": 118748,
    "Trent Alexander-Arnold": 169187, "ترينت": 169187,
    "Virgil van Dijk": 97032, "فان ديك": 97032,
    "Diogo Jota": 213129, "جوتا": 213129,
    "Luis Diaz": 461870, "لويس دياز": 461870,
    "Darwin Nunez": 462669, "نونيز": 462669,
    "Alisson": 116535,
    "Andrew Robertson": 122798, "روبيرتسون": 122798,
    "Dominik Szoboszlai": 461017, "سوبوسلاي": 461017,
    "Curtis Jones": 225796,
    "Harvey Elliott": 461260, "إليوت": 461260,
    # مانشستر سيتي
    "Erling Haaland": 447211, "هالاند": 447211,
    "Phil Foden": 209244, "فودن": 209244,
    "Kevin De Bruyne": 61366, "دي بروين": 61366,
    "Bernardo Silva": 165809, "برناردو": 165809,
    "Ederson": 111457,
    "Jeremy Doku": 473946, "ديوكو": 473946,
    "Rodri": 215040, "رودري": 215040,
    # أرسنال
    "Bukayo Saka": 223340, "ساكا": 223340, "بوكايو ساكا": 223340,
    "Martin Odegaard": 213345, "أوديجارد": 213345,
    "Leandro Trossard": 369232, "تروسار": 369232,
    "Gabriel Martinelli": 461134, "مارتينيلي": 461134,
    "Gabriel Magalhaes": 461192, "غابرييل": 461192,
    "David Raya": 95688,
    "Kai Havertz": 215677, "هافيرتز": 215677,
    "Declan Rice": 181655, "رايس": 181655,
    "Ben White": 230748,
    # مانشستر يونايتد
    "Bruno Fernandes": 175780, "برونو": 175780, "برونو فيرنانديز": 175780,
    "Rasmus Hojlund": 470303, "هوليند": 470303,
    "Marcus Rashford": 176297, "راشفورد": 176297,
    "Alejandro Garnacho": 480424, "غارناتشو": 480424,
    # تشيلسي
    "Cole Palmer": 224722, "كول بالمر": 224722,
    "Nicolas Jackson": 477285, "جاكسون": 477285,
    "Pedro Neto": 212168, "بيدرو نيتو": 212168,
    "Reece James": 198439,
    # توتنهام
    "Son Heung-min": 85971, "سون": 85971,
    "James Maddison": 184621, "ماديسون": 184621,
    "Dejan Kulusevski": 474524, "كولوسيفسكي": 474524,
    # نيوكاسل
    "Alexander Isak": 462459, "إيساك": 462459,
    "Anthony Gordon": 246025, "غوردون": 246025,
    "Nick Pope": 117374,
    # أستون فيلا
    "Ollie Watkins": 221566, "ووتكينز": 221566,
    "Morgan Rogers": 488413, "روجرز": 488413,
    "Leon Bailey": 213337, "بايلي": 213337,
    "Emiliano Martinez": 98745, "مارتينيز": 98745,
    # برايتون
    "Joao Pedro": 473975,
    "Kaoru Mitoma": 470288, "ميتوما": 470288,
    "Danny Welbeck": 63812, "ويلبيك": 63812,
    # بورنموث
    "Evanilson": 438808,
    "Justin Kluivert": 461340, "كلوفيرت": 461340,
    # كريستال بالاس
    "Jean-Philippe Mateta": 215075, "ماتيتا": 215075,
    "Eberechi Eze": 209088, "إيزي": 209088,
    # ويست هام
    "Jarrod Bowen": 220022, "بوين": 220022,
    "Lucas Paqueta": 439987, "باكيتا": 439987,
    # وولفز
    "Matheus Cunha": 479547, "كونيا": 479547,
}


# ══════════════════════════════════════════
# 1. جيب صورة اللاعب من FPL الرسمي
# ══════════════════════════════════════════
def get_player_image(player_name_or_code):
    """
    يجيب صورة اللاعب من FPL الرسمي أولاً، ثم TheSportsDB احتياطي.
    player_name_or_code: ممكن يكون اسم عربي/إنجليزي أو FPL code رقمي.
    """

    # ── المصدر 1: FPL Official ─────────────────
    # لو جالنا رقم مباشرة — استخدمه فوراً
    fpl_code = None

    if isinstance(player_name_or_code, int):
        fpl_code = player_name_or_code
    elif str(player_name_or_code).isdigit():
        fpl_code = int(player_name_or_code)
    else:
        # ابحث في القاموس باسم اللاعب
        fpl_code = FPL_CODES.get(str(player_name_or_code))

    if fpl_code:
        fpl_url = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{fpl_code}.png"
        print(f"🔵 FPL URL: {fpl_url}")
        try:
            r = requests.get(fpl_url, timeout=10,
                             headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 5000:
                print(f"✅ الصورة اتحملت من FPL ({len(r.content):,} bytes)")
                return r.content
            else:
                print(f"⚠️ FPL رجع {r.status_code}")
        except Exception as e:
            print(f"⚠️ FPL error: {e}")

    # ── المصدر 2: TheSportsDB احتياطي ──────────
    # نستخدم الاسم الإنجليزي (مش الرقم)
    en_name = str(player_name_or_code) if not str(player_name_or_code).isdigit() else None

    # لو الاسم في القاموس، نجيب نظيره الإنجليزي
    if en_name:
        # ابحث عن نظير إنجليزي في القاموس
        for key, code in FPL_CODES.items():
            if code == fpl_code and key.isascii():
                en_name = key
                break

    if en_name and not en_name.isdigit():
        try:
            url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={requests.utils.quote(en_name)}"
            r = requests.get(url, timeout=10)
            data = r.json()
            players = data.get("player") or []

            # فلتر كرة قدم فقط
            filtered = [
                p for p in players
                if "soccer" in (p.get("strSport") or "").lower()
                or "football" in (p.get("strSport") or "").lower()
            ] or players

            if filtered:
                player = filtered[0]
                img_url = player.get("strCutout") or player.get("strThumb")
                if img_url:
                    print(f"🟡 TheSportsDB: {img_url}")
                    img_r = requests.get(img_url, timeout=10)
                    if img_r.status_code == 200 and len(img_r.content) > 5000:
                        print(f"✅ TheSportsDB ({len(img_r.content):,} bytes)")
                        return img_r.content
        except Exception as e:
            print(f"⚠️ TheSportsDB error: {e}")

    print(f"❌ فشل جلب صورة {player_name_or_code}")
    return None


# ══════════════════════════════════════════
# 2. رفع صورة مؤقت (للـ Pollinations)
# ══════════════════════════════════════════
def upload_image_temp(image_bytes):
    try:
        import base64
        b64 = base64.b64encode(image_bytes).decode()
        r = requests.post(
            "https://imgbb.com/json",
            data={"source": b64, "type": "base64", "action": "upload"},
            timeout=30
        )
        url = r.json().get("image", {}).get("url")
        if url:
            print(f"✅ imgbb: {url}")
            return url
    except Exception as e:
        print(f"⚠️ imgbb فشل: {e}")

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

    return None


# ══════════════════════════════════════════
# 3. حوّل لكارتون Muse Style
# ══════════════════════════════════════════
def to_muse_style(image_bytes, team: str = "football"):
    """
    الترتيب: Cloudflare FLUX → Pollinations → Gemini → صورة حقيقية
    """

    # ── Cloudflare FLUX (الأول) ─────────────────
    if CF_ACCOUNT_ID and CF_API_TOKEN:
        try:
            prompt = (
                f"flat vector cartoon portrait of a {team} football player, "
                "bold black outlines, solid flat colors, white background, "
                "Muse State style, upper body portrait, FIFA card illustration, "
                "minimal shading, clean lines, professional avatar"
            )
            print("🎨 بنجرب Cloudflare FLUX...")
            r = requests.post(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell",
                headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
                json={"prompt": prompt},
                timeout=60
            )
            if r.status_code == 200:
                import base64
                try:
                    data = r.json()
                    img_b64 = data.get("result", {}).get("image", "")
                    if img_b64:
                        img_bytes = base64.b64decode(img_b64)
                        print(f"✅ Cloudflare نجح! ({len(img_bytes):,} bytes)")
                        return img_bytes
                except Exception:
                    pass
                if len(r.content) > 5000:
                    print(f"✅ Cloudflare نجح raw! ({len(r.content):,} bytes)")
                    return r.content
            print(f"⚠️ Cloudflare رجع {r.status_code}")
        except Exception as e:
            print(f"⚠️ Cloudflare فشل: {e}")

    # ── Pollinations (ثاني) ─────────────────────
    try:
        from urllib.parse import quote
        print("🎨 بنرفع الصورة...")
        image_url = upload_image_temp(image_bytes)
        if image_url:
            print("🎨 بنجرب Pollinations flux...")
            prompt = "Convert this football player photo into a Muse State flat cartoon illustration. Flat vector art, bold black outlines, solid flat colors only, zero gradients, clean minimal cartoon face recognizable but simplified, white background, upper body portrait centered, same jersey colors"
            url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
            r = requests.get(url, params={"model": "flux", "image": image_url,
                                           "width": 512, "height": 512,
                                           "nologo": "true", "seed": 42},
                             timeout=120)
            if r.status_code == 200 and len(r.content) > 10000:
                print("✅ Pollinations نجح!")
                return r.content
            print(f"⚠️ Pollinations رجع {r.status_code}")
    except Exception as e:
        print(f"⚠️ Pollinations فشل: {e}")

    # ── Gemini (ثالث) ───────────────────────────
    if GEMINI_API_KEY:
        try:
            from google import genai
            from google.genai import types
            print("🤖 بنجرب Gemini...")
            client = genai.Client(
                api_key=GEMINI_API_KEY,
                http_options=types.HttpOptions(api_version='v1alpha')
            )
            prompt = """Convert this football player photo into a Muse State flat cartoon illustration.
Flat vector art, bold black outlines (4px), solid flat colors only,
zero gradients, zero shading.
Clean minimal cartoon face — recognizable but simplified.
White background. Upper body portrait centered.
Same jersey colors as in the photo. High quality sharp edges."""
            image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[image_part, prompt],
                config=types.GenerateContentConfig(response_modalities=["IMAGE"])
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
# 4. أضف اللوجو
# ══════════════════════════════════════════
def add_logo(image_bytes, logo_size=120):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize((1080, 1080), Image.LANCZOS)
        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            x = img.width - logo_size - 20
            y = img.height - logo_size - 20
            img.paste(logo, (x, y), mask=logo.split()[3])
        else:
            print("⚠️ logo.png مش موجود")
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=92)
        result = output.getvalue()
        print(f"✅ اللوجو اتضاف ({len(result):,} bytes)")
        return result
    except Exception as e:
        print(f"❌ خطأ في اللوجو: {e}")
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=92)
            return output.getvalue()
        except:
            return image_bytes


# ══════════════════════════════════════════
# 5. Caption
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
# 6. الدالة الرئيسية
# ══════════════════════════════════════════
def create_goal_card(player_code, scorer_name, assist_name,
                     minute, home_team, away_team,
                     home_score, away_score):
    print(f"🎨 بنعمل كارت هدف لـ {scorer_name}...")

    # 1. صورة اللاعب — بنبعت الـ code الرقمي مباشرة ✅
    image_bytes = get_player_image(player_code)

    # لو الـ code مجبش صورة، جرّب الاسم العربي
    if not image_bytes and scorer_name:
        print(f"🔄 بنجرب الاسم: {scorer_name}")
        image_bytes = get_player_image(scorer_name)

    if not image_bytes:
        print("⚠️ مفيش صورة — هننشر نص بس")
        caption = make_goal_caption(scorer_name, assist_name, minute,
                                    home_team, away_team, home_score, away_score)
        return None, caption

    # 2. Muse Style
    print("🎨 بنحوّل لكارتون...")
    muse_bytes = to_muse_style(image_bytes)
    final_bytes = muse_bytes if muse_bytes else image_bytes

    # 3. اللوجو
    final_bytes = add_logo(final_bytes)

    # 4. تأكد JPEG
    if not final_bytes[:3] == b'\xff\xd8\xff':
        print("⚠️ بنحول لـ JPEG...")
        try:
            img = Image.open(io.BytesIO(final_bytes)).convert("RGB")
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=90)
            final_bytes = out.getvalue()
            print("✅ اتحولت لـ JPEG")
        except Exception as e:
            print(f"⚠️ فشل التحويل: {e}")
            final_bytes = image_bytes

    # 5. احفظ
    path = f"/tmp/goal_{scorer_name.replace(' ', '_')}.jpg"
    with open(path, "wb") as f:
        f.write(final_bytes)
    print(f"✅ الصورة: {path}")

    caption = make_goal_caption(scorer_name, assist_name, minute,
                                home_team, away_team, home_score, away_score)
    return path, caption


if __name__ == "__main__":
    path, caption = create_goal_card(
        player_code=118748,      # ← FPL code لمحمد صلاح
        scorer_name="محمد صلاح",
        assist_name="ترينت",
        minute=67,
        home_team="ليفربول",
        away_team="بورنموث",
        home_score=2,
        away_score=0
    )
    print(caption)
