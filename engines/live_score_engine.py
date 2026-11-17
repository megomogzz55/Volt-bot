"""
Live Score Engine for Kora Volt & Fantasy Volt
Pulls real-time soccer scores and live match incidents without any API keys:
- LiveScore public CDN API (for in-play instant alerts)
- ESPN soccer API (for major European and Arab leagues)
"""
import os
import json
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

class LiveScoreEngine:
    def __init__(self):
        self.livescore_base = "https://prod-cdn-mev-api.livescore.com/v1/api/app"
        self.espn_base = "https://site.api.espn.com/apis/site/v2/sports/soccer"

    def get_live_matches(self, tz_offset=2, country_code="EG"):
        """
        Fetch all currently live soccer matches globally.
        """
        url = f"{self.livescore_base}/live/soccer/{tz_offset}?countryCode={country_code}&locale=en"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                matches = []
                for stage in data.get("Stages", []):
                    comp_name = stage.get("CompN") or stage.get("Snm")
                    country = stage.get("Cnm")
                    for ev in stage.get("Events", []):
                        home = ev.get("T1", [{}])[0].get("Nm", "Home")
                        away = ev.get("T2", [{}])[0].get("Nm", "Away")
                        score_h = ev.get("Tr1", "0")
                        score_a = ev.get("Tr2", "0")
                        min_str = ev.get("Eps", "")
                        matches.append({
                            "event_id": ev.get("Eid"),
                            "competition": comp_name,
                            "country": country,
                            "home": home,
                            "away": away,
                            "score_home": score_h,
                            "score_away": score_a,
                            "minute": min_str,
                            "status": ev.get("Esid")
                        })
                return matches
        except Exception as e:
            print("LiveScore API error:", e)
        return []

    def get_espn_scoreboard(self, league_slug="eng.1"):
        """
        Fetch ESPN scoreboard for a league (e.g. eng.1, esp.1, ita.1, egy.1, uefa.champions).
        """
        url = f"{self.espn_base}/{league_slug}/scoreboard"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                events = []
                for ev in data.get("events", []):
                    comp = ev.get("competitions", [{}])[0]
                    competitors = comp.get("competitors", [])
                    home = next((c for c in competitors if c.get("homeAway") == "home"), {})
                    away = next((c for c in competitors if c.get("homeAway") == "away"), {})
                    events.append({
                        "id": ev.get("id"),
                        "name": ev.get("name"),
                        "date": ev.get("date"),
                        "status": comp.get("status", {}).get("type", {}).get("description"),
                        "home_team": home.get("team", {}).get("displayName"),
                        "away_team": away.get("team", {}).get("displayName"),
                        "home_score": home.get("score"),
                        "away_score": away.get("score")
                    })
                return events
        except Exception as e:
            print("ESPN API error:", e)
        return []

    def get_standings(self, league_slug="eng.1"):
        """
        Fetch official live league standings from ESPN API (Free, zero rate limits).
        """
        url = f"https://site.api.espn.com/apis/v2/sports/soccer/{league_slug}/standings"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                children = data.get("children", [])
                if not children:
                    return []
                entries = children[0].get("standings", {}).get("entries", [])
                table = []
                for entry in entries:
                    team = entry.get("team", {})
                    stats = {s.get("name"): s.get("displayValue") for s in entry.get("stats", [])}
                    table.append({
                        "rank": stats.get("rank"),
                        "team": team.get("displayName"),
                        "short_name": team.get("shortDisplayName"),
                        "logo": team.get("logos", [{}])[0].get("href") if team.get("logos") else None,
                        "played": stats.get("gamesPlayed"),
                        "wins": stats.get("wins"),
                        "ties": stats.get("ties"),
                        "losses": stats.get("losses"),
                        "points": stats.get("points"),
                        "goal_diff": stats.get("pointDifferential")
                    })
                return table
        except Exception as e:
            print(f"ESPN Standings API error: {e}")
        return []

    def format_standings_post(self, league_slug="eng.1"):
        league_names = {
            "eng.1": ("الدوري الإنجليزي الممتاز", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "#البريميرليج #الدوري_الانجليزي"),
            "esp.1": ("الدوري الإسباني (الليجا)", "🇪🇸", "#الليجا #ريال_مدريد #برشلونة"),
            "uefa.champions": ("دوري أبطال أوروبا", "🏆", "#دوري_أبطال_أوروبا #UCL"),
            "ita.1": ("الدوري الإيطالي (الكالتشيو)", "🇮🇹", "#الكالتشيو #الدوري_الايطالي"),
            "ger.1": ("الدوري الألماني (البوندسليجا)", "🇩🇪", "#البوندسليجا #بايرن_ميونخ")
        }
        info = league_names.get(league_slug, ("الدوري العام", "⚽", "#كرة_القدم"))
        table = self.get_standings(league_slug)
        if not table:
            return None
            
        lines = [
            f"📊 جدول ترتيب {info[0]} {info[1]} | كورة ڤولت",
            "",
            "إليك صراع الصدارة والمراكز الأولى بعد نهاية الجولة:",
            ""
        ]
        
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        for row in table[:10]:
            r = int(row.get("rank", 99))
            m = medals.get(r, f"{r}️⃣")
            lines.append(f"{m} {row['team']} - {row['points']} نقطة (فارق أهداف: {row['goal_diff']}) [لعب {row['played']}]")
            
        lines.extend([
            "",
            "🔥 مين الأقرب لحسم اللقب في رأيك؟ شاركنا توقعاتك في التعليقات! 👇",
            "",
            f"{info[2]} #كورة_ڤولت #ترتيب_الدوري"
        ])
        return "\n".join(lines)

if __name__ == "__main__":
    engine = LiveScoreEngine()
    print("Testing LiveScoreEngine...")
    live = engine.get_live_matches()
    print(f"Live Matches in-play right now: {len(live)}")
    if live:
        print("Sample live match:", live[0])
    epl = engine.get_espn_scoreboard("eng.1")
    print(f"ESPN Premier League matches found: {len(epl)}")
    if epl:
        print("Sample match:", epl[0])
