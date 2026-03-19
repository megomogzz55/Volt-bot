"""
card_templates.py — Fantasy Volt Card Templates
كروت HTML جاهزة للتحويل لصورة عن طريق Playwright
"""

def get_goal_card_html(player_name: str, assist: str, minute: int,
                        score: str, player_img_url: str, logo_base64: str = "") -> str:
    """
    كارت الهدف — Fantasy Volt Style
    أزرق #00AFCC فوق | كورالي #E85555 تحت
    """
    logo_html = ""
    if logo_base64:
        logo_html = f'<img class="logo" src="data:image/png;base64,{logo_base64}" alt="Fantasy Volt">'

    assist_html = ""
    if assist and assist.lower() not in ["none", "لا يوجد", "-", ""]:
        assist_html = f'<div class="info-row assist"><span class="icon">🅰️</span><span class="label">أسيست</span><span class="value">{assist}</span></div>'

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=500">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    width: 500px;
    height: 600px;
    overflow: hidden;
    font-family: 'Tajawal', sans-serif;
    background: #0a0e1a;
  }}

  .card {{
    width: 500px;
    height: 600px;
    position: relative;
    background: linear-gradient(160deg, #0d1f3c 0%, #0a0e1a 100%);
    border-radius: 0;
    overflow: hidden;
  }}

  /* الخطوط الزخرفية في الخلفية */
  .card::before {{
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    border: 40px solid rgba(0,175,204,0.08);
  }}
  .card::after {{
    content: '';
    position: absolute;
    bottom: -80px;
    left: -80px;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    border: 50px solid rgba(232,85,85,0.07);
  }}

  /* Header Bar */
  .header {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 70px;
    background: linear-gradient(90deg, #00AFCC, #0090aa);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    z-index: 10;
  }}

  .goal-badge {{
    font-family: 'Lilita One', cursive;
    font-size: 28px;
    color: #fff;
    letter-spacing: 3px;
    text-shadow: 2px 2px 0px rgba(0,0,0,0.3);
  }}

  .goal-icon {{
    font-size: 32px;
    animation: none;
  }}

  /* صورة اللاعب */
  .player-section {{
    position: absolute;
    top: 55px;
    left: 0; right: 0;
    height: 330px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    z-index: 5;
  }}

  .player-glow {{
    position: absolute;
    bottom: 0;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,175,204,0.25) 0%, transparent 70%);
  }}

  .player-img {{
    width: 260px;
    height: 300px;
    object-fit: cover;
    object-position: top center;
    position: relative;
    z-index: 6;
    filter: drop-shadow(0 -10px 30px rgba(0,175,204,0.4));
  }}

  /* اسم اللاعب */
  .player-name-bar {{
    position: absolute;
    top: 355px;
    left: 0; right: 0;
    text-align: center;
    z-index: 10;
    padding: 0 20px;
  }}

  .player-name {{
    font-family: 'Tajawal', sans-serif;
    font-weight: 900;
    font-size: 32px;
    color: #fff;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    line-height: 1.1;
  }}

  /* Bottom Info Section */
  .info-section {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 185px;
    background: linear-gradient(160deg, #E85555, #c73333);
    border-radius: 24px 24px 0 0;
    padding: 16px 24px 14px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  /* الديفايدر */
  .divider {{
    position: absolute;
    top: 350px;
    left: 20px; right: 20px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00AFCC, transparent);
    z-index: 10;
  }}

  .info-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 7px 14px;
  }}

  .icon {{ font-size: 16px; flex-shrink: 0; }}
  .label {{
    font-size: 13px;
    color: rgba(255,255,255,0.75);
    flex-shrink: 0;
    min-width: 55px;
  }}
  .value {{
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    margin-right: auto;
  }}

  .score-big {{
    font-family: 'Lilita One', cursive;
    font-size: 18px;
    color: #ffe066;
  }}

  /* اللوجو */
  .logo {{
    position: absolute;
    bottom: 14px;
    left: 16px;
    width: 48px;
    height: 48px;
    object-fit: contain;
    opacity: 0.9;
    z-index: 20;
    filter: brightness(0) invert(1);
  }}

  /* الدقيقة badge */
  .minute-badge {{
    position: absolute;
    top: 75px;
    left: 16px;
    background: rgba(0,0,0,0.6);
    border: 1.5px solid #00AFCC;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 13px;
    color: #00AFCC;
    font-weight: 700;
    z-index: 15;
  }}
</style>
</head>
<body>
<div class="card">
  <!-- Header -->
  <div class="header">
    <span class="goal-icon">⚽</span>
    <span class="goal-badge">GOAL!</span>
  </div>

  <!-- دقيقة الهدف -->
  <div class="minute-badge">⏱ {minute}'</div>

  <!-- صورة اللاعب -->
  <div class="player-section">
    <div class="player-glow"></div>
    <img class="player-img" src="{player_img_url}" 
         onerror="this.src='https://via.placeholder.com/260x300/0d1f3c/00AFCC?text=?'" 
         crossorigin="anonymous">
  </div>

  <!-- الديفايدر -->
  <div class="divider"></div>

  <!-- اسم اللاعب -->
  <div class="player-name-bar">
    <div class="player-name">{player_name}</div>
  </div>

  <!-- Info Section -->
  <div class="info-section">
    {assist_html}
    <div class="info-row">
      <span class="icon">🏆</span>
      <span class="label">النتيجة</span>
      <span class="value score-big">{score}</span>
    </div>
    {logo_html}
  </div>
