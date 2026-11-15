"""
Fantasy Volt Card Generation Engine
Generates 1080x1080 social media cards adhering to Fantasy Volt's signature visual identity:
1. Yellow Card (الإنذار)
2. Goal & Assist (الهدف والأسيست)
3. Bonus Points (نقاط البونص)
4. Full-Time (نهاية المباراة)
5. Daily Price Changes (تغيرات الأسعار)
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Font loaders with fallbacks
def get_arabic_font(size, bold=True):
    candidates = [
        "C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def get_latin_font(size, bold=True):
    candidates = [
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        os.path.join(FONTS_DIR, "Almarai-ExtraBold.ttf")
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def ar(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def draw_lightning_bolts(draw, width, height, color=(255, 255, 255, 25)):
    """Draw subtle lightning streaks in the background"""
    bolts = [
        [(150, 0), (120, 250), (190, 270), (100, 550)],
        [(width - 200, 0), (width - 150, 200), (width - 230, 240), (width - 120, 600)],
        [(50, height - 400), (120, height - 250), (80, height - 220), (140, height)],
        [(width - 100, height - 450), (width - 160, height - 300), (width - 110, height - 260), (width - 180, height)]
    ]
    for pts in bolts:
        draw.line(pts, fill=color, width=4)

def draw_text_with_glow(img, xy, text, font, fill_color, glow_color, glow_radius=12, stroke_width=0, stroke_fill=None):
    """Draw text with a soft radial glow bloom behind it"""
    width, height = img.size
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    
    # Draw text on glow layer
    glow_draw.text(xy, text, font=font, fill=glow_color, stroke_width=stroke_width + 4, stroke_fill=glow_color)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(glow_radius))
    
    # Composite glow onto base
    img.alpha_composite(glow_layer)
    
    # Draw crisp text on top
    draw = ImageDraw.Draw(img)
    draw.text(xy, text, font=font, fill=fill_color, stroke_width=stroke_width, stroke_fill=stroke_fill)


# ==============================================================================
# 1. YELLOW CARD TEMPLATE (كارت الإنذار)
# ==============================================================================
def render_yellow_card(player_name, team_name=None, minute=None, output_path=None):
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height), "#D32F2F")
    draw = ImageDraw.Draw(img)
    
    # Red gradient / vignette
    for y in range(height):
        ratio = y / height
        r = int(220 - 70 * ratio)
        g = int(45 - 25 * ratio)
        b = int(50 - 25 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    draw_lightning_bolts(draw, width, height, color=(255, 80, 80, 40))
    
    # 1. Top Headline "YELLOW CARD"
    font_hl = get_latin_font(95, bold=True)
    draw_text_with_glow(img, (width // 2, 70), "YELLOW", font_hl, fill_color="#FFE57F", glow_color="#FFA000", glow_radius=15, stroke_width=3, stroke_fill="#8A1E24")
    draw_text_with_glow(img, (width // 2, 175), "CARD", font_hl, fill_color="#FFE57F", glow_color="#FFA000", glow_radius=15, stroke_width=3, stroke_fill="#8A1E24")
    
    # Center text bounding box correction
    # 2. Main Yellow Card
    card_w, card_h = 620, 780
    card_x1 = (width - card_w) // 2
    card_y1 = 300
    card_x2 = card_x1 + card_w
    card_y2 = card_y1 + card_h
    
    # Card shadow
    draw.rounded_rectangle([card_x1 + 15, card_y1 + 15, card_x2 + 15, card_y2 + 15], radius=50, fill=(40, 5, 5, 120))
    # Card body
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=50, fill="#FFC400")
    
    # Diagonal card facet shadow
    facet_poly = [(card_x1 + 250, card_y2), (card_x2, card_y1 + 350), (card_x2, card_y2)]
    draw.polygon(facet_poly, fill="#E6A800")
    
    # 3. Lion silhouette inside top of yellow card
    lion_path = os.path.join(ASSETS_DIR, "pl_lion_600.png")
    if os.path.exists(lion_path):
        lion = Image.open(lion_path).convert("RGBA")
        lion = lion.resize((150, 150), Image.Resampling.LANCZOS)
        # Tint lion to dark bronze/gold #6A4E00
        r, g, b, a = lion.split()
        tint = Image.new("RGBA", lion.size, "#6A4E00")
        lion_tinted = Image.composite(tint, Image.new("RGBA", lion.size, (0,0,0,0)), a)
        img.alpha_composite(lion_tinted, ((width - 150) // 2, card_y1 + 45))
        
    # Micro text in lion
    font_micro = get_latin_font(18, bold=True)
    draw.text((width // 2, card_y1 + 205), "FANTASY VOLT", font=font_micro, fill="#785600", anchor="mm")
    
    # 4. Arabic Player Name (Sticker style: Coral Red fill with dark maroon stroke)
    font_name = get_arabic_font(85, bold=True)
    ar_name = ar(player_name)
    draw.text((width // 2, card_y1 + 330), ar_name, font=font_name, fill="#EF4145", stroke_width=5, stroke_fill="#30080C", anchor="mm")
    
    # 5. Optional details (Team name or minute)
    if team_name or minute:
        detail_text = []
        if team_name:
            detail_text.append(str(team_name))
        if minute:
            detail_text.append(f"الدقيقة {minute}'")
        font_sub = get_arabic_font(34, bold=True)
        sub_str = ar(" • ".join(detail_text))
        draw.text((width // 2, card_y1 + 430), sub_str, font=font_sub, fill="#4A3200", anchor="mm")
        
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"yellow_card_{player_name}.png")
        
    img.save(output_path)
    return output_path


# ==============================================================================
# 2. GOAL & ASSIST TEMPLATE (الهدف والأسيست)
# ==============================================================================
def render_goal_assist(goal_scorer, assist_provider, minute=None, output_path=None):
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    
    # Top 50% Teal (#007B8A)
    draw.rectangle([0, 0, width, height // 2], fill="#007B8A")
    # Bottom 50% Coral (#EF4145)
    draw.rectangle([0, height // 2, width, height], fill="#EF4145")
    
    # Lightning accents
    draw_lightning_bolts(draw, width, height, color=(255, 255, 255, 25))
    
    # Dividing Seam
    draw.line([(0, height // 2), (width, height // 2)], fill="#0D1117", width=6)
    
    # 1. Top Section: "GOAL" + Scorer
    font_action = get_latin_font(105, bold=True)
    draw_text_with_glow(img, (width // 2, 70), "GOAL", font_action, fill_color="#FFFFFF", glow_color="#67E8F9", glow_radius=18, stroke_width=3, stroke_fill="#004D56")
    
    # Arabic Scorer Name: Coral Red fill with clean charcoal stroke
    font_player = get_arabic_font(85, bold=True)
    draw.text((width // 2, 260), ar(goal_scorer), font=font_player, fill="#EF4145", stroke_width=5, stroke_fill="#1A1D20", anchor="mm")
    
    # 2. Bottom Section: "ASSIST" + Provider
    draw_text_with_glow(img, (width // 2, height // 2 + 65), "ASSIST", font_action, fill_color="#FFFFFF", glow_color="#FDA4AF", glow_radius=18, stroke_width=3, stroke_fill="#8B1E22")
    
    # Arabic Assist Name: Teal fill with clean charcoal stroke
    assist_txt = assist_provider if assist_provider else "بدون صناعة"
    draw.text((width // 2, height // 2 + 255), ar(assist_txt), font=font_player, fill="#007B8A", stroke_width=5, stroke_fill="#1A1D20", anchor="mm")
    
    # 3. Center Lion Logo
    lion_path = os.path.join(ASSETS_DIR, "pl_lion_600.png")
    if os.path.exists(lion_path):
        lion = Image.open(lion_path).convert("RGBA")
        lion = lion.resize((150, 150), Image.Resampling.LANCZOS)
        # White & Gold lion silhouette for maximum contrast
        r, g, b, a = lion.split()
        white_lion = Image.composite(Image.new("RGBA", lion.size, "#FFFFFF"), Image.new("RGBA", lion.size, (0,0,0,0)), a)
        
        # Center circle backplate
        center_x, center_y = width // 2, height // 2
        draw.ellipse([center_x - 95, center_y - 95, center_x + 95, center_y + 95], fill="#0A0D10", outline="#00E5FF", width=4)
        img.alpha_composite(white_lion, (center_x - 75, center_y - 75))
        
    if minute:
        font_min = get_arabic_font(32, bold=True)
        draw.text((width // 2, height - 50), ar(f"الدقيقة {minute}'"), font=font_min, fill="#FFFFFF", stroke_width=3, stroke_fill="#1A1D20", anchor="mm")
        
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"goal_assist_{goal_scorer}.png")
        
    img.save(output_path)
    return output_path


# ==============================================================================
# 3. BONUS POINTS TEMPLATE (نقاط البونص)
# ==============================================================================
def render_bonus(bonus_list, output_path=None):
    """
    bonus_list: list of tuples -> [("سيمينيو", 3), ("إيكيتيكي", 2), ("بالمر", 1)]
    """
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height), "#007B8A")
    draw = ImageDraw.Draw(img)
    
    # Gradient overlay
    for y in range(height):
        ratio = y / height
        r = int(0 + 15 * ratio)
        g = int(123 - 35 * ratio)
        b = int(138 - 35 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    draw_lightning_bolts(draw, width, height, color=(255, 255, 255, 20))
    
    # 1. Branding Header
    font_brand = get_latin_font(36, bold=True)
    draw.text((width // 2, 70), "FANTASY VOLT", font=font_brand, fill="#67E8F9", anchor="mm")
    
    # 2. Main Title: "BONUS"
    font_title = get_latin_font(95, bold=True)
    draw_text_with_glow(img, (width // 2, 150), "BONUS", font_title, fill_color="#EF4145", glow_color="#FDA4AF", glow_radius=14, stroke_width=4, stroke_fill="#1A1D20")
    
    # 3. Bonus Rows
    y_start = 320
    font_num = get_latin_font(110, bold=True)
    font_name = get_arabic_font(75, bold=True)
    
    for i, (name, pts) in enumerate(bonus_list[:3]):
        row_y = y_start + i * 190
        # Background pill
        draw.rounded_rectangle([100, row_y, width - 100, row_y + 140], radius=30, fill=(0, 60, 70, 180), outline="#00A3B5", width=2)
        
        # Player Arabic Name (Right aligned for RTL reading)
        ar_name = ar(name)
        draw.text((width - 180, row_y + 70), ar_name, font=font_name, fill="#EF4145", stroke_width=5, stroke_fill="#1A1D20", anchor="ra")
        
        # Points Number + Label (Left aligned)
        pts_str = f"+{pts}"
        draw.text((180, row_y + 70), pts_str, font=font_num, fill="#FFFFFF", stroke_width=7, stroke_fill="#1A1D20", anchor="la")
        
    # Footer (clean without unsupported emoji)
    font_foot = get_arabic_font(30, bold=True)
    draw.text((width // 2, height - 70), ar("نقاط البونص الرسمية • فانتازي الدوري الإنجليزي"), font=font_foot, fill="#67E8F9", anchor="mm")
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, "bonus_points.png")
        
    img.save(output_path)
    return output_path


# ==============================================================================
# 4. FULL-TIME SCORE TEMPLATE (نهاية المباراة)
# ==============================================================================
def render_fulltime(home_team, away_team, home_score, away_score, output_path=None):
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    
    # Split quadrants (Checkerboard: Teal / Coral)
    half_w, half_h = width // 2, height // 2
    draw.rectangle([0, 0, half_w, height], fill="#007B8A")
    draw.rectangle([half_w, 0, width, height], fill="#EF4145")
    
    draw_lightning_bolts(draw, width, height, color=(255, 255, 255, 25))
    
    # Center dividing line
    draw.line([(half_w, 0), (half_w, height)], fill="#1A1D20", width=6)
    
    # 1. Header
    font_brand = get_latin_font(34, bold=True)
    draw.text((width // 2, 60), "FANTASY VOLT", font=font_brand, fill="#FFFFFF", stroke_width=4, stroke_fill="#1A1D20", anchor="mm")
    
    font_ft = get_latin_font(85, bold=True)
    draw.text((width // 2, 140), "FULL-TIME", font=font_ft, fill="#FFFFFF", stroke_width=6, stroke_fill="#1A1D20", anchor="mm")
    
    # 2. Team Names in Arabic
    font_team = get_arabic_font(60, bold=True)
    draw.text((half_w // 2, 380), ar(home_team), font=font_team, fill="#FFFFFF", stroke_width=8, stroke_fill="#1A1D20", anchor="mm")
    draw.text((half_w + half_w // 2, 380), ar(away_team), font=font_team, fill="#FFFFFF", stroke_width=8, stroke_fill="#1A1D20", anchor="mm")
    
    # 3. Scores
    font_score = get_latin_font(180, bold=True)
    draw.text((half_w // 2, 680), str(home_score), font=font_score, fill="#FFFFFF", stroke_width=12, stroke_fill="#1A1D20", anchor="mm")
    draw.text((half_w + half_w // 2, 680), str(away_score), font=font_score, fill="#FFFFFF", stroke_width=12, stroke_fill="#1A1D20", anchor="mm")
    
    # Footer
    font_foot = get_arabic_font(32, bold=True)
    draw.text((width // 2, height - 70), ar("صافرة النهاية ⚡"), font=font_foot, fill="#FFFFFF", stroke_width=5, stroke_fill="#1A1D20", anchor="mm")
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, f"fulltime_{home_score}_{away_score}.png")
        
    img.save(output_path)
    return output_path


# ==============================================================================
# 5. DAILY PRICE CHANGES TEMPLATE (تغيرات الأسعار)
# ==============================================================================
def render_price_changes(rising, falling, date_str=None, output_path=None):
    """
    rising: [ (name, team, price, change, ownership), ... ]
    falling: [ (name, team, price, change, ownership), ... ]
    """
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)
    
    # Subtle gradient background
    for y in range(height):
        alpha = int(25 * (y / height))
        draw.line([(0, y), (width, y)], fill=(13 + alpha//2, 17 + alpha, 23 + alpha//2))
        
    margin = 40
    card_box = [margin, margin, width - margin, height - margin]
    draw.rounded_rectangle(card_box, radius=35, fill="#161b22", outline="#00ff88", width=3)
    
    font_title = get_arabic_font(42, bold=True)
    font_sub = get_arabic_font(26, bold=False)
    font_bold = get_arabic_font(32, bold=True)
    font_small = get_arabic_font(22, bold=False)
    
    # Header
    draw.text((width - 80, 75), ar("FANTASY VOLT | فانتازي ڤولت"), font=font_title, fill="#00ff88", anchor="ra")
    sub_title = f"نشرة تغيرات أسعار الفانتازي ({date_str})" if date_str else "نشرة تغيرات أسعار الفانتازي الرسمية"
    draw.text((width - 80, 130), ar(sub_title), font=font_sub, fill="#8b949e", anchor="ra")
    draw.line([(80, 175), (width - 80, 175)], fill="#30363d", width=2)
    
    # Rising Section (Top 3)
    draw.text((width - 80, 195), ar("الأكثر ارتفاعا في السعر"), font=font_bold, fill="#3fb950", anchor="ra")
    y_pos = 245
    for name, team, price, change, own in rising[:3]:
        draw.rounded_rectangle([80, y_pos, width - 80, y_pos + 85], radius=16, fill="#21262d")
        draw.text((110, y_pos + 26), f"{change}  |  {price}", font=font_bold, fill="#3fb950")
        draw.text((width - 110, y_pos + 14), ar(name), font=font_bold, fill="#ffffff", anchor="ra")
        draw.text((width - 110, y_pos + 48), ar(f"{team}  •  ملكية: {own}"), font=font_small, fill="#8b949e", anchor="ra")
        y_pos += 98
        
    # Falling Section (Top 3)
    y_pos += 15
    draw.text((width - 80, y_pos), ar("الأكثر انخفاضا في السعر"), font=font_bold, fill="#f85149", anchor="ra")
    y_pos += 50
    for name, team, price, change, own in falling[:3]:
        draw.rounded_rectangle([80, y_pos, width - 80, y_pos + 85], radius=16, fill="#21262d")
        draw.text((110, y_pos + 26), f"{change}  |  {price}", font=font_bold, fill="#f85149")
        draw.text((width - 110, y_pos + 14), ar(name), font=font_bold, fill="#ffffff", anchor="ra")
        draw.text((width - 110, y_pos + 48), ar(f"{team}  •  ملكية: {own}"), font=font_small, fill="#8b949e", anchor="ra")
        y_pos += 98
        
    # Footer
    draw.line([(80, height - 100), (width - 80, height - 100)], fill="#30363d", width=2)
    draw.text((width // 2, height - 60), ar("لو مش متابع ڤولت.. بتلعب فانتازي غلط"), font=font_bold, fill="#00ff88", anchor="mm")
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, "price_changes.png")
        
    img.save(output_path)
    return output_path

# ==============================================================================
# 6. TODAY'S FIXTURES TEMPLATE (مباريات اليوم) - Kora Volt
# ==============================================================================
def render_today_fixtures(matches, date_str=None, output_path=None):
    """
    matches: [
        {"home": "ليفربول", "away": "مانشستر سيتي", "time": "6:30 م", "comp": "الدوري الإنجليزي"},
        {"home": "ريال مدريد", "away": "برشلونة", "time": "9:00 م", "comp": "الدوري الإسباني"}, ...
    ]
    """
    width, height = 1080, 1080
    img = Image.new("RGBA", (width, height), "#0B0E14")
    draw = ImageDraw.Draw(img)
    
    # Gradient overlay
    for y in range(height):
        alpha = int(30 * (y / height))
        draw.line([(0, y), (width, y)], fill=(11 + alpha//2, 14 + alpha, 20 + alpha//2))
        
    draw_lightning_bolts(draw, width, height, color=(0, 229, 255, 20))
    
    # Outer Container
    margin = 40
    card_box = [margin, margin, width - margin, height - margin]
    draw.rounded_rectangle(card_box, radius=35, fill="#131923", outline="#00E5FF", width=3)
    
    font_brand = get_arabic_font(42, bold=True)
    font_sub = get_arabic_font(26, bold=False)
    font_team = get_arabic_font(34, bold=True)
    font_meta = get_arabic_font(22, bold=False)
    font_time = get_latin_font(32, bold=True)
    
    # Header
    draw.text((width - 80, 75), ar("KORA VOLT | كورة ڤولت"), font=font_brand, fill="#00E5FF", anchor="ra")
    sub_title = f"جدول أهم مباريات اليوم ({date_str}) • بتوقيت القاهرة" if date_str else "جدول أهم مباريات اليوم • بتوقيت القاهرة"
    draw.text((width - 80, 130), ar(sub_title), font=font_sub, fill="#8B949E", anchor="ra")
    draw.line([(80, 175), (width - 80, 175)], fill="#30363D", width=2)
    
    # Matches Rows (up to 4 matches)
    y_pos = 210
    row_h = 150
    for m in matches[:4]:
        # Row card
        draw.rounded_rectangle([75, y_pos, width - 75, y_pos + row_h], radius=20, fill="#1B2332", outline="#253247", width=2)
        
        # Competition tag pill
        comp_txt = ar(m.get("comp", "مباراة ودية"))
        draw.rounded_rectangle([width - 320, y_pos + 15, width - 100, y_pos + 48], radius=10, fill="#0D1117")
        draw.text((width - 210, y_pos + 31), comp_txt, font=font_meta, fill="#00E5FF", anchor="mm")
        
        # Home Team vs Away Team (Centered in row)
        home_name = ar(m.get("home", "المستضيف"))
        away_name = ar(m.get("away", "الضيف"))
        
        draw.text((width - 120, y_pos + 90), home_name, font=font_team, fill="#FFFFFF", anchor="ra")
        draw.text((width // 2, y_pos + 90), ar("VS"), font=font_time, fill="#EF4145", stroke_width=2, stroke_fill="#1A1D20", anchor="mm")
        draw.text((120, y_pos + 90), away_name, font=font_team, fill="#FFFFFF", anchor="la")
        
        # Kickoff Time badge (Left corner)
        time_txt = ar(f"{m.get('time', '9:00 م')}")
        draw.text((200, y_pos + 31), time_txt, font=font_meta, fill="#67E8F9", anchor="mm")
        
        y_pos += row_h + 25
        
    # Footer
    draw.line([(80, height - 105), (width - 80, height - 105)], fill="#30363D", width=2)
    font_foot = get_arabic_font(28, bold=True)
    draw.text((width // 2, height - 60), ar("توقعاتك إيه لقمة الليلة؟ شاركنا في التعليقات"), font=font_foot, fill="#00E5FF", anchor="mm")
    
    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, "today_fixtures.png")
        
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    print("Testing all 5 card templates...")
    p1 = render_yellow_card("كيركيز", "بورنموث", 42)
    print("Yellow Card:", p1)
    p2 = render_goal_assist("رايندرز", "أوسكار بوب", 34)
    print("Goal & Assist:", p2)
    p3 = render_bonus([("سيمينيو", 3), ("إيكيتيكي", 2), ("كول بالمر", 1)])
    print("Bonus Card:", p3)
    p4 = render_fulltime("بورنموث", "ليفربول", 2, 4)
    print("Full-Time Card:", p4)
    p5 = render_price_changes(
        [("كول بالمر", "تشيلسي", "£11.1m", "+£0.1m", "48.2%"), ("مبيومو", "برينتفورد", "£7.8m", "+£0.1m", "39.4%")],
        [("بوكايو ساكا", "أرسنال", "£10.0m", "-£0.1m", "31.5%"), ("إيزي", "كريستال بالاس", "£6.6m", "-£0.1m", "14.2%")]
    )
    print("Price Card:", p5)
    print("ALL 5 TEMPLATES GENERATED SUCCESSFULLY!")
