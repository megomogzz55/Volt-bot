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
STATEMENT_TEMPLATE_PATH = os.path.join(BASE_DIR, "assets", "templates", "kora_volt_headline_bg.png")
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "AraJozoor-Regular.ttf")
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
    source_tag: str = "",
    source_role: str = "",
    source_name: str = "",
    output_filename: str = "template_card.png",
    photo_focus: str = "center 15%"
) -> str:
    """
    Renders a news card using the exact official Kora Volt template layout:
    - Photo sits UNDER the template (full-bleed, natural shading from template gradient)
    - Shaded template on top (Logo + black gradient shadow + bottom lightning)
    - Headline in shadow area (Jozor bold)
    - Source role (in electric blue) ABOVE Source name (in white) at the bottom.
    
    Args:
        photo_path: Path to the article/player photo.
        headline: Main news headline in Arabic.
        source_tag: Combined source tag or fallback.
        source_role: The role (e.g. 'الصحفي', 'صحيفة', 'اللاعب', 'المدرب', 'شبكة', 'نادي') in electric blue.
        source_name: The name (e.g. 'فابريزيو رومانو', 'ماركا الإسبانية') in white.
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
        
    # If source_role and source_name not given, attempt to split source_tag
    if not source_role and not source_name:
        parts = source_tag.strip().split(maxsplit=1)
        if len(parts) == 2 and parts[0] in ["الصحفي", "صحيفة", "اللاعب", "المدرب", "شبكة", "نادي", "منصة", "وكالة", "المصدر"]:
            source_role, source_name = parts[0], parts[1]
        else:
            source_role, source_name = "", source_tag

    with open(TEMPLATE_PATH, "rb") as f:
        template_b64 = base64.b64encode(f.read()).decode()
        
    font_b64 = ""
    if os.path.exists(FONT_PATH):
        with open(FONT_PATH, "rb") as f:
            font_b64 = base64.b64encode(f.read()).decode()
            
    ext = os.path.splitext(photo_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode()
        
    l1, l2 = _split_headline_two_lines(headline)
    
    # Speaker HTML block: role in blue above name in white
    if source_role and source_name:
        speaker_html = f"""<div class="speaker-role">{source_role}</div>
      <div class="speaker-name">{source_name}</div>"""
    else:
        speaker_html = f"""<div class="speaker-name">{source_name or source_tag}</div>"""
    
    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<style>
@font-face {{
  font-family: 'Jozor';
  src: url(data:font/truetype;charset=utf-8;base64,{font_b64}) format('truetype');
  font-weight: normal;
  font-style: normal;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width: 1350px; height: 1688px;
  font-family: 'Jozor', 'Cairo', sans-serif;
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

/* 3. HEADLINE IN SHADOW AREA */
.headline-container {{
  position: absolute;
  left: 0; right: 0;
  top: 1190px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0 50px;
}}

.headline-1 {{
  font-size: 68px;
  color: #ffffff;
  line-height: 1.35;
  margin-bottom: 22px;
  -webkit-text-stroke: 1.2px #ffffff;
  text-shadow: 0 4px 20px rgba(0,0,0,0.9);
}}

.headline-2 {{
  font-size: 68px;
  color: #ffffff;
  line-height: 1.35;
  -webkit-text-stroke: 1.2px #ffffff;
  text-shadow: 0 4px 20px rgba(0,0,0,0.9);
}}

/* 4. SPEAKER AT THE BOTTOM: ROLE IN BLUE ABOVE NAME IN WHITE */
.speaker-container {{
  position: absolute;
  left: 0; right: 0;
  bottom: 85px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}}

.speaker-role {{
  font-size: 28px;
  font-weight: 700;
  color: #00b4d8;
  letter-spacing: 1px;
  margin-bottom: 4px;
  text-shadow: 0 0 12px rgba(0, 180, 216, 0.4);
}}

.speaker-name {{
  font-size: 38px;
  font-weight: 700;
  color: #ffffff;
  -webkit-text-stroke: 0.5px #ffffff;
  letter-spacing: 0.5px;
}}
</style>
</head>
<body>
  <div class="photo-layer"></div>
  <div class="template-overlay"></div>
  
  <div class="headline-container">
    <div class="headline-1">{l1}</div>
    {"<div class='headline-2'>" + l2 + "</div>" if l2 else ""}
  </div>
  
  <div class="speaker-container">
    {speaker_html}
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


def render_statement_card(
    photo_path: str,
    statement_text: str,
    source_role: str = "الصحفي",
    source_name: str = "فابريزيو رومانو",
    output_filename: str = "statement_card.png",
    photo_focus: str = "center 20%"
) -> str:
    """
    Renders Template #2 (Manchettes, Statements, Quotes & Interviews):
    - Photo on the left under template (width: 1400px, 2160x2700 HD).
    - Shaded horizontal gradient to black on the right.
    - KORA VOLT logo at top right.
    - Headline / statement in Jozor bold white font in the right column.
    - Speaker role (in electric blue) above Speaker name (in white) at bottom right.
    
    Args:
        photo_path: Path to the article/player photo.
        statement_text: Detailed statement / quote / manchette text in Arabic.
        source_role: The role (e.g. 'الصحفي', 'اللاعب', 'المدرب', 'نادي') in electric blue.
        source_name: The name (e.g. 'فابريزيو رومانو', 'واين روني') in white.
        output_filename: Filename for output PNG.
        photo_focus: CSS background-position for photo framing (default 'center 20%').
        
    Returns:
        Absolute path to rendered 2160x2700 PNG image.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    tmpl_file = STATEMENT_TEMPLATE_PATH if os.path.exists(STATEMENT_TEMPLATE_PATH) else TEMPLATE_PATH
    if not os.path.exists(tmpl_file):
        raise FileNotFoundError(f"Template not found at: {tmpl_file}")
    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Photo not found at: {photo_path}")
        
    with open(tmpl_file, "rb") as f:
        tmpl_b64 = base64.b64encode(f.read()).decode()
        
    font_b64 = ""
    if os.path.exists(FONT_PATH):
        with open(FONT_PATH, "rb") as f:
            font_b64 = base64.b64encode(f.read()).decode()
            
    ext = os.path.splitext(photo_path)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode()
        
    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<style>
