"""
News Card Engine — Original Branded Card Designer
===================================================
Generates professional 1080x1080 news cards with:
- Category-specific color schemes (10 categories)
- RTL Arabic text with proper reshaping
- Background photo overlay mode (blur+darken)
- Solid color mode (no photo needed)
- Brand watermark
- Badge pills
- Text shadows for readability
- Summary box with semi-transparent background
"""
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Category color schemes
CARD_COLORS = {
    "breaking":  {"bg": "#DC2626", "accent": "#FEF2F2", "badge_bg": "#991B1B"},
    "official":  {"bg": "#7C3AED", "accent": "#F5F3FF", "badge_bg": "#5B21B6"},
    "transfers": {"bg": "#EA580C", "accent": "#FFF7ED", "badge_bg": "#C2410C"},
    "quotes":    {"bg": "#0891B2", "accent": "#ECFEFF", "badge_bg": "#0E7490"},
    "stats":     {"bg": "#059669", "accent": "#ECFDF5", "badge_bg": "#047857"},
    "results":   {"bg": "#2563EB", "accent": "#EFF6FF", "badge_bg": "#1D4ED8"},
    "injury":    {"bg": "#DC2626", "accent": "#FEF2F2", "badge_bg": "#991B1B"},
    "lineup":    {"bg": "#4F46E5", "accent": "#EEF2FF", "badge_bg": "#4338CA"},
    "standings": {"bg": "#0D9488", "accent": "#F0FDFA", "badge_bg": "#0F766E"},
    "general":   {"bg": "#1E293B", "accent": "#F8FAFC", "badge_bg": "#334155"},
}

BADGE_ICONS = {
    "breaking": "⚡", "official": "🚨", "transfers": "🔥", "quotes": "🎙️",
    "stats": "📊", "results": "⚽", "injury": "🏥", "lineup": "📋",
    "standings": "📊", "general": "📰",
}

BADGE_TEXT = {
    "breaking": "عاجل", "official": "رسميًا", "transfers": "ميركاتو",
    "quotes": "تصريحات", "stats": "رقم قياسي", "results": "نتائج",
    "injury": "إصابات", "lineup": "التشكيل", "standings": "ترتيب",
    "general": "أخبار",
}


def _hex_to_rgb(hex_color):
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _wrap_text(draw, text, font, max_width):
    """Wrap Arabic text into lines that fit within max_width."""
    reshaped = arabic_reshaper.reshape(text)
    bidi = get_display(reshaped)
    words = bidi.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_news_card(title, summary="", category="general", brand="كورة ڤولت",
                     photo_path=None, output_path=None):
    """
    Render an original branded news card (1080×1080).
    
    If photo_path is provided: blurred photo background + dark overlay.
    Otherwise: solid category-colored background.
    
    Returns path to the generated PNG.
    """
    W, H = 1080, 1080
    colors = CARD_COLORS.get(category, CARD_COLORS["general"])
    bg_rgb = _hex_to_rgb(colors["bg"])
    badge_rgb = _hex_to_rgb(colors["badge_bg"])
    
    # === BASE IMAGE ===
    if photo_path and os.path.exists(photo_path):
        try:
            bg = Image.open(photo_path).convert("RGB")
            ratio = max(W / bg.width, H / bg.height)
            bg = bg.resize((int(bg.width * ratio), int(bg.height * ratio)), Image.LANCZOS)
            left = (bg.width - W) // 2
            top = (bg.height - H) // 2
            bg = bg.crop((left, top, left + W, top + H))
            bg = bg.filter(ImageFilter.GaussianBlur(radius=4))
            img = bg
        except Exception:
            img = Image.new("RGB", (W, H), bg_rgb)
    else:
        img = Image.new("RGB", (W, H), bg_rgb)
    
    # Dark gradient overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(H):
        alpha = int(180 - 60 * abs(y - H // 2) / (H // 2))
        alpha = max(100, min(alpha, 200))
        od.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # === BORDER FRAME ===
    for rect in [((0, 0), (W, 8)), ((0, H - 8), (W, H)),
                 ((0, 0), (8, H)), ((W - 8, 0), (W, H))]:
        draw.rectangle(rect, fill=bg_rgb)
    
    # === FONTS ===
    try:
        font_bold = ImageFont.truetype("tahomabd.ttf", 48)
        font_medium = ImageFont.truetype("tahoma.ttf", 28)
        font_badge = ImageFont.truetype("tahomabd.ttf", 30)
        font_brand = ImageFont.truetype("tahomabd.ttf", 38)
    except Exception:
        font_bold = ImageFont.load_default()
        font_medium = font_badge = font_brand = font_bold
    
    # === BRAND (top-right) ===
    brand_full = f"⚡ {brand}"
    reshaped_brand = arabic_reshaper.reshape(brand_full)
    bidi_brand = get_display(reshaped_brand)
    bb = draw.textbbox((0, 0), bidi_brand, font=font_brand)
    bw = bb[2] - bb[0]
    draw.text((W - bw - 40, 25), bidi_brand, fill="white", font=font_brand)
    
    # === BADGE PILL (top-left) ===
    icon = BADGE_ICONS.get(category, "📰")
    label = BADGE_TEXT.get(category, "أخبار")
    reshaped_label = arabic_reshaper.reshape(f" {label} ")
    bidi_label = get_display(reshaped_label)
    badge_full = f"{icon}{bidi_label}"
    
    bb = draw.textbbox((0, 0), badge_full, font=font_badge)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    draw.rounded_rectangle(
        [(30, 25), (30 + bw + 30, 25 + bh + 20)],
        radius=20, fill=badge_rgb
    )
    draw.text((45, 35), badge_full, fill="white", font=font_badge)
    
    # === TITLE (centered, RTL wrapped) ===
    max_w = W - 100
    title_lines = _wrap_text(draw, title, font_bold, max_w)
    line_h = 68
    total_h = len(title_lines) * line_h
    
    has_summary = summary and len(summary) > 20
    title_y = (H // 2 - total_h - 20) if has_summary else (H - total_h) // 2
    
    for i, line in enumerate(title_lines):
        bb = draw.textbbox((0, 0), line, font=font_bold)
        lw = bb[2] - bb[0]
        x = (W - lw) // 2
        y = title_y + i * line_h
        draw.text((x + 3, y + 3), line, fill=(0, 0, 0), font=font_bold)
        draw.text((x, y), line, fill="white", font=font_bold)
    
    # === SUMMARY ===
    if has_summary:
        sum_lines = _wrap_text(draw, summary[:160], font_medium, max_w - 60)
        sum_y = title_y + total_h + 25
        sum_total_h = len(sum_lines[:3]) * 40 + 25
        
        # Semi-transparent background
        sum_bg = Image.new("RGBA", (W - 60, sum_total_h + 10), (0, 0, 0, 100))
        img_rgba = img.convert("RGBA")
        img_rgba.paste(sum_bg, (30, sum_y - 5), sum_bg)
        img = img_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)
        
        for i, line in enumerate(sum_lines[:3]):
            bb = draw.textbbox((0, 0), line, font=font_medium)
            lw = bb[2] - bb[0]
            x = (W - lw) // 2
            draw.text((x, sum_y + i * 40 + 5), line, fill="#E2E8F0", font=font_medium)
    
    # === SAVE ===
    if not output_path:
        slug = hashlib.md5(title.encode()).hexdigest()[:8]
        output_path = os.path.join(OUTPUT_DIR, f"news_card_{slug}.png")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path
