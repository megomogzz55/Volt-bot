"""
Facebook Publishing Module for Fantasy Volt & Kora Volt
Using Facebook Graph API v22.0
"""
import os
import json
import requests

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_page_credentials(page_key="fantasy_volt"):
    # Check environment variables first (used by GitHub Actions & Cloud)
    env_token_fv = os.environ.get("FV_ACCESS_TOKEN")
    env_token_kv = os.environ.get("KV_ACCESS_TOKEN")
    
    if page_key == "fantasy_volt" and env_token_fv:
        page_id = os.environ.get("FV_PAGE_ID", "285388077999286")
        return page_id, env_token_fv
    elif page_key == "kora_volt" and env_token_kv:
        page_id = os.environ.get("KV_PAGE_ID", "300362406499652")
        return page_id, env_token_kv

    # Local fallback to config.json
    if os.path.exists(CONFIG_PATH):
        config = load_config()
        page = config.get("pages", {}).get(page_key)
        if page:
            return page["id"], page["access_token"]
            
    raise ValueError(f"Credentials for '{page_key}' not found in environment or config.json")

def post_text(message, page_key="fantasy_volt"):
    """
    Publish a plain text post to the specified Facebook page.
    """
    page_id, token = get_page_credentials(page_key)
    url = f"https://graph.facebook.com/v22.0/{page_id}/feed"
    payload = {
        "message": message,
        "access_token": token
    }
    resp = requests.post(url, data=payload, timeout=30)
    data = resp.json()
    if resp.status_code != 200:
        raise RuntimeError(f"FB Post Text Error ({resp.status_code}): {data}")
    return data

def post_photo(image_path, caption=None, page_key="fantasy_volt"):
    """
    Upload and publish a photo with optional caption to the specified Facebook page.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    page_id, token = get_page_credentials(page_key)
    url = f"https://graph.facebook.com/v22.0/{page_id}/photos"
    
    data = {
        "access_token": token
    }
    if caption:
        data["caption"] = caption

    with open(image_path, "rb") as img_file:
        files = {"source": img_file}
        resp = requests.post(url, data=data, files=files, timeout=60)
        res_data = resp.json()
        if resp.status_code != 200:
            raise RuntimeError(f"FB Post Photo Error ({resp.status_code}): {res_data}")
        return res_data

def verify_token(page_key="fantasy_volt"):
    page_id, token = get_page_credentials(page_key)
    url = f"https://graph.facebook.com/v22.0/{page_id}"
    params = {"fields": "id,name,link", "access_token": token}
    resp = requests.get(url, params=params, timeout=15)
    return resp.json()

if __name__ == "__main__":
    print("Testing Facebook module...")
    fv = verify_token("fantasy_volt")
    print("Fantasy Volt Status:", fv)
    kv = verify_token("kora_volt")
    print("Kora Volt Status:", kv)
