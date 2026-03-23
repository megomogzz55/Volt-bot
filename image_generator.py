"""
image_generator.py — Fantasy Volt
Cloudflare Workers AI (FLUX-1-schnell) — مجاني ♾️
"""

import os, io, requests
from PIL import Image
from pathlib import Path

CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "")
CF_API_TOKEN  = os.environ.get("CF_API_TOKEN", "")
LOGO_PATH     = Path(__file__).parent / "logo.png"


def generate_cartoon(player_name: str, team: str = "football") -> bytes | None:
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        print("⚠️ CF_ACCOUNT_ID أو CF_API_TOKEN مش موجودين")
        return None

    prompt = (
        f"flat vector cartoon portrait of a {team} football player, "
        "bold black outlines, solid flat colors, white background, "
        "Muse State style, upper body portrait, FIFA card illustration, "
        "minimal shading, clean lines, professional avatar"
    )

    try:
        print("🎨 Cloudflare FLUX بيولّد كارتون...")
        r = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell",
            headers={"Authorization": f"Bearer {CF_API_TOKEN}"},
            json={"prompt": prompt},
            timeout=60
        )
        if r.status_code == 200 and len(r.content) > 5000:
            print(f"✅ الكارتون جاهز ({len(r.content)} bytes)")
            return r.content
        print(f"❌ Cloudflare فشل: {r.status_code}")
        return None
    except Exception as e:
        print(f"❌ exception: {e}")
        return None


def add_logo_to_image(img_bytes: bytes, logo_size: int = 100) -> bytes:
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        img = img.resize((1080, 1080), Image.LANCZOS)

        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH).convert("RGBA").resize((logo_size, logo_size), Image.LANCZOS)
            r2, g2, b2, a2 = logo.split()
            logo_w = Image.merge("RGBA", (
                Image.new("L", logo.size, 255),
                Image.new("L", logo.size, 255),
                Image.new("L", logo.size, 255), a2
            ))
            img.paste(logo_w, (img.width - logo_size - 20, img.height - logo_size - 20), logo_w.split()[3])

        out = io.BytesIO()
        img.convert("RGB").save(out, "JPEG", quality=95)
        return out.getvalue()
    except Exception as e:
        print(f"❌ لوجو: {e}")
        return img_bytes


def get_player_image(player_name: str) -> bytes | None:
    try:
        r = requests.get(
            f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={requests.utils.quote(player_name)}",
            timeout=10
        )
        data = r.json()
        if not data.get("player"):
            return None
        img_url = data["player"][0].get("strCutout") or data["player"][0].get("strThumb")
        if not img_url:
            return None
        img_r = requests.get(img_url, timeout=10)
        if img_r.status_code == 200:
            return img_r.content
    except:
        pass
    return None


def price_card(*a, **k): return None
def captain_card(*a, **k): return None
def injury_card(*a, **k): return None
def transfers_card(*a, **k): return None
