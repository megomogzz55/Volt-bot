"""
FPL & Premier League Stats Engine — Official Opta xG, xA, Threat & Form Leaderboards.
Powers viral analytical posts for Fantasy Volt and Kora Volt.
100% Free, official Premier League data updated after every gameweek.
"""

import requests
import json

FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


class FPLStatsEngine:
    def __init__(self):
        self._data = None
        
    def _fetch_data(self):
        if not self._data:
            try:
                r = requests.get(FPL_BOOTSTRAP_URL, timeout=15)
                if r.status_code == 200:
                    self._data = r.json()
            except Exception as e:
                print(f"FPL API fetch error: {e}")
        return self._data
        
    def get_xg_leaders(self, limit=5):
        """Top players by Expected Goals (xG) vs Actual Goals."""
        data = self._fetch_data()
        if not data:
            return []
        elements = data.get("elements", [])
        teams = {t["id"]: t["name"] for t in data.get("teams", [])}
        
        sorted_players = sorted(elements, key=lambda x: float(x.get("expected_goals") or 0), reverse=True)
        results = []
        for p in sorted_players[:limit]:
            results.append({
                "name": f"{p['first_name']} {p['second_name']}",
                "web_name": p["web_name"],
                "team": teams.get(p["team"], ""),
                "xg": float(p.get("expected_goals") or 0),
                "goals": p.get("goals_scored", 0),
                "diff": p.get("goals_scored", 0) - float(p.get("expected_goals") or 0),
                "price": f"£{p['now_cost'] / 10}m",
                "points": p.get("total_points", 0),
                "photo_code": p.get("code")
            })
        return results

    def get_xa_leaders(self, limit=5):
        """Top players by Expected Assists (xA) and Creativity."""
        data = self._fetch_data()
        if not data:
            return []
        elements = data.get("elements", [])
        teams = {t["id"]: t["name"] for t in data.get("teams", [])}
        
        sorted_players = sorted(elements, key=lambda x: float(x.get("expected_assists") or 0), reverse=True)
        results = []
        for p in sorted_players[:limit]:
            results.append({
                "name": f"{p['first_name']} {p['second_name']}",
                "web_name": p["web_name"],
                "team": teams.get(p["team"], ""),
                "xa": float(p.get("expected_assists") or 0),
                "assists": p.get("assists", 0),
                "creativity": float(p.get("creativity") or 0),
                "price": f"£{p['now_cost'] / 10}m",
                "points": p.get("total_points", 0),
                "photo_code": p.get("code")
            })
        return results

    def get_transfer_trends(self, limit=5):
        """Most transferred IN and OUT players ahead of deadline."""
        data = self._fetch_data()
        if not data:
            return [], []
        elements = data.get("elements", [])
        teams = {t["id"]: t["name"] for t in data.get("teams", [])}
        
        in_trend = sorted(elements, key=lambda x: x.get("transfers_in_event", 0), reverse=True)[:limit]
        out_trend = sorted(elements, key=lambda x: x.get("transfers_out_event", 0), reverse=True)[:limit]
        
        top_in = [{"name": p["web_name"], "team": teams.get(p["team"], ""), "count": p["transfers_in_event"], "price": f"£{p['now_cost']/10}m"} for p in in_trend]
        top_out = [{"name": p["web_name"], "team": teams.get(p["team"], ""), "count": p["transfers_out_event"], "price": f"£{p['now_cost']/10}m"} for p in out_trend]
        
        return top_in, top_out

    def format_xg_report_post(self):
        """Generates ready-to-publish Facebook analytical post about xG."""
        leaders = self.get_xg_leaders(limit=5)
        if not leaders:
            return ""
            
        lines = [
            "📊 إحصائيات | ترتيب أخطر لاعبي البريميرليج وفقًا للأهداف المتوقعة (xG) 🔥",
            "",
            "الأرقام الحقيقية لا تكذب.. إليكم قائمة أكثر اللاعبين تهديدًا للمرمى حتى الآن في الدوري الإنجليزي:",
            ""
        ]
        
        for i, p in enumerate(leaders, 1):
            diff_icon = "🟢" if p["diff"] >= 0 else "🔴"
            lines.append(f"{i}⃣ {p['name']} ({p['team']})")
            lines.append(f"   🎯 أهداف متوقعة (xG): {p['xg']:.2f} | ⚽ أهداف فعلية: {p['goals']} {diff_icon}")
            lines.append(f"   💰 السعر: {p['price']} | 🏆 نقاط الفانتازي: {p['points']}")
            lines.append("")
            
        lines.append("💬 مين فيهم أساسي ومثبت في تشكيلة الفانتازي بتاعتك؟ 👇")
        lines.append("")
        lines.append("#فانتازي_البريميرليج #FPL #FantasyVolt #كورة_ڤولت")
        return "\n".join(lines)
