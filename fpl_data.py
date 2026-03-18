import requests
from config import FPL_BOOTSTRAP, FPL_LIVE, FPL_FIXTURES

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_bootstrap():
    """جيب كل بيانات FPL الأساسية"""
    try:
        r = requests.get(FPL_BOOTSTRAP, headers=HEADERS, timeout=10)
        return r.json()
    except:
        return None

def get_current_gameweek(data=None):
    """جيب رقم الجولة الحالية"""
    if not data:
        data = get_bootstrap()
    if not data:
        return None
    for event in data["events"]:
        if event["is_current"]:
            return event["id"]
    return None

def get_live_points(gw):
    """نقاط لحظية للجولة الحالية"""
    try:
        url = FPL_LIVE.format(gw=gw)
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json()
    except:
        return None

def get_price_changes(data=None):
    """اللاعبين اللي اتغير سعرهم النهارده"""
    if not data:
        data = get_bootstrap()
    if not data:
        return []

    changes = []
    for p in data["elements"]:
        now  = p["now_cost"] / 10
        prev = (p["now_cost"] + p["cost_change_event"]) / 10  # السعر قبل التغيير
        if p["cost_change_event"] != 0:
            changes.append({
                "name":       p["web_name"],
                "team":       p["team"],
                "position":   ["GK","DEF","MID","FWD"][p["element_type"]-1],
                "old_price":  prev,
                "new_price":  now,
                "change":     p["cost_change_event"] / 10,
                "ownership":  p["selected_by_percent"],
                "form":       p["form"],
                "transfers_in":  p["transfers_in_event"],
                "transfers_out": p["transfers_out_event"],
            })

    # رتّب من الأكبر تغييراً للأصغر
    changes.sort(key=lambda x: abs(x["change"]), reverse=True)
    return changes[:10]  # أهم 10

def get_top_transfers(data=None):
    """أكتر لاعبين اتشتروا وبيعوا النهارده"""
    if not data:
        data = get_bootstrap()
    if not data:
        return [], []

    players = data["elements"]

    # أكتر اتشتروا
    bought = sorted(players, key=lambda x: x["transfers_in_event"], reverse=True)[:5]
    # أكتر اتبيعوا
    sold   = sorted(players, key=lambda x: x["transfers_out_event"], reverse=True)[:5]

    def fmt(p):
        return {
            "name":       p["web_name"],
            "price":      p["now_cost"] / 10,
            "ownership":  p["selected_by_percent"],
            "form":       p["form"],
            "transfers_in":  p["transfers_in_event"],
            "transfers_out": p["transfers_out_event"],
        }

    return [fmt(p) for p in bought], [fmt(p) for p in sold]

def get_captain_picks(data=None, gw=None):
    """أفضل 5 خيارات للكابتن"""
    if not data:
        data = get_bootstrap()
    if not data:
        return []
    if not gw:
        gw = get_current_gameweek(data)

    players = data["elements"]

    # رتّب على أساس الفورم + الملكية
    candidates = [p for p in players if float(p["form"]) > 4]
    candidates.sort(key=lambda x: float(x["form"]), reverse=True)

    result = []
    for p in candidates[:5]:
        result.append({
            "name":      p["web_name"],
            "price":     p["now_cost"] / 10,
            "form":      p["form"],
            "ownership": p["selected_by_percent"],
            "position":  ["GK","DEF","MID","FWD"][p["element_type"]-1],
            "points_per_game": p["points_per_game"],
        })
    return result

def get_injured_players(data=None):
    """اللاعبين الموجودين على قائمة الإصابات"""
    if not data:
        data = get_bootstrap()
    if not data:
        return []

    injured = []
    for p in data["elements"]:
        if p["chance_of_playing_next_round"] is not None and \
           p["chance_of_playing_next_round"] < 100:
            injured.append({
                "name":       p["web_name"],
                "price":      p["now_cost"] / 10,
                "ownership":  p["selected_by_percent"],
                "chance":     p["chance_of_playing_next_round"],
                "news":       p["news"],
                "status":     p["status"],  # i=injured, d=doubt, s=suspend
            })

    injured.sort(key=lambda x: float(x["ownership"]), reverse=True)
    return injured[:10]

def get_fixtures(data=None):
    """جدول مباريات الجولة القادمة"""
    try:
        r = requests.get(FPL_FIXTURES, headers=HEADERS, timeout=10)
        fixtures = r.json()

        if not data:
            data = get_bootstrap()
        if not data:
            return []

        gw = get_current_gameweek(data)
        teams = {t["id"]: t["name"] for t in data["teams"]}

        upcoming = []
        for f in fixtures:
            if f["event"] == gw and not f["finished"]:
                upcoming.append({
                    "home": teams.get(f["team_h"], "?"),
                    "away": teams.get(f["team_a"], "?"),
                    "home_difficulty": f["team_h_difficulty"],
                    "away_difficulty": f["team_a_difficulty"],
                    "kickoff": f["kickoff_time"],
                })
        return upcoming
    except:
        return []
