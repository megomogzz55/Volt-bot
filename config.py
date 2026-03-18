import os

# ══════════════════════════════════════════
# Facebook — صفحة الفانتازي
# ══════════════════════════════════════════
FB_FANTASY_PAGE_ID      = os.environ.get("FB_FANTASY_PAGE_ID", "")
FB_FANTASY_ACCESS_TOKEN = os.environ.get("FB_FANTASY_ACCESS_TOKEN", "")

# Facebook — صفحة الأخبار
FB_NEWS_PAGE_ID         = os.environ.get("FB_NEWS_PAGE_ID", "")
FB_NEWS_ACCESS_TOKEN    = os.environ.get("FB_NEWS_ACCESS_TOKEN", "")

# ══════════════════════════════════════════
# Telegram
# ══════════════════════════════════════════
TG_BOT_TOKEN            = os.environ.get("TG_BOT_TOKEN", "")
TG_FANTASY_CHANNEL      = os.environ.get("TG_FANTASY_CHANNEL", "")
TG_NEWS_CHANNEL         = os.environ.get("TG_NEWS_CHANNEL", "")

# ══════════════════════════════════════════
# AI APIs
# ══════════════════════════════════════════
GROQ_API_KEY            = os.environ.get("GROQ_API_KEY", "")
GEMINI_API_KEY          = os.environ.get("GEMINI_API_KEY", "")

# ══════════════════════════════════════════
# FPL API — مجاني بدون key
# ══════════════════════════════════════════
FPL_BASE = "https://fantasy.premierleague.com/api"
FPL_BOOTSTRAP   = f"{FPL_BASE}/bootstrap-static/"
FPL_LIVE        = f"{FPL_BASE}/event/{{gw}}/live/"
FPL_FIXTURES    = f"{FPL_BASE}/fixtures/"

# ══════════════════════════════════════════
# ESPN Hidden API — مجاني بدون key
# ══════════════════════════════════════════
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"
ESPN_LEAGUES = {
    "بريميرليج":    "eng.1",
    "لاليجا":       "esp.1",
    "بوندسليجا":    "ger.1",
    "سيري A":       "ita.1",
    "الدوري المصري":"egy.1",
    "تشامبيونز":    "uefa.champions",
}

# ══════════════════════════════════════════
# الإعدادات العامة
# ══════════════════════════════════════════
PAGE_NAME_FANTASY = "فانتازي"
PAGE_NAME_NEWS    = "أخبار الكورة"

# ألوان الستايل
COLOR_TEAL  = "#00AFCC"
COLOR_CORAL = "#E85555"
