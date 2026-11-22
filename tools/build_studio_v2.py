import os
import base64

BASE_DIR = r"C:\Users\Mogz\fantasy-volt"
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Encode all fonts
font_files = {
    "AraJozoor": ("AraJozoor-Regular.ttf", "truetype"),
    "Ebhaar": ("Ebhaar.woff2", "woff2"),
    "Horizon": ("Horizon.woff2", "woff2"),
    "DroidKufi": ("DroidKufi-Bold.ttf", "truetype"),
    "LavaPro": ("LavaPro-Grunge.woff2", "woff2"),
    "ZuumeRough": ("ZuumeRough-Bold.woff2", "woff2")
}

font_faces = []
for font_name, (fname, fmt) in font_files.items():
    p = os.path.join(FONTS_DIR, fname)
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        font_faces.append(f"""
        @font-face {{
            font-family: '{font_name}';
            src: url('data:font/{fmt};charset=utf-8;base64,{b64}') format('{fmt}');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }}
        """)

all_fonts_css = "\n".join(font_faces)

html_code = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volt Card Studio — أستوديو تصاميم وقوالب ڤولت الاحترافي</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        {all_fonts_css}

        :root {{
            --bg-base: #06090e;
            --bg-surface: #0b1019;
            --bg-card: #121824;
            --bg-input: #172030;
            --border: #1e293b;
            --border-hover: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --cyan: #00d2ff;
            --blue: #0084d1;
            --gold: #ffb703;
            --emerald: #10b981;
            --rose: #f43f5e;
            --font-ui: 'Cairo', system-ui, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: var(--font-ui);
            -webkit-font-smoothing: antialiased;
        }}

        body {{
            background: var(--bg-base);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            user-select: none;
        }}

        /* TOP NAVIGATION */
        .topbar {{
            height: 58px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 18px;
            z-index: 100;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .brand-icon {{
            width: 34px;
            height: 34px;
            background: linear-gradient(135deg, rgba(0,210,255,0.25), rgba(0,119,182,0.4));
            border: 1px solid rgba(0,210,255,0.4);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 0 15px rgba(0,210,255,0.25);
        }}

        .brand-title {{
            font-family: 'AraJozoor', sans-serif;
            font-size: 18px;
            font-weight: 900;
            letter-spacing: 1.2px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .brand-badge {{
            background: rgba(0, 210, 255, 0.15);
            border: 1px solid rgba(0, 210, 255, 0.3);
            color: var(--cyan);
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 800;
        }}

        .topbar-center {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .preset-pill-group {{
            display: flex;
            background: var(--bg-base);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 3px;
            gap: 3px;
        }}

        .preset-pill {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .preset-pill:hover {{
            color: #ffffff;
        }}

        .preset-pill.active {{
            background: var(--bg-card);
            color: var(--cyan);
            box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            border: 1px solid rgba(0, 210, 255, 0.25);
        }}

        .dimension-tag {{
            font-size: 11px;
            color: var(--text-muted);
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 5px 9px;
            border-radius: 6px;
            font-family: monospace;
            font-weight: 700;
        }}

        .topbar-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn {{
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid transparent;
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}

        .btn-outline {{
            background: var(--bg-card);
            border-color: var(--border);
            color: var(--text-main);
        }}

        .btn-outline:hover {{
            background: var(--bg-input);
            border-color: var(--cyan);
            color: var(--cyan);
        }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--blue), #023e8a);
            color: #ffffff;
        }}

        .btn-primary:hover {{
            filter: brightness(1.15);
            box-shadow: 0 0 12px rgba(0, 132, 209, 0.4);
        }}

        .btn-accent {{
            background: linear-gradient(135deg, var(--cyan), var(--blue));
            color: #030712;
            font-weight: 900;
        }}

        .btn-accent:hover {{
            filter: brightness(1.1);
            box-shadow: 0 0 16px rgba(0, 210, 255, 0.5);
        }}

        /* MAIN APP LAYOUT */
        .app-body {{
            display: flex;
            flex: 1;
            height: calc(100vh - 58px);
            overflow: hidden;
        }}

        /* WORKSPACE (CENTER / LEFT) */
        .workspace {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: radial-gradient(circle at center, #0f1624 0%, #06090e 100%);
            position: relative;
            overflow: hidden;
        }}

        .workspace-bar {{
            height: 40px;
            background: rgba(11, 16, 25, 0.85);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            z-index: 10;
        }}

        .zoom-group {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .tool-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
        }}

        .tool-btn:hover {{
            border-color: var(--cyan);
            color: var(--cyan);
        }}

        .canvas-area {{
            flex: 1;
            overflow: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
        }}

        .canvas-frame {{
            position: relative;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.85), 0 0 0 1px rgba(0, 210, 255, 0.15);
            border-radius: 8px;
            overflow: hidden;
            line-height: 0;
            background: #000;
        }}

        #cardCanvas {{
            display: block;
            cursor: grab;
        }}

        #cardCanvas:active {{
            cursor: grabbing;
        }}

        /* SIDEBAR (RIGHT / CONTROLS) */
        .sidebar {{
            width: 500px;
            background: var(--bg-surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            z-index: 20;
        }}

        .nav-tabs {{
            display: flex;
            background: var(--bg-base);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 30;
        }}

        .nav-tab {{
            flex: 1;
            padding: 12px 6px;
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            color: var(--text-muted);
            font-size: 12px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }}

        .nav-tab:hover {{
            color: var(--text-main);
        }}

        .nav-tab.active {{
            color: var(--cyan);
            border-bottom-color: var(--cyan);
            background: rgba(0, 210, 255, 0.04);
        }}

        .panel-body {{
            padding: 16px;
            display: none;
            flex-direction: column;
            gap: 12px;
        }}

        .panel-body.active {{
            display: flex;
        }}

        /* BOX CARDS */
        .box {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 9px;
            padding: 13px;
            display: flex;
            flex-direction: column;
            gap: 9px;
            transition: border-color 0.2s;
        }}

        .box:hover {{
            border-color: var(--border-hover);
        }}

        .box-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 6px;
        }}

        .box-title {{
            font-size: 12px;
            font-weight: 800;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .box-action {{
            font-size: 11px;
            color: var(--cyan);
            background: rgba(0, 210, 255, 0.1);
            border: 1px solid rgba(0, 210, 255, 0.2);
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
        }}

        /* LAYER SELECTOR STRIP */
        .layers-strip {{
            display: flex;
            gap: 5px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .layer-btn {{
            background: var(--bg-base);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}

        .layer-btn:hover {{
            border-color: var(--cyan);
            color: #ffffff;
        }}

        .layer-btn.active {{
            background: var(--bg-input);
            border-color: var(--cyan);
            color: var(--cyan);
            box-shadow: 0 0 8px rgba(0, 210, 255, 0.2);
        }}

        .btn-add-layer {{
            background: rgba(0, 210, 255, 0.15);
            border: 1px dashed var(--cyan);
            color: var(--cyan);
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 800;
            cursor: pointer;
            white-space: nowrap;
        }}

        /* FORM CONTROLS */
        label {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 700;
            display: block;
            margin-bottom: 3px;
        }}

        input[type="text"], textarea, select {{
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 7px 9px;
            color: #ffffff;
            font-size: 12px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        input[type="text"]:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: var(--cyan);
            box-shadow: 0 0 8px rgba(0, 210, 255, 0.25);
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 7px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 7px;
        }}

        .slider-item {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .slider-header {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
        }}

        .slider-val {{
            color: var(--cyan);
            font-family: monospace;
            font-weight: 800;
        }}

        input[type="range"] {{
            width: 100%;
            height: 5px;
            background: var(--bg-input);
            border-radius: 3px;
            outline: none;
            -webkit-appearance: none;
            appearance: none;
            cursor: pointer;
        }}

        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--cyan);
            cursor: pointer;
            box-shadow: 0 0 6px rgba(0, 210, 255, 0.7);
        }}

        input[type="color"] {{
            width: 100%;
            height: 32px;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 6px;
            cursor: pointer;
            padding: 2px;
        }}

        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 32px;
            height: 18px;
        }}

        .toggle-switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}

        .toggle-slider {{
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: var(--bg-input);
            transition: .2s;
            border-radius: 20px;
            border: 1px solid var(--border);
        }}

        .toggle-slider:before {{
            position: absolute;
            content: "";
            height: 12px;
            width: 12px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: .2s;
            border-radius: 50%;
        }}

        input:checked + .toggle-slider {{
            background-color: var(--cyan);
            border-color: var(--cyan);
        }}

        input:checked + .toggle-slider:before {{
            transform: translateX(14px);
            background-color: #030712;
        }}

        /* GALLERIES */
        .thumbs-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            max-height: 150px;
            overflow-y: auto;
            padding: 2px;
        }}

        .thumb-box {{
            aspect-ratio: 1;
            border-radius: 6px;
            border: 1px solid var(--border);
            overflow: hidden;
            cursor: pointer;
            position: relative;
            background: #000;
        }}

        .thumb-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.2s;
        }}

        .thumb-box:hover img {{
            transform: scale(1.08);
        }}

        .thumb-box.active {{
            border-color: var(--cyan);
            box-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
        }}

        .thumb-box span {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.75);
            font-size: 9px;
            padding: 2px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* MODALS */
        .modal {{
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(6px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }}

        .modal.active {{
            display: flex;
        }}

        .modal-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            width: 90%;
            max-width: 600px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 60px rgba(0,0,0,0.9);
        }}

        .modal-head {{
            padding: 13px 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .modal-head h3 {{
            font-size: 15px;
            color: #ffffff;
        }}

        .modal-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 20px;
            cursor: pointer;
        }}

        .modal-content {{
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .news-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 7px;
            padding: 10px 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .news-item:hover {{
            border-color: var(--cyan);
            background: var(--bg-input);
        }}

        .news-item h4 {{
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 3px;
        }}

        .news-item p {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        /* TOAST */
        .toast {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: var(--bg-card);
            border: 1px solid var(--cyan);
            color: #ffffff;
            padding: 10px 16px;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(0, 210, 255, 0.3);
            font-size: 12px;
            font-weight: 700;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
            z-index: 2000;
        }}

        .toast.show {{
            transform: translateY(0);
            opacity: 1;
        }}
    </style>
</head>
<body>
    <!-- TOP TOOLBAR -->
    <header class="topbar">
        <div class="brand">
            <div class="brand-icon">⚡</div>
            <div class="brand-title">
                VOLT STUDIO
                <span class="brand-badge">PRO MULTI-LAYER</span>
            </div>
        </div>

        <div class="topbar-center">
            <div class="preset-pill-group">
                <button class="preset-pill active" data-preset="kora_breaking">⚡ قالب العاجل</button>
                <button class="preset-pill" data-preset="kora_manchette">📝 قالب المانشيت الطولي</button>
                <button class="preset-pill" data-preset="fantasy_stats">🟣 فانتازي xG</button>
            </div>
            <div class="dimension-tag" id="dimBadge">1350 × 1688 px</div>
        </div>

        <div class="topbar-actions">
            <button class="btn btn-outline" id="btnLiveNewsModal">📰 جلب خبر حقيقي</button>
            <button class="btn btn-outline" id="btnSavePreset">💾 حفظ الإعدادات</button>
            <button class="btn btn-primary" id="btnExportHd">📥 تنزيل عالي الجودة</button>
            <button class="btn btn-accent" id="btnPublishModal">🚀 نشر مباشر</button>
        </div>
    </header>

    <!-- APP BODY -->
    <div class="app-body">
        <!-- SIDEBAR CONTROLS (RIGHT) -->
        <aside class="sidebar">
            <nav class="nav-tabs">
                <button class="nav-tab active" data-target="panel-text">✍️ تخصيص الجمل والنصوص</button>
                <button class="nav-tab" data-target="panel-bg">🖼️ الصورة والخلفية</button>
                <button class="nav-tab" data-target="panel-vector">👤 اللاعب والفيكتور</button>
                <button class="nav-tab" data-target="panel-template">🎨 القالب والشعار</button>
            </nav>

            <!-- TAB 1: INDEPENDENT SENTENCE & TYPOGRAPHY CUSTOMIZER -->
            <div class="panel-body active" id="panel-text">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">اختر الجملة لتعديلها بشكل منفصل</span>
                        <button class="btn-add-layer" id="btnAddSentence">➕ إضافة جملة جديدة</button>
                    </div>
                    <div class="layers-strip" id="sentenceLayersStrip">
                        <!-- Dynamic sentence tabs -->
                    </div>
                </div>

                <!-- SELECTED SENTENCE DEDICATED CONTROLS -->
                <div class="box" id="sentenceControlsBox">
                    <div class="box-header">
                        <span class="box-title" id="activeSentenceTitle">الجملة 1 (العنوان الرئيسي)</span>
                        <div style="display:flex; gap:6px;">
                            <label class="toggle-switch" title="إظهار/إخفاء">
                                <input type="checkbox" id="sentVisible" checked>
                                <span class="toggle-slider"></span>
                            </label>
                            <span class="box-action" id="btnDeleteSentence" style="color:var(--rose); background:rgba(244,63,94,0.1); border-color:rgba(244,63,94,0.3);">حذف 🗑️</span>
                        </div>
                    </div>

                    <div>
                        <label>نص الجملة:</label>
                        <textarea id="sentText" rows="2" placeholder="اكتب نص الجملة هنا..."></textarea>
                    </div>

                    <!-- FONT SELECTOR WITH THE 6 NEW FONTS -->
                    <div class="grid-2">
                        <div>
                            <label>نوع الخط (Font Family):</label>
                            <select id="sentFont">
                                <optgroup label="الخطوط الجديدة المعتمدة">
                                    <option value="AraJozoor">★ Jozoor (خط جذور الرسمي)</option>
                                    <option value="Ebhaar">✨ Ebhaar (خط إبهار)</option>
                                    <option value="Horizon">⚡ Horizon (خط هورايزون)</option>
                                    <option value="DroidKufi">📜 Droid Arabic Kufi (درويد كوفي)</option>
                                    <option value="LavaPro">🔥 Lava Pro Grunge (لافا جرانج)</option>
                                    <option value="ZuumeRough">💥 Zuume Rough Bold (زوومي رف بولد)</option>
                                </optgroup>
                                <optgroup label="خطوط قياسية">
                                    <option value="Cairo">Cairo (كايرو)</option>
                                    <option value="Tajawal">Tajawal (تجوال)</option>
                                    <option value="Arial">Arial Black</option>
                                </optgroup>
                            </select>
                        </div>
                        <div>
                            <label>محاذاة النص:</label>
                            <select id="sentAlign">
                                <option value="center">المنتصف (Center)</option>
                                <option value="right">اليمين (Right)</option>
                                <option value="left">اليسار (Left)</option>
                            </select>
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>حجم الخط</span>
                                <span class="slider-val" id="valSentSize">78px</span>
                            </div>
                            <input type="range" id="sentSize" min="20" max="180" value="78">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>أقصى عرض للسطر</span>
                                <span class="slider-val" id="valSentWidth">1180px</span>
                            </div>
                            <input type="range" id="sentWidth" min="200" max="2100" value="1180">
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>الموقع الأفقي (X)</span>
                                <span class="slider-val" id="valSentX">675px</span>
                            </div>
                            <input type="range" id="sentX" min="0" max="2160" value="675">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>الموقع الرأسي (Y)</span>
                                <span class="slider-val" id="valSentY">1240px</span>
                            </div>
                            <input type="range" id="sentY" min="0" max="2700" value="1240">
                        </div>
                    </div>

                    <div class="grid-3">
                        <div>
                            <label>لون الجملة:</label>
                            <input type="color" id="sentColor" value="#ffffff">
                        </div>
                        <div>
                            <label>لون التحديد (Stroke):</label>
                            <input type="color" id="sentStrokeColor" value="#000000">
                        </div>
                        <div>
                            <label>سمك التحديد:</label>
                            <input type="number" id="sentStrokeWidth" min="0" max="20" value="4" style="height:32px;">
                        </div>
                    </div>

                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>كثافة الظل (Shadow)</span>
                                <span class="slider-val" id="valSentShadow">10px</span>
                            </div>
                            <input type="range" id="sentShadow" min="0" max="40" value="10">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>تباعد الأسطر</span>
                                <span class="slider-val" id="valSentLineHeight">1.25</span>
                            </div>
                            <input type="range" id="sentLineHeight" min="0.8" max="2.0" step="0.05" value="1.25">
                        </div>
                    </div>
                </div>

                <!-- SOURCE & SPEAKER SPECIAL BOX -->
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">المصدر والمتحدث (Speaker Role & Name)</span>
                    </div>

                    <div class="grid-2">
                        <div>
                            <label>صفة المتحدث (الصحفي / المدرب):</label>
                            <input type="text" id="roleText" value="الصحفي">
                        </div>
                        <div>
                            <label>لون الصفة:</label>
                            <input type="color" id="roleColor" value="#00b4d8">
                        </div>
                    </div>

                    <div class="grid-2">
                        <div>
                            <label>اسم المصدر / المتحدث:</label>
                            <input type="text" id="nameText" value="فابريزيو رومانو">
                        </div>
                        <div>
                            <label>لون الاسم:</label>
                            <input type="color" id="nameColor" value="#ffffff">
                        </div>
                    </div>

                    <div class="grid-2">
                        <div>
                            <label>خط المتحدث:</label>
                            <select id="sourceFont">
                                <option value="AraJozoor" selected>Jozoor (جذور)</option>
                                <option value="Ebhaar">Ebhaar (إبهار)</option>
                                <option value="Horizon">Horizon (هورايزون)</option>
                                <option value="DroidKufi">Droid Arabic Kufi</option>
                                <option value="LavaPro">Lava Pro Grunge</option>
                                <option value="ZuumeRough">Zuume Rough Bold</option>
                            </select>
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>الموقع الرأسي (Y)</span>
                                <span class="slider-val" id="valSourceY">1540px</span>
                            </div>
                            <input type="range" id="sourceY" min="300" max="2650" value="1540">
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 2: BACKGROUND IMAGE CONTROLS -->
            <div class="panel-body" id="panel-bg">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">صورة الخلفية / الخبر</span>
                    </div>
                    <button class="btn btn-outline" id="btnUploadBg" style="width:100%; justify-content:center;">📁 رفع صورة من جهازك</button>
                    <input type="file" id="fileBgInput" accept="image/*" style="display:none;">
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">✨ توليد خلفية رياضية AI بـ FLUX</span>
                    </div>
                    <input type="text" id="promptAiBg" value="football stadium pitch under dark dramatic floodlights, cinematic 4k sports background">
                    <button class="btn btn-primary" id="btnGenerateAiBg" style="width:100%; justify-content:center;">⚡ توليد فوري مجاني (2.5 ثانية)</button>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">معرض الصور الجاهزة</span>
                    </div>
                    <div class="thumbs-grid" id="bgGallery"></div>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">تحكم كامل في أبعاد ومكان وتأثير الصورة</span>
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>التكبير والزووم (Scale)</span>
                            <span class="slider-val" id="valBgScale">100%</span>
                        </div>
                        <input type="range" id="bgScale" min="50" max="250" value="100">
                    </div>
                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>تحريك أفقي (X)</span>
                                <span class="slider-val" id="valBgPanX">0px</span>
                            </div>
                            <input type="range" id="bgPanX" min="-1000" max="1000" value="0">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>تحريك رأسي (Y)</span>
                                <span class="slider-val" id="valBgPanY">0px</span>
                            </div>
                            <input type="range" id="bgPanY" min="-1000" max="1000" value="0">
                        </div>
                    </div>
                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>السطوع (Brightness)</span>
                                <span class="slider-val" id="valBgBrightness">100%</span>
                            </div>
                            <input type="range" id="bgBrightness" min="20" max="180" value="100">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>التباين (Contrast)</span>
                                <span class="slider-val" id="valBgContrast">100%</span>
                            </div>
                            <input type="range" id="bgContrast" min="50" max="200" value="100">
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 3: PLAYER VECTOR & CUTOUT CONTROLS -->
            <div class="panel-body" id="panel-vector">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">طبقة اللاعب المفرغة (Cutout)</span>
                        <label class="toggle-switch">
                            <input type="checkbox" id="chkShowVector" checked>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                    <button class="btn btn-outline" id="btnUploadCutout" style="width:100%; justify-content:center;">📁 رفع صورة لاعب مفرغ من جهازك</button>
                    <input type="file" id="fileCutoutInput" accept="image/*" style="display:none;">
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">✨ توليد فيكتور وعزل بـ Leonardo & Rembg</span>
                    </div>
                    <div class="grid-2">
                        <input type="text" id="aiPlayerName" placeholder="اسم اللاعب (Haaland)" value="Erling Haaland">
                        <input type="text" id="aiPlayerClub" placeholder="النادي (Man City)" value="Manchester City">
                    </div>
                    <button class="btn btn-primary" id="btnGenerateVectorAi" style="width:100%; justify-content:center;">⚡ رسم فيكتور وعزل في ثانيتين</button>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">معرض نجوم الكرة المفرغة جاهزة</span>
                    </div>
                    <div class="thumbs-grid" id="cutoutGallery"></div>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">تخصيص مكان وحجم وتأثيرات اللاعب</span>
                    </div>
                    <div class="grid-2">
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>الموقع الأفقي (X)</span>
                                <span class="slider-val" id="valVecX">350px</span>
                            </div>
                            <input type="range" id="vecX" min="-500" max="2100" value="350">
                        </div>
                        <div class="slider-item">
                            <div class="slider-header">
                                <span>الموقع الرأسي (Y)</span>
                                <span class="slider-val" id="valVecY">450px</span>
                            </div>
                            <input type="range" id="vecY" min="-200" max="2500" value="450">
                        </div>
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الحجم والتكبير (Scale)</span>
                            <span class="slider-val" id="valVecScale">100%</span>
                        </div>
                        <input type="range" id="vecScale" min="20" max="300" value="100">
                    </div>
                    <div class="grid-2">
                        <label><input type="checkbox" id="chkVecFlip"> عكس اتجاه اللاعب (Flip H)</label>
                        <label><input type="checkbox" id="chkVecShadow" checked> ظل واقعي (Drop Shadow)</label>
                    </div>
                </div>
            </div>

            <!-- TAB 4: TEMPLATE OVERLAY -->
            <div class="panel-body" id="panel-template">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">القالب المظلل والشعار (Overlay)</span>
                    </div>
                    <select id="selectTemplateOverlay">
                        <option value="/assets/templates/kora_volt/breaking.png">كورة ڤولت — العاجل (1350×1688)</option>
                        <option value="/assets/templates/kora_volt/manchette.png">كورة ڤولت — المانشيت الطولي (2160×2700)</option>
                        <option value="">بدون قالب (صورة حرة بدون تظليل)</option>
                    </select>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">➕ رفع قالب شفاف جديد (PNG)</span>
                    </div>
                    <p style="font-size:11px; color:var(--text-muted); line-height:1.4;">ارفع صورة القالب الشفاف المفرغ المصمم على كانفا أو فوتوشوب وسيحفظه الأستوديو فورًا.</p>
                    <button class="btn btn-accent" id="btnUploadTemplateOverlay" style="width:100%; justify-content:center;">📁 رفع قالب جديد (PNG)</button>
                    <input type="file" id="fileTemplateInput" accept="image/png" style="display:none;">
                </div>

                <div class="box">
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>شفافية القالب (Opacity)</span>
                            <span class="slider-val" id="valTmplOpacity">100%</span>
                        </div>
                        <input type="range" id="tmplOpacity" min="0" max="100" value="100">
                    </div>
                </div>
            </div>
        </aside>

        <!-- WORKSPACE (CENTER / LEFT) -->
        <main class="workspace">
            <div class="workspace-bar">
                <div class="zoom-group">
                    <button class="tool-btn" id="btnZoomOut">🔍 -</button>
                    <span class="zoom-label" id="zoomLevel">Fit</span>
                    <button class="tool-btn" id="btnZoomIn">🔍 +</button>
                    <button class="tool-btn" id="btnZoomFit">احتواء الشاشة</button>
                </div>

                <div class="workspace-tools">
                    <span style="font-size:11px; color:var(--cyan);">💡 يمكنك سحب أي جملة أو اللاعب مباشرة بالماوس على الكارت!</span>
                    <label style="margin:0; display:flex; align-items:center; gap:5px; cursor:pointer;">
                        <input type="checkbox" id="chkRefOverlay"> مقارنة بالمرجع
                    </label>
                    <input type="range" id="refOpacity" min="0" max="100" value="50" style="width: 70px; display:none;">
                </div>
            </div>

            <div class="canvas-area" id="canvasArea">
                <div class="canvas-frame" id="canvasFrame">
                    <canvas id="cardCanvas"></canvas>
                </div>
            </div>
        </main>
    </div>

    <!-- MODAL: LIVE NEWS -->
    <div class="modal" id="modalLiveNews">
        <div class="modal-card">
            <div class="modal-head">
                <h3>📰 اختيار خبر حقيقي لتجربة القالب</h3>
                <button class="modal-close" id="btnCloseNewsModal">&times;</button>
            </div>
            <div class="modal-content">
                <p style="font-size:12px; color:var(--text-muted);">انقر على أي خبر حقيقي لملء العنوان والصورة فورًا في الكارت:</p>
                <div id="liveNewsList" style="display:flex; flex-direction:column; gap:8px;">
                    <div style="text-align:center; padding:20px; color:var(--text-muted);">جاري جلب الأخبار الحية...</div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: PUBLISH -->
    <div class="modal" id="modalPublish">
        <div class="modal-card">
            <div class="modal-head">
                <h3>🚀 نشر مباشر على الصفحة</h3>
                <button class="modal-close" id="btnClosePublishModal">&times;</button>
            </div>
            <div class="modal-content">
                <label>الصفحة المستهدفة:</label>
                <select id="pubTargetPage">
                    <option value="kora_volt">كورة ڤولت (Kora Volt)</option>
                    <option value="fantasy_volt">فانتازي ڤولت (Fantasy Volt)</option>
                </select>

                <label>نص المنشور (الكابشن):</label>
                <textarea id="pubCaption" rows="4" placeholder="اكتب وصف المنشور..."></textarea>

                <div style="max-height:180px; display:flex; justify-content:center; background:#000; border-radius:6px; overflow:hidden;">
                    <img id="pubPreviewImg" src="" alt="Card" style="max-height:180px; object-fit:contain;">
                </div>

                <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:8px;">
                    <button class="btn btn-outline" id="btnCancelPublish">إلغاء</button>
                    <button class="btn btn-accent" id="btnConfirmPublish">تأكيد ونشر الآن</button>
                </div>
            </div>
        </div>
    </div>

    <!-- TOAST -->
    <div id="toast" class="toast">⚡ تم التنفيذ بنجاح!</div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5050' : '';

        function resolveUrl(url) {{
            if (!url) return '';
            if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
            if (window.location.protocol === 'file:') return '../../' + url.replace(/^\\//, '');
            return url;
        }}

        // ═══════════════════════════════════════════════════════════════════
        // MULTI-ELEMENT STATE (INDEPENDENT SENTENCES & LAYERS)
        // ═══════════════════════════════════════════════════════════════════

        const state = {{
            width: 1350,
            height: 1688,
            zoom: 'fit',

            // Multi-sentence layers
            sentences: [
                {{
                    id: "sent_1",
                    name: "الجملة 1 (الرئيسية)",
                    text: "مانشستر سيتي يتوصل لاتفاق نهائي",
                    font: "AraJozoor",
                    size: 82,
                    color: "#ffffff",
                    strokeColor: "#000000",
                    strokeWidth: 4,
                    shadow: 12,
                    x: 675,
                    y: 1180,
                    maxWidth: 1180,
                    align: "center",
                    lineHeight: 1.25,
                    visible: true
                }},
                {{
                    id: "sent_2",
                    name: "الجملة 2 (الفرعية)",
                    text: "مع بيب جوارديولا لتجديد عقده لموسم إضافي",
                    font: "AraJozoor",
                    size: 74,
                    color: "#ffffff",
                    strokeColor: "#000000",
                    strokeWidth: 4,
                    shadow: 12,
                    x: 675,
                    y: 1285,
                    maxWidth: 1180,
                    align: "center",
                    lineHeight: 1.25,
                    visible: true
                }}
            ],
            activeSentenceIndex: 0,

            // Source & Speaker Credits
            source: {{
                roleText: "الصحفي",
                roleColor: "#00b4d8",
                nameText: "فابريزيو رومانو",
                nameColor: "#ffffff",
                font: "AraJozoor",
                y: 1540,
                x: 675
            }},

            // Background Layer
            bg: {{
                url: resolveUrl('/assets/templates/default_football_bg.jpg'),
                scale: 1.0,
                panX: 0,
                panY: 0,
                brightness: 1.0,
                contrast: 1.0
            }},

            // Player Vector Layer
            vector: {{
                show: false,
                url: resolveUrl('/output/erling_haaland_vector_cutout.png'),
                x: 350,
                y: 450,
                scale: 1.0,
                flip: false,
                shadow: true
            }},

            // Template Overlay Layer
            template: {{
                url: resolveUrl('/assets/templates/kora_volt/breaking.png'),
                opacity: 1.0
            }},

            // Dragging tracking
            drag: {{
                isDragging: false,
                target: null, // 'sentence' or 'vector'
                targetIndex: 0,
                startX: 0,
                startY: 0,
                origX: 0,
                origY: 0
            }},

            ref: {{ show: false, img: null, opacity: 0.5 }}
        }};

        const PRESETS = {{
            kora_breaking: {{
                width: 1350,
                height: 1688,
                templateUrl: '/assets/templates/kora_volt/breaking.png',
                vectorShow: false,
                sourceRoleY: 1540,
                sourceAlign: 'center',
                sentences: [
                    {{
                        id: "sent_1",
                        name: "الجملة 1 (الرئيسية)",
                        text: "مانشستر سيتي يتوصل لاتفاق نهائي",
                        font: "AraJozoor",
                        size: 82,
                        color: "#ffffff",
                        strokeColor: "#000000",
                        strokeWidth: 4,
                        shadow: 12,
                        x: 675,
                        y: 1180,
                        maxWidth: 1180,
                        align: "center",
                        lineHeight: 1.25,
                        visible: true
                    }},
                    {{
                        id: "sent_2",
                        name: "الجملة 2 (الفرعية)",
                        text: "مع بيب جوارديولا لتجديد عقده لموسم إضافي",
                        font: "AraJozoor",
                        size: 74,
                        color: "#ffffff",
                        strokeColor: "#000000",
                        strokeWidth: 4,
                        shadow: 12,
                        x: 675,
                        y: 1285,
                        maxWidth: 1180,
                        align: "center",
                        lineHeight: 1.25,
                        visible: true
                    }}
                ]
            }},
            kora_manchette: {{
                width: 2160,
                height: 2700,
                templateUrl: '/assets/templates/kora_volt/manchette.png',
                vectorShow: false,
                sourceRoleY: 2420,
                sourceAlign: 'right',
                sentences: [
                    {{
                        id: "sent_1",
                        name: "المانشيت الطولي",
                        text: "توتنهام يقترب من حسم صفقة مورجان جيبس-وايت من نوتنجهام فورست بعد مفاوضات متقدمة لدعم خط الهجوم",
                        font: "AraJozoor",
                        size: 92,
                        color: "#ffffff",
                        strokeColor: "#000000",
                        strokeWidth: 4,
                        shadow: 14,
                        x: 1450,
                        y: 850,
                        maxWidth: 1050,
                        align: "right",
                        lineHeight: 1.35,
                        visible: true
                    }}
                ]
            }},
            fantasy_stats: {{
                width: 1350,
                height: 1688,
                templateUrl: '/assets/templates/kora_volt/breaking.png',
                vectorShow: true,
                sourceRoleY: 1540,
                sourceAlign: 'center',
                sentences: [
                    {{
                        id: "sent_1",
                        name: "عنوان الإحصائية",
                        text: "ترتيب أخطر مهاجمي البريميرليج بالأهداف المتوقعة",
                        font: "AraJozoor",
                        size: 72,
                        color: "#ffffff",
                        strokeColor: "#000000",
                        strokeWidth: 4,
                        shadow: 12,
                        x: 675,
                        y: 1200,
                        maxWidth: 1150,
                        align: "center",
                        lineHeight: 1.25,
                        visible: true
                    }},
                    {{
                        id: "sent_2",
                        name: "رقم الصدارة",
                        text: "هالاند يتصدر بـ 8.09 xG رسمياً من أوبتا",
                        font: "Horizon",
                        size: 64,
                        color: "#00d2ff",
                        strokeColor: "#000000",
                        strokeWidth: 3,
                        shadow: 12,
                        x: 675,
                        y: 1290,
                        maxWidth: 1150,
                        align: "center",
                        lineHeight: 1.25,
                        visible: true
                    }}
                ]
            }}
        }};

        const canvas = document.getElementById('cardCanvas');
        const ctx = canvas.getContext('2d');
        const canvasArea = document.getElementById('canvasArea');
        const imageCache = {{}};

        function loadImage(url) {{
            if (!url) return Promise.resolve(null);
            const resolved = resolveUrl(url);
            if (imageCache[resolved]) return Promise.resolve(imageCache[resolved]);
            return new Promise((resolve) => {{
                const img = new Image();
                img.crossOrigin = "anonymous";
                img.onload = () => {{
                    imageCache[resolved] = img;
                    resolve(img);
                }};
                img.onerror = () => {{
                    console.warn("Failed to load:", resolved);
                    resolve(null);
                }};
                img.src = resolved;
            }});
        }}

        // ═══════════════════════════════════════════════════════════════════
        // RENDER LOOP
        // ═══════════════════════════════════════════════════════════════════

        async function render() {{
            canvas.width = state.width;
            canvas.height = state.height;

            ctx.clearRect(0, 0, state.width, state.height);
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, state.width, state.height);

            // 1. Background Photo
            if (state.bg.url) {{
                const bgImg = await loadImage(state.bg.url);
                if (bgImg) {{
                    ctx.save();
                    let filters = [];
                    if (state.bg.brightness !== 1.0) filters.push(`brightness(${{state.bg.brightness}})`);
                    if (state.bg.contrast !== 1.0) filters.push(`contrast(${{state.bg.contrast}})`);
                    if (filters.length) ctx.filter = filters.join(' ');

                    const scale = Math.max(state.width / bgImg.width, state.height / bgImg.height) * state.bg.scale;
                    const w = bgImg.width * scale;
                    const h = bgImg.height * scale;
                    const x = (state.width - w) / 2 + state.bg.panX;
                    const y = (state.height - h) / 2 + state.bg.panY;
                    ctx.drawImage(bgImg, x, y, w, h);
                    ctx.restore();
                }}
            }}

            // 2. Player Cutout
            if (state.vector.show && state.vector.url) {{
                const vecImg = await loadImage(state.vector.url);
                if (vecImg) {{
                    ctx.save();
                    const vw = vecImg.width * state.vector.scale;
                    const vh = vecImg.height * state.vector.scale;
                    const vx = state.vector.x;
                    const vy = state.vector.y;

                    if (state.vector.shadow) {{
                        ctx.shadowColor = "rgba(0, 0, 0, 0.85)";
                        ctx.shadowBlur = 35;
                        ctx.shadowOffsetY = 15;
                    }}
                    if (state.vector.flip) {{
                        ctx.translate(vx + vw, vy);
                        ctx.scale(-1, 1);
                        ctx.drawImage(vecImg, 0, 0, vw, vh);
                    }} else {{
                        ctx.drawImage(vecImg, vx, vy, vw, vh);
                    }}
                    ctx.restore();
                }}
            }}

            // 3. Template Overlay
            if (state.template.url) {{
                const tmplImg = await loadImage(state.template.url);
                if (tmplImg) {{
                    ctx.save();
                    ctx.globalAlpha = state.template.opacity;
                    ctx.drawImage(tmplImg, 0, 0, state.width, state.height);
                    ctx.restore();
                }}
            }}

            // 4. Render All Independent Sentences
            renderAllSentences();

            // 5. Source Credits Block
            renderSourceBlock();

            // 6. Ref Overlay
            if (state.ref.show && state.ref.img) {{
                ctx.save();
                ctx.globalAlpha = state.ref.opacity;
                ctx.drawImage(state.ref.img, 0, 0, state.width, state.height);
                ctx.restore();
            }}

            updateZoom();
        }}

        function renderAllSentences() {{
            state.sentences.forEach((sent, idx) => {{
                if (!sent.visible) return;
                const text = (sent.text || '').trim();
                if (!text) return;

                ctx.save();
                ctx.direction = "rtl";
                ctx.textAlign = sent.align || "center";
                ctx.font = `${{sent.size}}px '${{sent.font}}', 'Cairo', sans-serif`;

                const words = text.split(/\\s+/);
                const lines = [];
                let currentLine = "";

                for (const word of words) {{
                    const test = currentLine ? `${{currentLine}} ${{word}}` : word;
                    if (ctx.measureText(test).width > sent.maxWidth && currentLine) {{
                        lines.push(currentLine);
                        currentLine = word;
                    }} else {{
                        currentLine = test;
                    }}
                }}
                if (currentLine) lines.push(currentLine);

                const lineH = sent.size * (sent.lineHeight || 1.25);
                lines.forEach((line, lineIdx) => {{
                    const y = sent.y + (lineIdx * lineH);

                    // Shadow
                    if (sent.shadow > 0) {{
                        ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
                        ctx.shadowBlur = sent.shadow;
                        ctx.shadowOffsetY = 4;
                    }}

                    // Stroke
                    if (sent.strokeWidth > 0) {{
                        ctx.strokeStyle = sent.strokeColor;
                        ctx.lineWidth = sent.strokeWidth * 2;
                        ctx.lineJoin = "round";
                        ctx.strokeText(line, sent.x, y);
                    }}

                    // Fill
                    ctx.fillStyle = sent.color;
                    ctx.fillText(line, sent.x, y);
                }});

                // Highlight active sentence with a subtle boundary box on canvas
                if (idx === state.activeSentenceIndex) {{
                    ctx.strokeStyle = "rgba(0, 210, 255, 0.5)";
                    ctx.lineWidth = 2;
                    ctx.setLineDash([6, 6]);
                    const estHeight = lines.length * lineH;
                    let boxX = sent.x;
                    if (sent.align === 'center') boxX = sent.x - (sent.maxWidth / 2);
                    else if (sent.align === 'right') boxX = sent.x - sent.maxWidth;
                    ctx.strokeRect(boxX - 10, sent.y - sent.size, sent.maxWidth + 20, estHeight + 15);
                }}

                ctx.restore();
            }});
        }}

        function renderSourceBlock() {{
            const role = (state.source.roleText || '').trim();
            const name = (state.source.nameText || '').trim();
            if (!role && !name) return;

            ctx.save();
            ctx.direction = "rtl";
            ctx.font = `38px '${{state.source.font}}', 'Cairo', sans-serif`;

            const activeP = document.querySelector('.preset-pill.active');
            const isManchette = activeP && activeP.dataset.preset === 'kora_manchette';
            const align = isManchette ? 'right' : 'center';
            ctx.textAlign = align;

            if (role) {{
                ctx.fillStyle = state.source.roleColor;
                ctx.shadowColor = "rgba(0, 0, 0, 0.8)";
                ctx.shadowBlur = 8;
                ctx.fillText(role, state.source.x, state.source.y - 48);
            }}

            if (name) {{
                ctx.font = `56px '${{state.source.font}}', 'Cairo', sans-serif`;
                ctx.fillStyle = state.source.nameColor;
                ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
                ctx.shadowBlur = 10;
                ctx.fillText(name, state.source.x, state.source.y);
            }}
            ctx.restore();
        }}

        function updateZoom() {{
            const vW = canvasArea.clientWidth - 40;
            const vH = canvasArea.clientHeight - 40;
            let scale = 1.0;
            if (state.zoom === 'fit') {{
                scale = Math.min(vW / state.width, vH / state.height);
            }} else {{
                scale = state.zoom;
            }}

            canvas.style.width = `${{state.width * scale}}px`;
            canvas.style.height = `${{state.height * scale}}px`;
            document.getElementById('zoomLevel').textContent = state.zoom === 'fit' ? `Fit (${{Math.round(scale * 100)}}%)` : `${{Math.round(scale * 100)}}%`;
            document.getElementById('dimBadge').textContent = `${{state.width}} × ${{state.height}} px`;
        }}

        // ═══════════════════════════════════════════════════════════════════
        // SENTENCE LAYER MANAGER & STRIP
        // ═══════════════════════════════════════════════════════════════════

        function rebuildSentenceStrip() {{
            const strip = document.getElementById('sentenceLayersStrip');
            strip.innerHTML = '';

            state.sentences.forEach((sent, idx) => {{
                const btn = document.createElement('button');
                btn.className = `layer-btn ${{idx === state.activeSentenceIndex ? 'active' : ''}}`;
                btn.textContent = `${{idx + 1}}. ${{sent.name}}`;
                btn.onclick = () => {{
                    state.activeSentenceIndex = idx;
                    rebuildSentenceStrip();
                    loadActiveSentenceIntoInputs();
                    render();
                }};
                strip.appendChild(btn);
            }});
        }}

        function loadActiveSentenceIntoInputs() {{
            const sent = state.sentences[state.activeSentenceIndex];
            if (!sent) return;

            document.getElementById('activeSentenceTitle').textContent = `${{sent.name}} (تخصيص كامل)`;
            document.getElementById('sentText').value = sent.text;
            document.getElementById('sentFont').value = sent.font;
            document.getElementById('sentAlign').value = sent.align;
            document.getElementById('sentSize').value = sent.size;
            document.getElementById('valSentSize').textContent = `${{sent.size}}px`;
            document.getElementById('sentWidth').value = sent.maxWidth;
            document.getElementById('valSentWidth').textContent = `${{sent.maxWidth}}px`;
            document.getElementById('sentX').value = sent.x;
            document.getElementById('valSentX').textContent = `${{sent.x}}px`;
            document.getElementById('sentY').value = sent.y;
            document.getElementById('valSentY').textContent = `${{sent.y}}px`;
            document.getElementById('sentColor').value = sent.color;
            document.getElementById('sentStrokeColor').value = sent.strokeColor;
            document.getElementById('sentStrokeWidth').value = sent.strokeWidth;
            document.getElementById('sentShadow').value = sent.shadow;
            document.getElementById('valSentShadow').textContent = `${{sent.shadow}}px`;
            document.getElementById('sentLineHeight').value = sent.lineHeight || 1.25;
            document.getElementById('valSentLineHeight').textContent = sent.lineHeight || 1.25;
            document.getElementById('sentVisible').checked = sent.visible;
        }}

        function saveInputsIntoActiveSentence() {{
            const sent = state.sentences[state.activeSentenceIndex];
            if (!sent) return;

            sent.text = document.getElementById('sentText').value;
            sent.font = document.getElementById('sentFont').value;
            sent.align = document.getElementById('sentAlign').value;
            sent.size = parseInt(document.getElementById('sentSize').value);
            sent.maxWidth = parseInt(document.getElementById('sentWidth').value);
            sent.x = parseInt(document.getElementById('sentX').value);
            sent.y = parseInt(document.getElementById('sentY').value);
            sent.color = document.getElementById('sentColor').value;
            sent.strokeColor = document.getElementById('sentStrokeColor').value;
            sent.strokeWidth = parseInt(document.getElementById('sentStrokeWidth').value);
            sent.shadow = parseInt(document.getElementById('sentShadow').value);
            sent.lineHeight = parseFloat(document.getElementById('sentLineHeight').value);
            sent.visible = document.getElementById('sentVisible').checked;

            render();
        }}

        function applyPreset(id) {{
            const p = PRESETS[id];
            if (!p) return;

            state.width = p.width;
            state.height = p.height;
            state.template.url = resolveUrl(p.templateUrl);
            state.vector.show = p.vectorShow;
            state.source.y = p.sourceRoleY;
            state.source.x = p.sourceAlign === 'right' ? 1450 : (p.width / 2);

            // Deep copy sentences
            state.sentences = JSON.parse(JSON.stringify(p.sentences));
            state.activeSentenceIndex = 0;

            document.querySelectorAll('.preset-pill').forEach(b => b.classList.remove('active'));
            const pill = document.querySelector(`[data-preset="${{id}}"]`);
            if (pill) pill.classList.add('active');

            rebuildSentenceStrip();
            loadActiveSentenceIntoInputs();
            render();
        }}

        // ═══════════════════════════════════════════════════════════════════
        // INTERACTIVE CANVAS DRAGGING
        // ═══════════════════════════════════════════════════════════════════

        function setupCanvasDragging() {{
            canvas.addEventListener('mousedown', (e) => {{
                const rect = canvas.getBoundingClientRect();
                const scale = state.width / rect.width;
                const clickX = (e.clientX - rect.left) * scale;
                const clickY = (e.clientY - rect.top) * scale;

                // Check if clicked near an active sentence
                for (let i = 0; i < state.sentences.length; i++) {{
                    const s = state.sentences[i];
                    if (!s.visible) continue;
                    // Simple bounding box check
                    const dist = Math.hypot(clickX - s.x, clickY - s.y);
                    if (dist < 150) {{
                        state.drag.isDragging = true;
                        state.drag.target = 'sentence';
                        state.drag.targetIndex = i;
                        state.drag.startX = clickX;
                        state.drag.startY = clickY;
                        state.drag.origX = s.x;
                        state.drag.origY = s.y;
                        state.activeSentenceIndex = i;
                        rebuildSentenceStrip();
                        loadActiveSentenceIntoInputs();
                        render();
                        return;
                    }}
                }}

                // Check player cutout
                if (state.vector.show) {{
                    const vDist = Math.hypot(clickX - state.vector.x, clickY - state.vector.y);
                    if (vDist < 250) {{
                        state.drag.isDragging = true;
                        state.drag.target = 'vector';
                        state.drag.startX = clickX;
                        state.drag.startY = clickY;
                        state.drag.origX = state.vector.x;
                        state.drag.origY = state.vector.y;
                        return;
                    }}
                }}
            }});

            window.addEventListener('mousemove', (e) => {{
                if (!state.drag.isDragging) return;
                const rect = canvas.getBoundingClientRect();
                const scale = state.width / rect.width;
                const curX = (e.clientX - rect.left) * scale;
                const curY = (e.clientY - rect.top) * scale;
                const dx = curX - state.drag.startX;
                const dy = curY - state.drag.startY;

                if (state.drag.target === 'sentence') {{
                    const s = state.sentences[state.drag.targetIndex];
                    s.x = Math.round(state.drag.origX + dx);
                    s.y = Math.round(state.drag.origY + dy);
                    loadActiveSentenceIntoInputs();
                }} else if (state.drag.target === 'vector') {{
                    state.vector.x = Math.round(state.drag.origX + dx);
                    state.vector.y = Math.round(state.drag.origY + dy);
                    document.getElementById('vecX').value = state.vector.x;
                    document.getElementById('vecY').value = state.vector.y;
                    document.getElementById('valVecX').textContent = `${{state.vector.x}}px`;
                    document.getElementById('valVecY').textContent = `${{state.vector.y}}px`;
                }}
                render();
            }});

            window.addEventListener('mouseup', () => {{
                state.drag.isDragging = false;
            }});
        }}

        // ═══════════════════════════════════════════════════════════════════
        // EVENT LISTENERS & WIRING
        // ═══════════════════════════════════════════════════════════════════

        function setupListeners() {{
            setupCanvasDragging();

            // Preset Pills
            document.querySelectorAll('.preset-pill').forEach(b => {{
                b.addEventListener('click', () => applyPreset(b.dataset.preset));
            }});

            // Tabs
            document.querySelectorAll('.nav-tab').forEach(b => {{
                b.addEventListener('click', () => {{
                    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.panel-body').forEach(p => p.classList.remove('active'));
                    b.classList.add('active');
                    document.getElementById(b.dataset.target).classList.add('active');
                }});
            }});

            // Add Sentence Button
            document.getElementById('btnAddSentence').addEventListener('click', () => {{
                const newId = `sent_${{state.sentences.length + 1}}`;
                state.sentences.push({{
                    id: newId,
                    name: `جملة ${{state.sentences.length + 1}}`,
                    text: "نص جملة جديد للتخصيص",
                    font: "AraJozoor",
                    size: 64,
                    color: "#00d2ff",
                    strokeColor: "#000000",
                    strokeWidth: 3,
                    shadow: 10,
                    x: state.width / 2,
                    y: 1050 + (state.sentences.length * 70),
                    maxWidth: 1000,
                    align: "center",
                    lineHeight: 1.25,
                    visible: true
                }});
                state.activeSentenceIndex = state.sentences.length - 1;
                rebuildSentenceStrip();
                loadActiveSentenceIntoInputs();
                render();
                showToast("➕ تم إضافة جملة جديدة مع تحكم منفصل في لونها ومكانها وخطها!");
            }});

            // Delete Sentence
            document.getElementById('btnDeleteSentence').addEventListener('click', () => {{
                if (state.sentences.length <= 1) {{
                    showToast("يجب أن يحتوي التصميم على جملة واحدة على الأقل");
                    return;
                }}
                state.sentences.splice(state.activeSentenceIndex, 1);
                state.activeSentenceIndex = Math.max(0, state.activeSentenceIndex - 1);
                rebuildSentenceStrip();
                loadActiveSentenceIntoInputs();
                render();
                showToast("🗑️ تم حذف الجملة المحددة");
            }});

            // Active Sentence Input changes
            ['sentText', 'sentFont', 'sentAlign', 'sentColor', 'sentStrokeColor', 'sentStrokeWidth', 'sentVisible'].forEach(id => {{
                document.getElementById(id).addEventListener('input', saveInputsIntoActiveSentence);
            }});
            ['sentSize', 'sentWidth', 'sentX', 'sentY', 'sentShadow', 'sentLineHeight'].forEach(id => {{
                document.getElementById(id).addEventListener('input', (e) => {{
                    const valSpan = document.getElementById(`val${{id.charAt(0).toUpperCase() + id.slice(1)}}`);
                    if (valSpan) valSpan.textContent = id === 'sentLineHeight' ? e.target.value : `${{e.target.value}}px`;
                    saveInputsIntoActiveSentence();
                }});
            }});

            // Source block inputs
            document.getElementById('roleText').addEventListener('input', (e) => {{ state.source.roleText = e.target.value; render(); }});
            document.getElementById('roleColor').addEventListener('input', (e) => {{ state.source.roleColor = e.target.value; render(); }});
            document.getElementById('nameText').addEventListener('input', (e) => {{ state.source.nameText = e.target.value; render(); }});
            document.getElementById('nameColor').addEventListener('input', (e) => {{ state.source.nameColor = e.target.value; render(); }});
            document.getElementById('sourceFont').addEventListener('change', (e) => {{ state.source.font = e.target.value; render(); }});
            document.getElementById('sourceY').addEventListener('input', (e) => {{
                state.source.y = parseInt(e.target.value);
                document.getElementById('valSourceY').textContent = `${{e.target.value}}px`;
                render();
            }});

            // Background controls
            document.getElementById('bgScale').addEventListener('input', (e) => {{
                state.bg.scale = parseInt(e.target.value) / 100;
                document.getElementById('valBgScale').textContent = `${{e.target.value}}%`;
                render();
            }});
            document.getElementById('bgPanX').addEventListener('input', (e) => {{
                state.bg.panX = parseInt(e.target.value);
                document.getElementById('valBgPanX').textContent = `${{e.target.value}}px`;
                render();
            }});
            document.getElementById('bgPanY').addEventListener('input', (e) => {{
                state.bg.panY = parseInt(e.target.value);
                document.getElementById('valBgPanY').textContent = `${{e.target.value}}px`;
                render();
            }});
            document.getElementById('bgBrightness').addEventListener('input', (e) => {{
                state.bg.brightness = parseInt(e.target.value) / 100;
                document.getElementById('valBgBrightness').textContent = `${{e.target.value}}%`;
                render();
            }});
            document.getElementById('bgContrast').addEventListener('input', (e) => {{
                state.bg.contrast = parseInt(e.target.value) / 100;
                document.getElementById('valBgContrast').textContent = `${{e.target.value}}%`;
                render();
            }});

            // Player controls
            document.getElementById('chkShowVector').addEventListener('change', (e) => {{ state.vector.show = e.target.checked; render(); }});
            document.getElementById('vecX').addEventListener('input', (e) => {{
                state.vector.x = parseInt(e.target.value);
                document.getElementById('valVecX').textContent = `${{e.target.value}}px`;
                render();
            }});
            document.getElementById('vecY').addEventListener('input', (e) => {{
                state.vector.y = parseInt(e.target.value);
                document.getElementById('valVecY').textContent = `${{e.target.value}}px`;
                render();
            }});
            document.getElementById('vecScale').addEventListener('input', (e) => {{
                state.vector.scale = parseInt(e.target.value) / 100;
                document.getElementById('valVecScale').textContent = `${{e.target.value}}%`;
                render();
            }});
            document.getElementById('chkVecFlip').addEventListener('change', (e) => {{ state.vector.flip = e.target.checked; render(); }});
            document.getElementById('chkVecShadow').addEventListener('change', (e) => {{ state.vector.shadow = e.target.checked; render(); }});

            // Template overlay
            document.getElementById('selectTemplateOverlay').addEventListener('change', (e) => {{ state.template.url = resolveUrl(e.target.value); render(); }});
            document.getElementById('tmplOpacity').addEventListener('input', (e) => {{
                state.template.opacity = parseInt(e.target.value) / 100;
                document.getElementById('valTmplOpacity').textContent = `${{e.target.value}}%`;
                render();
            }});

            // Uploads
            document.getElementById('btnUploadBg').addEventListener('click', () => document.getElementById('fileBgInput').click());
            document.getElementById('fileBgInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const reader = new FileReader();
                reader.onload = (evt) => {{ state.bg.url = evt.target.result; render(); showToast("✅ تم وضع الصورة الخلفية!"); }};
                reader.readAsDataURL(e.target.files[0]);
            }});

            document.getElementById('btnUploadCutout').addEventListener('click', () => document.getElementById('fileCutoutInput').click());
            document.getElementById('fileCutoutInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const reader = new FileReader();
                reader.onload = (evt) => {{ state.vector.url = evt.target.result; state.vector.show = true; document.getElementById('chkShowVector').checked = true; render(); showToast("✅ تم وضع صورة اللاعب المفرغة!"); }};
                reader.readAsDataURL(e.target.files[0]);
            }});

            document.getElementById('btnUploadTemplateOverlay').addEventListener('click', () => document.getElementById('fileTemplateInput').click());
            document.getElementById('fileTemplateInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const reader = new FileReader();
                reader.onload = (evt) => {{ state.template.url = evt.target.result; render(); showToast("🎉 تم تطبيق القالب الجديد فورًا!"); }};
                reader.readAsDataURL(e.target.files[0]);
            }});

            // Zoom Buttons
            document.getElementById('btnZoomFit').addEventListener('click', () => {{ state.zoom = 'fit'; updateZoom(); }});
            document.getElementById('btnZoomIn').addEventListener('click', () => {{ state.zoom = typeof state.zoom === 'number' ? Math.min(state.zoom + 0.15, 1.5) : 0.6; updateZoom(); }});
            document.getElementById('btnZoomOut').addEventListener('click', () => {{ state.zoom = typeof state.zoom === 'number' ? Math.max(state.zoom - 0.15, 0.2) : 0.35; updateZoom(); }});
            window.addEventListener('resize', updateZoom);

            // Export
            document.getElementById('btnExportHd').addEventListener('click', () => {{
                const link = document.createElement('a');
                link.download = `volt_card_${{Date.now()}}.jpg`;
                link.href = canvas.toDataURL('image/jpeg', 0.94);
                link.click();
                showToast("📥 تم تنزيل الكارت عالي الجودة بنجاح!");
            }});

            // Live News Modal
            document.getElementById('btnLiveNewsModal').addEventListener('click', openNewsModal);
            document.getElementById('btnCloseNewsModal').addEventListener('click', () => document.getElementById('modalLiveNews').classList.remove('active'));

            // Publish Modal
            document.getElementById('btnPublishModal').addEventListener('click', () => {{
                const captionText = state.sentences.map(s => s.text).join(' - ');
                document.getElementById('pubCaption').value = `${{captionText}}\\n\\n#كورة_ڤولت #فانتازي_ڤولت`;
                document.getElementById('pubPreviewImg').src = canvas.toDataURL('image/jpeg', 0.8);
                document.getElementById('modalPublish').classList.add('active');
            }});
            document.getElementById('btnClosePublishModal').addEventListener('click', () => document.getElementById('modalPublish').classList.remove('active'));
            document.getElementById('btnCancelPublish').addEventListener('click', () => document.getElementById('modalPublish').classList.remove('active'));
            document.getElementById('btnConfirmPublish').addEventListener('click', publishFacebook);

            // AI Background
            document.getElementById('btnGenerateAiBg').addEventListener('click', async () => {{
                const prompt = document.getElementById('promptAiBg').value.trim();
                if (!prompt) return;
                showToast("⚡ جاري توليد خلفية AI بـ FLUX (2.5 ثانية)...");
                try {{
                    const formData = new FormData();
                    formData.append('prompt', prompt);
                    const res = await fetch(`${{API_BASE}}/api/generate_ai_bg`, {{ method: 'POST', body: formData }}).then(r => r.json());
                    if (res.status === 'success') {{
                        state.bg.url = resolveUrl(res.url);
                        render();
                        showToast("✅ تم توليد وتطبيق الخلفية بنجاح!");
                    }} else {{
                        showToast(`❌ ${{res.message}}`);
                    }}
                }} catch (e) {{
                    showToast("تأكد من تشغيل السيرفر المحلي عبر start_studio.bat");
                }}
            }});

            // AI Vector
            document.getElementById('btnGenerateVectorAi').addEventListener('click', async () => {{
                const name = document.getElementById('aiPlayerName').value.trim();
                const club = document.getElementById('aiPlayerClub').value.trim();
                if (!name) return;
                showToast(`⚡ جاري رسم فيكتور كرتوني لـ ${{name}} وعزل الخلفية بـ Rembg...`);
                try {{
                    const formData = new FormData();
                    formData.append('player_name', name);
                    formData.append('club', club);
                    const res = await fetch(`${{API_BASE}}/api/generate_ai_vector`, {{ method: 'POST', body: formData }}).then(r => r.json());
                    if (res.status === 'success') {{
                        state.vector.url = resolveUrl(res.url);
                        state.vector.show = true;
                        document.getElementById('chkShowVector').checked = true;
                        render();
                        showToast(`🎉 تم رسم وعزل فيكتور ${{name}} بنجاح!`);
                    }} else {{
                        showToast(`❌ ${{res.message}}`);
                    }}
                }} catch (e) {{
                    showToast("تأكد من تشغيل السيرفر المحلي عبر start_studio.bat");
                }}
            }});
        }}

        async function loadGalleries() {{
            try {{
                const res = await fetch(`${{API_BASE}}/api/resources`).then(r => r.json());
                const bgGrid = document.getElementById('bgGallery');
                bgGrid.innerHTML = '';
                res.photos.forEach(p => {{
                    const el = document.createElement('div');
                    el.className = 'thumb-box';
                    el.innerHTML = `<img src="${{resolveUrl(p.url)}}"><span>${{p.name}}</span>`;
                    el.onclick = () => {{
                        document.querySelectorAll('#bgGallery .thumb-box').forEach(i => i.classList.remove('active'));
                        el.classList.add('active');
                        state.bg.url = resolveUrl(p.url);
                        render();
                    }};
                    bgGrid.appendChild(el);
                }});

                const cutGrid = document.getElementById('cutoutGallery');
                cutGrid.innerHTML = '';
                res.cutouts.forEach(c => {{
                    const el = document.createElement('div');
                    el.className = 'thumb-box';
                    el.innerHTML = `<img src="${{resolveUrl(c.url)}}"><span>${{c.name}}</span>`;
                    el.onclick = () => {{
                        document.querySelectorAll('#cutoutGallery .thumb-box').forEach(i => i.classList.remove('active'));
                        el.classList.add('active');
                        state.vector.url = resolveUrl(c.url);
                        state.vector.show = true;
                        document.getElementById('chkShowVector').checked = true;
                        render();
                    }};
                    cutGrid.appendChild(el);
                }});
            }} catch (e) {{
                console.log("Galleries offline mode.");
            }}
        }}

        async function openNewsModal() {{
            const modal = document.getElementById('modalLiveNews');
            modal.classList.add('active');
            const list = document.getElementById('liveNewsList');
            list.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-muted);">جاري جلب أحدث الأخبار الحقيقية...</div>';

            try {{
                const res = await fetch(`${{API_BASE}}/api/live_feed`).then(r => r.json());
                list.innerHTML = '';
                res.articles.forEach(a => {{
                    const item = document.createElement('div');
                    item.className = 'news-item';
                    item.innerHTML = `<h4>${{a.title}}</h4><p>📍 المصدر: ${{a.source}} ${{a.photo_url ? '• 📷 صورة متوفرة' : ''}}</p>`;
                    item.onclick = () => {{
                        // Split title into sentences if suitable
                        const words = a.title.split(' ');
                        if (words.length > 7 && state.sentences.length >= 2) {{
                            const mid = Math.ceil(words.length / 2);
                            state.sentences[0].text = words.slice(0, mid).join(' ');
                            state.sentences[1].text = words.slice(mid).join(' ');
                        }} else {{
                            state.sentences[0].text = a.title;
                        }}
                        if (a.photo_url) state.bg.url = a.photo_url;
                        loadActiveSentenceIntoInputs();
                        modal.classList.remove('active');
                        render();
                        showToast("📰 تم ملء الخبر الحقيقي وتوزيعه على الجمل!");
                    }};
                    list.appendChild(item);
                }});
            }} catch (e) {{
                list.innerHTML = '<div style="color:var(--rose); padding:10px;">فشل الاتصال بالأخبار الحية</div>';
            }}
        }}

        async function publishFacebook() {{
            const btn = document.getElementById('btnConfirmPublish');
            btn.disabled = true;
            btn.textContent = "جاري النشر...";

            try {{
                const b64 = canvas.toDataURL('image/jpeg', 0.94);
                const caption = document.getElementById('pubCaption').value;
                const page = document.getElementById('pubTargetPage').value;

                const res = await fetch(`${{API_BASE}}/api/publish_card`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ image_base64: b64, caption: caption, target_page: page }})
                }}).then(r => r.json());

                if (res.status === 'success') {{
                    document.getElementById('modalPublish').classList.remove('active');
                    showToast(`🎉 تم النشر بنجاح على فيسبوك! معرف البوست: ${{res.post_id}}`);
                }} else {{
                    showToast(`❌ فشل النشر: ${{res.message}}`);
                }}
            }} catch (e) {{
                showToast(`❌ خطأ: ${{e.message}}`);
            }} finally {{
                btn.disabled = false;
                btn.textContent = "تأكيد ونشر الآن";
            }}
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3500);
        }}

        // Init
        window.addEventListener('DOMContentLoaded', async () => {{
            setupListeners();
            await loadGalleries();
            applyPreset('kora_breaking');
        }});
    </script>
</body>
</html>
'''

target_file = os.path.join(BASE_DIR, "studio", "static", "index.html")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"✅ Generated studio with all 6 requested fonts & multi-element customizer: {target_file}")
print(f"Total HTML file size: {len(html_code)/1024:.1f} KB")
