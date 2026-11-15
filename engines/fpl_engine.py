"""
FPL Engine for Fantasy Volt
Interacts with the official Fantasy Premier League API to track:
- Gameweek deadlines & status
- Match events (Goals, Assists, Yellow Cards, Bonus Points)
- Daily Price Changes (Rises & Falls)
- Injury & Suspension alerts
"""
import os
import json
import requests
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Premier League Teams Arabic Mapping by English Name
TEAMS_NAME_AR = {
    "Arsenal": "أرسنال",
    "Aston Villa": "أستون فيلا",
    "Bournemouth": "بورنموث",
    "Brentford": "برينتفورد",
    "Brighton": "برايتون",
    "Chelsea": "تشيلسي",
    "Crystal Palace": "كريستال بالاس",
    "Everton": "إيفرتون",
    "Fulham": "فولهام",
    "Ipswich Town": "إبسويتش تاون",
    "Ipswich": "إبسويتش تاون",
    "Leicester City": "ليستر سيتي",
    "Leicester": "ليستر سيتي",
    "Liverpool": "ليفربول",
    "Man City": "مانشستر سيتي",
    "Manchester City": "مانشستر سيتي",
    "Man Utd": "مانشستر يونايتد",
    "Manchester United": "مانشستر يونايتد",
    "Newcastle": "نيوكاسل",
    "Newcastle United": "نيوكاسل",
    "Nott'm Forest": "نوتينجهام فورست",
    "Nottingham Forest": "نوتينجهام فورست",
    "Southampton": "ساوثهامبتون",
    "Spurs": "توتنهام",
    "Tottenham": "توتنهام",
    "West Ham": "وست هام",
    "West Ham United": "وست هام",
    "Wolves": "وولفرهامبتون",
    "Wolverhampton Wanderers": "وولفرهامبتون",
    "Coventry City": "كوفنتري سيتي",
    "Hull City": "هال سيتي",
    "Leeds": "ليدز يونايتد",
    "Sunderland": "سندرلاند"
}

# Common Players Arabic Transliteration Cache
PLAYERS_AR = {
    "Salah": "محمد صلاح",
    "Haaland": "هالاند",
    "Palmer": "كول بالمر",
    "Saka": "بوكايو ساكا",
    "Foden": "فودين",
    "Son": "سون",
    "Diaz": "لويس دياز",
    "Watkins": "واتكينز",
    "Isak": "إيزاك",
    "Mbeumo": "مبيومو",
    "Wood": "كريس وود",
    "Cunha": "كونيا",
    "Gabriel": "جابرييل",
    "Saliba": "صاليبا",
    "Alexander-Arnold": "أرنولد",
    "Gvardiol": "جفارديول",
    "Raya": "ديفيد رايا",
    "Semenyo": "سيمينيو",
    "Kerkez": "كيركيز",
    "Rogers": "مورجان روجرز",
    "Bowen": "جارود بوين",
    "Johnson": "برينان جونسون",
    "Kulusevski": "كولوسيفسكي",
    "Jackson": "نيكولاس جاكسون",
    "Solanke": "سولانكي",
    "Havertz": "كاي هافيرتز",
    "Martinelli": "مارتينيلي",
    "Bobb": "أوسكار بوب",
    "Reijnders": "رايندرز",
    "Ekitike": "إيكيتيكي",
    "Bruno Fernandes": "برونو فيرنانديز"
}

def get_arabic_player_name(web_name):
    return PLAYERS_AR.get(web_name, web_name)

def get_arabic_team_name(team_id, teams_by_id=None):
    if teams_by_id and team_id in teams_by_id:
        tname = teams_by_id[team_id].get("name", "")
        return TEAMS_NAME_AR.get(tname, tname)
    return f"فريق {team_id}"

