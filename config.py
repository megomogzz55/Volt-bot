import os

class Config:
    # ══════════════════════════════════════════
    # Facebook & Telegram (The Dispatcher)
    # ══════════════════════════════════════════
    # صفحة الفانتازي
    FB_FANTASY_PAGE_ID      = os.environ.get("FB_FANTASY_PAGE_ID", "")
    FB_FANTASY_ACCESS_TOKEN = os.environ.get("FB_FANTASY_ACCESS_TOKEN", "")
    
    # صفحة الكورة
    FB_NEWS_PAGE_ID         = os.environ.get("FB_KORA_PAGE_ID", "")
    FB_NEWS_ACCESS_TOKEN    = os.environ.get("FB_KORA_ACCESS_TOKEN", "")

    # تليجرام
    TG_BOT_TOKEN            = os.environ.get("TG_BOT_TOKEN", "")
    TG_FANTASY_CHANNEL      = os.environ.get("TG_FANTASY_CHANNEL", "")
    TG_NEWS_CHANNEL         = os.environ.get("TG_NEWS_CHANNEL", "")

    # ══════════════════════════════════════════
    # AI & Multi-Tokens (The Brain)
    # ══════════════════════════════════════════
    HF_TOKENS      = os.environ.get("HF_TOKENS", "").split(",") # جيش التوكنز
    GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "") # للكابشن الذكي
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "") # للصور

    # ══════════════════════════════════════════
    # APIs Endpoints (The Sources)
    # ══════════════════════════════════════════
    # FPL API
    FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
    FPL_FIXTURES  = "https://fantasy.premierleague.com/api/fixtures/"
    
    # ESPN Hidden API
    ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"
    ESPN_LEAGUES = {
        "eng.1": "بريميرليج", "esp.1": "لاليجا", "ger.1": "بوندسليجا",
        "ita.1": "سيري A", "egy.1": "الدوري المصري", "uefa.champions": "تشامبيونز"
    }

    # ══════════════════════════════════════════
    # R2 Storage & Visual Style
    # ══════════════════════════════════════════
    R2_ENDPOINT   = os.environ.get("R2_ENDPOINT")
    R2_ACCESS_KEY = os.environ.get("R2_ACCESS_KEY")
    R2_SECRET_KEY = os.environ.get("R2_SECRET_KEY")
    R2_BUCKET     = "volt-assets"
    CDN_URL       = os.environ.get("CDN_URL") # رابط الـ CDN الدائم

    # ألوان الهوية البصرية (Fantasy Volt Style)
    COLOR_TEAL  = "#00AFCC"
    COLOR_CORAL = "#E85555"
