import os
import base64

BASE_DIR = r"C:\Users\Mogz\fantasy-volt"
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Encode all 6 fonts
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

# Read v3 code from build_studio_v3.py
with open(os.path.join(BASE_DIR, "tools", "build_studio_v3.py"), "r", encoding="utf-8") as f:
    text = f.read()

# Replace HTML in v3 to output v4
text_v4 = text.replace("PRO MULTI-LAYER", "PRO AUTOMATION")

# 1. Quick Alignment Toolbar in Tab 1
align_toolbar_html = """
                <!-- QUICK ALIGNMENT TOOLBAR -->
                <div class="box" style="padding:10px;">
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:6px;">
                        <span style="font-size:11px; font-weight:800; color:var(--cyan);">المحاذاة السريعة:</span>
                        <div style="display:flex; gap:5px;">
                            <button class="tool-btn" id="btnCenterActive" title="توسيط العنصر المحدد في المنتصف">🎯 توسيط</button>
                            <button class="tool-btn" id="btnAutoStack" title="رص الجمل عموديًا تحت بعضها بمسافات متناسقة">📐 رص عمودي متناسق</button>
                            <button class="tool-btn" id="btnAlignRight" title="محاذاة لليمين">➡️ يمين</button>
                            <button class="tool-btn" id="btnAlignLeft" title="محاذاة لليسار">⬅️ يسار</button>
                        </div>
                    </div>
                </div>
"""

old_tab1_start = '<div class="panel-body active" id="panel-text">'
new_tab1_start = old_tab1_start + "\n" + align_toolbar_html
text_v4 = text_v4.replace(old_tab1_start, new_tab1_start, 1)

# 2. Preset Manager & Delete custom preset section in Tab 4 (panel-template)
preset_manager_html = """
                <!-- PRESET MANAGER & DELETE LIST -->
                <div class="box">
                    <div class="box-header">
                        <span class="box-title">إدارة وحذف القوالب المحفوظة في النظام</span>
                    </div>
                    <div id="savedPresetsList" style="display:flex; flex-direction:column; gap:6px;">
                        <span style="font-size:11px; color:var(--text-muted);">لا توجد قوالب محفوظة حالياً.</span>
                    </div>
                </div>
"""

old_tmpl_box = '<div class="box">\n                    <div class="box-header">\n                        <span class="box-title">➕ رفع قالب شفاف جديد (PNG)</span>'
new_tmpl_box = preset_manager_html + "\n                " + old_tmpl_box
text_v4 = text_v4.replace(old_tmpl_box, new_tmpl_box, 1)

# 3. Add Save Preset Modal with Role Selection & Link to bot system
save_preset_modal_html = """
    <!-- MODAL: SAVE PRESET TO SYSTEM -->
    <div class="modal" id="modalSavePreset">
        <div class="modal-card">
            <div class="modal-head">
                <h3>💾 حفظ القالب وربطه بنظام النشر الآلي فورًا</h3>
                <button class="modal-close" id="btnCloseSaveModal">&times;</button>
            </div>
            <div class="modal-content">
                <label>اسم القالب:</label>
                <input type="text" id="presetSaveName" placeholder="مثال: قالب العاجل المطور 2026" value="قالب العاجل المطور">

                <label>تحديد الدور النشط في نظام البوت (Active Automation Role):</label>
                <select id="presetActiveRole">
                    <option value="kora_breaking">⚡ قالب الأخبار العاجلة لصفحة كورة ڤولت (Kora Breaking)</option>
                    <option value="kora_manchette">📝 قالب المانشيت والتصريحات لصفحة كورة ڤولت (Kora Manchette)</option>
                    <option value="fantasy_breaking">🟣 قالب الأخبار لصفحة فانتازي ڤولت (Fantasy Breaking)</option>
                    <option value="fantasy_stats">📊 قالب الإحصائيات لصفحة فانتازي ڤولت (Fantasy Stats)</option>
                    <option value="">➕ قالب مخصص إضافي (بدون تعيين افتراضي)</option>
                </select>

                <p style="font-size:11px; color:var(--cyan); line-height:1.5;">
                    💡 عند اختيارك لدور رسمي، سيقوم النظام البرمجي تلقائيًا باعتماد هذا القالب بكل خطوطه وألوانه ومواقع جملة لجميع المنشورات القادمة في البوت وجدول السحابة!
                </p>

                <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:8px;">
                    <button class="btn btn-outline" id="btnCancelSavePreset">إلغاء</button>
                    <button class="btn btn-accent" id="btnConfirmSavePreset">تأكيد الحفظ والتفعيل فورًا</button>
                </div>
            </div>
        </div>
    </div>
"""

