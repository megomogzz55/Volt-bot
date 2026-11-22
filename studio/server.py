"""
Volt Card Studio — Local Interactive Template & Card Design Server.
Allows visual real-time editing, testing with live football news & player cutouts,
saving custom template presets, and one-click Facebook test posting.
"""

import os
import sys
import json
import base64
import time
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

app = FastAPI(title="Volt Card Studio", version="1.0.0")

STUDIO_DIR = os.path.join(BASE_DIR, "studio")
STATIC_DIR = os.path.join(STUDIO_DIR, "static")
TEMPLATES_CONFIG_PATH = os.path.join(BASE_DIR, "assets", "templates", "custom_templates.json")

# Ensure directories exist
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)


# ══════════════════════════════════════════════════════════════
# API ROUTES: RESOURCES & DATA
# ══════════════════════════════════════════════════════════════

@app.get("/api/resources")
def get_resources():
    """Lists all available templates, fonts, cutouts, sample photos and custom presets."""
    templates_dir = os.path.join(BASE_DIR, "assets", "templates")
    fonts_dir = os.path.join(BASE_DIR, "assets", "fonts")
    output_dir = os.path.join(BASE_DIR, "output")
    
    # 1. Templates
    templates = [
        {"id": "kora_breaking", "name": "كورة ڤولت — قالب العاجل (1350×1688)", "width": 1350, "height": 1688, "url": "/assets/templates/kora_volt/breaking.png"},
        {"id": "kora_manchette", "name": "كورة ڤولت — قالب المانشيت الطولي (2160×2700)", "width": 2160, "height": 2700, "url": "/assets/templates/kora_volt/manchette.png"},
        {"id": "blank_card", "name": "لوحة بيضاء فارغة (1350×1688)", "width": 1350, "height": 1688, "url": ""}
    ]
    
    # Scan custom uploaded templates
    custom_dir = os.path.join(templates_dir, "custom")
    if os.path.exists(custom_dir):
        for f in os.listdir(custom_dir):
            if f.endswith(('.png', '.jpg', '.webp')):
                templates.append({
                    "id": f"custom_{f}",
                    "name": f"قالب مخصص: {f}",
                    "width": 1350,
                    "height": 1688,
                    "url": f"/assets/templates/custom/{f}"
                })
                
    # 2. Player Cutouts
    cutouts = []
    # Collect from output and assets
    search_dirs = [output_dir, os.path.join(BASE_DIR, "assets", "vectors")]
    for d in search_dirs:
        if os.path.exists(d):
            for root, _, files in os.walk(d):
                for f in files:
                    if "cutout" in f.lower() or "transparent" in f.lower() or "vector" in f.lower():
                        if f.endswith(('.png', '.webp')):
                            rel = os.path.relpath(os.path.join(root, f), BASE_DIR).replace("\\", "/")
                            name_clean = f.replace("_vector_cutout", "").replace("_cutout", "").replace("_transparent", "").replace(".png", "").replace("_", " ").title()
                            cutouts.append({
                                "id": f,
                                "name": name_clean,
                                "url": f"/{rel}"
                            })
                            
    # Deduplicate cutouts by url
    seen_urls = set()
    unique_cutouts = []
    for c in cutouts:
        if c["url"] not in seen_urls:
            seen_urls.add(c["url"])
            unique_cutouts.append(c)

    # 3. Sample background photos
    photos = [
        {"name": "خلفية ملعب ليلية سينمائية", "url": "/assets/templates/default_football_bg.jpg"},
        {"name": "خلفية إضاءة رياضية ذكية", "url": "/output/ai_bg_sports.jpg"},
    ]
    news_photos_dir = os.path.join(output_dir, "news_photos")
    if os.path.exists(news_photos_dir):
        for f in os.listdir(news_photos_dir)[:8]:
            if f.endswith(('.jpg', '.png', '.jpeg')):
                photos.append({
                    "name": f"صورة خبر: {f[:18]}...",
                    "url": f"/output/news_photos/{f}"
                })

    # 4. Custom Saved Presets
    custom_presets = {}
    if os.path.exists(TEMPLATES_CONFIG_PATH):
        try:
            with open(TEMPLATES_CONFIG_PATH, "r", encoding="utf-8") as f:
                custom_presets = json.load(f)
        except Exception:
            pass

    return {
        "templates": templates,
        "cutouts": unique_cutouts,
        "photos": photos,
        "custom_presets": custom_presets
    }


@app.get("/api/live_feed")
def get_live_feed():
    """Fetches real sports news and statements from live RSS feeds to test designs instantly."""
    from engines.mega_news_engine import MegaNewsEngine
    engine = MegaNewsEngine()
    articles = engine.fetch_kora_volt_news(limit=12)
    
    samples = []
    for a in articles[:12]:
        title = a.get("title", "")
        # Clean title
        title_clean = title.split(" - ")[0].split(" | ")[0].strip()
        samples.append({
            "title": title_clean,
            "summary": a.get("summary", ""),
            "source": a.get("source", "كورة ڤولت"),
            "photo_url": a.get("photo_url", "")
        })
    return {"articles": samples}


