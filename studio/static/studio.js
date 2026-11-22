/**
 * VOLT CARD STUDIO — INTERACTIVE CLIENT ENGINE
 * Handles Canvas 2D rendering, interactive dragging, live feed loading,
 * presets switching, AI generation & direct Facebook posting.
 */

// ═══════════════════════════════════════════════════════════════════
// STATE DEFINITIONS
// ═══════════════════════════════════════════════════════════════════

const state = {
    width: 1350,
    height: 1688,
    zoom: 'fit', // 'fit', 0.25, 0.5, 0.75, 1.0

    // Layer 1: Background Photo
    bg: {
        img: null,
        url: '/assets/templates/default_football_bg.jpg',
        scale: 1.0,
        panX: 0,
        panY: 0,
        brightness: 1.0
    },

    // Layer 2: Player Cutout / Vector
    vector: {
        show: true,
        img: null,
        url: '/output/erling_haaland_vector_cutout.png',
        x: 350,
        y: 450,
        scale: 1.0,
        flip: false,
        shadow: true
    },

    // Layer 3: Template Overlay (Shading & Volt Logos)
    template: {
        img: null,
        url: '/assets/templates/kora_volt/breaking.png',
        opacity: 1.0
    },

    // Layer 4: Typography & Headlines
    text: {
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
        strokeWidth: 4,
        shadowBlur: 10
    },

    // Layer 5: Source & Speaker
    source: {
        role: "الصحفي",
        roleColor: "#00b4d8",
        roleSize: 38,
        name: "فابريزيو رومانو",
        nameColor: "#ffffff",
        nameSize: 56,
        x: 675,
        y: 1540
    },

    // Reference Comparison Overlay
    ref: {
        show: false,
        img: null,
        opacity: 0.5
    }
};

// ═══════════════════════════════════════════════════════════════════
// PRESETS
// ═══════════════════════════════════════════════════════════════════

const PRESETS = {
    kora_breaking: {
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
    },
    kora_manchette: {
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
    },
    fantasy_stats: {
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
    }
};

// ═══════════════════════════════════════════════════════════════════
// DOM ELEMENTS & INITIALIZATION
// ═══════════════════════════════════════════════════════════════════

const canvas = document.getElementById('cardCanvas');
const ctx = canvas.getContext('2d');
const viewport = document.getElementById('canvasViewport');
const wrapper = document.getElementById('canvasWrapper');

// Image Cache
const imageCache = {};

function loadImage(url) {
    if (!url) return Promise.resolve(null);
    if (imageCache[url]) return Promise.resolve(imageCache[url]);
    return new Promise((resolve) => {
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {
            imageCache[url] = img;
            resolve(img);
        };
        img.onerror = () => {
            console.warn("Failed to load image:", url);
            resolve(null);
        };
        img.src = url;
    });
}

async function initStudio() {
    setupTabs();
    setupEventListeners();
    await loadResources();
    applyPreset('kora_breaking');
    showToast("⚡ أستوديو تصاميم ڤولت جاهز للعمل!");
}

// ═══════════════════════════════════════════════════════════════════
// CANVAS RENDERING ENGINE (WYSIWYG)
// ═══════════════════════════════════════════════════════════════════