text_v4 = text_v4.replace('<div class="modal" id="modalLiveNews">', save_preset_modal_html + '\n    <div class="modal" id="modalLiveNews">', 1)
text_v4 = text_v4.replace('id="btnSavePreset"', 'id="btnSavePresetModal"', 1)

# 4. Add alignment, smart snapping and preset delete JS functions
js_extras = """
        // SMART ALIGNMENT & AUTO-STACK FUNCTIONS
        function centerActiveElement() {
            const center = Math.round(state.width / 2);
            const activeSent = state.sentences[state.activeSentenceIndex];
            if (activeSent) {
                activeSent.x = center;
                activeSent.align = "center";
                loadActiveSentenceIntoInputs();
            }
            render();
            recordHistory();
            showToast("🎯 تم توسيط العنصر في المنتصف!");
        }

        function autoStackSentences() {
            const center = Math.round(state.width / 2);
            let currentY = 1140;

            state.sentences.forEach(s => {
                if (!s.visible) return;
                s.x = center;
                s.y = currentY;
                s.align = "center";
                const lineH = s.size * (s.lineHeight || 1.25);
                const lineCount = Math.max(1, Math.ceil(s.text.length / 28));
                currentY += Math.round(lineCount * lineH) + 25;
            });

            state.source.roleX = center;
            state.source.roleY = currentY + 30;
            state.source.nameX = center;
            state.source.nameY = currentY + 90;

            loadActiveSentenceIntoInputs();
            loadSourceInputs();
            render();
            recordHistory();
            showToast("📐 تم رص الجمل والمصدر عموديًا وتوسيطها بنجاح!");
        }

        function alignRight() {
            const sent = state.sentences[state.activeSentenceIndex];
            if (sent) {
                sent.align = "right";
                sent.x = state.width - 120;
                loadActiveSentenceIntoInputs();
                render();
                recordHistory();
            }
        }

        function alignLeft() {
            const sent = state.sentences[state.activeSentenceIndex];
            if (sent) {
                sent.align = "left";
                sent.x = 120;
                loadActiveSentenceIntoInputs();
                render();
                recordHistory();
            }
        }

        async function saveAndLinkPreset() {
            const name = document.getElementById('presetSaveName').value.trim() || 'قالب مخصص';
            const role = document.getElementById('presetActiveRole').value;

            const presetData = {
                width: state.width,
                height: state.height,
                templateUrl: state.template.url,
                sentences: state.sentences,
                source: state.source,
                bg: state.bg,
                vector: state.vector
            };

            try {
                const res = await fetch(`${API_BASE}/api/save_preset`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        preset_name: name,
                        preset_data: presetData,
                        active_role: role || null
                    })
                }).then(r => r.json());

                if (res.status === 'success') {
                    document.getElementById('modalSavePreset').classList.remove('active');
                    showToast(res.message);
                    loadSavedPresetsList();
                } else {
                    showToast(`❌ ${res.message}`);
                }
            } catch (e) {
                showToast("تأكد من تشغيل start_studio.bat لحفظ القالب");
            }
        }

        async function deletePreset(presetName) {
            if (!confirm(`هل أنت متأكد من حذف القالب '${presetName}' من النظام؟`)) return;

            try {
                const res = await fetch(`${API_BASE}/api/delete_preset`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ preset_name: presetName })
                }).then(r => r.json());

                if (res.status === 'success') {
                    showToast(`🗑️ ${res.message}`);
                    loadSavedPresetsList();
                } else {
                    showToast(`❌ ${res.message}`);
                }
            } catch (e) {
                showToast("فشل حذف القالب");
            }
        }

        async function loadSavedPresetsList() {
            try {
                const res = await fetch(`${API_BASE}/api/resources`).then(r => r.json());
                const container = document.getElementById('savedPresetsList');
                if (!container) return;
                container.innerHTML = '';

                const presets = res.custom_presets || {};
                const keys = Object.keys(presets).filter(k => !k.startsWith('ACTIVE_'));

                if (!keys.length) {
                    container.innerHTML = '<span style="font-size:11px; color:var(--text-muted);">لا توجد قوالب مخصصة محفوظة بعد. احفظ قالبك الآن!</span>';
                    return;
                }

                keys.forEach(k => {
                    const item = document.createElement('div');
                    item.className = 'preset-manage-item';

                    let roleBadge = '';
                    for (let r of ['kora_breaking', 'kora_manchette', 'fantasy_breaking', 'fantasy_stats']) {
                        if (presets[`ACTIVE_${r.toUpperCase()}`] === k) {
                            roleBadge = `<span>⚡ رسمي (${r})</span>`;
                            break;
                        }
                    }

                    item.innerHTML = `
                        <div>
                            <h4>${k}</h4>
                            ${roleBadge}
                        </div>
                        <div style="display:flex; gap:6px;">
                            <button class="tool-btn btn-apply-preset">تطبيق</button>
                            <button class="btn-del-preset">🗑️ حذف</button>
                        </div>
                    `;

                    item.querySelector('.btn-apply-preset').onclick = () => {
                        const p = presets[k];
                        state.width = p.width || 1350;
                        state.height = p.height || 1688;
                        state.template.url = resolveUrl(p.templateUrl);
                        if (p.sentences) state.sentences = JSON.parse(JSON.stringify(p.sentences));
                        if (p.source) state.source = JSON.parse(JSON.stringify(p.source));
                        if (p.vector) state.vector = JSON.parse(JSON.stringify(p.vector));
                        rebuildSentenceStrip();
                        loadActiveSentenceIntoInputs();
                        loadSourceInputs();
                        loadVectorInputs();
                        render();
                        recordHistory();
                        showToast(`✅ تم تطبيق القالب: ${k}`);
                    };

                    item.querySelector('.btn-del-preset').onclick = () => deletePreset(k);

                    container.appendChild(item);
                });
            } catch (e) {
                console.log("Could not load custom presets list.");
            }
        }
"""

