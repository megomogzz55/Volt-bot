"""
Cloudflare Workers AI Engine — Ultra-fast free AI image generation & LLMs.
Uses:
- Image: @cf/black-forest-labs/flux-1-schnell (1024x1024 FLUX, 4 steps, ~2.5s)
- LLM: @cf/meta/llama-3.1-70b-instruct (Text rewriting & translation)
"""

import base64
import json
import os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def _get_credentials():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            pass
            
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID") or cfg.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN") or cfg.get("CLOUDFLARE_API_TOKEN")
    return account_id, token


def generate_flux_image(prompt: str, output_path: str = None) -> str:
    """
    Generates a 1024x1024 AI image using FLUX.1 Schnell via Cloudflare Workers AI.
    Runs in ~2.5 seconds.
    """
    account_id, token = _get_credentials()
    if not account_id or not token:
        raise ValueError("Cloudflare credentials not found in config.json or environment")
        
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"prompt": prompt}
    
    resp = requests.post(url, headers=headers, json=payload, timeout=45)
    if resp.status_code != 200:
        raise RuntimeError(f"Cloudflare FLUX API Error: {resp.status_code} - {resp.text[:200]}")
        
    res = resp.json()
    b64_img = res.get("result", {}).get("image")
    if not b64_img:
        raise ValueError("No image data in Cloudflare FLUX response")
        
    img_bytes = base64.b64decode(b64_img)
    if not output_path:
        import hashlib
        h = hashlib.md5(prompt.encode()).hexdigest()[:8]
        output_path = os.path.join(OUTPUT_DIR, f"cf_flux_{h}.jpg")
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)
        
    return output_path


def rewrite_with_cloudflare(title: str, summary: str = "") -> dict:
    """
    Rewrites article title and summary into Arabic using Cloudflare LLaMA 3.1 70B.
    """
    account_id, token = _get_credentials()
    if not account_id or not token:
        return {}
        
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3.1-70b-instruct"
    headers = {"Authorization": f"Bearer {token}"}
    
    system_prompt = (
        "أنت محرر رياضي محترف. أعد صياغة الخبر التالي بعنوان جذاب ومختصر في سطرين، "
        "مع ملخص في جملتين. إذا كان الخبر بالإنجليزية ترجمه لعربية فصحى مشوقة. "
        "ممنوع ذكر أي منافسين عرب. الرد بصيغة JSON فقط: {\"title\": \"...\", \"summary\": \"...\"}"
    )
    user_content = f"العنوان: {title}\nالملخص: {summary}"
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.5,
        "max_tokens": 300
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code == 200:
            raw_text = resp.json().get("result", {}).get("response", "").strip()
            # Clean markdown code blocks if any
            if "```" in raw_text:
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:].strip()
            return json.loads(raw_text)
    except Exception as e:
        print(f"Cloudflare LLM error: {e}")
        
    return {}
