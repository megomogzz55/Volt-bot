"""
Player Face & Vector Art Engine (Automated 100% Free)
- Source 1: FPL Official Premier League CDN (670+ transparent studio cutouts)
- Source 2: Wikipedia / Wikimedia Commons API (European & World Stars)
- Tool: High-Performance Pure PIL Pop-Art Cel-Shaded Vectorizer
- Cache: assets/vectors/cache/{player_slug}.png
"""
import os
import re
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "assets", "vectors", "cache")
RAW_CACHE_DIR = os.path.join(BASE_DIR, "assets", "vectors", "raw")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RAW_CACHE_DIR, exist_ok=True)

# Tier-1 Superstars registry: maps Arabic and English aliases to (source_type, identifier)
# source_type: 'fpl' (uses FPL code) or 'wiki' (uses Wikipedia search slug)
SUPERSTAR_REGISTRY = {
    # Premier League Superstars (FPL CDN: transparent 500x500 PNG)
    "هالاند": ("fpl", 223094, "haaland"),
    "إيرلينج هالاند": ("fpl", 223094, "haaland"),
    "haaland": ("fpl", 223094, "haaland"),
    
    "صلاح": ("local_or_wiki", "Mohamed_Salah", "salah"),
    "محمد صلاح": ("local_or_wiki", "Mohamed_Salah", "salah"),
    "salah": ("local_or_wiki", "Mohamed_Salah", "salah"),
    
    "ساكا": ("fpl", 223340, "saka"),
    "بوكايو ساكا": ("fpl", 223340, "saka"),
    "saka": ("fpl", 223340, "saka"),
    
    "بالمر": ("fpl", 244851, "palmer"),
    "كول بالمر": ("fpl", 244851, "palmer"),
    "palmer": ("fpl", 244851, "palmer"),
    
    "فودين": ("fpl", 209244, "foden"),
    "فيل فودين": ("fpl", 209244, "foden"),
    "foden": ("fpl", 209244, "foden"),
    
    "إيزاك": ("fpl", 219168, "isak"),
    "ألكسندر إيزاك": ("fpl", 219168, "isak"),
    "isak": ("fpl", 219168, "isak"),
    
    "واتكينز": ("fpl", 178301, "watkins"),
    "أولي واتكينز": ("fpl", 178301, "watkins"),
    "watkins": ("fpl", 178301, "watkins"),
    
    "ماينو": ("fpl", 516895, "mainoo"),
    "كوبي ماينو": ("fpl", 516895, "mainoo"),
    "mainoo": ("fpl", 516895, "mainoo"),
    
    "جارناتشو": ("fpl", 493105, "garnacho"),
    "أليخاندرو جارناتشو": ("fpl", 493105, "garnacho"),
    "garnacho": ("fpl", 493105, "garnacho"),
    
    "برونو": ("fpl", 141746, "bruno"),
    "برونو فيرنانديز": ("fpl", 141746, "bruno"),
    "fernandes": ("fpl", 141746, "bruno"),
    
    "جاكبو": ("fpl", 243298, "gakpo"),
    "كودي جاكبو": ("fpl", 243298, "gakpo"),
    "gakpo": ("fpl", 243298, "gakpo"),
    
    "دياز": ("fpl", 244731, "diaz"),
    "لويس دياز": ("fpl", 244731, "diaz"),
    "diaz": ("fpl", 244731, "diaz"),
    
    "رايس": ("fpl", 204480, "rice"),
    "ديكلان رايس": ("fpl", 204480, "rice"),
    "rice": ("fpl", 204480, "rice"),
    
    "سون": ("fpl", 85971, "son"),
    "سون هيونج مين": ("fpl", 85971, "son"),
    "son": ("fpl", 85971, "son"),
    
    "دي بروين": ("fpl", 61366, "debruyne"),
    "كيفين دي بروين": ("fpl", 61366, "debruyne"),
    "de bruyne": ("fpl", 61366, "debruyne"),
    
    # World & European Superstars (Wikipedia / Local)
    "مبابي": ("wiki", "Kylian Mbappé", "mbappe"),
    "كيليان مبابي": ("wiki", "Kylian Mbappé", "mbappe"),
    "mbappe": ("wiki", "Kylian Mbappé", "mbappe"),
    
    "فينيسيوس": ("wiki", "Vinícius Júnior", "vinicius"),
    "فينيسيوس جونيور": ("wiki", "Vinícius Júnior", "vinicius"),
    "vinicius": ("wiki", "Vinícius Júnior", "vinicius"),
    
    "بيلينجهام": ("wiki", "Jude Bellingham", "bellingham"),
    "جود بيلينجهام": ("wiki", "Jude Bellingham", "bellingham"),
    "bellingham": ("wiki", "Jude Bellingham", "bellingham"),
    
    "يامال": ("wiki", "Lamine Yamal", "yamal"),
    "لامين يامال": ("wiki", "Lamine Yamal", "yamal"),
    "yamal": ("wiki", "Lamine Yamal", "yamal"),
    
    "كين": ("wiki", "Harry Kane", "kane"),
    "هاري كين": ("wiki", "Harry Kane", "kane"),
    "kane": ("wiki", "Harry Kane", "kane"),
    
    "ليفاندوفسكي": ("wiki", "Robert Lewandowski", "lewandowski"),
    "روبرت ليفاندوفسكي": ("wiki", "Robert Lewandowski", "lewandowski"),
    "lewandowski": ("wiki", "Robert Lewandowski", "lewandowski"),
    
    "رودريجو": ("wiki", "Rodrygo", "rodrygo"),
    "rodrygo": ("wiki", "Rodrygo", "rodrygo"),
    
    "فالفيردي": ("wiki", "Federico Valverde", "valverde"),
    "فيديريكو فالفيردي": ("wiki", "Federico Valverde", "valverde"),
    "valverde": ("wiki", "Federico Valverde", "valverde")
}