text_v4 = text_v4.replace('function rebuildSentenceStrip()', js_extras + '\n        function rebuildSentenceStrip()', 1)

# 5. Add Alignment Buttons event listeners & Save preset modal listeners
align_listeners = """
            // Quick Alignment Buttons
            document.getElementById('btnCenterActive').addEventListener('click', centerActiveElement);
            document.getElementById('btnAutoStack').addEventListener('click', autoStackSentences);
            document.getElementById('btnAlignRight').addEventListener('click', alignRight);
            document.getElementById('btnAlignLeft').addEventListener('click', alignLeft);

            // Save Preset Modal trigger
            document.getElementById('btnSavePresetModal').addEventListener('click', () => {
                document.getElementById('modalSavePreset').classList.add('active');
            });
            document.getElementById('btnCloseSaveModal').addEventListener('click', () => {
                document.getElementById('modalSavePreset').classList.remove('active');
            });
            document.getElementById('btnCancelSavePreset').addEventListener('click', () => {
                document.getElementById('modalSavePreset').classList.remove('active');
            });
            document.getElementById('btnConfirmSavePreset').addEventListener('click', saveAndLinkPreset);
"""

text_v4 = text_v4.replace("// Preset Pills", align_listeners + "\n            // Preset Pills", 1)

# Add loadSavedPresetsList call inside loadGalleries
text_v4 = text_v4.replace('loadGalleries() {', 'loadGalleries() {\n            loadSavedPresetsList();', 1)

# 6. Add snapping guide lines rendering in render()
snap_render_code = """
            // 6. Magnetic Snapping Guide Lines (while dragging)
            if (state.drag.isDragging) {
                if (state.drag.snapCenter) {
                    ctx.save();
                    ctx.strokeStyle = "#00d2ff";
                    ctx.lineWidth = 2.5;
                    ctx.setLineDash([8, 6]);
                    ctx.shadowColor = "#00d2ff";
                    ctx.shadowBlur = 10;
                    ctx.beginPath();
                    ctx.moveTo(state.width / 2, 0);
                    ctx.lineTo(state.width / 2, state.height);
                    ctx.stroke();
                    ctx.restore();
                }
            }
"""

text_v4 = text_v4.replace('// 6. Ref Overlay', snap_render_code + '\n            // 7. Ref Overlay', 1)

# 7. Add magnetic center snapping logic inside mousemove
old_mouse_move = "let targetX = Math.round(state.drag.origX + dx);"
new_mouse_move = """
                let targetX = Math.round(state.drag.origX + dx);
                let targetY = Math.round(state.drag.origY + dy);

                // Magnetic Snapping to Center (within 22px)
                const center = Math.round(state.width / 2);
                state.drag.snapCenter = false;
                if (Math.abs(targetX - center) < 22) {
                    targetX = center;
                    state.drag.snapCenter = true;
                }
"""

text_v4 = text_v4.replace(old_mouse_move, new_mouse_move, 1)

target_index = os.path.join(BASE_DIR, "studio", "static", "index.html")
with open(target_index, "w", encoding="utf-8") as f:
    f.write(text_v4)

print(f"✅ Generated Studio v4 with Template Deletion, Smart Snapping, Auto-Stack & Bot System Linking: {target_index}")
print(f"File Size: {len(text_v4)/1024:.1f} KB")