async function render() {
    canvas.width = state.width;
    canvas.height = state.height;

    // Clear Canvas
    ctx.clearRect(0, 0, state.width, state.height);
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, state.width, state.height);

    // 1. LAYER 1: Background Photo
    if (state.bg.url) {
        const bgImg = await loadImage(state.bg.url);
        if (bgImg) {
            ctx.save();
            if (state.bg.brightness !== 1.0) {
                ctx.filter = `brightness(${state.bg.brightness})`;
            }

            // Calculate cover with user scale & pan
            const scale = Math.max(state.width / bgImg.width, state.height / bgImg.height) * state.bg.scale;
            const w = bgImg.width * scale;
            const h = bgImg.height * scale;
            const x = (state.width - w) / 2 + state.bg.panX;
            const y = (state.height - h) / 2 + state.bg.panY;

            ctx.drawImage(bgImg, x, y, w, h);
            ctx.restore();
        }
    }

    // 2. LAYER 2: Player Cutout / Vector (under template overlay)
    if (state.vector.show && state.vector.url) {
        const vecImg = await loadImage(state.vector.url);
        if (vecImg) {
            ctx.save();
            const vw = vecImg.width * state.vector.scale;
            const vh = vecImg.height * state.vector.scale;
            const vx = state.vector.x;
            const vy = state.vector.y;

            if (state.vector.shadow) {
                ctx.shadowColor = "rgba(0, 0, 0, 0.85)";
                ctx.shadowBlur = 35;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 15;
            }

            if (state.vector.flip) {
                ctx.translate(vx + vw, vy);
                ctx.scale(-1, 1);
                ctx.drawImage(vecImg, 0, 0, vw, vh);
            } else {
                ctx.drawImage(vecImg, vx, vy, vw, vh);
            }
            ctx.restore();
        }
    }

    // 3. LAYER 3: Template Overlay (Transparent PNG with shading and Volt logos)
    if (state.template.url) {
        const tmplImg = await loadImage(state.template.url);
        if (tmplImg) {
            ctx.save();
            ctx.globalAlpha = state.template.opacity;
            ctx.drawImage(tmplImg, 0, 0, state.width, state.height);
            ctx.restore();
        }
    }

    // 4. LAYER 4: Typography (Headline / Statement)
    renderHeadlineText();

    // 5. LAYER 5: Source & Speaker
    renderSourceBlock();

    // 6. LAYER 6: Reference Comparison (if active)
    if (state.ref.show && state.ref.img) {
        ctx.save();
        ctx.globalAlpha = state.ref.opacity;
        ctx.drawImage(state.ref.img, 0, 0, state.width, state.height);
        ctx.restore();
    }

    updateZoomDisplay();
}

// ═══════════════════════════════════════════════════════════════════
// TEXT RENDERING HELPERS
// ═══════════════════════════════════════════════════════════════════

function renderHeadlineText() {
    const text = state.text.headline.trim();
    if (!text) return;

    ctx.save();
    ctx.direction = "rtl";
    ctx.textAlign = state.text.align;
    ctx.font = `${state.text.fontSize}px '${state.text.fontFamily}', 'Cairo', sans-serif`;

    // Wrap text into lines based on maxWidth
    const words = text.split(/\s+/);
    const lines = [];
    let currentLine = "";

    for (const word of words) {
        const testLine = currentLine ? `${currentLine} ${word}` : word;
        const metrics = ctx.measureText(testLine);
        if (metrics.width > state.text.maxWidth && currentLine) {
            lines.push(currentLine);
            currentLine = word;
        } else {
            currentLine = testLine;
        }
    }
    if (currentLine) lines.push(currentLine);

    // Compute line height & start Y
    const lineHeightPx = state.text.fontSize * state.text.lineHeight;
    let startY = state.text.y;

    lines.forEach((line, idx) => {
        const lineY = startY + (idx * lineHeightPx);

        // Text Shadow
        ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
        ctx.shadowBlur = state.text.shadowBlur;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 4;

        // Stroke
        if (state.text.strokeWidth > 0) {
            ctx.strokeStyle = state.text.strokeColor;
            ctx.lineWidth = state.text.strokeWidth * 2;
            ctx.lineJoin = "round";
            ctx.miterLimit = 2;
            ctx.strokeText(line, state.text.x, lineY);
        }

        // Fill
        ctx.fillStyle = state.text.color;
        ctx.fillText(line, state.text.x, lineY);
    });

    ctx.restore();
}

