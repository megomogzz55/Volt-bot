"""
Dual-Mode Goal & Assist Card Generator
Supports:
1. Standard Mode (اللاعبين العاديين): Pure Typography & Badge (No Photo) - Instant, matches orig_goal_assist.jpg 100%
2. Superstar Mode (نجوم الصف الأول): Vector Pop-Art with Halftone & Hero Portrait
"""
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VECTORS_DIR = os.path.join(BASE_DIR, "assets", "vectors")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
HTML_TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "temp_vector_goal.html")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SUPERSTARS = {
    "صلاح": "salah_pop.jpg",
    "محمد صلاح": "salah_pop.jpg",
    "salah": "salah_pop.jpg",
    "مبابي": "mbappe_transparent.png",
    "كيليان مبابي": "mbappe_transparent.png",
    "mbappe": "mbappe_transparent.png",
    "ماينو": "mainoo.jpg",
    "mainoo": "mainoo.jpg",
    "جارناتشو": "garnacho.jpg",
    "garnacho": "garnacho.jpg",
    "برونو": "bruno.jpg",
    "برونو فيرنانديز": "bruno.jpg",
    "كين": "kane.jpg",
    "هاري كين": "kane.jpg",
    "نيلسون": "nelson.jpg"
}

def is_superstar(player_name):
    clean = str(player_name).lower()
    for k in SUPERSTARS.keys():
        if k in clean:
            return True, SUPERSTARS[k]
    return False, None

def render_standard_goal_card(scorer, assister="بدون صناعة", minute=34, output_path=None):
    """
    Standard Mode for ordinary players: PURE TYPOGRAPHY (NO PHOTO)
    Matches orig_goal_assist.jpg with 1080x1350 resolution, neon glows, and center lion logo.
    """
    lion_uri = f"file:///{os.path.join(BASE_DIR, 'assets', 'pl_lion_600.png').replace(os.sep, '/')}"
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Montserrat:wght@900&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px; height: 1350px; overflow: hidden;
    font-family: 'Almarai', sans-serif; position: relative;
    display: flex; flex-direction: column;
  }}
  .top-half {{
    width: 1080px; height: 675px;
    background: linear-gradient(135deg, #028E9B 0%, #005662 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding-bottom: 60px; position: relative;
  }}
  .bottom-half {{
    width: 1080px; height: 675px;
    background: linear-gradient(135deg, #F0484C 0%, #B71C1C 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding-top: 60px; position: relative;
  }}
  .halftone {{
    position: absolute; width: 100%; height: 100%;
    background-image: radial-gradient(rgba(0, 0, 0, 0.18) 18%, transparent 18%);
    background-size: 28px 28px; pointer-events: none;
  }}
  .english-tag {{
    font-family: 'Montserrat', sans-serif; font-size: 135px; font-weight: 900;
    color: #FFFFFF; letter-spacing: 6px; line-height: 1; margin-bottom: 25px;
    text-shadow: 0 0 15px #FFFFFF, 0 0 35px rgba(0, 229, 255, 0.95), 0 0 70px rgba(0, 229, 255, 0.6);
  }}
  .assist-tag {{
    text-shadow: 0 0 15px #FFFFFF, 0 0 35px rgba(255, 120, 120, 0.95), 0 0 70px rgba(255, 120, 120, 0.6);
  }}
  .player-name-top {{
    font-size: 105px; font-weight: 800; color: #F0484C;
    -webkit-text-stroke: 5px #1A1D20; text-shadow: 4px 6px 0px #1A1D20;
    z-index: 2;
  }}
  .player-name-bottom {{
    font-size: 105px; font-weight: 800; color: #00E5FF;
    -webkit-text-stroke: 5px #1A1D20; text-shadow: 4px 6px 0px #1A1D20;
    z-index: 2;
  }}
  .center-badge {{
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 210px; height: 210px; background: #0A0D10; border-radius: 50%;
    border: 5px solid #FFFFFF; box-shadow: 0 15px 40px rgba(0,0,0,0.8);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    z-index: 10;
  }}
  .badge-lion {{
    width: 105px; height: 105px;
    background: url('{lion_uri}') no-repeat center;
    background-size: contain; filter: brightness(0) invert(1);
  }}
  .badge-txt {{
    font-family: 'Montserrat', sans-serif; font-size: 15px; font-weight: 900;
    color: #00E5FF; letter-spacing: 2px; margin-top: 5px;
  }}
  .minute-pill {{
    position: absolute; bottom: 35px;
    background: rgba(10, 13, 16, 0.9); border: 2px solid #00E5FF;
    padding: 10px 30px; border-radius: 30px; color: #00E5FF;
    font-size: 26px; font-weight: 800;
  }}
</style>
</head>
<body>
  <div class="top-half">
    <div class="halftone"></div>
    <div class="english-tag">GOAL</div>
    <div class="player-name-top">{scorer}</div>
  </div>
  
  <div class="center-badge">
    <div class="badge-lion"></div>
    <div class="badge-txt">FANTASY VOLT</div>
  </div>
  
  <div class="bottom-half">
    <div class="halftone"></div>
    <div class="english-tag assist-tag">ASSIST</div>
    <div class="player-name-bottom">{assister}</div>
    <div class="minute-pill">⏱️ الدقيقة {minute}'</div>
  </div>
</body>
</html>"""

    with open(HTML_TEMPLATE_PATH, "w", encoding="utf-8") as f:
        f.write(html)
        
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"goal_{scorer.replace(' ', '_')}.png")
        
    _render_html(HTML_TEMPLATE_PATH, output_path)
    return output_path

def render_superstar_goal_card(scorer, assister, team, minute, stats, vector_file, output_path=None):
    """
    Superstar Mode: Hero Vector Portrait + Pop Art Card
    """
    vector_uri = f"file:///{os.path.join(VECTORS_DIR, vector_file).replace(os.sep, '/')}"
    lion_uri = f"file:///{os.path.join(BASE_DIR, 'assets', 'pl_lion_600.png').replace(os.sep, '/')}"

    html = f"""<!DOCTYPE html>
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
    background: radial-gradient(circle at 50% 40%, #1A237E 0%, #0D1333 100%);
    display: flex; align-items: center; justify-content: center;
  }}
  .vector-img {{ max-width: 95%; max-height: 95%; object-fit: contain; }}
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
        f.write(html)
        
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"superstar_goal_{scorer.replace(' ', '_')}.png")
        
    _render_html(HTML_TEMPLATE_PATH, output_path)
    return output_path

def _render_html(html_file, output_path):
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
        f"file:///{html_file.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, capture_output=True, check=True)

def render_goal_card(scorer, assister="بدون صناعة", team="البريميرليج", minute=34, stats="هدف حاسم", output_path=None):
    """
    Smart Dispatcher:
    - Superstars (Salah, Haaland, Mbappe, Bruno, Palmer, Mainoo): Uses Hero Vector Pop-Art!
    - Ordinary Players (Kerkez, Semenyo, Gboho, Barry, etc.): Uses Pure Typography (NO PHOTO) - 100% matches orig_goal_assist.jpg!
    """
    is_star, vector_file = is_superstar(scorer)
    if is_star:
        print(f"Goal Scorer '{scorer}' is a SUPERSTAR -> Rendering with Vector Art ({vector_file})")
        return render_superstar_goal_card(scorer, assister, team, minute, stats, vector_file, output_path)
    else:
        print(f"Goal Scorer '{scorer}' is an ORDINARY PLAYER -> Rendering Pure Typography (No Photo)")
        return render_standard_goal_card(scorer, assister, minute, output_path)