@font-face {{
  font-family: 'Jozor';
  src: url(data:font/truetype;charset=utf-8;base64,{font_b64}) format('truetype');
  font-weight: normal;
  font-style: normal;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width: 2160px; height: 2700px;
  font-family: 'Jozor', sans-serif;
  overflow: hidden; position: relative;
  background: #000;
}}

/* 1. PHOTO ON THE LEFT UNDER TEMPLATE */
.photo-layer {{
  position: absolute;
  top: 0; left: 0; bottom: 0;
  width: 1400px;
  background: url(data:{mime};base64,{photo_b64}) no-repeat {photo_focus};
  background-size: cover;
  z-index: 1;
}}

/* 2. SHADED HORIZONTAL TEMPLATE OVERLAY (Logo + Gradient) */
.template-overlay {{
  position: absolute; inset: 0;
  background: url(data:image/png;base64,{tmpl_b64}) center/cover;
  z-index: 2;
  pointer-events: none;
}}

/* 3. HEADLINE COLUMN ON THE RIGHT */
.content-col {{
  position: absolute;
  left: 1160px; right: 100px;
  top: 820px; bottom: 120px;
  z-index: 3;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  text-align: center;
}}

.headline-box {{
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 20px 0;
}}

.headline-text {{
  font-size: 64px;
  color: #ffffff;
  line-height: 1.55;
  -webkit-text-stroke: 1.2px #ffffff;
  text-shadow: 0 4px 20px rgba(0,0,0,0.95);
  max-width: 860px;
}}

/* 4. SPEAKER AT THE BOTTOM OF THE COLUMN */
.speaker-box {{
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 20px;
}}

.speaker-role {{
  font-size: 32px;
  font-weight: 700;
  color: #00b4d8;
  letter-spacing: 1.5px;
  margin-bottom: 8px;
  text-shadow: 0 0 15px rgba(0, 180, 216, 0.5);
}}

.speaker-name {{
  font-size: 46px;
  font-weight: 700;
  color: #ffffff;
  -webkit-text-stroke: 0.8px #ffffff;
  letter-spacing: 0.5px;
  text-shadow: 0 4px 15px rgba(0,0,0,0.9);
}}
</style>
</head>
<body>
  <div class="photo-layer"></div>
  <div class="template-overlay"></div>
  
  <div class="content-col">
    <div class="headline-box">
      <div class="headline-text">{statement_text}</div>
    </div>
    
    <div class="speaker-box">
      <div class="speaker-role">{source_role}</div>
      <div class="speaker-name">{source_name}</div>
    </div>
  </div>
</body>
</html>"""

    html_path = os.path.join(OUTPUT_DIR, "_tmp_statement.html")
    png_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        f"--screenshot={png_path}",
        "--window-size=2160,2700",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)
    
    if os.path.exists(png_path):
        img = Image.open(png_path).crop((0, 0, 2160, 2700))
        img.save(png_path)
        try:
            os.remove(html_path)
        except OSError:
            pass
        return png_path
        
    raise RuntimeError("Failed to render statement card with Edge Headless")