function renderSourceBlock() {
    const role = state.source.role.trim();
    const name = state.source.name.trim();
    if (!role && !name) return;

    ctx.save();
    ctx.direction = "rtl";
    ctx.textAlign = state.text.align;

    // Role (Electric Blue, e.g. #00b4d8)
    if (role) {
        ctx.font = `${state.source.roleSize}px '${state.text.fontFamily}', 'Cairo', sans-serif`;
        ctx.fillStyle = state.source.roleColor;
        ctx.shadowColor = "rgba(0, 0, 0, 0.8)";
        ctx.shadowBlur = 8;
        ctx.shadowOffsetY = 2;
        ctx.fillText(role, state.source.x, state.source.y - (state.source.nameSize * 0.85));
    }

    // Name (White, e.g. #ffffff)
    if (name) {
        ctx.font = `${state.source.nameSize}px '${state.text.fontFamily}', 'Cairo', sans-serif`;
        ctx.fillStyle = state.source.nameColor;
        ctx.shadowColor = "rgba(0, 0, 0, 0.9)";
        ctx.shadowBlur = 10;
        ctx.shadowOffsetY = 3;
        ctx.fillText(name, state.source.x, state.source.y);
    }

    ctx.restore();
}

// ═══════════════════════════════════════════════════════════════════
// UI & PRESET BINDINGS
// ═══════════════════════════════════════════════════════════════════

function applyPreset(presetId) {
    const p = PRESETS[presetId];
    if (!p) return;

    state.width = p.width;
    state.height = p.height;
    state.template.url = p.templateUrl;
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

    syncInputsWithState();
    render();
}

function syncInputsWithState() {
    document.getElementById('fontSize').value = state.text.fontSize;
    document.getElementById('valFontSize').textContent = `${state.text.fontSize}px`;
    document.getElementById('lineHeight').value = state.text.lineHeight;
    document.getElementById('valLineHeight').textContent = state.text.lineHeight;
    document.getElementById('posY').value = state.text.y;
    document.getElementById('valPosY').textContent = `${state.text.y}px`;
    document.getElementById('posX').value = state.text.x;
    document.getElementById('valPosX').textContent = `${state.text.x}px`;
    document.getElementById('textWidth').value = state.text.maxWidth;
    document.getElementById('valTextWidth').textContent = `${state.text.maxWidth}px`;
    document.getElementById('textAlign').value = state.text.align;
    document.getElementById('sourceRole').value = state.source.role;
    document.getElementById('sourceName').value = state.source.name;
    document.getElementById('sourceY').value = state.source.y;
    document.getElementById('valSourceY').textContent = `${state.source.y}px`;
    document.getElementById('sourceX').value = state.source.x;
    document.getElementById('valSourceX').textContent = `${state.source.x}px`;
    document.getElementById('chkShowVector').checked = state.vector.show;
    document.getElementById('selectTemplateOverlay').value = state.template.url;
}

function updateZoomDisplay() {
    let scale = 1.0;
    const vW = viewport.clientWidth - 40;
    const vH = viewport.clientHeight - 40;

    if (state.zoom === 'fit') {
        scale = Math.min(vW / state.width, vH / state.height);
    } else {
        scale = state.zoom;
    }

    canvas.style.width = `${state.width * scale}px`;
    canvas.style.height = `${state.height * scale}px`;
    document.getElementById('zoomLevel').textContent = state.zoom === 'fit' ? `Fit (${Math.round(scale * 100)}%)` : `${Math.round(scale * 100)}%`;
}

// ═══════════════════════════════════════════════════════════════════
// TABS & EVENT LISTENERS
// ═══════════════════════════════════════════════════════════════════

function setupTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });
}

