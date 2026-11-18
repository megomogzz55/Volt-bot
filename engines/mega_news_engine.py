"""
Mega News Engine v2.0 — Kora Volt & Fantasy Volt
=================================================
Multi-source aggregator with:
- 4 Direct RSS feeds (WinWin, Sky News Arabia, France24, RT Arabic) → embedded HD images
- 10+ Google News site-specific queries (FilGoal, Yallakora, Kooora, beIN, Btolat...)
- 15+ Google News topic queries (EPL, La Liga, UCL, Egypt, Transfers...)
- Smart deduplication (title similarity + hash)
- Competitor name stripping
- Category auto-detection (رسميًا / ميركاتو / تصريحات / إحصائية / عاجل)
- Rich caption formatting with engagement questions
- Image extraction and HD upscaling
"""
import os
import re
import json
import hashlib
import urllib.request
import urllib.parse
import feedparser
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "output", "news_photos")
STATE_FILE = os.path.join(DATA_DIR, "mega_news_state.json")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ─── Competitor names to strip from titles and NEVER mention ───
COMPETITORS = [
    "FilGoal", "في الجول", "يلا كورة", "يلا كوره", "يلاكورة", "يلاكوره", "Yallakora",
    "winwin", "WinWin", "وين وين", "كووورة", "Kooora", "kooora",
    "اليوم السابع", "كورة بلس", "بطولات", "Btolat", "سكاي نيوز",
    "الجزيرة نت", "العربية", "بي إن سبورت", "beIN SPORTS", "beIN",
    "RT Arabic", "روسيا اليوم", "France24", "فرانس 24",
    "المصري اليوم", "الشروق", "الوفد", "صدى البلد", "بوابة الأهرام",
    "مبتدا", "اخبارك نت", "Goal.com", "365Scores",
    "BBC", "CNN Arabic", "سبورت 360", "أخبار اليوم", "الأهرام",
    "koraplus", "Koraplus", "KoraPlus",
]

# ─── Football keyword filter ───
FOOTBALL_KW = [
    "كرة", "دوري", "نادي", "لاعب", "مدرب", "هدف", "مباراة", "مباريات",
    "تعاقد", "انتقال", "ميركاتو", "صفقة", "منتخب", "صلاح", "ريال مدريد",
    "برشلونة", "ليفربول", "مانشستر", "أرسنال", "تشيلسي", "بايرن", "باريس",
    "جوارديولا", "أنشيلوتي", "أرتيتا", "سلوت", "فينيسيوس", "مبابي", "هالاند",
    "البريميرليج", "الليجا", "الكالتشيو", "بوندسليجا", "أبطال", "يوروبا",
    "ساكا", "بالمر", "فودين", "دي بروين", "يامال", "بيلينجهام",
    "الأهلي", "الزمالك", "بيراميدز", "المنتخب", "حسام حسن",
    "مرموش", "إيزاك", "سون", "واتكينز", "كين", "فيرتز", "موسيالا",
    "كأس", "بطولة", "تصفيات", "أفريقيا", "تأهل", "إقصاء",
    "فوز", "خسارة", "تعادل", "ثنائية", "هاتريك", "ركلة جزاء",
    "كارت أحمر", "إيقاف", "إصابة", "جراحة", "غياب",
    "ترتيب", "صدارة", "هبوط", "صعود",
]

NON_FOOTBALL = [
    "مترو", "قطار", "انتخابات", "حرب", "بورصة", "أسهم", "طقس", "زلزال",
    "وزارة", "سعر الذهب", "سعر الدولار", "جريمة", "حادث", "كنيست",
    "ملاكم", "تنس", "فورمولا", "سباق", "يوروليغ", "كرة السلة", "سباحة",
]

# ─── Sources Configuration ───

DIRECT_RSS = [
    {
        "name": "WinWin",
        "url": "https://winwin.com/rss",
        "type": "football",
        "quality": "high",
    },
    {
        "name": "Sky News Arabia Sports",
        "url": "https://www.skynewsarabia.com/rss/sport.xml",
        "type": "sports",
        "quality": "high",
        "img_upscale": lambda u: u.replace("/95/53/", "/1920/1080/") if "/95/53/" in u else u,
    },
    {
        "name": "France24 Arabic Sports",
        "url": "https://www.france24.com/ar/sports/rss",
        "type": "sports",
        "quality": "high",
    },
    {
        "name": "RT Arabic Sports",
        "url": "https://arabic.rt.com/rss/sport/",
        "type": "sports",
        "quality": "medium",
    },
]

