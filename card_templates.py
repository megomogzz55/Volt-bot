"""
card_templates.py
HTML templates للكروت بستايل Fantasy Volt
بيتحول لصور بـ Playwright
"""

BASE_FONTS = """
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@900&family=Tajawal:wght@900&display=swap');
"""

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 960px; height: 1200px; overflow: hidden; font-family: 'Tajawal', 'Cairo', sans-serif; }

.card {
  width: 960px;
  height: 1200px;
  position: relative;
  overflow: hidden;
}

/* خلفية البرق */
.lightning-bg {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='110' height='130'%3E%3Cpolygon points='36,0 12,32 26,32 0,72 40,28 24,28' fill='rgba(0,0,0,0.12)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  pointer-events: none;
}

.outlined {
  -webkit-text-stroke: 10px black;
  paint-order: stroke fill;
}

.glow {
  text-shadow:
    0 0 20px currentColor,
    0 0 40px currentColor,
    0 0 60px rgba(255,255,255,0.4);
}
"""

# ══════════════════════════════════════════════════════════
# GOAL + ASSIST
# ══════════════════════════════════════════════════════════
def goal_template(scorer_name, assist_name=None):
    assist_html = f"""
      <div class="assist-name outlined">{assist_name}</div>
    """ if assist_name else """
      <div class="no-assist">—</div>
    """

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}

.card {{
  display: flex;
  flex-direction: column;
}}

.top {{
  flex: 1;
  background: #00AFCC;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 20px;
}}

.bot {{
  flex: 1;
  background: #E85555;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 20px;
}}

.goal-text {{
  font-size: 200px;
  font-weight: 900;
  color: white;
  letter-spacing: -4px;
  line-height: 1;
  font-family: 'Arial Black', sans-serif;
  -webkit-text-stroke: 6px white;
  text-shadow:
    0 0 30px rgba(255,255,255,0.8),
    0 0 60px rgba(255,255,255,0.4);
}}

.scorer-name {{
  font-size: 115px;
  font-weight: 900;
  color: #E85555;
  -webkit-text-stroke: 9px black;
  paint-order: stroke fill;
  text-align: center;
  line-height: 1.1;
  margin-top: 10px;
}}

.logo-center {{
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 180px;
  height: 180px;
  z-index: 10;
}}

.logo-center img {{
  width: 100%;
  height: 100%;
  object-fit: contain;
}}

.assist-text {{
  font-size: 160px;
  font-weight: 900;
  color: white;
  letter-spacing: -3px;
  line-height: 1;
  font-family: 'Arial Black', sans-serif;
  -webkit-text-stroke: 5px white;
  text-shadow:
    0 0 30px rgba(255,255,255,0.8),
    0 0 60px rgba(255,255,255,0.4);
}}

.assist-name {{
  font-size: 110px;
  font-weight: 900;
  color: #00AFCC;
  -webkit-text-stroke: 9px black;
  paint-order: stroke fill;
  text-align: center;
  line-height: 1.1;
  margin-top: 10px;
}}

.no-assist {{
  font-size: 100px;
  color: rgba(255,255,255,0.3);
}}
</style>
</head>
<body>
<div class="card">
  <div class="top">
    <div class="lightning-bg"></div>
    <div class="goal-text">GOAL</div>
    <div class="scorer-name">{scorer_name}</div>
  </div>

  <!-- اللوجو في المنتصف -->
  <div class="logo-center">
    <img src="logo.png" alt="Fantasy Volt">
  </div>

  <div class="bot">
    <div class="lightning-bg"></div>
    <div class="assist-text">ASSIST</div>
    {assist_html}
  </div>
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# YELLOW CARD
# ══════════════════════════════════════════════════════════
def yellow_card_template(player_name):
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}

.card {{
  background: radial-gradient(ellipse at center, #cc3333 0%, #991111 100%);
}}

.yellow-title {{
  position: absolute;
  top: 60px;
  width: 100%;
  text-align: center;
  font-size: 175px;
  font-weight: 900;
  color: #F5C518;
  font-family: 'Arial Black', sans-serif;
  -webkit-text-stroke: 6px #8a6a00;
  paint-order: stroke fill;
  text-shadow: 0 0 40px rgba(245,197,24,0.6);
  line-height: 0.95;
}}

.yellow-card-rect {{
  position: absolute;
  top: 420px;
  left: 50%;
  transform: translateX(-50%);
  width: 340px;
  height: 440px;
  background: #F5C518;
  border-radius: 32px;
  border: 5px solid #c9a200;
  overflow: hidden;
  box-shadow: 8px 8px 30px rgba(0,0,0,0.4);
}}

.card-shadow {{
  position: absolute;
  top: 0; right: 0;
  width: 50%;
  height: 100%;
  background: rgba(0,0,0,0.12);
}}

.card-logo {{
  position: absolute;
  top: 18px;
  left: 50%;
  transform: translateX(-50%);
  width: 115px;
  height: 115px;
  object-fit: contain;
}}

.player-on-card {{
  position: absolute;
  bottom: 120px;
  width: 100%;
  text-align: center;
  font-size: 82px;
  font-weight: 900;
  color: #D83355;
  -webkit-text-stroke: 6px #6a0010;
  paint-order: stroke fill;
}}

.minus-pts {{
  position: absolute;
  bottom: 20px;
  width: 100%;
  text-align: center;
  font-size: 52px;
  font-weight: 900;
  color: #D83355;
  -webkit-text-stroke: 4px #6a0010;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
  line-height: 1;
}}
</style>
</head>
<body>
<div class="card">
  <div class="lightning-bg" style="opacity:0.6"></div>
  <div class="yellow-title">YELLOW<br>CARD</div>
  <div class="yellow-card-rect">
    <div class="card-shadow"></div>
    <img class="card-logo" src="logo.png">
    <div class="player-on-card">{player_name}</div>
    <div class="minus-pts">-1<br>POINTS</div>
  </div>
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# BONUS
# ══════════════════════════════════════════════════════════
def bonus_template(players):
    rows = ""
    for p in players[:3]:
        rows += f"""
        <div class="bonus-row">
          <span class="bonus-num">{p.get('points','')}</span>
          <span class="bonus-pname">{p.get('name','')}</span>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}

