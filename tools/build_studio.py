import os
import base64

BASE_DIR = r"C:\Users\Mogz\fantasy-volt"
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "AraJozoor-Regular.ttf")

with open(FONT_PATH, "rb") as f:
    jozoor_b64 = base64.b64encode(f.read()).decode()

html_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Volt Card Studio — أستوديو تصاميم وقوالب ڤولت</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        /* ═══════════════════════════════════════════════════════════════
           EMBEDDED OFFICIAL JOZOOR FONT (Works offline & local)
           ═══════════════════════════════════════════════════════════════ */
        @font-face {{
            font-family: 'AraJozoor';
            src: url('data:font/truetype;charset=utf-8;base64,{jozoor_b64}') format('truetype');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }}

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
            --font-jozor: 'AraJozoor', 'Cairo', sans-serif;
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

        /* TOP NAVIGATION BAR */
        .topbar {{
            height: 60px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 100;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-icon {{
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, rgba(0,210,255,0.2), rgba(0,119,182,0.4));
            border: 1px solid rgba(0,210,255,0.4);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 0 15px rgba(0,210,255,0.25);
        }}

        .brand-title {{
            font-family: var(--font-jozor);
            font-size: 19px;
            font-weight: 900;
            letter-spacing: 1.5px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .brand-badge {{
            background: rgba(0, 210, 255, 0.15);
            border: 1px solid rgba(0, 210, 255, 0.3);
            color: var(--cyan);
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 700;
        }}

        .topbar-center {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .preset-badge-group {{
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
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
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
            border: 1px solid rgba(0, 210, 255, 0.2);
        }}

        .dimension-tag {{
            font-size: 12px;
            color: var(--text-muted);
            background: var(--bg-card);
            border: 1px solid var(--border);
            padding: 5px 10px;
            border-radius: 6px;
            font-family: monospace;
            font-weight: 700;
        }}

        .topbar-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* BUTTONS */
        .btn {{
            padding: 7px 14px;
            border-radius: 7px;
            border: 1px solid transparent;
            font-size: 12px;
            font-weight: 700;
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
            border-color: rgba(0, 132, 209, 0.4);
        }}

        .btn-primary:hover {{
            filter: brightness(1.15);
            box-shadow: 0 0 12px rgba(0, 132, 209, 0.4);
        }}

        .btn-accent {{
            background: linear-gradient(135deg, var(--cyan), var(--blue));
            color: #030712;
            font-weight: 800;
        }}

        .btn-accent:hover {{
            filter: brightness(1.1);
            box-shadow: 0 0 16px rgba(0, 210, 255, 0.5);
        }}

        /* MAIN APP LAYOUT */
        .app-body {{
            display: flex;
            flex: 1;
            height: calc(100vh - 60px);
            overflow: hidden;
            position: relative;
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
            height: 42px;
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
            gap: 6px;
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

        .zoom-label {{
            font-size: 12px;
            color: var(--text-muted);
            min-width: 60px;
            text-align: center;
            font-family: monospace;
            font-weight: 700;
        }}

        .workspace-tools {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 12px;
            color: var(--text-muted);
        }}

        .canvas-area {{
            flex: 1;
            overflow: auto;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
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
            cursor: default;
        }}

        /* SIDEBAR (RIGHT / CONTROLS) */
        .sidebar {{
            width: 480px;
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
            gap: 6px;
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
            padding: 18px;
            display: none;
            flex-direction: column;
            gap: 14px;
        }}

        .panel-body.active {{
            display: flex;
        }}

        /* CARDS / CONTROL GROUPS */
        .box {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
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

        /* FORM CONTROLS */
        label {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 700;
            display: block;
            margin-bottom: 4px;
        }}

        input[type="text"], textarea, select {{
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 8px 10px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
        }}

        input[type="text"]:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: var(--cyan);
            box-shadow: 0 0 8px rgba(0, 210, 255, 0.25);
        }}

        textarea {{
            resize: vertical;
            line-height: 1.5;
            font-family: var(--font-jozor);
            font-size: 14px;
        }}

        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }}

        .slider-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
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
            height: 34px;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 6px;
            cursor: pointer;
            padding: 2px;
        }}

        /* SWITCH TOGGLE */
        .toggle-switch {{
            position: relative;
            display: inline-block;
            width: 34px;
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
            transform: translateX(16px);
            background-color: #030712;
        }}

        /* GALLERIES */
        .thumbs-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            max-height: 160px;
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
            max-width: 620px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 25px 60px rgba(0,0,0,0.9);
        }}

        .modal-head {{
            padding: 14px 18px;
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
            font-size: 22px;
            cursor: pointer;
        }}

        .modal-close:hover {{
            color: #ffffff;
        }}

        .modal-content {{
            padding: 18px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .news-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .news-item:hover {{
            border-color: var(--cyan);
            background: var(--bg-input);
        }}

        .news-item h4 {{
            font-size: 13px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
        }}

        .news-item p {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        /* TOAST */
        .toast {{
            position: fixed;
            bottom: 24px;
            left: 24px;
            background: var(--bg-card);
            border: 1px solid var(--cyan);
            color: #ffffff;
            padding: 12px 18px;
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8), 0 0 15px rgba(0, 210, 255, 0.3);
            font-size: 13px;
            font-weight: 700;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
            z-index: 2000;
            display: flex;
            align-items: center;
            gap: 8px;
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
                <span class="brand-badge">PRO CARD ENGINE</span>
            </div>
        </div>

        <div class="topbar-center">
            <div class="preset-badge-group">
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

    <!-- MAIN STUDIO BODY -->
    <div class="app-body">
        <!-- SIDEBAR CONTROLS (RIGHT) -->
        <aside class="sidebar">
            <nav class="nav-tabs">
                <button class="nav-tab active" data-target="panel-text">✍️ النصوص</button>
                <button class="nav-tab" data-target="panel-bg">🖼️ الخلفية</button>
                <button class="nav-tab" data-target="panel-vector">👤 اللاعب</button>
                <button class="nav-tab" data-target="panel-template">🎨 القالب</button>
            </nav>

            <!-- TAB 1: TYPOGRAPHY -->
            <div class="panel-body active" id="panel-text">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">نص العنوان / المانشيت</span>
                        <span class="box-action" id="btnSampleText">تعبئة نموذج</span>
                    </div>
                    <textarea id="textHeadline" rows="3" placeholder="اكتب العنوان هنا..."></textarea>
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">خصائص الخط العربي (Typography)</span>
                    </div>

                    <div class="grid-2">
                        <div>
                            <label>نوع الخط:</label>
                            <select id="fontFamily">
                                <option value="AraJozoor" selected>خط جذور (Jozor Flat) ★</option>
                                <option value="Cairo">خط كايرو (Cairo)</option>
                                <option value="Tajawal">خط تجوال (Tajawal)</option>
                                <option value="Arial">Arial Black</option>
                            </select>
                        </div>
                        <div>
                            <label>المحاذاة:</label>
                            <select id="textAlign">
                                <option value="center">المنتصف (Center)</option>
                                <option value="right" selected>اليمين (Right)</option>
                                <option value="left">اليسار (Left)</option>
                            </select>
                        </div>
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>حجم الخط (Font Size)</span>
                            <span class="slider-val" id="valFontSize">78px</span>
                        </div>
                        <input type="range" id="fontSize" min="30" max="150" value="78">
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>تباعد الأسطر (Line Height)</span>
                            <span class="slider-val" id="valLineHeight">1.25</span>
                        </div>
                        <input type="range" id="lineHeight" min="0.8" max="2.0" step="0.05" value="1.25">
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الموقع الرأسي (Y Position)</span>
                            <span class="slider-val" id="valPosY">1240px</span>
                        </div>
                        <input type="range" id="posY" min="100" max="2500" value="1240">
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الموقع الأفقي (X Position)</span>
                            <span class="slider-val" id="valPosX">675px</span>
                        </div>
                        <input type="range" id="posX" min="50" max="2100" value="675">
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>أقصى عرض للكتلة (Max Width)</span>
                            <span class="slider-val" id="valTextWidth">1180px</span>
                        </div>
                        <input type="range" id="textWidth" min="400" max="2100" value="1180">
                    </div>

                    <div class="grid-3">
                        <div>
                            <label>لون الخط:</label>
                            <input type="color" id="textColor" value="#ffffff">
                        </div>
                        <div>
                            <label>تحديد الحواف:</label>
                            <input type="color" id="strokeColor" value="#000000">
                        </div>
                        <div>
                            <label>سمك التحديد:</label>
                            <input type="number" id="strokeWidth" min="0" max="15" value="4" style="height:34px;">
                        </div>
                    </div>
                </div>

                <!-- SOURCE & SPEAKER -->
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">المصدر والمتحدث (Bottom Credits)</span>
                    </div>

                    <div class="grid-2">
                        <div>
                            <label>صفة المصدر (أزرق سماوي):</label>
                            <input type="text" id="sourceRole" value="الصحفي">
                        </div>
                        <div>
                            <label>اسم المصدر (أبيض):</label>
                            <input type="text" id="sourceName" value="فابريزيو رومانو">
                        </div>
                    </div>

                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الموقع الرأسي للمصدر (Y)</span>
                            <span class="slider-val" id="valSourceY">1540px</span>
                        </div>
                        <input type="range" id="sourceY" min="300" max="2650" value="1540">
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الموقع الأفقي للمصدر (X)</span>
                            <span class="slider-val" id="valSourceX">675px</span>
                        </div>
                        <input type="range" id="sourceX" min="50" max="2100" value="675">
                    </div>
                </div>
            </div>

            <!-- TAB 2: BACKGROUND -->
            <div class="panel-body" id="panel-bg">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">صورة الخبر / الاستاد</span>
                    </div>
                    <button class="btn btn-outline" id="btnUploadBg" style="width:100%; justify-content:center;">📁 رفع صورة من جهازك</button>
                    <input type="file" id="fileBgInput" accept="image/*" style="display:none;">
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">✨ توليد خلفية رياضية AI بـ FLUX</span>
                    </div>
                    <input type="text" id="promptAiBg" value="football stadium pitch under dark dramatic lights, cinematic 4k sports background">
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
                        <span class="box-title">التحكم في أبعاد وموقع الصورة</span>
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الزووم (Scale)</span>
                            <span class="slider-val" id="valBgScale">100%</span>
                        </div>
                        <input type="range" id="bgScale" min="50" max="250" value="100">
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>تحريك أفقي (Pan X)</span>
                            <span class="slider-val" id="valBgPanX">0px</span>
                        </div>
                        <input type="range" id="bgPanX" min="-1000" max="1000" value="0">
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>تحريك رأسي (Pan Y)</span>
                            <span class="slider-val" id="valBgPanY">0px</span>
                        </div>
                        <input type="range" id="bgPanY" min="-1000" max="1000" value="0">
                    </div>
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>السطوع (Brightness)</span>
                            <span class="slider-val" id="valBgBrightness">100%</span>
                        </div>
                        <input type="range" id="bgBrightness" min="20" max="180" value="100">
                    </div>
                </div>
            </div>

            <!-- TAB 3: PLAYER CUTOUT -->
            <div class="panel-body" id="panel-vector">
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">طبقة اللاعب المفرغة (Cutout)</span>
                        <label class="toggle-switch">
                            <input type="checkbox" id="chkShowVector" checked>
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                    <button class="btn btn-outline" id="btnUploadCutout" style="width:100%; justify-content:center;">📁 رفع لاعب مفرغ من جهازك</button>
                    <input type="file" id="fileCutoutInput" accept="image/*" style="display:none;">
                </div>

                <div class="box">
                    <div class="box-header">
                        <span class="box-title">✨ توليد فيكتور وعزل بـ Leonardo & Rembg</span>
                    </div>
                    <div class="grid-2">
                        <input type="text" id="aiPlayerName" placeholder="اسم اللاعب" value="Erling Haaland">
                        <input type="text" id="aiPlayerClub" placeholder="النادي" value="Manchester City">
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
                        <span class="box-title">موقع وحجم اللاعب</span>
                    </div>
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
                    <div class="slider-item">
                        <div class="slider-header">
                            <span>الحجم (Scale)</span>
                            <span class="slider-val" id="valVecScale">100%</span>
                        </div>
                        <input type="range" id="vecScale" min="20" max="300" value="100">
                    </div>
                    <div class="grid-2">
                        <label><input type="checkbox" id="chkVecFlip"> عكس أفقي (Flip)</label>
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

        <!-- WORKSPACE AREA (CENTER / LEFT) -->
        <main class="workspace">
            <div class="workspace-bar">
                <div class="zoom-group">
                    <button class="tool-btn" id="btnZoomOut">🔍 -</button>
                    <span class="zoom-label" id="zoomLevel">Fit</span>
                    <button class="tool-btn" id="btnZoomIn">🔍 +</button>
                    <button class="tool-btn" id="btnZoomFit">احتواء الشاشة</button>
                </div>

                <div class="workspace-tools">
                    <label style="margin:0; display:flex; align-items:center; gap:6px; cursor:pointer;">
                        <input type="checkbox" id="chkRefOverlay"> مقارنة بالمرجع الأصلي
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
        // Automatic Protocol Resolver (Handles both http://localhost:5050 and file:///)
        const API_BASE = window.location.protocol === 'file:' ? 'http://localhost:5050' : '';

        function resolveUrl(url) {{
            if (!url) return '';
            if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
            if (window.location.protocol === 'file:') {{
                // Fix relative paths for local file mode
                return '../../' + url.replace(/^\\//, '');
            }}
            return url;
        }}

        const state = {{
            width: 1350,
            height: 1688,
            zoom: 'fit',
            bg: {{
                img: null,
                url: resolveUrl('/assets/templates/default_football_bg.jpg'),
                scale: 1.0,
                panX: 0,
                panY: 0,
                brightness: 1.0
            }},
            vector: {{
                show: false,
                img: null,
                url: resolveUrl('/output/erling_haaland_vector_cutout.png'),
                x: 350,
                y: 450,
                scale: 1.0,
                flip: false,
                shadow: true
            }},
            template: {{
                img: null,
                url: resolveUrl('/assets/templates/kora_volt/breaking.png'),
                opacity: 1.0
            }},
            text: {{
                headline: "مانشستر سيتي يتوصل لاتفاق نهائي مع بيب جوارديولا لتجديد عقده لموسم إضافي",
                fontFamily: "AraJozoor",
                fontSize: 78,
                lineHeight: 1.25,
                align: "center",
                x: 675,
                y: 1240,
                maxWidth: 1180,
                color: "#ffffff",
                strokeColor: "#000000",
                strokeWidth: 4
            }},
            source: {{
                role: "الصحفي",
                roleColor: "#00b4d8",
                roleSize: 38,
                name: "فابريزيو رومانو",
                nameColor: "#ffffff",
                nameSize: 56,
                x: 675,
                y: 1540
            }},
            ref: {{
                show: false,
                img: null,
                opacity: 0.5
            }}
        }};

        const PRESETS = {{
            kora_breaking: {{
                width: 1350,
                height: 1688,
                templateUrl: '/assets/templates/kora_volt/breaking.png',
                fontSize: 78,
                lineHeight: 1.25,
                align: 'center',
                x: 675,
                y: 1240,
                maxWidth: 1180,
                sourceRole: 'الصحفي',
                sourceName: 'فابريزيو رومانو',
                sourceRoleSize: 38,
                sourceNameSize: 56,
                sourceX: 675,
                sourceY: 1540,
                vectorShow: false
            }},
            kora_manchette: {{
                width: 2160,
                height: 2700,
                templateUrl: '/assets/templates/kora_volt/manchette.png',
                fontSize: 92,
                lineHeight: 1.35,
                align: 'right',
                x: 1450,
                y: 850,
                maxWidth: 1050,
                sourceRole: 'الصحفي',
                sourceName: 'فابريزيو رومانو',
                sourceRoleSize: 42,
                sourceNameSize: 62,
                sourceX: 1450,
                sourceY: 2420,
                vectorShow: false
            }},
            fantasy_stats: {{
                width: 1350,
                height: 1688,
                templateUrl: '/assets/templates/kora_volt/breaking.png',
                fontSize: 74,
                lineHeight: 1.28,
                align: 'center',
                x: 675,
                y: 1220,
                maxWidth: 1160,
                sourceRole: 'إحصائيات',
                sourceName: 'أوبتا xG الرسمية',
                sourceRoleSize: 36,
                sourceNameSize: 52,
                sourceX: 675,
                sourceY: 1540,
                vectorShow: true
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
                    if (state.bg.brightness !== 1.0) {{
                        ctx.filter = `brightness(${{state.bg.brightness}})`;
                    }}
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

            // 4. Headline
            renderText();

            // 5. Source Credits
            renderSource();

            // 6. Ref comparison
            if (state.ref.show && state.ref.img) {{
                ctx.save();
                ctx.globalAlpha = state.ref.opacity;
                ctx.drawImage(state.ref.img, 0, 0, state.width, state.height);
                ctx.restore();
            }}

            updateZoom();
        }}

        function renderText() {{
            const text = state.text.headline.trim();
            if (!text) return;

            ctx.save();
            ctx.direction = "rtl";
            ctx.textAlign = state.text.align;
            ctx.font = `${{state.text.fontSize}}px '${{state.text.fontFamily}}', 'Cairo', sans-serif`;

            const words = text.split(/\\s+/);
            const lines = [];
            let currentLine = "";

            for (const word of words) {{
                const test = currentLine ? `${{currentLine}} ${{word}}` : word;
                if (ctx.measureText(test).width > state.text.maxWidth && currentLine) {{
                    lines.push(currentLine);
                    currentLine = word;
                }} else {{
                    currentLine = test;
                }}
            }}
            if (currentLine) lines.push(currentLine);

            const lineHeight = state.text.fontSize * state.text.lineHeight;
            lines.forEach((line, i) => {{
                const y = state.text.y + (i * lineHeight);
                ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
                ctx.shadowBlur = 10;
                ctx.shadowOffsetY = 4;

                if (state.text.strokeWidth > 0) {{
                    ctx.strokeStyle = state.text.strokeColor;
                    ctx.lineWidth = state.text.strokeWidth * 2;
                    ctx.lineJoin = "round";
                    ctx.strokeText(line, state.text.x, y);
                }}
                ctx.fillStyle = state.text.color;
                ctx.fillText(line, state.text.x, y);
            }});
            ctx.restore();
        }}

        function renderSource() {{
            const role = state.source.role.trim();
            const name = state.source.name.trim();
            if (!role && !name) return;

            ctx.save();
            ctx.direction = "rtl";
            ctx.textAlign = state.text.align;

            if (role) {{
                ctx.font = `${{state.source.roleSize}}px '${{state.text.fontFamily}}', 'Cairo', sans-serif`;
                ctx.fillStyle = state.source.roleColor;
                ctx.shadowColor = "rgba(0, 0, 0, 0.8)";
                ctx.shadowBlur = 8;
                ctx.fillText(role, state.source.x, state.source.y - (state.source.nameSize * 0.85));
            }}

            if (name) {{
                ctx.font = `${{state.source.nameSize}}px '${{state.text.fontFamily}}', 'Cairo', sans-serif`;
                ctx.fillStyle = state.source.nameColor;
                ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
                ctx.shadowBlur = 10;
                ctx.fillText(name, state.source.x, state.source.y);
            }}
            ctx.restore();
        }}

        function updateZoom() {{
            const vW = canvasArea.clientWidth - 48;
            const vH = canvasArea.clientHeight - 48;
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

        function applyPreset(id) {{
            const p = PRESETS[id];
            if (!p) return;

            state.width = p.width;
            state.height = p.height;
            state.template.url = resolveUrl(p.templateUrl);
            state.text.fontSize = p.fontSize;
            state.text.lineHeight = p.lineHeight;
            state.text.align = p.align;
            state.text.x = p.x;
            state.text.y = p.y;
            state.text.maxWidth = p.maxWidth;
            state.source.role = p.sourceRole;
            state.source.name = p.sourceName;
            state.source.roleSize = p.sourceRoleSize;
            state.source.nameSize = p.sourceNameSize;
            state.source.x = p.sourceX;
            state.source.y = p.sourceY;
            state.vector.show = p.vectorShow;

            // Update pills
            document.querySelectorAll('.preset-pill').forEach(b => b.classList.remove('active'));
            const pill = document.querySelector(`[data-preset="${{id}}"]`);
            if (pill) pill.classList.add('active');

            syncUi();
            render();
        }}

        function syncUi() {{
            document.getElementById('fontSize').value = state.text.fontSize;
            document.getElementById('valFontSize').textContent = `${{state.text.fontSize}}px`;
            document.getElementById('lineHeight').value = state.text.lineHeight;
            document.getElementById('valLineHeight').textContent = state.text.lineHeight;
            document.getElementById('posY').value = state.text.y;
            document.getElementById('valPosY').textContent = `${{state.text.y}}px`;
            document.getElementById('posX').value = state.text.x;
            document.getElementById('valPosX').textContent = `${{state.text.x}}px`;
            document.getElementById('textWidth').value = state.text.maxWidth;
            document.getElementById('valTextWidth').textContent = `${{state.text.maxWidth}}px`;
            document.getElementById('textAlign').value = state.text.align;
            document.getElementById('sourceRole').value = state.source.role;
            document.getElementById('sourceName').value = state.source.name;
            document.getElementById('sourceY').value = state.source.y;
            document.getElementById('valSourceY').textContent = `${{state.source.y}}px`;
            document.getElementById('sourceX').value = state.source.x;
            document.getElementById('valSourceX').textContent = `${{state.source.x}}px`;
            document.getElementById('chkShowVector').checked = state.vector.show;
        }}

        function setupListeners() {{
            // Preset pills
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

            // Text Inputs
            document.getElementById('textHeadline').addEventListener('input', (e) => {{
                state.text.headline = e.target.value;
                render();
            }});
            document.getElementById('fontFamily').addEventListener('change', (e) => {{
                state.text.fontFamily = e.target.value;
                render();
            }});
            document.getElementById('textAlign').addEventListener('change', (e) => {{
                state.text.align = e.target.value;
                render();
            }});
            document.getElementById('fontSize').addEventListener('input', (e) => {{
                state.text.fontSize = parseInt(e.target.value);
                document.getElementById('valFontSize').textContent = `${{state.text.fontSize}}px`;
                render();
            }});
            document.getElementById('lineHeight').addEventListener('input', (e) => {{
                state.text.lineHeight = parseFloat(e.target.value);
                document.getElementById('valLineHeight').textContent = state.text.lineHeight;
                render();
            }});
            document.getElementById('posY').addEventListener('input', (e) => {{
                state.text.y = parseInt(e.target.value);
                document.getElementById('valPosY').textContent = `${{state.text.y}}px`;
                render();
            }});
            document.getElementById('posX').addEventListener('input', (e) => {{
                state.text.x = parseInt(e.target.value);
                document.getElementById('valPosX').textContent = `${{state.text.x}}px`;
                render();
            }});
            document.getElementById('textWidth').addEventListener('input', (e) => {{
                state.text.maxWidth = parseInt(e.target.value);
                document.getElementById('valTextWidth').textContent = `${{state.text.maxWidth}}px`;
                render();
            }});
            document.getElementById('textColor').addEventListener('input', (e) => {{
                state.text.color = e.target.value;
                render();
            }});
            document.getElementById('strokeColor').addEventListener('input', (e) => {{
                state.text.strokeColor = e.target.value;
                render();
            }});
            document.getElementById('strokeWidth').addEventListener('input', (e) => {{
                state.text.strokeWidth = parseInt(e.target.value);
                render();
            }});

            // Source
            document.getElementById('sourceRole').addEventListener('input', (e) => {{
                state.source.role = e.target.value;
                render();
            }});
            document.getElementById('sourceName').addEventListener('input', (e) => {{
                state.source.name = e.target.value;
                render();
            }});
            document.getElementById('sourceY').addEventListener('input', (e) => {{
                state.source.y = parseInt(e.target.value);
                document.getElementById('valSourceY').textContent = `${{state.source.y}}px`;
                render();
            }});
            document.getElementById('sourceX').addEventListener('input', (e) => {{
                state.source.x = parseInt(e.target.value);
                document.getElementById('valSourceX').textContent = `${{state.source.x}}px`;
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

            // Player Vector controls
            document.getElementById('chkShowVector').addEventListener('change', (e) => {{
                state.vector.show = e.target.checked;
                render();
            }});
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
            document.getElementById('chkVecFlip').addEventListener('change', (e) => {{
                state.vector.flip = e.target.checked;
                render();
            }});
            document.getElementById('chkVecShadow').addEventListener('change', (e) => {{
                state.vector.shadow = e.target.checked;
                render();
            }});

            // Template selector
            document.getElementById('selectTemplateOverlay').addEventListener('change', (e) => {{
                state.template.url = resolveUrl(e.target.value);
                render();
            }});
            document.getElementById('tmplOpacity').addEventListener('input', (e) => {{
                state.template.opacity = parseInt(e.target.value) / 100;
                document.getElementById('valTmplOpacity').textContent = `${{e.target.value}}%`;
                render();
            }});

            // Zoom
            document.getElementById('btnZoomFit').addEventListener('click', () => {{
                state.zoom = 'fit';
                updateZoom();
            }});
            document.getElementById('btnZoomIn').addEventListener('click', () => {{
                state.zoom = typeof state.zoom === 'number' ? Math.min(state.zoom + 0.15, 1.5) : 0.6;
                updateZoom();
            }});
            document.getElementById('btnZoomOut').addEventListener('click', () => {{
                state.zoom = typeof state.zoom === 'number' ? Math.max(state.zoom - 0.15, 0.2) : 0.35;
                updateZoom();
            }});
            window.addEventListener('resize', updateZoom);

            // Export HD
            document.getElementById('btnExportHd').addEventListener('click', () => {{
                const link = document.createElement('a');
                link.download = `volt_card_${{Date.now()}}.jpg`;
                link.href = canvas.toDataURL('image/jpeg', 0.94);
                link.click();
                showToast("📥 تم تنزيل الكارت عالي الجودة!");
            }});

            // Upload Background
            document.getElementById('btnUploadBg').addEventListener('click', () => {{
                document.getElementById('fileBgInput').click();
            }});
            document.getElementById('fileBgInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = (evt) => {{
                    state.bg.url = evt.target.result;
                    render();
                    showToast("✅ تم تطبيق الصورة الخلفية بنجاح!");
                }};
                reader.readAsDataURL(file);
            }});

            // Upload Cutout
            document.getElementById('btnUploadCutout').addEventListener('click', () => {{
                document.getElementById('fileCutoutInput').click();
            }});
            document.getElementById('fileCutoutInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = (evt) => {{
                    state.vector.url = evt.target.result;
                    state.vector.show = true;
                    document.getElementById('chkShowVector').checked = true;
                    render();
                    showToast("✅ تم وضع صورة اللاعب في الكارت!");
                }};
                reader.readAsDataURL(file);
            }});

            // Upload Template
            document.getElementById('btnUploadTemplateOverlay').addEventListener('click', () => {{
                document.getElementById('fileTemplateInput').click();
            }});
            document.getElementById('fileTemplateInput').addEventListener('change', (e) => {{
                if (!e.target.files.length) return;
                const file = e.target.files[0];
                const reader = new FileReader();
                reader.onload = (evt) => {{
                    state.template.url = evt.target.result;
                    render();
                    showToast("🎉 تم تطبيق القالب الجديد على الفور!");
                }};
                reader.readAsDataURL(file);
            }});

            // Fill sample text
            document.getElementById('btnSampleText').addEventListener('click', () => {{
                state.text.headline = "بيب جوارديولا يحسم مصيره رسميًا: وقعت عقدي الجديد مع مانشستر سيتي ومستمر لموسم آخر لأنني أحب هذا النادي وجمهوره الاستثنائي";
                document.getElementById('textHeadline').value = state.text.headline;
                render();
            }});

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

            // Modals
            document.getElementById('btnLiveNewsModal').addEventListener('click', openNewsModal);
            document.getElementById('btnCloseNewsModal').addEventListener('click', () => {{
                document.getElementById('modalLiveNews').classList.remove('active');
            }});

            document.getElementById('btnPublishModal').addEventListener('click', () => {{
                document.getElementById('pubCaption').value = `${{state.text.headline}}\\n\\n#كورة_ڤولت #فانتازي_ڤولت`;
                document.getElementById('pubPreviewImg').src = canvas.toDataURL('image/jpeg', 0.8);
                document.getElementById('modalPublish').classList.add('active');
            }});
            document.getElementById('btnClosePublishModal').addEventListener('click', () => {{
                document.getElementById('modalPublish').classList.remove('active');
            }});
            document.getElementById('btnCancelPublish').addEventListener('click', () => {{
                document.getElementById('modalPublish').classList.remove('active');
            }});
            document.getElementById('btnConfirmPublish').addEventListener('click', publishFacebook);

            // Ref overlay
            document.getElementById('chkRefOverlay').addEventListener('change', async (e) => {{
                state.ref.show = e.target.checked;
                document.getElementById('refOpacity').style.display = e.target.checked ? 'inline-block' : 'none';
                if (e.target.checked && !state.ref.img) {{
                    state.ref.img = await loadImage('/assets/templates/kora_volt_example.png');
                }}
                render();
            }});
            document.getElementById('refOpacity').addEventListener('input', (e) => {{
                state.ref.opacity = parseInt(e.target.value) / 100;
                render();
            }});
        }}

        async function loadGalleries() {{
            try {{
                const res = await fetch(`${{API_BASE}}/api/resources`).then(r => r.json());
                // BG Gallery
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

                // Cutout Gallery
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
                console.log("Galleries loaded offline.");
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
                        state.text.headline = a.title;
                        document.getElementById('textHeadline').value = a.title;
                        if (a.photo_url) state.bg.url = a.photo_url;
                        modal.classList.remove('active');
                        render();
                        showToast("📰 تم ملء الخبر والصورة بنجاح في الكارت!");
                    }};
                    list.appendChild(item);
                }});
            }} catch (e) {{
                list.innerHTML = '<div style="color:var(--rose); padding:10px;">فشل الاتصال، تأكد من تشغيل start_studio.bat</div>';
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
    f.write(html_content)

print(f"✅ Generated single-file interactive studio: {target_file}")
print(f"File size: {len(html_content)/1024:.1f} KB")