</div>
</body>
</html>"""


def get_yellow_card_html(player_name: str, minute: int,
                          team: str, player_img_url: str, logo_base64: str = "") -> str:
    """كارت الكرت الأصفر"""
    logo_html = ""
    if logo_base64:
        logo_html = f'<img class="logo" src="data:image/png;base64,{logo_base64}" alt="Fantasy Volt">'

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:500px; height:600px; overflow:hidden; font-family:'Tajawal',sans-serif; background:#0a0e1a; }}
  .card {{ width:500px; height:600px; position:relative; background:linear-gradient(160deg,#1a1200 0%,#0a0e1a 100%); overflow:hidden; }}
  .header {{ position:absolute; top:0; left:0; right:0; height:70px; background:linear-gradient(90deg,#f5c518,#e6a800); display:flex; align-items:center; justify-content:center; gap:12px; z-index:10; }}
  .badge {{ font-family:'Lilita One',cursive; font-size:26px; color:#1a1200; letter-spacing:2px; }}
  .player-section {{ position:absolute; top:55px; left:0; right:0; height:330px; display:flex; align-items:flex-end; justify-content:center; }}
  .player-img {{ width:260px; height:300px; object-fit:cover; object-position:top; filter:drop-shadow(0 -10px 30px rgba(245,197,24,0.35)); position:relative; z-index:6; }}
  .player-name-bar {{ position:absolute; top:355px; left:0; right:0; text-align:center; z-index:10; padding:0 20px; }}
  .player-name {{ font-weight:900; font-size:32px; color:#fff; }}
  .divider {{ position:absolute; top:350px; left:20px; right:20px; height:2px; background:linear-gradient(90deg,transparent,#f5c518,transparent); z-index:10; }}
  .info-section {{ position:absolute; bottom:0; left:0; right:0; height:185px; background:linear-gradient(160deg,#c8a000,#9a7800); border-radius:24px 24px 0 0; padding:16px 24px 14px; z-index:10; display:flex; flex-direction:column; gap:8px; }}
  .info-row {{ display:flex; align-items:center; gap:10px; background:rgba(255,255,255,0.15); border-radius:10px; padding:7px 14px; }}
  .label {{ font-size:13px; color:rgba(255,255,255,0.75); min-width:55px; }}
  .value {{ font-size:15px; font-weight:700; color:#fff; margin-right:auto; }}
  .logo {{ position:absolute; bottom:14px; left:16px; width:48px; height:48px; object-fit:contain; z-index:20; filter:brightness(0) invert(1); opacity:0.9; }}
  .minute-badge {{ position:absolute; top:75px; left:16px; background:rgba(0,0,0,0.6); border:1.5px solid #f5c518; border-radius:20px; padding:4px 12px; font-size:13px; color:#f5c518; font-weight:700; z-index:15; }}
</style>
</head>
<body>
<div class="card">
  <div class="header"><span style="font-size:32px">🟨</span><span class="badge">YELLOW CARD</span></div>
  <div class="minute-badge">⏱ {minute}'</div>
  <div class="player-section">
    <img class="player-img" src="{player_img_url}" onerror="this.src='https://via.placeholder.com/260x300'" crossorigin="anonymous">
  </div>
  <div class="divider"></div>
  <div class="player-name-bar"><div class="player-name">{player_name}</div></div>
  <div class="info-section">
    <div class="info-row"><span>⚽</span><span class="label">الفريق</span><span class="value">{team}</span></div>
    <div class="info-row"><span>⏱</span><span class="label">الدقيقة</span><span class="value">{minute}'</span></div>
    {logo_html}
  </div>
</div>
</body>
</html>"""


def get_full_time_html(home_team: str, away_team: str,
                        home_score: int, away_score: int, logo_base64: str = "") -> str:
    """كارت نهاية المباراة"""
    logo_html = ""
    if logo_base64:
        logo_html = f'<img class="logo" src="data:image/png;base64,{logo_base64}" alt="Fantasy Volt">'

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@700;900&family=Lilita+One&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:500px; height:500px; overflow:hidden; font-family:'Tajawal',sans-serif; }}
  .card {{ width:500px; height:500px; position:relative; background:linear-gradient(160deg,#0d1f3c,#0a0e1a); overflow:hidden; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:0; }}
  .header {{ position:absolute; top:0; left:0; right:0; height:60px; background:linear-gradient(90deg,#00AFCC,#0090aa); display:flex; align-items:center; justify-content:center; }}
  .badge {{ font-family:'Lilita One',cursive; font-size:24px; color:#fff; letter-spacing:3px; }}
  .teams-row {{ display:flex; align-items:center; justify-content:center; gap:0; width:100%; padding:0 30px; margin-top:30px; }}
  .team {{ flex:1; text-align:center; }}
  .team-name {{ font-weight:900; font-size:22px; color:#fff; }}
  .score-box {{ background:linear-gradient(160deg,#E85555,#c73333); border-radius:16px; padding:18px 28px; margin:0 10px; }}
  .score {{ font-family:'Lilita One',cursive; font-size:52px; color:#fff; line-height:1; white-space:nowrap; }}
  .fpl-note {{ margin-top:24px; font-size:14px; color:rgba(255,255,255,0.6); text-align:center; }}
  .logo {{ position:absolute; bottom:14px; left:16px; width:48px; height:48px; object-fit:contain; z-index:20; filter:brightness(0) invert(1); opacity:0.9; }}
</style>
</head>
<body>
<div class="card">
  <div class="header"><span class="badge">FULL TIME ⏱</span></div>
  <div class="teams-row">
    <div class="team"><div class="team-name">{home_team}</div></div>
    <div class="score-box"><div class="score">{home_score} - {away_score}</div></div>
    <div class="team"><div class="team-name">{away_team}</div></div>
  </div>
  <div class="fpl-note">🎯 احسب نقاط الفانتازي دلوقتي</div>
  {logo_html}
</div>
</body>
</html>"""