.card {{
  background: #00AFCC;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 30px;
}}

.logo-top {{
  width: 155px;
  height: 155px;
  object-fit: contain;
  margin-bottom: 10px;
}}

.bonus-title {{
  font-size: 175px;
  font-weight: 900;
  color: #E85555;
  -webkit-text-stroke: 11px black;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
  line-height: 1;
  margin-bottom: 20px;
}}

.bonus-row {{
  display: flex;
  align-items: center;
  gap: 40px;
  margin: 10px 0;
  width: 100%;
  padding: 0 80px;
}}

.bonus-num {{
  font-size: 145px;
  font-weight: 900;
  color: #E85555;
  -webkit-text-stroke: 10px black;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
  min-width: 120px;
  line-height: 1;
}}

.bonus-pname {{
  font-size: 105px;
  font-weight: 900;
  color: #E85555;
  -webkit-text-stroke: 9px black;
  paint-order: stroke fill;
  line-height: 1;
}}
</style>
</head>
<body>
<div class="card">
  <div class="lightning-bg"></div>
  <img class="logo-top" src="logo.png">
  <div class="bonus-title">BONUS</div>
  {rows}
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# FULL TIME
# ══════════════════════════════════════════════════════════
def fulltime_template(home_team, away_team, home_score, away_score,
                      home_logo_url=None, away_logo_url=None):
    home_img = f'<img src="{home_logo_url}" onerror="this.style.display=\'none\'">' if home_logo_url else ""
    away_img = f'<img src="{away_logo_url}" onerror="this.style.display=\'none\'">' if away_logo_url else ""

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}

.card {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}}

