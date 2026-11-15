"""
Vector-Art Goal & Assist Card Generator
Generates 1080x1350 mobile-portrait sports cards in Pop-Art / Comic Ben-Day Dot style:
- Vector player portrait integration
- Neon glow typography for GOAL and ASSIST
- Ben-Day halftone retro dots on split Teal/Red background
- Renders via Headless Chromium in 1.5s
"""
import os
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VECTORS_DIR = os.path.join(BASE_DIR, "assets", "vectors")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "temp_vector_goal.html")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map player name keywords to vector portrait files
VECTOR_MAPPING = {
    "صلاح": "salah_pop.jpg",
    "محمد صلاح": "salah_pop.jpg",
    "ماينو": "mainoo.jpg",
    "كوبي ماينو": "mainoo.jpg",
    "جارناتشو": "garnacho.jpg",
    "برونو": "bruno.jpg",
    "برونو فيرنانديز": "bruno.jpg",
    "كين": "kane.jpg",
    "هاري كين": "kane.jpg",
    "نيلسون": "nelson.jpg",
    "ريس نيلسون": "nelson.jpg"
}

def get_vector_image_path(player_name):
    for k, fname in VECTOR_MAPPING.items():
        if k in player_name:
            p = os.path.join(VECTORS_DIR, fname)
            if os.path.exists(p):
                return p
    # Default fallback to salah_pop
    return os.path.join(VECTORS_DIR, "salah_pop.jpg")

def render_vector_goal_card(scorer, assister="بدون صناعة", team="البريميرليج", minute=34, stats="هدف حاسم", output_path=None):
    vector_img = get_vector_image_path(scorer)
    vector_uri = f"file:///{vector_img.replace(os.sep, '/')}"
    lion_uri = f"file:///{os.path.join(BASE_DIR, 'assets', 'pl_lion_600.png').replace(os.sep, '/')}"

    html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Montserrat:wght@900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px; height: 1350px; overflow: hidden;
    background: #0B1118; font-family: 'Almarai', sans-serif;
    position: relative; display: flex; flex-direction: column;
  }}
  .bg-top {{
    position: absolute; top: 0; left: 0; width: 1080px; height: 675px;
    background: linear-gradient(135deg, #028E9B 0%, #005662 100%);
  }}
  .bg-bottom {{
    position: absolute; bottom: 0; left: 0; width: 1080px; height: 675px;
    background: linear-gradient(135deg, #F0484C 0%, #B71C1C 100%);
  }}
  .halftone {{
    position: absolute; width: 100%; height: 100%;
    background-image: radial-gradient(rgba(0, 0, 0, 0.22) 20%, transparent 20%);
    background-size: 24px 24px; pointer-events: none;
  }}
  .container {{
    position: relative; z-index: 2; width: 1080px; height: 1350px;
    display: flex; flex-direction: column; padding: 60px 50px;
  }}
  .top-brand {{
    display: flex; align-items: center; justify-content: space-between;
    width: 100%; margin-bottom: 20px;
  }}
  .brand-logo-wrap {{ display: flex; align-items: center; gap: 15px; }}
  .brand-lion {{
    width: 60px; height: 60px;
    background: url('{lion_uri}') no-repeat center;
    background-size: contain; filter: brightness(0) invert(1);
  }}
  .brand-title {{
    font-family: 'Montserrat', sans-serif; font-size: 32px; font-weight: 900;
    color: #FFFFFF; letter-spacing: 3px;
  }}
  .match-pill {{
    background: rgba(10, 13, 16, 0.85); border: 2px solid #00E5FF;
    padding: 10px 24px; border-radius: 25px; color: #00E5FF;
    font-size: 24px; font-weight: 800;
  }}
  .main-grid {{
    display: flex; align-items: center; justify-content: space-between;
    margin-top: 40px; height: 1000px;
  }}
  .vector-hero-container {{
    width: 480px; height: 900px; display: flex;
    flex-direction: column; align-items: center; justify-content: center;
  }}
  .vector-frame {{
    width: 460px; height: 620px; border-radius: 40px; overflow: hidden;
    position: relative; border: 8px solid #FFFFFF;
    box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 0 16px rgba(10, 13, 16, 0.5);
    background: #A51010;
  }}
  .vector-img {{ width: 100%; height: 100%; object-fit: cover; }}
  .details-container {{
    width: 480px; display: flex; flex-direction: column; gap: 40px;
  }}
  .action-block {{
    background: rgba(10, 17, 24, 0.75); backdrop-filter: blur(10px);
    border-radius: 35px; padding: 40px 35px; border: 4px solid #00E5FF;
    box-shadow: 0 15px 35px rgba(0,0,0,0.5); display: flex; flex-direction: column;
  }}
  .assist-block {{ border-color: #FF5252; }}
  .action-tag {{
    font-family: 'Montserrat', sans-serif; font-size: 85px; font-weight: 900;
    color: #FFFFFF; letter-spacing: 4px; line-height: 1; margin-bottom: 15px;
    text-shadow: 0 0 15px #FFFFFF, 0 0 30px rgba(0, 229, 255, 0.9);
  }}
  .assist-tag {{
    text-shadow: 0 0 15px #FFFFFF, 0 0 30px rgba(255, 82, 82, 0.9);
  }}
  .player-name {{
    font-size: 65px; font-weight: 800; color: #FFFFFF;
    text-shadow: 3px 4px 0px #000000; line-height: 1.2;
  }}
  .team-sub {{ font-size: 26px; font-weight: 700; color: #00E5FF; margin-top: 8px; }}
  .assist-team {{ color: #FF8A80; }}
  .footer-slogan {{
    position: absolute; bottom: 30px; left: 50%;
    transform: translateX(-50%); font-size: 24px; font-weight: 800;
    color: #00E5FF; letter-spacing: 1px;
  }}
</style>
</head>
<body>
  <div class="bg-top"><div class="halftone"></div></div>
  <div class="bg-bottom"><div class="halftone"></div></div>
  <div class="container">
    <div class="top-brand">
      <div class="brand-logo-wrap">
        <div class="brand-lion"></div>
        <div class="brand-title">FANTASY VOLT</div>
      </div>
      <div class="match-pill">⏱️ الدقيقة {minute}'</div>
    </div>
    <div class="main-grid">
      <div class="vector-hero-container">
        <div class="vector-frame">
          <img class="vector-img" src="{vector_uri}" alt="{scorer}">
        </div>
      </div>
      <div class="details-container">
        <div class="action-block">
          <div class="action-tag">GOAL</div>
          <div class="player-name">{scorer}</div>
          <div class="team-sub">{team} • {stats}</div>
        </div>
        <div class="action-block assist-block">
          <div class="action-tag assist-tag">ASSIST</div>
          <div class="player-name">{assister}</div>
          <div class="team-sub assist-team">{team} • صناعة هدف</div>
        </div>
      </div>
    </div>
    <div class="footer-slogan">لو مش متابع ڤولت.. بتلعب فانتازي غلط ⚡</div>
  </div>
</body>
</html>"""

    with open(HTML_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)

    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"vector_goal_{scorer.replace(' ', '_')}.png")

    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = "chromium"

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1080,1350",
        f"--screenshot={output_path}",
        f"file:///{HTML_TEMPLATE_PATH.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_path
