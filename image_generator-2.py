"""
image_generator.py — Fantasy Volt Image Generator
- HTML كارت → Playwright screenshot
- Muse Style عبر Gemini 2.0 Flash (مجاني)
- Fallback: Pollinations flux
- Logo: من الريبو مباشرة
"""

import os
import base64
import requests
import time
import json
from pathlib import Path


# ══════════════════════════════════════════
# 1. تحميل اللوجو
# ══════════════════════════════════════════
def load_logo_base64(logo_path: str = "logo.png") -> str:
    """تحميل اللوجو وتحويله لـ base64"""
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"⚠️ logo.png مش موجود في {logo_path}")
        return ""


# ══════════════════════════════════════════
# 2. Muse Style — تحويل صورة لكارتون
# ══════════════════════════════════════════
MUSE_PROMPT = (
    "Convert this football player photo into a Muse State flat cartoon illustration. "
    "Flat vector art, bold black outlines (4px), solid flat colors only, "
    "zero gradients, zero shading. "
    "Clean minimal cartoon face — recognizable but simplified. "
    "White background. Upper body portrait centered. "
    "Same jersey colors as in the photo. High quality sharp edges."
)


def muse_style_gemini(image_url: str, gemini_key: str) -> str | None:
    """
    تحويل صورة لكارتون بـ Gemini 2.0 Flash
    Returns: URL للصورة المحوّلة أو None عند الفشل
    """
    try:
        # تحميل الصورة
        print("📥 تحميل صورة اللاعب...")
        resp = requests.get(image_url, timeout=15)
        if resp.status_code != 200:
            print(f"❌ فشل تحميل الصورة: {resp.status_code}")
            return None

        img_b64 = base64.b64encode(resp.content).decode("utf-8")
        print(f"✅ الصورة اتحملت ({len(resp.content)} bytes)")

        # إرسال لـ Gemini
        print("🤖 بيحول لكارتون Gemini 2.0...")
        api_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash-exp:generateContent"
            f"?key={gemini_key}"
        )

        payload = {
            "contents": [{
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    },
                    {"text": MUSE_PROMPT}
                ]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE", "TEXT"],
                "temperature": 1,
            }
        }

        r = requests.post(api_url, json=payload, timeout=60)

        if r.status_code == 429:
            print(f"⚠️ Gemini 429 — quota خلصت، جرّب بعدين")
            return None
        if r.status_code != 200:
            print(f"❌ Gemini فشل: {r.status_code} — {r.text[:200]}")
            return None

        data = r.json()

        # استخراج الصورة من الـ response
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if part.get("inlineData", {}).get("mimeType", "").startswith("image/"):
                img_data = base64.b64decode(part["inlineData"]["data"])

                # رفع الصورة على catbox.moe
                cartoon_url = upload_to_catbox(img_data)
                if cartoon_url:
                    print(f"✅ Muse Style جاهز: {cartoon_url}")
                    return cartoon_url

        print("❌ Gemini ما رجّعش صورة في الـ response")
        return None

    except Exception as e:
        print(f"❌ Gemini exception: {e}")
        return None


def muse_style_pollinations(player_name: str) -> str | None:
    """
    Fallback: Pollinations flux لو Gemini فشل
    """
    try:
        print("🎨 بيجرب Pollinations flux...")
        prompt = (
            f"flat cartoon illustration of football player {player_name}, "
            "Muse State style, flat vector art, bold black outlines, "
            "solid colors, no gradients, white background, upper body portrait"
        )
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?model=flux&width=512&height=600&nologo=true&seed=42"

        r = requests.get(url, timeout=45)
        if r.status_code == 200 and len(r.content) > 5000:
            cartoon_url = upload_to_catbox(r.content)
            if cartoon_url:
                print(f"✅ Pollinations نجح: {cartoon_url}")
                return cartoon_url

        print(f"⚠️ Pollinations رجع {r.status_code} ({len(r.content)} bytes)")
        return None

    except Exception as e:
        print(f"❌ Pollinations exception: {e}")
        return None


def upload_to_catbox(img_bytes: bytes) -> str | None:
    """رفع صورة على catbox.moe والحصول على URL"""
    try:
        print("☁️ بيرفع الصورة على catbox...")
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload"},
            files={"fileToUpload": ("cartoon.png", img_bytes, "image/png")},
            timeout=30
        )
        if r.status_code == 200 and r.text.startswith("https://"):
            print(f"✅ catbox: {r.text.strip()}")
            return r.text.strip()
        print(f"⚠️ catbox فشل: {r.text[:100]}")
        return None
    except Exception as e:
        print(f"❌ catbox exception: {e}")
        return None


# ══════════════════════════════════════════
# 3. HTML → Screenshot بـ Playwright
# ══════════════════════════════════════════
def html_to_image(html_content: str, output_path: str, width: int = 500, height: int = 600) -> bool:
    """
    تحويل HTML لصورة PNG بـ Playwright
    Returns: True لو نجح
    """
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page(viewport={"width": width, "height": height})
            page.set_content(html_content, wait_until="networkidle")
            page.wait_for_timeout(1500)  # وقت كافي للفونت يتحمل
            page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": width, "height": height})
            browser.close()

        print(f"✅ Screenshot: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Playwright فشل: {e}")
        return False


# ══════════════════════════════════════════
# 4. الدالة الرئيسية — توليد كارت الهدف
# ══════════════════════════════════════════
def generate_goal_card(player_name: str, assist: str, minute: int,
                        score: str, player_img_url: str,
                        output_path: str = "/tmp/goal_card.png") -> str | None:
    """
    توليد كارت الهدف الكامل
    1. حاول Muse Style (Gemini → Pollinations)
    2. لو فشل: استخدم الصورة الحقيقية
    3. ارسم الكارت بـ Playwright
    Returns: مسار الصورة الناتجة أو None
    """
    from card_templates import get_goal_card_html

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    logo_b64 = load_logo_base64("logo.png")

    # محاولة Muse Style
    cartoon_url = None

    if gemini_key:
        cartoon_url = muse_style_gemini(player_img_url, gemini_key)
        if not cartoon_url:
            time.sleep(2)
            cartoon_url = muse_style_pollinations(player_name)
    else:
        print("⚠️ GEMINI_API_KEY مش موجود — بيجرب Pollinations")
        cartoon_url = muse_style_pollinations(player_name)

    # اختيار الصورة المستخدمة
    final_img_url = cartoon_url if cartoon_url else player_img_url
    is_cartoon = bool(cartoon_url)

    print(f"🖼️ الصورة: {'كارتون Muse Style' if is_cartoon else 'صورة حقيقية'}")

    # توليد الـ HTML
    html = get_goal_card_html(
        player_name=player_name,
        assist=assist,
        minute=minute,
        score=score,
        player_img_url=final_img_url,
        logo_base64=logo_b64
    )

    # تحويل لصورة
    success = html_to_image(html, output_path, width=500, height=600)

    if success:
        print(f"✅ الكارت جاهز: {output_path}")
        return output_path
    else:
        print("❌ فشل توليد الكارت")
        return None


# ══════════════════════════════════════════
# 5. اختبار محلي
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("🧪 اختبار كارت الهدف...")
    result = generate_goal_card(
        player_name="محمد صلاح",
        assist="ترينت",
        minute=67,
        score="ليفربول 2 - 0 بورنموث",
        player_img_url="https://r2.thesportsdb.com/images/media/player/cutout/3blc581757088735.png",
        output_path="/tmp/test_goal_card.png"
    )
    if result:
        print(f"✅ النتيجة: {result}")
    else:
        print("❌ الاختبار فشل")
