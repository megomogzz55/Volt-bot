"""
Photo News Engine (beIN Fantasy & Top Sports Style)
- Strips all local competitor sources (Yallakora, FilGoal, Kooora, etc.)
- Automatically fetches authentic high-res photos for players, managers, and clubs
- Generates punchy, viral Facebook sports copy (clean quotes, breaking news, stats)
- Publishes photo + caption to Facebook
"""
import os
import json
import re
import urllib.request
import urllib.parse
import hashlib
import feedparser

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "news_photos")
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_FILE = os.path.join(DATA_DIR, "posted_news.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

ENTITY_MAP = {
    # Top Players
    'محمد صلاح': 'Mohamed Salah',
    'صلاح': 'Mohamed Salah',
    'هالاند': 'Erling Haaland',
    'بالمر': 'Cole Palmer',
    'ساكا': 'Bukayo Saka',
    'فينيسيوس': 'Vinícius Júnior',
    'مبابي': 'Kylian Mbappé',
    'يامال': 'Lamine Yamal',
    'لامين': 'Lamine Yamal',
    'بيلينجهام': 'Jude Bellingham',
    'ليفاندوفسكي': 'Robert Lewandowski',
    'رودريجو': 'Rodrygo',
    'دي بروين': 'Kevin De Bruyne',
    'فودين': 'Phil Foden',
    'رافينيا': 'Raphinha',
    'دياز': 'Luis Díaz',
    'فان دايك': 'Virgil van Dijk',
    'أليسون': 'Alisson',
    'كورتوا': 'Thibaut Courtois',
    'مودريتش': 'Luka Modrić',
    'مرموش': 'Omar Marmoush',
    'عمر مرموش': 'Omar Marmoush',
    'مصطفى محمد': 'Mostafa Mohamed',
    'زيزو': 'Ahmed Sayed Zizo',
    'إمام عاشور': 'Emam Ashour',
    'مروان عطية': 'Marwan Attia',
    'إيزاك': 'Alexander Isak',
    'سيمينيو': 'Antoine Semenyo',
    'رايس': 'Declan Rice',
    'سون': 'Son Heung-min',
    'فيرتز': 'Florian Wirtz',
    'موسيالا': 'Jamal Musiala',
    'كين': 'Harry Kane',
    'كريستيانو': 'Cristiano Ronaldo',
    'رونالدو': 'Cristiano Ronaldo',
    'ميسي': 'Lionel Messi',

    # Managers
    'جوارديولا': 'Pep Guardiola',
    'بيب': 'Pep Guardiola',
    'أرتيتا': 'Mikel Arteta',
    'أنشيلوتي': 'Carlo Ancelotti',
    'سلوت': 'Arne Slot',
    'كولر': 'Marcel Koller',
    'جوميز': 'José Gomes',
    'مورينيو': 'José Mourinho',
    'كلوب': 'Jürgen Klopp',
    'تين هاج': 'Erik ten Hag',
    'فليك': 'Hansi Flick',

    # Clubs
    'ريال مدريد': 'Real Madrid CF',
    'برشلونة': 'FC Barcelona',
    'ليفربول': 'Liverpool F.C.',
    'مانشستر سيتي': 'Manchester City F.C.',
    'مانشستر يونايتد': 'Manchester United F.C.',
    'أرسنال': 'Arsenal F.C.',
    'تشيلسي': 'Chelsea F.C.',
    'بايرن ميونخ': 'FC Bayern Munich',
    'باريس سان جيرمان': 'Paris Saint-Germain F.C.',
    'الأهلي': 'Al Ahly FC',
    'الزمالك': 'Zamalek SC'
}

COMPETITOR_PATTERNS = [
    r'\s*-\s*(?:يلا\s*كورة|يلا\s*شوت|في\s*الجول|اليوم\s*السابع|كووورة|بطولات|الوطن|المصري\s*اليوم|الشروق|الوفد|صدى\s*البلد|بوابة\s*الأهرام|Goal\.com|Kooora|FilGoal|Yallakora|winwin|365Scores|CNN Arabic|beIN SPORTS|العربية).*$',
    r'\s*\|\s*(?:يلا\s*كورة|في\s*الجول|كووورة|اليوم\s*السابع).*$'
]

def clean_headline(title):
    t = title
    for pat in COMPETITOR_PATTERNS:
        t = re.sub(pat, '', t, flags=re.IGNORECASE)
    # Strip trailing quotes or dashes
    t = t.strip(' -–|:')
    return t

def detect_entity(text):
    for ar_key, en_name in ENTITY_MAP.items():
        if ar_key in text:
            return en_name, ar_key
    return None, None

def fetch_entity_photo(en_name):
    """
    Fetch the official high-resolution photo from Wikimedia Commons
    """
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(en_name)}&prop=pageimages&format=json&pilicense=any&piprop=original"
    req = urllib.request.Request(url, headers={'User-Agent': 'VoltSportsBot/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                orig = pdata.get('original', {})
                if 'source' in orig:
                    return orig['source']
    except Exception as e:
        print(f"Error fetching photo for {en_name}:", e)
    return None

def download_image(img_url, filename):
    dest = os.path.join(OUTPUT_DIR, filename)
    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp, open(dest, 'wb') as f:
            f.write(resp.read())
        return dest
    except Exception as e:
        print("Download image failed:", e)
        return None

class PhotoNewsEngine:
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

    def is_posted(self, title):
        clean = "".join(c for c in title if c.isalnum()).lower()
        h = hashlib.md5(clean.encode("utf-8")).hexdigest()
        return h in self.state.get("posted_hashes", [])

    def mark_posted(self, title):
        clean = "".join(c for c in title if c.isalnum()).lower()
        h = hashlib.md5(clean.encode("utf-8")).hexdigest()
        if h not in self.state["posted_hashes"]:
            self.state["posted_hashes"].append(h)
            self._save_state()

    def fetch_top_stories_with_photos(self, limit=5):
        """
        Fetch breaking stories, resolve entities, and attach real photos
        """
        queries = [
            "محمد صلاح OR ليفربول",
            "هالاند OR مانشستر سيتي",
            "ريال مدريد OR فينيسيوس OR مبابي",
            "برشلونة OR يامال",
            "عمر مرموش",
            "الأهلي OR الزمالك",
            "الدوري الإنجليزي ميركاتو"
        ]

        results = []
        for q in queries:
            encoded = urllib.parse.quote(q)
            url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:
                    raw_title = entry.title
                    clean_t = clean_headline(raw_title)

                    if self.is_posted(clean_t):
                        continue

                    en_name, ar_key = detect_entity(clean_t)
                    if not en_name:
                        continue

                    # Fetch real photo
                    img_url = fetch_entity_photo(en_name)
                    if not img_url:
                        continue

                    results.append({
                        "raw_title": raw_title,
                        "title": clean_t,
                        "entity_en": en_name,
                        "entity_ar": ar_key,
                        "img_url": img_url,
                        "link": entry.link
                    })
                    if len(results) >= limit:
                        return results
            except Exception as e:
                print("Error in query:", e)

        return results

    def format_bein_style_caption(self, story):
        """
        Format clean, natural, punchy caption without ANY competitor names
        """
        title = story["title"]

        # Check if title has quotes
        if ":" in title or "：" in title:
            prefix = "🎙️ "
        elif "رسمي" in title:
            prefix = "🚨 رسمياً | "
        elif "صفقة" in title or "ميركاتو" in title or "انتقال" in title:
            prefix = "🔥 صفقة مدوية | "
        else:
            prefix = "⚡ "

        caption = f"{prefix}{title}!\n\n#كورة_ڤولت #كرة_القدم"
        return caption
