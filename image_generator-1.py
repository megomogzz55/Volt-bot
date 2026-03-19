"""
image_generator.py
بيولّد صور الكروت من HTML templates بـ Playwright
"""

import os
import tempfile
from pathlib import Path
from card_templates import (
    goal_template, yellow_card_template, bonus_template,
    fulltime_template, price_template, captain_template, injury_template
)

BASE_DIR  = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"


def html_to_image(html_content, output_path, width=960, height=1200):
    """حوّل HTML لصورة بـ Playwright"""
    try:
        from playwright.sync_api import sync_playwright

        with tempfile.NamedTemporaryFile(suffix=".html", mode="w",
                                         encoding="utf-8", delete=False) as f:
            html = html_content.replace('src="logo.png"', f'src="file://{LOGO_PATH}"')
            f.write(html)
            tmp_path = f.name

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file://{tmp_path}")
            page.wait_for_timeout(800)
            page.screenshot(path=output_path, full_page=False,
                           clip={"x": 0, "y": 0, "width": width, "height": height})
            browser.close()

        os.unlink(tmp_path)
        print(f"✅ الصورة جاهزة: {output_path}")
        return output_path

    except ImportError:
        print("❌ Playwright مش متثبّت")
        return None
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return None


def goal_card(scorer_name, assist_name=None):
    return html_to_image(goal_template(scorer_name, assist_name),
                         f"/tmp/goal_{scorer_name.replace(' ','_')}.jpg")

def yellow_card(player_name):
    return html_to_image(yellow_card_template(player_name),
                         f"/tmp/yellow_{player_name.replace(' ','_')}.jpg")

def bonus_card(players):
    return html_to_image(bonus_template(players), "/tmp/bonus_card.jpg")

def fulltime_card(home_team, away_team, home_score, away_score,
                  home_logo_url=None, away_logo_url=None):
    return html_to_image(
        fulltime_template(home_team, away_team, home_score, away_score,
                         home_logo_url, away_logo_url),
        f"/tmp/fulltime_{home_team}_{away_team}.jpg")

def price_card(player_name, old_price, new_price):
    return html_to_image(price_template(player_name, old_price, new_price),
                         f"/tmp/price_{player_name.replace(' ','_')}.jpg")

def captain_card(player_name, price, form, ownership, fixture):
    return html_to_image(captain_template(player_name, price, form, ownership, fixture),
                         f"/tmp/captain_{player_name.replace(' ','_')}.jpg")

def injury_card(player_name, chance, news):
    return html_to_image(injury_template(player_name, chance, news),
                         f"/tmp/injury_{player_name.replace(' ','_')}.jpg")

def transfers_card(bought_list, sold_list):
    players = [{"name": f"↑ {p['name']} £{p['price']}m", "points": ""} for p in bought_list[:3]]
    return html_to_image(bonus_template(players), "/tmp/transfers_card.jpg")


if __name__ == "__main__":
    print("🧪 اختبار...")
    goal_card("محمد صلاح", "إيندو")
    yellow_card("كيركيز")
    bonus_card([{"name":"سيمينيو","points":3},{"name":"إيكيتيكي","points":2},{"name":"صلاح","points":1}])
    price_card("أرزيبالاجا", 3.9, 4.0)
    captain_card("هالاند", 15.0, "8.5", 65.3, "مان سيتي vs ويست هام")
    injury_card("تشالوبا", 75, "إصابة في الكاحل — 75% يلعب")
    print("✅ خلص!")