# Google News site-specific queries (scrape their content via GN cache)
GN_SITE_QUERIES = [
    ("في الجول", "site:filgoal.com"),
    ("يلا كورة", "site:yallakora.com"),
    ("كووورة", "site:kooora.com"),
    ("بطولات", "site:btolat.com"),
    ("كورة بلس", "site:koraplus.com"),
]

# Google News topic queries
GN_TOPIC_QUERIES_FANTASY = [
    ("البريميرليج", "الدوري الإنجليزي البريميرليج"),
    ("ليفربول", "ليفربول أخبار"),
    ("أرسنال", "أرسنال أخبار"),
    ("مانشستر سيتي", "مانشستر سيتي أخبار"),
    ("تشيلسي", "تشيلسي أخبار"),
    ("ريال مدريد", "ريال مدريد أخبار"),
    ("برشلونة", "برشلونة أخبار"),
    ("دوري الأبطال", "دوري أبطال أوروبا"),
    ("محمد صلاح", "محمد صلاح"),
    ("مبابي", "مبابي ريال مدريد"),
    ("هالاند", "هالاند مانشستر سيتي"),
]

GN_TOPIC_QUERIES_KORA = [
    ("الكرة المصرية", "الأهلي OR الزمالك OR بيراميدز OR الدوري المصري"),
    ("ميركاتو", "ميركاتو صفقة انتقال تعاقد كرة قدم"),
    ("تصفيات أفريقيا", "تصفيات أمم أفريقيا 2027"),
    ("الكرة السعودية", "دوري روشن OR الاتحاد OR الهلال OR النصر"),
    ("يوروبا ليج", "يوروبا ليج OR الدوري الأوروبي"),
    ("الكرة الإيطالية", "الدوري الإيطالي OR إنتر ميلان OR يوفنتوس OR نابولي"),
    ("الكرة الألمانية", "البوندسليجا OR بايرن ميونخ OR دورتموند"),
    ("كأس العالم", "كأس العالم 2026 OR مونديال"),
]


def _clean_title(raw):
    """Remove competitor source names from titles"""
    t = raw
    # Remove trailing " - Source" or " | Source"
    for sep in [" - ", " | ", " — ", " – "]:
        if sep in t:
            parts = t.rsplit(sep, 1)
            tail = parts[1].lower()
            for c in COMPETITORS:
                if c.lower() in tail:
                    t = parts[0].strip()
                    break
    # Remove inline competitor mentions like "يكشف لـ في الجول" or "حصريًا لـ يلا كورة"
    inline_patterns = [
        r'(?:يكشف|حصريًا|حصريا|خاص)\s*(?:لـ?|لـ)\s*(?:' + '|'.join(re.escape(c) for c in COMPETITORS) + r')',
        r'(?:' + '|'.join(re.escape(c) for c in COMPETITORS) + r')\s*(?:يكشف|تعلم|تنفرد)',
    ]
    for pat in inline_patterns:
        t = re.sub(pat, '', t, flags=re.IGNORECASE)
    # Simple replacements
    for c in COMPETITORS:
        t = t.replace(f"- {c}", "").replace(f"| {c}", "").replace(f"— {c}", "")
    return t.strip(" -–|:")


def _is_football(title, summary=""):
    """Check if article is football-related"""
    full = f"{title} {summary}".lower()
    for ex in NON_FOOTBALL:
        if ex in full:
            return False
    for kw in FOOTBALL_KW:
        if kw in full:
            return True
    return False


def _extract_image(entry):
    """Extract the best available image URL from an RSS entry"""
    for attr in ['media_content', 'media_thumbnail']:
        val = entry.get(attr)
        if val and isinstance(val, list) and len(val) > 0:
            url = val[0].get('url') or val[0].get('href')
            if url:
                return url
    enc = entry.get('enclosures')
    if enc and isinstance(enc, list) and len(enc) > 0:
        url = enc[0].get('href') or enc[0].get('url')
        if url:
            return url
    # Try to find <img> in summary/content
    content = entry.get('summary', '') or entry.get('description', '')
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
    if m:
        return m.group(1)
    return None


