"""
Template Registry — Manages and separates templates for Kora Volt vs Fantasy Volt.
Provides instant lookup based on target page and card type.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_ROOT = os.path.join(BASE_DIR, "assets", "templates")


TEMPLATE_MAP = {
    "kora_volt": {
        "breaking": os.path.join(TEMPLATES_ROOT, "kora_volt", "breaking.png"),
        "manchette": os.path.join(TEMPLATES_ROOT, "kora_volt", "manchette.png"),
        # Future templates for Kora Volt:
        # "matchday": os.path.join(TEMPLATES_ROOT, "kora_volt", "matchday.png"),
        # "lineup": os.path.join(TEMPLATES_ROOT, "kora_volt", "lineup.png"),
        # "fulltime": os.path.join(TEMPLATES_ROOT, "kora_volt", "fulltime.png"),
    },
    "fantasy_volt": {
        # Reserved for Fantasy Volt templates (Purple/Green EPL brand)
        "breaking": os.path.join(TEMPLATES_ROOT, "fantasy_volt", "breaking.png"),
        "stats": os.path.join(TEMPLATES_ROOT, "fantasy_volt", "stats.png"),
        "picks": os.path.join(TEMPLATES_ROOT, "fantasy_volt", "picks.png"),
        "prices": os.path.join(TEMPLATES_ROOT, "fantasy_volt", "prices.png"),
    }
}


def get_template(page: str = "kora_volt", card_type: str = "breaking") -> str:
    """Returns absolute path to the requested template, checking existence."""
    page_key = "fantasy_volt" if "fantasy" in page.lower() else "kora_volt"
    tmpl_path = TEMPLATE_MAP.get(page_key, {}).get(card_type)
    
    if tmpl_path and os.path.exists(tmpl_path):
        return tmpl_path
        
    # Fallback to Kora Volt default if Fantasy Volt template not uploaded yet
    fallback = TEMPLATE_MAP["kora_volt"].get(card_type) or TEMPLATE_MAP["kora_volt"]["breaking"]
    return fallback
