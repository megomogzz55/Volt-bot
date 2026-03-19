"""
Fantasy Bot — Main Runner
بيشتغل كل 5 دقايق عبر GitHub Actions
"""

import os
import json
import datetime
from fpl_data import (
    get_bootstrap, get_current_gameweek,
    get_price_changes, get_top_transfers,
    get_captain_picks, get_injured_players,
    get_fixtures
)
from content_writer import (
    price_rise_text, price_fall_text,
    captain_text, top_transfers_text,
    injury_text, fixtures_text
)
from publisher import post_fantasy, post_news

# image_generator معطّل مؤقتاً — بنستخدم goal_card.py بدله
def price_card(*args, **kwargs): return None
def captain_card(*args, **kwargs): return None
def injury_card(*args, **kwargs): return None
def transfers_card(*args, **kwargs): return None
from goal_card import create_goal_card

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.load(open(STATE_FILE))
        except:
            pass
    return {
        "posted_price_changes": [],
        "posted_injuries": [],
        "last_captain_post": None,
        "last_transfers_post": None,
        "last_fixtures_post": None,
    }

def save_state(state):
    json.dump(state, open(STATE_FILE, "w"), ensure_ascii=False, indent=2)

def get_schedule():
    now = datetime.datetime.utcnow()
    hour = now.hour
    minute = now.minute
    weekday = now.weekday()

    tasks = []
    tasks.append("check_prices")
    tasks.append("check_injuries")

    if hour == 8 and minute < 10:
        tasks.append("post_price_summary")
    if hour == 12 and minute < 10:
        tasks.append("post_top_transfers")
    if hour == 15 and minute < 10:
        tasks.append("post_captain")
    if weekday == 4 and hour == 10 and minute < 10:
        tasks.append("post_fixtures")

    return tasks

# ══════════════════════════════════════════
# 🧪 تجربة كارت الهدف — مؤقت
# ══════════════════════════════════════════
def test_goal_card():
    print("🧪 تجربة كارت الهدف...")
    try:
        path, caption = create_goal_card(
            player_code="Mohamed Salah",  # الاسم الإنجليزي لـ TheSportsDB
            scorer_name="محمد صلاح",
            assist_name="ترينت",
            minute=67,
            home_team="ليفربول",
            away_team="بورنموث",
            home_score=2,
            away_score=0
        )
        if path:
            result = post_fantasy(caption, path)
            if result:
                print("✅ كارت الهدف اتنشر على فيسبوك!")
            else:
                print("❌ فشل النشر على فيسبوك")
        else:
            print("❌ فشل إنشاء الصورة — هينشر caption بدون صورة")
            post_fantasy(caption)
    except Exception as e:
        print(f"❌ خطأ: {e}")

# ══════════════════════════════════════════
# المهام
# ══════════════════════════════════════════

def run_check_prices(data, state):
    changes = get_price_changes(data)
    posted = 0
    for c in changes:
        player_key = f"{c['name']}_{c['new_price']}"
        if player_key in state["posted_price_changes"]:
            continue
        if c["change"] > 0:
            text = price_rise_text(c["name"], c["old_price"], c["new_price"])
        else:
            text = price_fall_text(c["name"], c["old_price"], c["new_price"])
        try:
            img_path = price_card(c["name"], c["old_price"], c["new_price"])
        except Exception as e:
            print(f"⚠️ فشل توليد الصورة: {e}")
            img_path = None
        result = post_fantasy(text, img_path)
        if result:
            state["posted_price_changes"].append(player_key)
            state["posted_price_changes"] = state["posted_price_changes"][-50:]
            posted += 1
            print(f"✅ نشرنا تغيير سعر: {c['name']}")
        if posted >= 3:
            break
    return state


def run_check_injuries(data, state):
    injured = get_injured_players(data)
    for p in injured:
        if float(p["ownership"]) < 15:
            continue
        player_key = f"{p['name']}_{p['chance']}"
        if player_key in state["posted_injuries"]:
            continue
        text = injury_text(p)
        try:
            img_path = injury_card(p["name"], p["chance"], p["news"])
        except Exception as e:
            print(f"⚠️ فشل توليد صورة الإصابة: {e}")
            img_path = None
        result = post_fantasy(text, img_path)
        if result:
            state["posted_injuries"].append(player_key)
            state["posted_injuries"] = state["posted_injuries"][-30:]
            print(f"✅ نشرنا إصابة: {p['name']}")
            break
    return state


def run_post_captain(data, state):
    today = datetime.date.today().isoformat()
    if state.get("last_captain_post") == today:
        print("⏭️ الكابتن اتنشر النهارده")
        return state
    players = get_captain_picks(data)
    if not players:
        return state
    text = captain_text(players)
    top = players[0]
    try:
        img_path = captain_card(top["name"], top["price"], top["form"],
                                top["ownership"], top.get("fixture", "جولة قادمة"))
    except Exception as e:
        print(f"⚠️ فشل توليد كارت الكابتن: {e}")
        img_path = None
    result = post_fantasy(text, img_path)
    if result:
        state["last_captain_post"] = today
        print("✅ نشرنا توصية الكابتن")
    return state


def run_post_top_transfers(data, state):
    today = datetime.date.today().isoformat()
    if state.get("last_transfers_post") == today:
        print("⏭️ التحويلات اتنشرت النهارده")
        return state
    bought, sold = get_top_transfers(data)
    if not bought:
        return state
    text = top_transfers_text(bought, sold)
    try:
        img_path = transfers_card(bought, sold)
    except Exception as e:
        print(f"⚠️ فشل توليد كارت التحويلات: {e}")
        img_path = None
    result = post_fantasy(text, img_path)
    if result:
        state["last_transfers_post"] = today
        print("✅ نشرنا التحويلات")
    return state


def run_post_fixtures(data, state):
    today = datetime.date.today().isoformat()
    if state.get("last_fixtures_post") == today:
        print("⏭️ الجدول اتنشر النهارده")
        return state
    fixture_list = get_fixtures(data)
    if not fixture_list:
        return state
    text = fixtures_text(fixture_list)
    if not text:
        return state
    result = post_fantasy(text)
    if result:
        state["last_fixtures_post"] = today
        print("✅ نشرنا الجدول")
    return state


# ══════════════════════════════════════════
# Main
# ══════════════════════════════════════════
def main():
    print(f"🤖 Fantasy Bot بيشتغل — {datetime.datetime.utcnow()}")

    print("📡 بنجيب بيانات FPL...")
    data = get_bootstrap()
    if not data:
        print("❌ فشل في جيب بيانات FPL — هنحاول تاني")
        return

    gw = get_current_gameweek(data)
    print(f"⚽ الجولة الحالية: {gw}")

    state = load_state()
    tasks = get_schedule()
    print(f"📋 المهام: {tasks}")

    for task in tasks:
        try:
            if task == "check_prices":
                state = run_check_prices(data, state)
            elif task == "check_injuries":
                state = run_check_injuries(data, state)
            elif task == "post_captain":
                state = run_post_captain(data, state)
            elif task == "post_top_transfers":
                state = run_post_top_transfers(data, state)
            elif task == "post_fixtures":
                state = run_post_fixtures(data, state)
        except Exception as e:
            print(f"❌ خطأ في {task}: {e}")

    save_state(state)
    print("✅ خلص — هنشتغل تاني بعد شوية")


if __name__ == "__main__":
    main()