def _extract_summary(entry):
    """Extract clean text summary from RSS entry"""
    raw = entry.get('summary', '') or entry.get('description', '')
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', '', raw)
    # Strip HTML entities
    clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    clean = re.sub(r'&[a-zA-Z]+;', ' ', clean)
    clean = clean.strip()
    # Remove competitor names from summary too
    for c in COMPETITORS:
        clean = clean.replace(c, '').strip()
    # Remove duplicate spaces
    clean = re.sub(r'\s{2,}', ' ', clean)
    # If summary is basically just the title repeated, return empty
    title = entry.get('title', '')
    if clean and _similar(clean, _clean_title(title), threshold=0.7):
        return ""
    # Limit length
    if len(clean) > 300:
        clean = clean[:297] + "..."
    return clean


def _hash(text):
    clean = "".join(c for c in text if c.isalnum()).lower()
    return hashlib.md5(clean.encode("utf-8")).hexdigest()


def _similar(title1, title2, threshold=0.6):
    """Simple word-overlap similarity check"""
    words1 = set(title1.split())
    words2 = set(title2.split())
    if not words1 or not words2:
        return False
    overlap = len(words1 & words2) / max(len(words1), len(words2))
    return overlap >= threshold


def _detect_category(title):
    """Auto-detect news category from title keywords"""
    if any(w in title for w in ["رسميًا", "رسميا", "أعلن رسميًا", "حسم", "تم الإعلان"]):
        return "official", "🚨 رسميًا"
    if any(w in title for w in ["عاجل", "الآن", "خبر عاجل", "لحظة"]):
        return "breaking", "⚡ عاجل"
    if any(w in title for w in ["قال", "صرح", "يؤكد", "يكشف", "يعلق", ":", "يرد", "يفتح النار", "يفجر"]):
        return "quotes", "🎙️ تصريحات"
    if any(w in title for w in ["ميركاتو", "صفقة", "ضم", "تعاقد", "انتقال", "يفاوض", "عرض", "يقترب من"]):
        return "transfers", "🔥 ميركاتو"
    if any(w in title for w in ["رقم", "تاريخي", "أكثر", "إحصائية", "أول لاعب", "يصل لـ", "يكسر", "قياسي"]):
        return "stats", "📊 رقم قياسي"
    if any(w in title for w in ["تشكيل", "تشكيلة", "التشكيل المتوقع"]):
        return "lineup", "📋 التشكيل"
    if any(w in title for w in ["إصابة", "يغيب", "جراحة", "خارج", "يعود"]):
        return "injury", "🏥 إصابات"
    if any(w in title for w in ["ترتيب", "جدول", "صدارة", "المتأهلين"]):
        return "standings", "📊 ترتيب"
    if any(w in title for w in ["فوز", "يفوز", "يهزم", "يسقط", "نتيجة", "يتعادل", "يتأهل", "درامي"]):
        return "results", "⚽ نتائج"
    return "general", "📰 أخبار"


def _engagement_question(cat_id, title):
    """Generate a relevant engagement question for the post"""
    questions = {
        "official": [
            "إيه رأيكم في القرار ده؟ شاركونا في الكومنتات! 👇",
            "متوقعين الخطوة دي ولا مفاجأة؟ 👇",
        ],
        "breaking": [
            "فاتكم الخبر ده ولا متابعين أول بأول؟ 👇",
            "إيه أول رد فعل ليكم؟ 👇",
        ],
        "quotes": [
            "متفقين مع الكلام ده ولا لأ؟ قولوا رأيكم! 👇",
            "كلام منطقي ولا مبالغة؟ 👇",
        ],
        "transfers": [
            "لو الصفقة دي تمت.. هتغير إيه في الفريق؟ 👇",
            "صفقة ناجحة ولا فلوس ضايعة؟ شاركنا رأيك! 👇",
        ],
        "stats": [
            "توقعتوا الرقم ده؟ 🤯👇",
            "مين يقدر يكسر الرقم ده في المستقبل؟ 👇",
        ],
        "results": [
            "توقعتوا النتيجة دي؟ 👇",
            "مين كان الأفضل في الماتش من وجهة نظركم؟ 👇",
        ],
        "injury": [
            "هيأثر غيابه على الفريق بشكل كبير ولا عندهم بدايل؟ 👇",
        ],
        "lineup": [
            "موافقين على التشكيلة دي ولا كنتوا هتغيروا حاجة؟ 👇",
        ],
        "standings": [
            "مين هياخد اللقب في الآخر من وجهة نظركم؟ 👇",
        ],
    }
    import random
    opts = questions.get(cat_id, ["شاركنا رأيك في الكومنتات! 👇"])
    return random.choice(opts)