def is_superstar_player(player_name):
    """
    Checks if a player is in the Superstar tier.
    Returns (True, entry_tuple) or (False, None).
    """
    clean = str(player_name).strip().lower()
    # Check exact match
    if clean in SUPERSTAR_REGISTRY:
        return True, SUPERSTAR_REGISTRY[clean]
    # Check substring match
    for k, val in SUPERSTAR_REGISTRY.items():
        if k in clean:
            return True, val
    return False, None


def download_fpl_cutout(code, raw_path):
    """Downloads official 500x500 transparent PNG from Premier League CDN."""
    url = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{code}.png"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp, open(raw_path, 'wb') as f:
        f.write(resp.read())
    return raw_path


def download_wiki_portrait(query_title, raw_path):
    """Fetches high-res portrait thumbnail from Wikipedia API."""
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(query_title)}&prop=pageimages&format=json&pithumbsize=900"
    req = urllib.request.Request(url, headers={'User-Agent': 'VoltFootballBot/1.0 (contact: info@kora-volt.com)'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    
    pages = data.get('query', {}).get('pages', {})
    thumb_url = None
    for pid, pdata in pages.items():
        if 'thumbnail' in pdata:
            thumb_url = pdata['thumbnail']['source']
            break
            
    if not thumb_url:
        raise ValueError(f"No Wikipedia thumbnail found for {query_title}")
        
    img_req = urllib.request.Request(thumb_url, headers={'User-Agent': 'VoltFootballBot/1.0'})
    with urllib.request.urlopen(img_req, timeout=10) as resp, open(raw_path, 'wb') as f:
        f.write(resp.read())
    return raw_path


def photo_to_vector_art(raw_image_path, out_vector_path, num_colors=12):
    """
    Automated Vectorizer & Pop-Art Stylizer (Pure PIL):
    1. Bilateral-like smoothing to flatten skin tone
    2. Vibrant color & contrast boost
    3. Cel-shading color quantization
    4. Bold comic ink outlines extraction
    5. Multiply composite & alpha retention
    """
    img = Image.open(raw_image_path).convert('RGBA')
    alpha = img.split()[-1]
    ext = alpha.getextrema()
    has_alpha = False
    if isinstance(ext, tuple):
        has_alpha = ext[0] < 250
    
    rgb_img = img.convert('RGB')
    
    # 1. Bilateral smoothing (multi-pass median + smooth)
    smoothed = rgb_img.filter(ImageFilter.MedianFilter(size=5))
    smoothed = smoothed.filter(ImageFilter.SMOOTH_MORE)
    
    # 2. Boost color vibrancy & contrast
    vibrant = ImageEnhance.Color(smoothed).enhance(1.4)
    high_contrast = ImageEnhance.Contrast(vibrant).enhance(1.3)
    
    # 3. Posterize / Quantize to create cel-shading flats
    cel_shaded = high_contrast.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT).convert('RGB')
    
    # 4. Bold Comic Ink Outlines
    gray = rgb_img.convert('L').filter(ImageFilter.GaussianBlur(1.2))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    ink_mask = edges.point(lambda p: 0 if p > 35 else 255)
    ink_mask = ink_mask.filter(ImageFilter.MinFilter(size=3))
    
    # 5. Multiply ink outlines over cel-shaded image
    ink_rgb = Image.merge('RGB', [ink_mask, ink_mask, ink_mask])
    blended = ImageChops.multiply(cel_shaded, ink_rgb)
    
    # 6. Final punchy color enhancement
    final = ImageEnhance.Color(blended).enhance(1.15)
    
    if has_alpha:
        final_rgba = final.convert('RGBA')
        final_rgba.putalpha(alpha)
        final_rgba.save(out_vector_path, 'PNG')
    else:
        final.save(out_vector_path, 'JPEG', quality=95)
        
    return out_vector_path


def get_player_vector_art(player_name):
    """
    Main Entry Point:
    - If ordinary player -> returns None (signals Pure Typography mode)
    - If superstar -> returns path to cached or newly generated vector illustration PNG
    """
    is_star, info = is_superstar_player(player_name)
    if not is_star or info is None:
        return None
        
    src_type, identifier, slug = info
    cached_vector = os.path.join(CACHE_DIR, f"{slug}_vector.png")
    
    # Check if cached vector exists
    if os.path.exists(cached_vector):
        return cached_vector
        
    # Check if manual vector exists in assets/vectors/
    manual_files = [f"{slug}_pop.jpg", f"{slug}.jpg", f"{slug}_transparent.png", f"{slug}.png"]
    for mf in manual_files:
        p = os.path.join(BASE_DIR, "assets", "vectors", mf)
        if os.path.exists(p):
            return p
            
    # Automated Fetch & Vectorize Pipeline
    raw_path = os.path.join(RAW_CACHE_DIR, f"{slug}_raw.png")
    try:
        if src_type == "fpl":
            print(f"⚡ Auto-fetching official FPL cutout for '{player_name}' (code: {identifier})...")
            download_fpl_cutout(identifier, raw_path)
        elif src_type == "wiki":
            print(f"⚡ Auto-fetching Wikipedia portrait for '{player_name}' ({identifier})...")
            download_wiki_portrait(identifier, raw_path)
        else: # local_or_wiki
            try:
                download_wiki_portrait(identifier, raw_path)
            except Exception:
                pass
                
        if os.path.exists(raw_path):
            print(f"🎨 Auto-vectorizing player photo for '{slug}'...")
            photo_to_vector_art(raw_path, cached_vector)
            return cached_vector
            
    except Exception as e:
        print(f"Warning: Failed to auto-vectorize {player_name}: {e}")
        
    return None