.q1 {{ background: #E85555; }}
.q2 {{ background: #00AFCC; }}
.q3 {{ background: #00AFCC; }}
.q4 {{ background: #E85555; }}

.quadrant {{
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}}

.quadrant img {{
  max-width: 210px;
  max-height: 210px;
  object-fit: contain;
}}

.score-num {{
  font-size: 300px;
  font-weight: 900;
  color: white;
  -webkit-text-stroke: 14px black;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
  line-height: 1;
}}

/* اللوجو + FULL TIME فوق */
.header {{
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 25px;
  z-index: 20;
  pointer-events: none;
  grid-column: 1 / 3;
}}

.ft-logo {{
  width: 150px;
  height: 150px;
  object-fit: contain;
}}

.ft-text-wrap {{
  background: white;
  padding: 8px 40px;
  border-radius: 6px;
  margin-top: 8px;
}}

.ft-text {{
  font-size: 105px;
  font-weight: 900;
  color: black;
  font-family: 'Arial Black', sans-serif;
  letter-spacing: -2px;
  line-height: 1;
}}
</style>
</head>
<body>
<div class="card">
  <div class="quadrant q1">
    <div class="lightning-bg"></div>
    {home_img}
  </div>
  <div class="quadrant q2">
    <div class="lightning-bg"></div>
    {away_img}
  </div>
  <div class="quadrant q3">
    <div class="score-num">{home_score}</div>
  </div>
  <div class="quadrant q4">
    <div class="score-num">{away_score}</div>
  </div>

  <!-- header overlay -->
  <div style="position:absolute;top:0;left:0;width:100%;display:flex;flex-direction:column;align-items:center;padding-top:22px;z-index:20">
    <img style="width:148px;height:148px;object-fit:contain" src="logo.png">
    <div style="background:white;padding:7px 38px;border-radius:5px;margin-top:6px">
      <div style="font-size:100px;font-weight:900;color:black;font-family:'Arial Black',sans-serif;line-height:1">FULL-TIME</div>
    </div>
  </div>
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# تغيير السعر
# ══════════════════════════════════════════════════════════
def price_template(player_name, old_price, new_price):
    rising = new_price > old_price
    top_bg = "#00AFCC" if rising else "#991111"
    label  = "ارتفع السعر!" if rising else "انخفض السعر!"
    arrow  = "▲" if rising else "▼"
    diff   = abs(new_price - old_price)
    arrow_color = "#32E664" if rising else "#FF5050"

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}

.card {{ display: flex; flex-direction: column; }}

.top {{
  flex: 1;
  background: {top_bg};
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 30px;
  gap: 15px;
}}

.bot {{
  flex: 1;
  background: #E85555;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 30px;
  gap: 15px;
}}

.label {{
  font-size: 88px;
  font-weight: 900;
  color: #F5C518;
  -webkit-text-stroke: 7px black;
  paint-order: stroke fill;
}}

.pname {{
  font-size: 118px;
  font-weight: 900;
  color: white;
  -webkit-text-stroke: 9px black;
  paint-order: stroke fill;
  text-align: center;
}}

.prices {{
  font-size: 85px;
  font-weight: 900;
  color: #F5C518;
  -webkit-text-stroke: 6px black;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
}}

.logo-center {{
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 165px; height: 165px;
  z-index: 10;
}}

.logo-center img {{ width: 100%; height: 100%; object-fit: contain; }}

.arrow {{
  font-size: 155px;
  font-weight: 900;
  color: {arrow_color};
  -webkit-text-stroke: 10px black;
  paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
}}

.cta {{
  font-size: 85px;
  font-weight: 900;
  color: white;
  -webkit-text-stroke: 6px black;
  paint-order: stroke fill;
}}

.hashtags {{
  font-size: 68px;
  font-weight: 900;
  color: #F5C518;
  -webkit-text-stroke: 5px black;
  paint-order: stroke fill;
}}
</style>
</head>
<body>
<div class="card">
  <div class="top">
    <div class="lightning-bg"></div>
    <div class="label">{label}</div>
    <div class="pname">{player_name}</div>
    <div class="prices">£{old_price}m → £{new_price}m</div>
  </div>

  <div class="logo-center"><img src="logo.png"></div>

  <div class="bot">
    <div class="lightning-bg"></div>
    <div class="arrow">{arrow} {diff:.1f}m</div>
    <div class="cta">{"اشتريته؟" if rising else "بعته؟"}</div>
    <div class="hashtags">#فانتازي #FPL</div>
  </div>
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# الكابتن
# ══════════════════════════════════════════════════════════
def captain_template(player_name, price, form, ownership, fixture):
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}
.card {{ display: flex; flex-direction: column; }}
.top {{
  flex: 1; background: #00AFCC;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; padding: 25px; gap: 12px;
}}
.bot {{
  flex: 1; background: #E85555;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; padding: 25px; gap: 18px;
}}
.logo-center {{
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 165px; height: 165px; z-index: 10;
}}
.logo-center img {{ width: 100%; height: 100%; object-fit: contain; }}
.cap-title {{
  font-size: 170px; font-weight: 900;
  color: #F5C518; font-family: 'Arial Black', sans-serif;
  -webkit-text-stroke: 9px black; paint-order: stroke fill;
  line-height: 1;
}}
.cap-name {{
  font-size: 108px; font-weight: 900;
  color: white; -webkit-text-stroke: 9px black; paint-order: stroke fill;
  text-align: center;
}}
.cap-price {{
  font-size: 85px; font-weight: 900;
  color: #F5C518; -webkit-text-stroke: 6px black; paint-order: stroke fill;
  font-family: 'Arial Black', sans-serif;
}}
.stat {{
  font-size: 78px; font-weight: 900;
  color: white; -webkit-text-stroke: 5px black; paint-order: stroke fill;
}}
.fixture {{
  font-size: 75px; font-weight: 900;
  color: #F5C518; -webkit-text-stroke: 5px black; paint-order: stroke fill;
  text-align: center;
}}
.cta {{
  font-size: 95px; font-weight: 900;
  color: white; -webkit-text-stroke: 7px black; paint-order: stroke fill;
}}
</style></head><body>
<div class="card">
  <div class="top">
    <div class="lightning-bg"></div>
    <div class="cap-title">CAPTAIN</div>
    <div class="cap-name">{player_name}</div>
    <div class="cap-price">£{price}m</div>
  </div>
  <div class="logo-center"><img src="logo.png"></div>
  <div class="bot">
    <div class="lightning-bg"></div>
    <div class="stat">فورم: {form} | ملكية: {ownership}%</div>
    <div class="fixture">{fixture}</div>
    <div class="cta">موافق؟ 👇</div>
  </div>
</div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# الإصابة
# ══════════════════════════════════════════════════════════
def injury_template(player_name, chance, news):
    status = "غايب 🔴" if chance == 0 else f"{chance}% يلعب 🟡"
    status_color = "#FF5050" if chance == 0 else "#F5C518"

    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<style>
{BASE_FONTS}
{BASE_CSS}
.card {{ display: flex; flex-direction: column; }}
.top {{
  flex: 1; background: #991111;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; padding: 25px; gap: 12px;
}}
.bot {{
  flex: 1; background: #E85555;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  position: relative; padding: 25px; gap: 18px;
}}
.logo-center {{
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 155px; height: 155px; z-index: 10;
}}
.logo-center img {{ width: 100%; height: 100%; object-fit: contain; }}
.inj-title {{
  font-size: 155px; font-weight: 900;
  color: #FF5050; font-family: 'Arial Black', sans-serif;
  -webkit-text-stroke: 8px white; paint-order: stroke fill;
  text-shadow: 0 0 40px rgba(255,80,80,0.7);
}}
.inj-sub {{
  font-size: 90px; font-weight: 900;
  color: white; -webkit-text-stroke: 7px black; paint-order: stroke fill;
}}
.inj-name {{
  font-size: 125px; font-weight: 900;
  color: white; -webkit-text-stroke: 10px black; paint-order: stroke fill;
  text-align: center;
}}
.status {{
  font-size: 88px; font-weight: 900;
  color: {status_color}; -webkit-text-stroke: 6px black; paint-order: stroke fill;
}}
.news-text {{
  font-size: 72px; font-weight: 900;
  color: white; -webkit-text-stroke: 5px black; paint-order: stroke fill;
  text-align: center; line-height: 1.3;
}}
.cta {{
  font-size: 88px; font-weight: 900;
  color: white; -webkit-text-stroke: 6px black; paint-order: stroke fill;
}}
</style></head><body>
<div class="card">
  <div class="top">
    <div class="lightning-bg"></div>
    <div class="inj-title">INJURY</div>
    <div class="inj-sub">تحذير إصابة</div>
    <div class="inj-name">{player_name}</div>
    <div class="status">{status}</div>
  </div>
  <div class="logo-center"><img src="logo.png"></div>
  <div class="bot">
    <div class="lightning-bg"></div>
    <div class="news-text">{news}</div>
    <div class="cta">فكّر في بديل 🤔</div>
  </div>
</div>
</body></html>"""