def _smart_hashtags(title, cat_id):
    """Generate relevant hashtags based on title content"""
    tags = set()
    tag_map = {
        "صلاح": "#محمد_صلاح", "ليفربول": "#ليفربول", "أرسنال": "#أرسنال",
        "تشيلسي": "#تشيلسي", "مانشستر سيتي": "#مانشستر_سيتي",
        "مانشستر يونايتد": "#مانشستر_يونايتد", "توتنهام": "#توتنهام",
        "ريال مدريد": "#ريال_مدريد", "برشلونة": "#برشلونة",
        "بايرن": "#بايرن_ميونخ", "باريس": "#باريس_سان_جيرمان",
        "هالاند": "#هالاند", "مبابي": "#مبابي", "ساكا": "#ساكا",
        "بالمر": "#بالمر", "فينيسيوس": "#فينيسيوس", "يامال": "#يامال",
        "الأهلي": "#الأهلي", "الزمالك": "#الزمالك", "مرموش": "#مرموش",
        "البريميرليج": "#البريميرليج", "الليجا": "#الليجا",
        "دوري أبطال": "#دوري_أبطال_أوروبا", "ميركاتو": "#ميركاتو",
        "منتخب مصر": "#منتخب_مصر", "أفريقيا": "#أمم_أفريقيا",
    }
    for kw, tag in tag_map.items():
        if kw in title:
            tags.add(tag)
    if not tags:
        tags.add("#كرة_القدم")
    return " ".join(list(tags)[:5])


