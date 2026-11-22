import os
import base64

BASE_DIR = r"C:\Users\Mogz\fantasy-volt"
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Encode all available fonts
font_files = {
    "AraJozoor": ("AraJozoor-Regular.ttf", "truetype"),
    "Ebhaar": ("Ebhaar.woff2", "woff2"),
    "Horizon": ("Horizon.woff2", "woff2"),
    "DroidKufi": ("DroidKufi-Bold.ttf", "truetype"),
    "LavaPro": ("LavaPro-Grunge.woff2", "woff2"),
    "ZuumeRough": ("ZuumeRough-Bold.woff2", "woff2")
}

font_faces_css = []
for font_name, (fname, fmt) in font_files.items():
    p = os.path.join(FONTS_DIR, fname)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        font_faces_css.append(f"""
        @font-face {{
            font-family: '{font_name}';
            src: url('data:font/{fmt};charset=utf-8;base64,{b64}') format('{fmt}');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }}
        """)
        print(f"✅ Encoded font: {font_name} ({len(b64)//1024} KB)")

print(f"Total font faces: {len(font_faces_css)}")