function setupEventListeners() {
    // Quick Preset Dropdown
    document.getElementById('quickPresetSelect').addEventListener('change', (e) => {
        applyPreset(e.target.value);
    });

    // Headline Text
    document.getElementById('textHeadline').addEventListener('input', (e) => {
        state.text.headline = e.target.value;
        render();
    });
    document.getElementById('fontFamily').addEventListener('change', (e) => {
        state.text.fontFamily = e.target.value;
        render();
    });
    document.getElementById('textAlign').addEventListener('change', (e) => {
        state.text.align = e.target.value;
        render();
    });
    document.getElementById('fontSize').addEventListener('input', (e) => {
        state.text.fontSize = parseInt(e.target.value);
        document.getElementById('valFontSize').textContent = `${state.text.fontSize}px`;
        render();
    });
    document.getElementById('lineHeight').addEventListener('input', (e) => {
        state.text.lineHeight = parseFloat(e.target.value);
        document.getElementById('valLineHeight').textContent = state.text.lineHeight;
        render();
    });
    document.getElementById('posY').addEventListener('input', (e) => {
        state.text.y = parseInt(e.target.value);
        document.getElementById('valPosY').textContent = `${state.text.y}px`;
        render();
    });
    document.getElementById('posX').addEventListener('input', (e) => {
        state.text.x = parseInt(e.target.value);
        document.getElementById('valPosX').textContent = `${state.text.x}px`;
        render();
    });
    document.getElementById('textWidth').addEventListener('input', (e) => {
        state.text.maxWidth = parseInt(e.target.value);
        document.getElementById('valTextWidth').textContent = `${state.text.maxWidth}px`;
        render();
    });
    document.getElementById('textColor').addEventListener('input', (e) => {
        state.text.color = e.target.value;
        render();
    });
    document.getElementById('strokeColor').addEventListener('input', (e) => {
        state.text.strokeColor = e.target.value;
        render();
    });
    document.getElementById('strokeWidth').addEventListener('input', (e) => {
        state.text.strokeWidth = parseInt(e.target.value);
        render();
    });

    // Source Block
    document.getElementById('sourceRole').addEventListener('input', (e) => {
        state.source.role = e.target.value;
        render();
    });
    document.getElementById('sourceRoleColor').addEventListener('input', (e) => {
        state.source.roleColor = e.target.value;
        render();
    });
    document.getElementById('sourceName').addEventListener('input', (e) => {
        state.source.name = e.target.value;
        render();
    });
    document.getElementById('sourceNameColor').addEventListener('input', (e) => {
        state.source.nameColor = e.target.value;
        render();
    });
    document.getElementById('sourceY').addEventListener('input', (e) => {
        state.source.y = parseInt(e.target.value);
        document.getElementById('valSourceY').textContent = `${state.source.y}px`;
        render();
    });
    document.getElementById('sourceX').addEventListener('input', (e) => {
        state.source.x = parseInt(e.target.value);
        document.getElementById('valSourceX').textContent = `${state.source.x}px`;
        render();
    });

    // Background Controls
    document.getElementById('bgScale').addEventListener('input', (e) => {
        state.bg.scale = parseInt(e.target.value) / 100;
        document.getElementById('valBgScale').textContent = `${e.target.value}%`;
        render();
    });
    document.getElementById('bgPanX').addEventListener('input', (e) => {
        state.bg.panX = parseInt(e.target.value);
        document.getElementById('valBgPanX').textContent = `${e.target.value}px`;
        render();
    });
    document.getElementById('bgPanY').addEventListener('input', (e) => {
        state.bg.panY = parseInt(e.target.value);
        document.getElementById('valBgPanY').textContent = `${e.target.value}px`;
        render();
    });
    document.getElementById('bgBrightness').addEventListener('input', (e) => {
        state.bg.brightness = parseInt(e.target.value) / 100;
        document.getElementById('valBgBrightness').textContent = `${e.target.value}%`;
        render();
    });

    // Player Vector Controls
    document.getElementById('chkShowVector').addEventListener('change', (e) => {
        state.vector.show = e.target.checked;
        render();
    });
    document.getElementById('vecX').addEventListener('input', (e) => {
        state.vector.x = parseInt(e.target.value);
        document.getElementById('valVecX').textContent = `${e.target.value}px`;
        render();
    });
    document.getElementById('vecY').addEventListener('input', (e) => {
        state.vector.y = parseInt(e.target.value);
        document.getElementById('valVecY').textContent = `${e.target.value}px`;
        render();
    });
    document.getElementById('vecScale').addEventListener('input', (e) => {
        state.vector.scale = parseInt(e.target.value) / 100;
        document.getElementById('valVecScale').textContent = `${e.target.value}%`;
        render();
    });
    document.getElementById('chkVecFlip').addEventListener('change', (e) => {
        state.vector.flip = e.target.checked;
        render();
    });
    document.getElementById('chkVecShadow').addEventListener('change', (e) => {
        state.vector.shadow = e.target.checked;
        render();
    });

    // Template Overlay Controls
    document.getElementById('selectTemplateOverlay').addEventListener('change', (e) => {
        state.template.url = e.target.value;
        render();
    });
    document.getElementById('tmplOpacity').addEventListener('input', (e) => {
        state.template.opacity = parseInt(e.target.value) / 100;
        document.getElementById('valTmplOpacity').textContent = `${e.target.value}%`;
        render();
    });

    // Zoom Buttons
    document.getElementById('btnZoomFit').addEventListener('click', () => {
        state.zoom = 'fit';
        updateZoomDisplay();
    });
    document.getElementById('btnZoomIn').addEventListener('click', () => {
        state.zoom = typeof state.zoom === 'number' ? Math.min(state.zoom + 0.15, 1.5) : 0.6;
        updateZoomDisplay();
    });
    document.getElementById('btnZoomOut').addEventListener('click', () => {
        state.zoom = typeof state.zoom === 'number' ? Math.max(state.zoom - 0.15, 0.2) : 0.35;
        updateZoomDisplay();
    });
    window.addEventListener('resize', updateZoomDisplay);

    // Reference Comparison Toggle
    document.getElementById('chkRefOverlay').addEventListener('change', async (e) => {
        state.ref.show = e.target.checked;
        document.getElementById('refOpacity').style.display = e.target.checked ? 'inline-block' : 'none';
        if (e.target.checked && !state.ref.img) {
            state.ref.img = await loadImage('/assets/templates/kora_volt_example.png');
        }
        render();
    });
    document.getElementById('refOpacity').addEventListener('input', (e) => {
        state.ref.opacity = parseInt(e.target.value) / 100;
        render();
    });

    // Upload Background
    document.getElementById('btnUploadBg').addEventListener('click', () => {
        document.getElementById('fileBgInput').click();
    });
    document.getElementById('fileBgInput').addEventListener('change', async (e) => {
        if (!e.target.files.length) return;
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        showToast("جاري رفع الصورة الخلفية...");
        const res = await fetch('/api/upload_image', { method: 'POST', body: formData }).then(r => r.json());
        if (res.status === 'success') {
            state.bg.url = res.url;
            render();
            showToast("✅ تم تطبيق الصورة الخلفية بنجاح!");
        }
    });

    // Upload Cutout
    document.getElementById('btnUploadCutout').addEventListener('click', () => {
        document.getElementById('fileCutoutInput').click();
    });
    document.getElementById('fileCutoutInput').addEventListener('change', async (e) => {
        if (!e.target.files.length) return;
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        showToast("جاري رفع صورة اللاعب...");
        const res = await fetch('/api/upload_image', { method: 'POST', body: formData }).then(r => r.json());
        if (res.status === 'success') {
            state.vector.url = res.url;
            state.vector.show = true;
            document.getElementById('chkShowVector').checked = true;
            render();
            showToast("✅ تم وضع صورة اللاعب في الكارت!");
        }
    });

    // Upload New Template PNG
    document.getElementById('btnUploadTemplateOverlay').addEventListener('click', () => {
        document.getElementById('fileTemplateInput').click();
    });
    document.getElementById('fileTemplateInput').addEventListener('change', async (e) => {
        if (!e.target.files.length) return;
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);
        showToast("جاري رفع القالب الشفاف وحفظه...");
        const res = await fetch('/api/upload_template', { method: 'POST', body: formData }).then(r => r.json());
        if (res.status === 'success') {
            state.template.url = res.url;
            // Add to dropdown
            const opt = document.createElement('option');
            opt.value = res.url;
            opt.textContent = `قالب جديد: ${res.filename}`;
            opt.selected = true;
            document.getElementById('selectTemplateOverlay').appendChild(opt);
            render();
            showToast("🎉 تم حفظ القالب الجديد وتطبيقه على الفور!");
        }
    });

    // AI BG Generation (Cloudflare FLUX)
    document.getElementById('btnGenerateAiBg').addEventListener('click', async () => {
        const prompt = document.getElementById('promptAiBg').value.trim();
        if (!prompt) return;
        showToast("⚡ جاري توليد خلفية AI رياضية بـ FLUX (2.5 ثانية)...");
        const formData = new FormData();
        formData.append('prompt', prompt);
        const res = await fetch('/api/generate_ai_bg', { method: 'POST', body: formData }).then(r => r.json());
        if (res.status === 'success') {
            state.bg.url = res.url;
            render();
            showToast("✅ تم توليد وتطبيق الخلفية الرياضية بنجاح!");
        } else {
            showToast(`❌ خطأ: ${res.message}`);
        }
    });

    // AI Player Vector Generation (Leonardo Phoenix + Rembg u2net)
    document.getElementById('btnGenerateVectorAi').addEventListener('click', async () => {
        const name = document.getElementById('aiPlayerName').value.trim();
        const club = document.getElementById('aiPlayerClub').value.trim();
        if (!name) return;
        showToast(`⚡ جاري رسم فيكتور كرتوني لـ ${name} وعزل الخلفية بـ Rembg...`);
        const formData = new FormData();
        formData.append('player_name', name);
        formData.append('club', club);
        const res = await fetch('/api/generate_ai_vector', { method: 'POST', body: formData }).then(r => r.json());
        if (res.status === 'success') {
            state.vector.url = res.url;
            state.vector.show = true;
            document.getElementById('chkShowVector').checked = true;
            render();
            showToast(`🎉 تم رسم وعزل فيكتور ${name} في ثوانٍ!`);
        } else {
            showToast(`❌ خطأ: ${res.message}`);
        }
    });

    // Export HD Card
    document.getElementById('btnExportHd').addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = `volt_card_${Date.now()}.jpg`;
        link.href = canvas.toDataURL('image/jpeg', 0.94);
        link.click();
        showToast("📥 تم تنزيل الكارت عالي الجودة!");
    });

    // Live News Modal
    document.getElementById('btnLiveNewsModal').addEventListener('click', openNewsModal);
    document.getElementById('btnCloseNewsModal').addEventListener('click', () => {
        document.getElementById('modalLiveNews').classList.remove('active');
    });

    // Publish Modal
    document.getElementById('btnPublishModal').addEventListener('click', () => {
        document.getElementById('pubCaption').value = `${state.text.headline}\n\n#كورة_ڤولت #فانتازي_ڤولت`;
        document.getElementById('pubPreviewImg').src = canvas.toDataURL('image/jpeg', 0.8);
        document.getElementById('modalPublish').classList.add('active');
    });
    document.getElementById('btnClosePublishModal').addEventListener('click', () => {
        document.getElementById('modalPublish').classList.remove('active');
    });
    document.getElementById('btnCancelPublish').addEventListener('click', () => {
        document.getElementById('modalPublish').classList.remove('active');
    });
    document.getElementById('btnConfirmPublish').addEventListener('click', publishToFacebook);

    // Save Preset
    document.getElementById('btnSavePreset').addEventListener('click', saveCustomPreset);

    // Fill Sample
    document.getElementById('btnPasteSampleNews').addEventListener('click', () => {
        state.text.headline = "بيب جوارديولا يحسم مصيره رسميًا: وقعت عقدي الجديد مع مانشستر سيتي ومستمر لموسم آخر لأنني أحب هذا النادي وجمهوره الاستثنائي";
        document.getElementById('textHeadline').value = state.text.headline;
        render();
    });
}

