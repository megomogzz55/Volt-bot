"""
Template Card Engine — Renders sports news cards using Kora Volt's official template.
Matches the exact visual hierarchy of the reference design:
- Layer 1: Solid background color (#ca2424 or category color)
- Layer 2: Player/article photo centered in upper region (height: 1100px)
- Layer 3: Official template overlay (logo + black gradient + electric lightning bolts)
- Layer 4: Typography (Source tag -> 2-line Cairo 900 bold headline -> Footer tag)
"""

import base64
import os
import subprocess
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "assets", "templates", "kora_volt_bg.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def _split_headline_two_lines(headline: str) -> tuple:
    """Split a headline cleanly into two balanced lines for maximum visual punch."""
    words = headline.strip().split()
    if len(words) <= 5:
        return headline, ""
    
    mid = len(words) // 2
    # Adjust cut to avoid splitting right before short prepositions
    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])
    return line1, line2


def render_template_card(
    photo_path: str,
    headline: str,
    source_tag: str,
    output_filename: str = "template_card.png",
    photo_focus: str = "center 15%"
) -> str:
    """
    Renders a news card using the exact official Kora Volt template layout:
    - Photo sits UNDER the template (full-bleed, natural shading from template gradient)
    - Shaded template on top (Logo + black gradient shadow + bottom lightning)
    - Speaker/source name + headline ONLY.
    
    Args:
        photo_path: Path to the article/player photo.
        headline: Main news headline in Arabic.
        source_tag: Name of the speaker or source (e.g. 'الصحفي فابريزيو رومانو', 'رسميًا 🔴').
        output_filename: Filename for output PNG.
        photo_focus: CSS background-position for photo framing (default 'center 15%').
        
    Returns:
        Absolute path to rendered 1350x1688 PNG image.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template not found at: {TEMPLATE_PATH}")
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Photo not found at: {photo_path}")
        
    with open(TEMPLATE_PATH, "rb") as f:
        template_b64 = base64.b64encode(f.read()).decode()
        
    ext = os.path.splitext(photo_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode()
        
    l1, l2 = _split_headline_two_lines(headline)
    
    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;800;900&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width: 1350px; height: 1688px;
  font-family: 'Cairo', sans-serif;
  overflow: hidden; position: relative;
  background: #000;
}}

/* 1. PHOTO UNDER TEMPLATE */
.photo-layer {{
  position: absolute;
  inset: 0;
  background: url(data:{mime};base64,{photo_b64}) no-repeat {photo_focus};
  background-size: cover;
  z-index: 1;
}}

/* 2. SHADED TEMPLATE OVERLAY (Logo + Gradient Shadow + Lightning) */
.template-overlay {{
  position: absolute; inset: 0;
  background: url(data:image/png;base64,{template_b64}) center/cover;
  z-index: 2;
  pointer-events: none;
}}

/* 3. TEXT ON TOP (Source/Speaker + Headline ONLY) */
.text-layer {{
  position: absolute;
  left: 0; right: 0;
  top: 1120px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0 60px;
}}

.source-tag {{
  font-size: 34px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 35px;
}}

.headline-1 {{
  font-size: 60px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.25;
  margin-bottom: 20px;
  text-shadow: 0 4px 20px rgba(0,0,0,0.9);
}}

.headline-2 {{
  font-size: 60px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.25;
  text-shadow: 0 4px 20px rgba(0,0,0,0.9);
}}
</style>
</head>
<body>
  <div class="photo-layer"></div>
  <div class="template-overlay"></div>
  <div class="text-layer">
    <div class="source-tag">{source_tag}</div>
    <div class="headline-1">{l1}</div>
    {"<div class='headline-2'>" + l2 + "</div>" if l2 else ""}
  </div>
</body>
</html>"""

    html_path = os.path.join(OUTPUT_DIR, "_tmp_card.html")
    png_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_path}",
        "--window-size=1350,1688",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    
    subprocess.run(cmd, capture_output=True, timeout=30)
    
    if os.path.exists(png_path):
        img = Image.open(png_path).crop((0, 0, 1350, 1688))
        img.save(png_path)
        try:
            os.remove(html_path)
        except OSError:
            pass
        return png_path
        
    raise RuntimeError("Failed to render card with Edge Headless")
