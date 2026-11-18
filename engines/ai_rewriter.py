"""
AI Rewriter Engine — Rewrite news titles & summaries using FREE LLMs
====================================================================
Supports:
- Groq (Llama 3.1 70B) — 30 req/min FREE, fastest
- Google Gemini — 15 req/min FREE, best Arabic
- Fallback: Template-based rewriting (no API needed)
"""
import os
import json
import urllib.request
import random

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load API keys from config or environment
def _get_key(name):
    # Try environment first (GitHub Actions)
    val = os.environ.get(name)
    if val:
        return val
    # Try config.json
    config_path = os.path.join(BASE_DIR, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
            return cfg.get(name)
        except Exception:
            pass
    return None


GROQ_API_KEY = _get_key("GROQ_API_KEY")
GEMINI_API_KEY = _get_key("GEMINI_API_KEY")


SYSTEM_PROMPT = """أنت محرر رياضي محترف في صفحة أخبار كرة قدم عربية.
أعد صياغة الخبر التالي بأسلوبك الخاص.
القواعد:
- اكتب بالعربية الفصحى مع لمسة مصرية خفيفة
- لا تذكر أبدًا: يلا كورة، في الجول، كووورة، وين وين، بي إن سبورت، اليوم السابع
- غير الصياغة تمامًا لكن حافظ على المعنى والحقائق
- اجعل العنوان جذابًا ومثيرًا
- أضف ملخص قصير (جملتين-3 جمل) يوضح تفاصيل الخبر
- الرد بصيغة JSON: {"title": "...", "summary": "..."}
- لا تضف معلومات من عندك أو أرقام لم تُذكر"""


def rewrite_with_groq(title, summary=""):
    """Rewrite using Groq's FREE LLMs (30 req/min)"""
    if not GROQ_API_KEY:
        return None
    
    user_msg = f"العنوان: {title}"
    if summary:
        user_msg += f"\nالتفاصيل: {summary}"
    
    try:
        import requests as _req
    except ImportError:
        return None
    
    # Try models in order of quality
    models = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "allam-2-7b"]
    
    for model in models:
        try:
            resp = _req.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_msg}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 300,
                },
                timeout=15
            )
            
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                # Clean markdown code blocks if present
                content = content.strip()
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                content = content.strip()
                result = json.loads(content)
                if result.get("title"):
                    return result
            # If model fails, try next
        except Exception:
            continue
    
    return None


def rewrite_with_gemini(title, summary=""):
    """Rewrite using Google Gemini (FREE: 15 req/min)"""
    if not GEMINI_API_KEY:
        return None
    
    user_msg = f"العنوان: {title}"
    if summary:
        user_msg += f"\nالتفاصيل: {summary}"
    
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{user_msg}"}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 300,
            "responseMimeType": "application/json",
        }
    }).encode("utf-8")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Try to parse JSON from the response
            result = json.loads(text)
            return result
    except Exception as e:
        print(f"Gemini rewrite failed: {e}")
        return None


def rewrite_with_templates(title, summary="", category="general"):
    """Fallback: template-based rewriting (no API needed)"""
    # Category-specific openers
    openers = {
        "official": ["رسميًا |", "تم الإعلان رسميًا عن", "بشكل رسمي.."],
        "breaking": ["عاجل |", "الآن |", "خبر عاجل |"],
        "transfers": ["ميركاتو |", "في سوق الانتقالات |", "صفقة جديدة |"],
        "quotes": ["تصريح ناري |", "كلام مهم |", "حديث خاص |"],
        "results": ["نتيجة |", "انتهت المباراة |", "فوز كبير |"],
        "stats": ["رقم تاريخي |", "إنجاز جديد |", "إحصائية مذهلة |"],
        "injury": ["تحديث طبي |", "خبر مقلق |", "آخر التطورات |"],
        "general": ["", "", ""],
    }
    
    # For template mode, we just prepend a category opener if not already present
    cat_openers = openers.get(category, openers["general"])
    opener = random.choice(cat_openers)
    
    # Don't double-add if title already starts with similar
    if any(title.startswith(o.rstrip(" |")) for o in cat_openers if o):
        new_title = title
    elif opener:
        new_title = f"{opener} {title}"
    else:
        new_title = title
    
    return {"title": new_title, "summary": summary}


def rewrite_article(title, summary="", category="general"):
    """
    Rewrite article using the best available method.
    Priority: Groq > Gemini > Templates (fallback)
    """
    # Try Groq first (fastest)
    result = rewrite_with_groq(title, summary)
    if result and result.get("title"):
        return result
    
    # Try Gemini
    result = rewrite_with_gemini(title, summary)
    if result and result.get("title"):
        return result
    
    # Fallback to templates
    return rewrite_with_templates(title, summary, category)
