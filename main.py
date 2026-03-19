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
# 5. كروت FPL الأخرى (price / captain / injury / transfers)
# ══════════════════════════════════════════

def _render_simple_card(html: str, output_path: str, width=500, height=500) -> str | None:
    """Helper: render HTML → PNG"""
    success = html_to_image(html, output_path, width=width, height=height)
    return output_path if success else None


def price_card(player_name: str, old_price: float, new_price: float,
               output_path: str = "/tmp/price_card.png") -> str | None:
    direction = "📈 ارتفع" if new_price > old_price else "📉 انخفض"
    color = "#00a86b" if new_price > old_price else "#E85555"
    logo_b64 = load_logo_base64("logo.png")
    logo_html = f'<img class="logo" src="data:image/png;base64,{logo_b64}" alt="">' if logo_b64 else ""

    html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:500px;height:400px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.card {{width:500px;height:400px;background:linear-gradient(160deg,#0d1f3c,#0a0e1a);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;position:relative;}}
.header {{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(90deg,{color},{color}cc);display:flex;align-items:center;justify-content:center;}}
.badge {{font-family:'Lilita One',cursive;font-size:22px;color:#fff;letter-spacing:2px;}}
.name {{font-size:28px;font-weight:900;color:#fff;margin-top:20px;}}
.prices {{display:flex;gap:30px;align-items:center;}}
.old {{font-size:22px;color:#aaa;text-decoration:line-through;}}
.arrow {{font-size:28px;}}
.new {{font-size:32px;font-weight:900;color:{color};}}
.logo {{position:absolute;bottom:14px;left:16px;width:44px;height:44px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.85;}}
</style></head><body>
<div class="card">
  <div class="header"><span class="badge">💰 تغيير سعر</span></div>
  <div class="name">{player_name}</div>
  <div class="prices">
    <span class="old">{old_price:.1f}م</span>
    <span class="arrow">{direction}</span>
    <span class="new">{new_price:.1f}م</span>
  </div>
  {logo_html}
</div></body></html>"""
    return _render_simple_card(html, output_path, width=500, height=400)


def captain_card(player_name: str, price: float, form: float,
                  ownership: float, fixture: str,
                  output_path: str = "/tmp/captain_card.png") -> str | None:
    logo_b64 = load_logo_base64("logo.png")
    logo_html = f'<img class="logo" src="data:image/png;base64,{logo_b64}" alt="">' if logo_b64 else ""

    html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:500px;height:450px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.card {{width:500px;height:450px;background:linear-gradient(160deg,#0d1f3c,#0a0e1a);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;position:relative;}}
.header {{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(90deg,#00AFCC,#0090aa);display:flex;align-items:center;justify-content:center;gap:10px;}}
.badge {{font-family:'Lilita One',cursive;font-size:22px;color:#fff;letter-spacing:2px;}}
.name {{font-size:30px;font-weight:900;color:#fff;margin-top:16px;}}
.stats {{display:flex;gap:16px;margin-top:8px;}}
.stat {{background:rgba(255,255,255,0.1);border-radius:12px;padding:10px 18px;text-align:center;}}
.stat-val {{font-size:20px;font-weight:900;color:#00AFCC;}}
.stat-lbl {{font-size:12px;color:#aaa;margin-top:2px;}}
.fixture {{font-size:16px;color:#ffe066;font-weight:700;}}
.logo {{position:absolute;bottom:14px;left:16px;width:44px;height:44px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.85;}}
</style></head><body>
<div class="card">
  <div class="header"><span style="font-size:26px">©️</span><span class="badge">توصية الكابتن</span></div>
  <div class="name">{player_name}</div>
  <div class="stats">
    <div class="stat"><div class="stat-val">{price:.1f}م</div><div class="stat-lbl">السعر</div></div>
    <div class="stat"><div class="stat-val">{form}</div><div class="stat-lbl">الفورم</div></div>
    <div class="stat"><div class="stat-val">{ownership:.1f}%</div><div class="stat-lbl">الملكية</div></div>
  </div>
  <div class="fixture">⚽ {fixture}</div>
  {logo_html}
</div></body></html>"""
    return _render_simple_card(html, output_path, width=500, height=450)


def injury_card(player_name: str, chance: int, news: str,
                 output_path: str = "/tmp/injury_card.png") -> str | None:
    logo_b64 = load_logo_base64("logo.png")
    logo_html = f'<img class="logo" src="data:image/png;base64,{logo_b64}" alt="">' if logo_b64 else ""

    html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:500px;height:380px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.card {{width:500px;height:380px;background:linear-gradient(160deg,#1a0a0a,#0a0e1a);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;position:relative;}}
.header {{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(90deg,#E85555,#c73333);display:flex;align-items:center;justify-content:center;gap:10px;}}
.badge {{font-family:'Lilita One',cursive;font-size:22px;color:#fff;letter-spacing:2px;}}
.name {{font-size:28px;font-weight:900;color:#fff;margin-top:16px;}}
.chance {{font-size:42px;font-weight:900;color:#E85555;}}
.news {{font-size:14px;color:#aaa;text-align:center;padding:0 30px;line-height:1.5;}}
.logo {{position:absolute;bottom:14px;left:16px;width:44px;height:44px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.85;}}
</style></head><body>
<div class="card">
  <div class="header"><span style="font-size:26px">🚑</span><span class="badge">تحديث إصابة</span></div>
  <div class="name">{player_name}</div>
  <div class="chance">{chance}% للمشاركة</div>
  <div class="news">{news}</div>
  {logo_html}
</div></body></html>"""
    return _render_simple_card(html, output_path, width=500, height=380)


def transfers_card(bought: list, sold: list,
                    output_path: str = "/tmp/transfers_card.png") -> str | None:
    logo_b64 = load_logo_base64("logo.png")
    logo_html = f'<img class="logo" src="data:image/png;base64,{logo_b64}" alt="">' if logo_b64 else ""

    bought_rows = "".join([
        f'<div class="row"><span class="in">▲</span><span class="pname">{p["name"]}</span><span class="num">+{p.get("transfers_in",0):,}</span></div>'
        for p in bought[:4]
    ])
    sold_rows = "".join([
        f'<div class="row"><span class="out">▼</span><span class="pname">{p["name"]}</span><span class="num">-{p.get("transfers_out",0):,}</span></div>'
        for p in sold[:4]
    ])

    html = f"""<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{width:500px;height:520px;overflow:hidden;font-family:'Tajawal',sans-serif;}}
.card {{width:500px;height:520px;background:linear-gradient(160deg,#0d1f3c,#0a0e1a);display:flex;flex-direction:column;position:relative;padding-top:60px;}}
.header {{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(90deg,#00AFCC,#0090aa);display:flex;align-items:center;justify-content:center;}}
.badge {{font-family:'Lilita One',cursive;font-size:20px;color:#fff;letter-spacing:2px;}}
.section {{padding:12px 24px;}}
.section-title {{font-size:14px;font-weight:700;margin-bottom:8px;}}
.in-title {{color:#00a86b;}} .out-title {{color:#E85555;}}
.row {{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.07);border-radius:8px;padding:8px 12px;margin-bottom:6px;}}
.pname {{flex:1;font-size:14px;font-weight:700;color:#fff;}}
.num {{font-size:13px;color:#aaa;}}
.in {{color:#00a86b;font-size:16px;}} .out {{color:#E85555;font-size:16px;}}
.logo {{position:absolute;bottom:14px;left:16px;width:44px;height:44px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.85;}}
</style></head><body>
<div class="card">
  <div class="header"><span class="badge">🔄 أكتر التحويلات</span></div>
  <div class="section">
    <div class="section-title in-title">الأكتر دخولاً</div>
    {bought_rows}
  </div>
  <div class="section">
    <div class="section-title out-title">الأكتر خروجاً</div>
    {sold_rows}
  </div>
  {logo_html}
</div></body></html>"""
    return _render_simple_card(html, output_path, width=500, height=520)


# ══════════════════════════════════════════
# 6. اختبار محلي
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
