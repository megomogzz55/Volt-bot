"""
Advanced Sports News Engine for Kora Volt & Fantasy Volt
Features:
- Multi-category Arabic football aggregation
- Strict sports-only filtering (zero non-football noise)
- Persistent deduplication tracking in data/posted_news.json
- High-engagement viral post copywriting
"""
import os
import json
import hashlib
import urllib.parse
import feedparser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_FILE = os.path.join(DATA_DIR, "posted_news.json")
os.makedirs(DATA_DIR, exist_ok=True)

FOOTBALL_KEYWORDS = [
    "كرة قدم", "دوري", "نادي", "لاعب", "مدرب", "هدف", "مباراة", "مباريات",
    "تعاقد", "انتقال", "ميركاتو", "صفقة", "منتخب", "صلاح", "ريال مدريد",
    "برشلونة", "الأهلي", "الزمالك", "ليفربول", "مانشستر", "أرسنال", "تشيلسي",
    "بايرن", "باريس", "أنشيلوتي", "جوارديولا", "أرتيتا", "سلوت", "كولر",
    "جوميز", "فينيسيوس", "مبابي", "هالاند", "البريميرليج", "الكلاسيكو", "كأس"
]

NON_SPORTS_EXCLUDES = [
    "مترو", "قطار", "انتخابات", "حرب", "بورصة", "أسهم", "طقس", "زلزال",
    "مجلس نواب", "وزارة", "اقتصاد", "سعر الذهب", "سعر الدولار", "جريمة", "حادث"
]

class NewsEngine:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"posted_hashes": [], "history": []}

    def _save_state(self):
        self.state["posted_hashes"] = self.state["posted_hashes"][-500:]
        self.state["history"] = self.state["history"][-200:]
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def _hash_title(self, title):
        clean = "".join(c for c in title if c.isalnum()).lower()
        return hashlib.md5(clean.encode("utf-8")).hexdigest()

    def is_posted(self, title):
        h = self._hash_title(title)
        return h in self.state.get("posted_hashes", [])

    def mark_posted(self, title, category=None):
        h = self._hash_title(title)
        if h not in self.state["posted_hashes"]:
            self.state["posted_hashes"].append(h)
            self.state["history"].append({
                "hash": h,
                "title": title,
                "category": category
            })
            self._save_state()

    def is_valid_football_article(self, title, summary=""):
        full_text = f"{title} {summary}".lower()
        for excl in NON_SPORTS_EXCLUDES:
            if excl in full_text:
                return False
        for kw in FOOTBALL_KEYWORDS:
            if kw in full_text:
                return True
        return False

    def fetch_news_stream(self, limit=20):
        queries = [
            ("ميركاتو وانتقالات", "ميركاتو كرة قدم OR انتقال لاعب OR صفقة ليفربول OR صفقة ريال مدريد"),
            ("الدوري الإنجليزي", "الدوري الإنجليزي OR مانشستر سيتي OR ليفربول OR أرسنال OR تشيلسي"),
            ("الكرة الإسبانية", "ريال مدريد OR برشلونة OR مبابي OR فينيسيوس"),
            ("الكرة المصرية والأفريقية", "الأهلي OR الزمالك OR الدوري المصري الممتاز OR حسام حسن"),
            ("محمد صلاح", "محمد صلاح ليفربول OR عقد محمد صلاح"),
            ("دوري أبطال أوروبا", "دوري أبطال أوروبا OR قرعة دوري الأبطال")
        ]

        collected = []
        seen_titles = set()

        for category, q in queries:
            encoded = urllib.parse.quote(q)
            url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:8]:
                    raw_title = entry.title
                    title = raw_title
                    source = "كورة ڤولت"
                    if " - " in title:
                        parts = title.rsplit(" - ", 1)
                        title = parts[0].strip()
                        source = parts[1].strip()

                    if title in seen_titles:
                        continue
                    seen_titles.add(title)

                    if self.is_posted(title):
                        continue

                    summary = getattr(entry, "summary", "")
                    if not self.is_valid_football_article(title, summary):
                        continue

                    collected.append({
                        "category": category,
                        "title": title,
                        "source": source,
                        "link": entry.link,
                        "published": getattr(entry, "published", "")
                    })
            except Exception as e:
                print(f"Error fetching query: {e}")

        return collected[:limit]

    def format_engaging_post(self, item):
        cat = item.get("category", "")
        title = item.get("title", "")
        source = item.get("source", "كورة ڤولت")

        if "ميركاتو" in cat:
            header = "🔥 ميركاتو ڤولت | صفقات وانتقالات"
            q = "في رأيك.. هل اللاعب ده هيكون إضافة قوية للفريق؟ شاركنا رأيك في الكومنتات! 👇"
            tags = "#ميركاتو #صفقات #كرة_القدم #كورة_ڤولت"
        elif "صلاح" in cat:
            header = "👑 الملك المصري | محمد صلاح"
            q = "شايف صلاح هيكمل التاريخ مع الريدز ولا حان وقت خوض تحدي جديد؟ مستنيين رأيكم! 👇"
            tags = "#محمد_صلاح #ليفربول #صلاح #كورة_ڤولت"
        elif "الإنجليزي" in cat:
            header = "🏴󠁧󠁢󠁥󠁮󠁧󠁿 البريميرليج | كورة ڤولت"
            q = "شايف مين الأقرب لحسم الصراع في الجولات الجاية؟ شاركنا توقعاتك! 👇"
            tags = "#الدوري_الانجليزي #البريميرليج #ليفربول #مانشستر_سيتي #أرسنال #كورة_ڤولت"
        elif "الإسبانية" in cat:
            header = "🇪🇸 الليجا | ريال مدريد وبرشلونة"
            q = "شاركونا توقعاتكم في التعليقات.. مين بطل الموسم ده؟ 👇"
            tags = "#ريال_مدريد #برشلونة #الكلاسيكو #الليجا #كورة_ڤولت"
        elif "المصرية" in cat:
            header = "🇪🇬 الكرة المصرية | الدوري الممتاز"
            q = "رأيك إيه في القرار ده؟ شاركنا رأيك في الكومنتات! 👇"
            tags = "#الأهلي #الزمالك #الدوري_المصري #كورة_ڤولت"
        else:
            header = "⚡ عاجل من ملاعب الكرة | كورة ڤولت"
            q = "شاركنا وجهة نظرك في الكومنتات! 💬👇"
            tags = "#كرة_القدم #أخبار_الرياضة #كورة_ڤولت"

        lines = [
            header,
            "",
            f"📌 {title}",
            "",
            f"📰 المصدر: {source}",
            "",
            f"💬 {q}",
            "",
            tags
        ]
        return "\n".join(lines)

if __name__ == "__main__":
    eng = NewsEngine()
    print("Testing NewsEngine Stream...")
    news = eng.fetch_news_stream(limit=5)
    print(f"Fresh unposted articles found: {len(news)}")
    for i, n in enumerate(news[:3], 1):
        print(f"\n--- [SAMPLE POST #{i}] ---")
        print(eng.format_engaging_post(n))