class FPLEngine:
    def __init__(self):
        self._bootstrap = None
        self._elements_by_id = {}
        self._teams_by_id = {}

    def fetch_bootstrap(self, force=False):
        if self._bootstrap and not force:
            return self._bootstrap
        url = "https://fantasy.premierleague.com/api/bootstrap-static/"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        self._bootstrap = resp.json()
        
        self._elements_by_id = {el["id"]: el for el in self._bootstrap.get("elements", [])}
        self._teams_by_id = {t["id"]: t for t in self._bootstrap.get("teams", [])}
        return self._bootstrap

    def get_current_gameweek(self):
        boot = self.fetch_bootstrap()
        events = boot.get("events", [])
        current = next((e for e in events if e.get("is_current")), None)
        if not current:
            current = next((e for e in events if e.get("is_next")), None)
        return current

    def get_deadline_status(self):
        boot = self.fetch_bootstrap()
        next_event = next((e for e in boot.get("events", []) if e.get("is_next")), None)
        if not next_event:
            return None
        deadline_time_str = next_event.get("deadline_time")
        # Format: 2026-11-21T11:00:00Z
        dt = datetime.fromisoformat(deadline_time_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = dt - now
        hours_left = diff.total_seconds() / 3600.0
        return {
            "gameweek_id": next_event["id"],
            "name": next_event["name"],
            "deadline_utc": deadline_time_str,
            "hours_left": hours_left,
            "is_passed": hours_left <= 0
        }

    def get_fixtures(self, gw=None):
        if gw is None:
            curr = self.get_current_gameweek()
            gw = curr["id"] if curr else 1
        url = f"https://fantasy.premierleague.com/api/fixtures/?event={gw}"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return resp.json()

    def get_price_changes(self):
        """
        Extract players whose price changed today (cost_change_event != 0).
        """
        boot = self.fetch_bootstrap(force=True)
        elements = boot.get("elements", [])
        
        rising = []
        falling = []
        
        for el in elements:
            chg = el.get("cost_change_event", 0)
            if chg > 0:
                name_ar = get_arabic_player_name(el["web_name"])
                team_ar = get_arabic_team_name(el["team"], self._teams_by_id)
                price = f"£{el['now_cost'] / 10:.1f}m"
                change = f"+£{chg / 10:.1f}m"
                own = f"{el.get('selected_by_percent', '0')}%"
                rising.append((name_ar, team_ar, price, change, own))
            elif chg < 0:
                name_ar = get_arabic_player_name(el["web_name"])
                team_ar = get_arabic_team_name(el["team"], self._teams_by_id)
                price = f"£{el['now_cost'] / 10:.1f}m"
                change = f"-£{abs(chg) / 10:.1f}m"
                own = f"{el.get('selected_by_percent', '0')}%"
                falling.append((name_ar, team_ar, price, change, own))
                
        return rising, falling

    def get_fixture_details(self, fixture):
        """
        Extract detailed stats (goals, assists, cards, bonus) for a fixture.
        """
        self.fetch_bootstrap()
        home_team_id = fixture.get("team_h")
        away_team_id = fixture.get("team_a")
        
        home_team_ar = get_arabic_team_name(home_team_id, self._teams_by_id)
        away_team_ar = get_arabic_team_name(away_team_id, self._teams_by_id)
        
        home_score = fixture.get("team_h_score")
        away_score = fixture.get("team_a_score")
        started = fixture.get("started", False)
        finished = fixture.get("finished", False)
        minutes = fixture.get("minutes", 0)
        
        stats = {s["identifier"]: s for s in fixture.get("stats", [])}
        
        def resolve_players(stat_key):
            items = stats.get(stat_key, {})
            result = []
            for side in ["h", "a"]:
                for entry in items.get(side, []):
                    el_id = entry.get("element")
                    el = self._elements_by_id.get(el_id, {})
                    wname = el.get("web_name", f"Player {el_id}")
                    val = entry.get("value", 1)
                    name_ar = get_arabic_player_name(wname)
                    team_ar = home_team_ar if side == "h" else away_team_ar
                    result.append({"name_ar": name_ar, "value": val, "team_ar": team_ar, "web_name": wname})
            return result

        goals = resolve_players("goals_scored")
        assists = resolve_players("assists")
        yellows = resolve_players("yellow_cards")
        bonus = resolve_players("bonus")
        bps = resolve_players("bps")
        
        return {
            "id": fixture.get("id"),
            "home_team": home_team_ar,
            "away_team": away_team_ar,
            "home_score": home_score,
            "away_score": away_score,
            "started": started,
            "finished": finished,
            "minutes": minutes,
            "goals": goals,
            "assists": assists,
            "yellow_cards": yellows,
            "bonus": bonus,
            "bps": sorted(bps, key=lambda x: x["value"], reverse=True)[:5]
        }

if __name__ == "__main__":
    engine = FPLEngine()
    print("Testing FPLEngine...")
    boot = engine.fetch_bootstrap()
    print("Boot loaded:", len(boot["elements"]), "players")
    dl = engine.get_deadline_status()
    print("Next Deadline:", dl)
    rising, falling = engine.get_price_changes()
    print(f"Price Changes: {len(rising)} rises, {len(falling)} falls")
    fixtures = engine.get_fixtures()
    print(f"Loaded {len(fixtures)} fixtures for current gameweek.")
    if fixtures:
        det = engine.get_fixture_details(fixtures[0])
        print("Fixture 1 summary:", det["home_team"], det["home_score"], "-", det["away_score"], det["away_team"])
        print("Goals:", det["goals"])
        print("Bonus:", det["bonus"])