class MegaNewsEngine:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"posted_hashes": [], "titles_cache": []}

    def _save_state(self):
        self.state["posted_hashes"] = self.state["posted_hashes"][-1000:]
        self.state["titles_cache"] = self.state["titles_cache"][-500:]
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def is_posted(self, title):
        h = _hash(title)
        return h in self.state.get("posted_hashes", [])

    def is_similar_to_posted(self, title):
        for prev in self.state.get("titles_cache", []):
            if _similar(title, prev):
                return True
        return False

    def mark_posted(self, title):
        h = _hash(title)
        if h not in self.state["posted_hashes"]:
            self.state["posted_hashes"].append(h)
            self.state["titles_cache"].append(title)
            self._save_state()

    # ─── Source Fetchers ───

    def _fetch_direct_rss(self):
        """Fetch from all 4 direct RSS feeds with embedded images"""
        articles = []
        for src in DIRECT_RSS:
            try:
                req = urllib.request.Request(src["url"], headers=UA)
                with urllib.request.urlopen(req, timeout=12) as resp:
                    feed = feedparser.parse(resp.read())
                for entry in feed.entries:
                    title = _clean_title(entry.title)
                    summary = _extract_summary(entry)
                    if not _is_football(title, summary):
                        continue
                    img = _extract_image(entry)
                    # Upscale if needed
                    upscale = src.get("img_upscale")
                    if img and upscale:
                        img = upscale(img)
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "image_url": img,
                        "source_name": src["name"],
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "quality": src["quality"],
                    })
            except Exception as e:
                print(f"RSS error [{src['name']}]: {e}")
        return articles

    def _fetch_google_news(self, queries):
        """Fetch from Google News RSS with site-specific or topic queries"""
        articles = []
        for label, q in queries:
            encoded = urllib.parse.quote(q)
            url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:
                    raw = entry.title
                    title = _clean_title(raw)
                    summary = _extract_summary(entry)
                    if not _is_football(title, summary):
                        continue
                    articles.append({
                        "title": title,
                        "summary": summary,
                        "image_url": None,  # GN doesn't embed images
                        "source_name": f"GN:{label}",
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "quality": "medium",
                    })
            except Exception as e:
                print(f"GN error [{label}]: {e}")
        return articles

    # ─── Main Fetch Methods ───

    def fetch_fantasy_volt_news(self, limit=10):
        """
        Fantasy Volt: EPL, UCL, World Stars, Real Madrid, Barcelona
        Priority: Direct RSS (with images) > GN Topics
        """
        pool = []
        pool.extend(self._fetch_direct_rss())
        pool.extend(self._fetch_google_news(GN_TOPIC_QUERIES_FANTASY))
        pool.extend(self._fetch_google_news(GN_SITE_QUERIES))
        return self._filter_and_rank(pool, limit)

    def fetch_kora_volt_news(self, limit=10):
        """
        Kora Volt: ALL football news (Egypt, Europe, Africa, Transfers, etc.)
        Priority: Direct RSS (with images) > GN Sites > GN Topics
        """
        pool = []
        pool.extend(self._fetch_direct_rss())
        pool.extend(self._fetch_google_news(GN_SITE_QUERIES))
        pool.extend(self._fetch_google_news(GN_TOPIC_QUERIES_KORA))
        pool.extend(self._fetch_google_news(GN_TOPIC_QUERIES_FANTASY))
        return self._filter_and_rank(pool, limit)

    def _filter_and_rank(self, pool, limit):
        """Deduplicate, filter posted, and rank by quality + image + source diversity"""
        seen = set()
        filtered = []
        source_counts = {}  # Track per-source usage for diversity
        
        for art in pool:
            t = art["title"]
            # Skip if already posted
            if self.is_posted(t):
                continue
            # Skip if too similar to something already posted before
            if self.is_similar_to_posted(t):
                continue
            # Skip duplicates within this batch
            h = _hash(t)
            if h in seen:
                continue
            # Check similarity to other items in filtered
            is_dup = False
            for prev in filtered:
                if _similar(t, prev["title"]):
                    is_dup = True
                    break
            if is_dup:
                continue
            seen.add(h)
            # Detect category
            cat_id, cat_badge = _detect_category(t)
            art["cat_id"] = cat_id
            art["cat_badge"] = cat_badge
            filtered.append(art)

        # === Source-diverse ranking ===
        # Round-robin across sources so no single source dominates
        from collections import defaultdict
        by_source = defaultdict(list)
        for art in filtered:
            # Articles with images get priority within their source bucket
            by_source[art["source_name"]].append(art)
        
        # Sort each source's articles: images first, then quality
        quality_order = {"high": 0, "medium": 1, "low": 2}
        for src in by_source:
            by_source[src].sort(key=lambda a: (
                0 if a.get("image_url") else 1,
                quality_order.get(a.get("quality", "low"), 2)
            ))
        
        # Round-robin pick
        result = []
        source_keys = list(by_source.keys())
        idx = 0
        while len(result) < limit and source_keys:
            src = source_keys[idx % len(source_keys)]
            if by_source[src]:
                result.append(by_source[src].pop(0))
            else:
                source_keys.remove(src)
                if not source_keys:
                    break
                idx = idx % len(source_keys) if source_keys else 0
                continue
            idx += 1
        
        return result

    # ─── Caption Formatting ───

    def format_post(self, article, page="kora_volt"):
        """Generate a rich, engaging Facebook post from an article"""
        title = article["title"]
        summary = article.get("summary", "")
        cat_id = article.get("cat_id", "general")
        badge = article.get("cat_badge", "📰 أخبار")
        question = _engagement_question(cat_id, title)
        hashtags = _smart_hashtags(title, cat_id)

        if page == "kora_volt":
            brand_tag = "#كورة_ڤولت"
        else:
            brand_tag = "#FantasyVolt #فانتازي_ڤولت"

        # Build post: Badge | Title
        lines = [f"{badge} | {title}"]
        
        # Add summary only if it's meaningful (not just the title repeated)
        if summary and len(summary) > 25:
            lines.append("")
            lines.append(summary)
        
        # Add engagement question
        lines.append("")
        lines.append(f"💬 {question}")
        lines.append("")
        lines.append(f"{hashtags} {brand_tag}")
        return "\n".join(lines)

    # ─── Image Download ───

    def download_article_image(self, article):
        """Download the article's image to local disk, return path or None"""
        img_url = article.get("image_url")
        if not img_url:
            return None
        slug = _hash(article["title"])[:10]
        ext = "jpg"
        if ".png" in img_url.lower():
            ext = "png"
        elif ".webp" in img_url.lower():
            ext = "webp"
        dest = os.path.join(IMG_DIR, f"news_{slug}.{ext}")
        if os.path.exists(dest):
            return dest
        try:
            req = urllib.request.Request(img_url, headers=UA)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) < 2000:  # Too small, likely broken
                    return None
                with open(dest, "wb") as f:
                    f.write(data)
            return dest
        except Exception as e:
            print(f"Image download failed: {e}")
            return None