@app.post("/api/upload_template")
async def upload_template(file: UploadFile = File(...)):
    """Upload a new template overlay PNG."""
    custom_dir = os.path.join(BASE_DIR, "assets", "templates", "custom")
    os.makedirs(custom_dir, exist_ok=True)
    
    fname = file.filename or f"tmpl_{int(time.time())}.png"
    file_path = os.path.join(custom_dir, fname)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    return {
        "status": "success",
        "filename": fname,
        "url": f"/assets/templates/custom/{fname}"
    }


@app.post("/api/upload_image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an arbitrary background or player image."""
    up_dir = os.path.join(BASE_DIR, "output", "uploads")
    os.makedirs(up_dir, exist_ok=True)
    
    fname = file.filename or f"img_{int(time.time())}.jpg"
    file_path = os.path.join(up_dir, fname)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    return {
        "status": "success",
        "url": f"/output/uploads/{fname}"
    }


@app.post("/api/generate_ai_bg")
def generate_ai_bg(prompt: str = Form(...)):
    """Generate background with Cloudflare FLUX."""
    try:
        from engines.cloudflare_ai import generate_flux_image
        p = generate_flux_image(prompt)
        rel = os.path.relpath(p, BASE_DIR).replace("\\", "/")
        return {"status": "success", "url": f"/{rel}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/generate_ai_vector")
def generate_ai_vector(player_name: str = Form(...), club: str = Form("")):
    """Generate player vector cartoon and auto-remove background with u2net."""
    try:
        from engines.player_vector_engine import generate_cartoon_player
        cutout_path = generate_cartoon_player(player_name, club_or_country=club, model="leonardo", isolate_bg=True)
        rel = os.path.relpath(cutout_path, BASE_DIR).replace("\\", "/")
        return {"status": "success", "url": f"/{rel}", "player": player_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/isolate_bg")
def isolate_bg(image_url: str = Form(...)):
    """Removes background from any image URL or local path using Rembg u2net."""
    try:
        from engines.player_vector_engine import remove_background
        # Map URL to local path
        clean_url = image_url.lstrip("/")
        local_path = os.path.join(BASE_DIR, clean_url.replace("/", os.sep))
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found for {image_url}")
            
        cutout = remove_background(local_path)
        rel = os.path.relpath(cutout, BASE_DIR).replace("\\", "/")
        return {"status": "success", "url": f"/{rel}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


class SavePresetRequest(BaseModel):
    preset_name: str
    preset_data: dict

@app.post("/api/save_preset")
def save_preset(req: SavePresetRequest):
    """Saves customized template configuration so the engine can reuse it."""
    presets = {}
    if os.path.exists(TEMPLATES_CONFIG_PATH):
        try:
            with open(TEMPLATES_CONFIG_PATH, "r", encoding="utf-8") as f:
                presets = json.load(f)
        except Exception:
            pass
            
    presets[req.preset_name] = req.preset_data
    with open(TEMPLATES_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)
        
    return {"status": "success", "message": f"تم حفظ القالب: {req.preset_name}"}


class PublishRequest(BaseModel):
    image_base64: str
    caption: str
    target_page: str = "kora_volt" # or fantasy_volt

@app.post("/api/publish_card")
def publish_card(req: PublishRequest):
    """Publishes the created card directly to Facebook."""
    try:
        from publish.fb import post_photo
        # Decode base64 and save to temp file
        header, b64_data = req.image_base64.split(",", 1) if "," in req.image_base64 else ("", req.image_base64)
        raw_bytes = base64.b64decode(b64_data)
        
        out_path = os.path.join(BASE_DIR, "output", f"studio_publish_{int(time.time())}.jpg")
        with open(out_path, "wb") as f:
            f.write(raw_bytes)
            
        page_key = "fantasy_volt" if "fantasy" in req.target_page.lower() else "kora_volt"
        res = post_photo(image_path=out_path, caption=req.caption, page_key=page_key)
        post_id = res.get("id") or res.get("post_id", "published")
        return {"status": "success", "post_id": post_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ══════════════════════════════════════════════════════════════
# STATIC FILE MOUNTING & HOME PAGE
# ══════════════════════════════════════════════════════════════

# Mount assets and output directories for image serving
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/output", StaticFiles(directory=os.path.join(BASE_DIR, "output")), name="output")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Volt Card Studio is loading...</h1>"


if __name__ == "__main__":
    import uvicorn
    print("\n" + "═"*60)
    print("⚡ VOLT CARD STUDIO IS STARTING ON: http://localhost:5050")
    print("═"*60 + "\n")
    uvicorn.run("studio.server:app", host="127.0.0.1", port=5050, reload=True)