// ═══════════════════════════════════════════════════════════════════
// RESOURCES & LIVE NEWS LOADERS
// ═══════════════════════════════════════════════════════════════════

async function loadResources() {
    try {
        const res = await fetch('/api/resources').then(r => r.json());

        // Background Photos Gallery
        const bgGrid = document.getElementById('bgGallery');
        bgGrid.innerHTML = '';
        res.photos.forEach(p => {
            const el = document.createElement('div');
            el.className = 'thumb-item';
            el.innerHTML = `<img src="${p.url}"><span>${p.name}</span>`;
            el.onclick = () => {
                document.querySelectorAll('#bgGallery .thumb-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
                state.bg.url = p.url;
                render();
            };
            bgGrid.appendChild(el);
        });

        // Cutouts Gallery
        const cutGrid = document.getElementById('cutoutGallery');
        cutGrid.innerHTML = '';
        res.cutouts.forEach(c => {
            const el = document.createElement('div');
            el.className = 'thumb-item';
            el.innerHTML = `<img src="${c.url}"><span>${c.name}</span>`;
            el.onclick = () => {
                document.querySelectorAll('#cutoutGallery .thumb-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
                state.vector.url = c.url;
                state.vector.show = true;
                document.getElementById('chkShowVector').checked = true;
                render();
            };
            cutGrid.appendChild(el);
        });

        // Template Options
        const tmplSelect = document.getElementById('selectTemplateOverlay');
        res.templates.forEach(t => {
            if (t.url && !Array.from(tmplSelect.options).some(o => o.value === t.url)) {
                const opt = document.createElement('option');
                opt.value = t.url;
                opt.textContent = t.name;
                tmplSelect.appendChild(opt);
            }
        });
    } catch (e) {
        console.error("Failed to load studio resources:", e);
    }
}

async function openNewsModal() {
    const modal = document.getElementById('modalLiveNews');
    modal.classList.add('active');
    const list = document.getElementById('liveNewsList');
    list.innerHTML = '<div class="loading">جاري جلب أحدث الأخبار الحقيقية...</div>';

    try {
        const res = await fetch('/api/live_feed').then(r => r.json());
        list.innerHTML = '';
        res.articles.forEach(a => {
            const item = document.createElement('div');
            item.className = 'news-item';
            item.innerHTML = `
                <div class="news-item-title">${a.title}</div>
                <div class="news-item-meta">
                    <span>📍 المصدر: ${a.source}</span>
                    <span>${a.photo_url ? '📷 صورة متوفرة' : ''}</span>
                </div>
            `;
            item.onclick = () => {
                state.text.headline = a.title;
                document.getElementById('textHeadline').value = a.title;
                if (a.photo_url) {
                    state.bg.url = a.photo_url;
                }
                modal.classList.remove('active');
                render();
                showToast("📰 تم ملء الخبر والصورة بنجاح في الكارت!");
            };
            list.appendChild(item);
        });
    } catch (e) {
        list.innerHTML = '<div class="error">فشل جلب الأخبار الحية، تأكد من الاتصال بالإنترنت.</div>';
    }
}

async function publishToFacebook() {
    const btn = document.getElementById('btnConfirmPublish');
    btn.disabled = true;
    btn.textContent = "جاري النشر لفيسبوك...";

    try {
        const b64 = canvas.toDataURL('image/jpeg', 0.94);
        const caption = document.getElementById('pubCaption').value;
        const page = document.getElementById('pubTargetPage').value;

        const res = await fetch('/api/publish_card', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image_base64: b64,
                caption: caption,
                target_page: page
            })
        }).then(r => r.json());

        if (res.status === 'success') {
            document.getElementById('modalPublish').classList.remove('active');
            showToast(`🎉 تم النشر بنجاح على فيسبوك! معرف البوست: ${res.post_id}`);
        } else {
            showToast(`❌ فشل النشر: ${res.message}`);
        }
    } catch (e) {
        showToast(`❌ خطأ: ${e.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = "تأكيد ونشر الآن";
    }
}

async function saveCustomPreset() {
    const name = prompt("اكتب اسماً للقالب لحفظه في النظام البرمجي:", "قالب مخصص 1");
    if (!name) return;

    const presetData = {
        width: state.width,
        height: state.height,
        templateUrl: state.template.url,
        fontSize: state.text.fontSize,
        lineHeight: state.text.lineHeight,
        align: state.text.align,
        x: state.text.x,
        y: state.text.y,
        maxWidth: state.text.maxWidth,
        sourceRole: state.source.role,
        sourceName: state.source.name,
        sourceRoleSize: state.source.roleSize,
        sourceNameSize: state.source.nameSize,
        sourceX: state.source.x,
        sourceY: state.source.y
    };

    try {
        const res = await fetch('/api/save_preset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                preset_name: name,
                preset_data: presetData
            })
        }).then(r => r.json());

        showToast(`💾 ${res.message}`);
    } catch (e) {
        showToast("فشل حفظ إعدادات القالب");
    }
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3500);
}

// Start application
window.addEventListener('DOMContentLoaded', initStudio);
