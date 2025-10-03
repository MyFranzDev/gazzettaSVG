<div class="step-container">
    <h2 class="step-title">🎨 Step 2: Risorse</h2>
    <p class="step-subtitle">Carica i loghi, scegli lo sfondo e visualizza i font disponibili</p>

    <form method="POST" enctype="multipart/form-data">
        <!-- Logo Upload -->
        <div class="form-group">
            <label>Logo (richiesto) *</label>
            <p style="font-size: 13px; color: #666; margin-bottom: 15px;">Carica il logo in 2 versioni: su sfondo chiaro e su sfondo scuro. Solo PNG trasparenti.</p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <!-- Logo White Background -->
                <div>
                    <label style="font-size: 14px; color: #333; margin-bottom: 8px; display: block;">Logo su sfondo chiaro *</label>
                    <div class="upload-area-small" id="logoWhiteBgArea" style="padding: 30px; border: 2px dashed #e0e0e0; border-radius: 8px; text-align: center; cursor: pointer; background: white; display: none;">
                        <input type="file" id="logoWhiteBg" name="logo_white_bg" accept="image/png" style="display: none;">
                        <div style="font-size: 32px;">📄</div>
                        <div style="font-size: 12px; color: #666; margin-top: 8px;">Clicca per caricare</div>
                        <div style="font-size: 11px; color: #999;">PNG trasparente</div>
                    </div>
                    <div id="logoWhiteBgPreview" style="margin-top: 10px; display: block; padding: 15px; background: white; border: 1px solid #e0e0e0; border-radius: 6px; text-align: center;">
                        <img id="logoWhiteBgImg" src="logos/logo_gazzetta_nero.png" style="max-width: 100px; max-height: 60px;">
                        <p style="margin-top: 8px; font-size: 12px; color: #666;">
                            <a href="#" id="removeLogoWhiteBg" style="color: #f44336; text-decoration: none;">✕ Rimuovi</a>
                        </p>
                    </div>
                    <input type="hidden" name="logo_white_bg_default" value="logos/logo_gazzetta_nero.png">
                </div>

                <!-- Logo Dark Background -->
                <div>
                    <label style="font-size: 14px; color: #333; margin-bottom: 8px; display: block;">Logo su sfondo scuro *</label>
                    <div class="upload-area-small" id="logoDarkBgArea" style="padding: 30px; border: 2px dashed #e0e0e0; border-radius: 8px; text-align: center; cursor: pointer; background: #2a2a2a; display: none;">
                        <input type="file" id="logoDarkBg" name="logo_dark_bg" accept="image/png" style="display: none;">
                        <div style="font-size: 32px;">📄</div>
                        <div style="font-size: 12px; color: #ccc; margin-top: 8px;">Clicca per caricare</div>
                        <div style="font-size: 11px; color: #999;">PNG trasparente</div>
                    </div>
                    <div id="logoDarkBgPreview" style="margin-top: 10px; display: block; padding: 15px; background: #2a2a2a; border: 1px solid #444; border-radius: 6px; text-align: center;">
                        <img id="logoDarkBgImg" src="logos/logo_gazzetta_bianco.png" style="max-width: 100px; max-height: 60px;">
                        <p style="margin-top: 8px; font-size: 12px; color: #ccc;">
                            <a href="#" id="removeLogoDarkBg" style="color: #ff6b6b; text-decoration: none;">✕ Rimuovi</a>
                        </p>
                    </div>
                    <input type="hidden" name="logo_dark_bg_default" value="logos/logo_gazzetta_bianco.png">
                </div>
            </div>
        </div>

        <!-- Logo Small Upload -->
        <div class="form-group" style="margin-top: 30px;">
            <label>Logo Versione Contratta (per spazi ristretti) *</label>
            <p style="font-size: 13px; color: #666; margin-bottom: 15px;">Versione compatta/quadrata del logo per banner piccoli. Solo PNG trasparenti.</p>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <!-- Logo Small White Background -->
                <div>
                    <label style="font-size: 14px; color: #333; margin-bottom: 8px; display: block;">Logo small su sfondo chiaro *</label>
                    <div id="logoSmallWhiteBgPreview" style="margin-top: 10px; display: block; padding: 15px; background: white; border: 1px solid #e0e0e0; border-radius: 6px; text-align: center;">
                        <img id="logoSmallWhiteBgImg" src="logos/G_nero.png" style="max-width: 80px; max-height: 80px;">
                        <p style="margin-top: 8px; font-size: 12px; color: #666;">
                            <a href="#" id="removeLogoSmallWhiteBg" style="color: #f44336; text-decoration: none;">✕ Rimuovi</a>
                        </p>
                    </div>
                    <input type="hidden" name="logo_small_white_default" value="logos/G_nero.png">
                </div>

                <!-- Logo Small Dark Background -->
                <div>
                    <label style="font-size: 14px; color: #333; margin-bottom: 8px; display: block;">Logo small su sfondo scuro *</label>
                    <div id="logoSmallDarkBgPreview" style="margin-top: 10px; display: block; padding: 15px; background: #2a2a2a; border: 1px solid #444; border-radius: 6px; text-align: center;">
                        <img id="logoSmallDarkBgImg" src="logos/G_bianco.png" style="max-width: 80px; max-height: 80px;">
                        <p style="margin-top: 8px; font-size: 12px; color: #ccc;">
                            <a href="#" id="removeLogoSmallDarkBg" style="color: #ff6b6b; text-decoration: none;">✕ Rimuovi</a>
                        </p>
                    </div>
                    <input type="hidden" name="logo_small_dark_default" value="logos/G_bianco.png">
                </div>
            </div>
        </div>

        <!-- Font List -->
        <div class="form-group" style="margin-top: 30px;">
            <label>Font Disponibili</label>
            <p style="font-size: 13px; color: #666; margin-bottom: 15px;">I seguenti font sono sempre disponibili nei banner.</p>

            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0;">
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="padding: 10px 0; color: #333; font-size: 15px; border-bottom: 1px solid #e0e0e0;">✓ Oswald Bold</li>
                    <li style="padding: 10px 0; color: #333; font-size: 15px; border-bottom: 1px solid #e0e0e0;">✓ Roboto Bold</li>
                    <li style="padding: 10px 0; color: #333; font-size: 15px;">✓ Roboto Regular</li>
                </ul>
            </div>

            <!-- Upload Custom Font (Demo - Disabled) -->
            <div style="margin-top: 15px;">
                <button type="button" id="uploadCustomFont" style="font-size: 13px; color: #999; background: none; border: none; cursor: pointer; text-decoration: underline; padding: 0;">
                    + Aggiungi un font personalizzato
                </button>
            </div>
        </div>

        <!-- Image Upload (Optional) -->
        <div class="form-group" style="margin-top: 30px;">
            <label>Immagine Aggiuntiva (opzionale)</label>
            <div class="upload-area" id="uploadArea">
                <input type="file" id="imageUpload" name="image" accept="image/*" style="display: none;">
                <div class="upload-icon">📤</div>
                <div class="upload-text">Clicca per caricare o trascina un'immagine qui</div>
                <div class="upload-hint">JPG, PNG - Max 5MB</div>
            </div>
            <div id="imagePreview" style="margin-top: 15px; display: none;">
                <img id="previewImg" style="max-width: 200px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <p style="margin-top: 10px; font-size: 14px; color: #666;">
                    <span id="fileName"></span> -
                    <a href="#" id="removeImage" style="color: #f44336;">Rimuovi</a>
                </p>
            </div>
        </div>

        <!-- Background Selection -->
        <div class="form-group" style="margin-top: 40px;">
            <label>Sfondo per <?= htmlspecialchars($wizardData['sport'] ?? 'Generico') ?> *</label>
            <?php
            $selectedSport = $wizardData['sport'] ?? 'Generico';
            $sportBackgrounds = $mockBackgrounds[$selectedSport] ?? $mockBackgrounds['Generico'];
            ?>
            <div class="background-grid">
                <?php foreach ($sportBackgrounds as $bg): ?>
                    <?php $selected = ($wizardData['background'] ?? '') === $bg['id']; ?>
                    <label class="background-card <?= $selected ? 'selected' : '' ?>">
                        <input type="radio" name="data[background]" value="<?= htmlspecialchars($bg['id']) ?>"
                               <?= $selected ? 'checked' : '' ?> required>
                        <img src="<?= htmlspecialchars($bg['thumb']) ?>" alt="<?= htmlspecialchars($bg['name']) ?>">
                        <div class="bg-name"><?= htmlspecialchars($bg['name']) ?></div>
                    </label>
                <?php endforeach; ?>
            </div>

            <!-- AI Generation Option (collapsable) -->
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                <button type="button" id="toggleAiSection" style="font-size: 13px; color: #999; background: none; border: none; cursor: pointer; text-decoration: none; padding: 0; display: flex; align-items: center; gap: 5px;">
                    <span id="toggleIcon">▶</span> Oppure genera un nuovo sfondo
                </button>

                <!-- AI Generation Panel (collapsed by default) -->
                <div id="aiGenerationPanel" style="display: none; margin-top: 15px; padding: 20px; background: #f9f9f9; border-radius: 8px;">
                    <p style="font-size: 13px; color: #666; margin-bottom: 15px;">
                        Genera uno sfondo personalizzato per lo sport selezionato usando l'intelligenza artificiale.
                    </p>
                    <button type="button" id="generateAiBackground" class="btn btn-primary" style="padding: 10px 24px; font-size: 14px;">
                        ✨ Genera Sfondo con AI
                    </button>

                    <!-- Loader -->
                    <div id="aiLoader" style="display: none; margin-top: 15px; padding: 30px; background: #fff; border-radius: 8px; text-align: center;">
                        <div style="font-size: 48px; animation: spin 2s linear infinite;">⚙️</div>
                        <p style="margin-top: 15px; color: #666;">Generazione in corso...</p>
                    </div>

                    <!-- Generated Image -->
                    <div id="aiGeneratedResult" style="display: none; margin-top: 15px;">
                        <label class="background-card selected" style="max-width: 300px; cursor: pointer;">
                            <input type="radio" name="data[background]" value="ai_generated" id="aiGeneratedRadio" checked>
                            <img id="aiGeneratedImage" src="" alt="Sfondo generato dall'AI" style="width: 100%; height: auto;">
                            <div class="bg-name">✨ Generato dall'AI</div>
                        </label>
                    </div>
                </div>

                <!-- AI History (if exists) -->
                <div id="aiHistory" style="display: none; margin-top: 15px;">
                    <p style="font-size: 12px; color: #666; margin-bottom: 10px;">Sfondi generati in precedenza:</p>
                    <div id="aiHistoryGrid" class="background-grid"></div>
                </div>

                <!-- Hidden field for AI prompt -->
                <input type="hidden" name="data[ai_background_prompt]" id="aiPromptHidden" value="">
            </div>
        </div>

        <div class="wizard-actions">
            <button type="submit" name="action" value="back" class="btn btn-secondary">
                ← Indietro
            </button>
            <button type="submit" name="action" value="next" class="btn btn-primary" id="nextBtn" disabled>
                Avanti: Generazione Testi AI →
            </button>
        </div>
    </form>
</div>

<!-- Snackbar -->
<div id="snackbar" style="visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 8px; padding: 16px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; transform: translateX(-50%); font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
    Funzione disponibile solo in produzione
</div>

<script>
// Logo White Background
const logoWhiteBgArea = document.getElementById('logoWhiteBgArea');
const logoWhiteBg = document.getElementById('logoWhiteBg');
const logoWhiteBgPreview = document.getElementById('logoWhiteBgPreview');
const logoWhiteBgImg = document.getElementById('logoWhiteBgImg');
const removeLogoWhiteBg = document.getElementById('removeLogoWhiteBg');

// Logo Dark Background
const logoDarkBgArea = document.getElementById('logoDarkBgArea');
const logoDarkBg = document.getElementById('logoDarkBg');
const logoDarkBgPreview = document.getElementById('logoDarkBgPreview');
const logoDarkBgImg = document.getElementById('logoDarkBgImg');
const removeLogoDarkBg = document.getElementById('removeLogoDarkBg');

// Font upload (disabled in demo)
const uploadCustomFont = document.getElementById('uploadCustomFont');

// Optional Image
const uploadArea = document.getElementById('uploadArea');
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const fileName = document.getElementById('fileName');
const removeImage = document.getElementById('removeImage');

// Logo White Background handlers
logoWhiteBgArea.addEventListener('click', () => logoWhiteBg.click());

logoWhiteBg.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleLogoUpload(e.target.files[0], 'white');
    }
});

removeLogoWhiteBg.addEventListener('click', (e) => {
    e.preventDefault();
    logoWhiteBg.value = '';
    logoWhiteBgPreview.style.display = 'none';
    logoWhiteBgArea.style.display = 'block';
    updateButtonState();
});

// Logo Dark Background handlers
logoDarkBgArea.addEventListener('click', () => logoDarkBg.click());

logoDarkBg.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleLogoUpload(e.target.files[0], 'dark');
    }
});

removeLogoDarkBg.addEventListener('click', (e) => {
    e.preventDefault();
    logoDarkBg.value = '';
    logoDarkBgPreview.style.display = 'none';
    logoDarkBgArea.style.display = 'block';
    updateButtonState();
});

// Handle logo upload with PNG validation
function handleLogoUpload(file, type) {
    if (file.type !== 'image/png') {
        alert('⚠️ Per favore carica solo file PNG trasparenti');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        if (type === 'white') {
            logoWhiteBgImg.src = e.target.result;
            logoWhiteBgPreview.style.display = 'block';
            logoWhiteBgArea.style.display = 'none';
        } else {
            logoDarkBgImg.src = e.target.result;
            logoDarkBgPreview.style.display = 'block';
            logoDarkBgArea.style.display = 'none';
        }
        updateButtonState();
    };
    reader.readAsDataURL(file);
}

// Custom font upload (DEMO MODE - disabled)
uploadCustomFont.addEventListener('click', function() {
    showSnackbar('⚠️ Ambiente demo - Funzione non disponibile');
});

// Click to upload
uploadArea.addEventListener('click', () => imageUpload.click());

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageUpload.files = files;
        handleImageUpload(files[0]);
    }
});

// File input change
imageUpload.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleImageUpload(e.target.files[0]);
    }
});

// Handle image upload
function handleImageUpload(file) {
    if (!file.type.startsWith('image/')) {
        alert('Per favore carica un\'immagine valida');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        fileName.textContent = file.name;
        imagePreview.style.display = 'block';
        uploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Remove image
removeImage.addEventListener('click', (e) => {
    e.preventDefault();
    imageUpload.value = '';
    imagePreview.style.display = 'none';
    uploadArea.style.display = 'block';
});

// Background card selection
const nextBtn = document.getElementById('nextBtn');
const toggleAiSection = document.getElementById('toggleAiSection');
const toggleIcon = document.getElementById('toggleIcon');
const aiGenerationPanel = document.getElementById('aiGenerationPanel');
const generateAiBtn = document.getElementById('generateAiBackground');
const aiLoader = document.getElementById('aiLoader');
const aiGeneratedResult = document.getElementById('aiGeneratedResult');
const aiGeneratedImage = document.getElementById('aiGeneratedImage');
const aiGeneratedRadio = document.getElementById('aiGeneratedRadio');
const aiPromptHidden = document.getElementById('aiPromptHidden');
const aiHistory = document.getElementById('aiHistory');
const aiHistoryGrid = document.getElementById('aiHistoryGrid');
const snackbar = document.getElementById('snackbar');

function updateButtonState() {
    const backgroundSelected = document.querySelector('input[name="data[background]"]:checked');

    // Check if logos are uploaded OR default logos are shown
    const logoWhiteUploaded = logoWhiteBg.files.length > 0 || logoWhiteBgPreview.style.display === 'block';
    const logoDarkUploaded = logoDarkBg.files.length > 0 || logoDarkBgPreview.style.display === 'block';

    // Enable only if background selected AND both logos available
    const allValid = backgroundSelected && logoWhiteUploaded && logoDarkUploaded;

    nextBtn.disabled = !allValid;
    nextBtn.style.opacity = allValid ? '1' : '0.5';
    nextBtn.style.cursor = allValid ? 'pointer' : 'not-allowed';
}

// Toggle AI Section
toggleAiSection.addEventListener('click', function() {
    const isVisible = aiGenerationPanel.style.display === 'block';
    aiGenerationPanel.style.display = isVisible ? 'none' : 'block';
    toggleIcon.textContent = isVisible ? '▶' : '▼';
});

// Show snackbar
function showSnackbar(message) {
    snackbar.textContent = message;
    snackbar.style.visibility = 'visible';
    snackbar.style.animation = 'fadein 0.5s, fadeout 0.5s 2.5s';

    setTimeout(() => {
        snackbar.style.visibility = 'hidden';
        snackbar.style.animation = '';
    }, 3000);
}

// AI Background Generation (DEMO MODE - disabled)
generateAiBtn.addEventListener('click', function() {
    showSnackbar('⚠️ Ambiente demo - Funzione non disponibile');
});

// Load AI history from localStorage
function loadAiHistory() {
    const history = JSON.parse(localStorage.getItem('aiBackgroundHistory') || '[]');
    if (history.length > 0) {
        aiHistory.style.display = 'block';
        aiHistoryGrid.innerHTML = '';

        history.forEach((item, index) => {
            const card = document.createElement('label');
            card.className = 'background-card';
            card.innerHTML = `
                <input type="radio" name="data[background]" value="ai_history_${index}">
                <img src="${item.image}" alt="AI Background ${index + 1}">
                <div class="bg-name">✨ ${item.sport} - ${item.date}</div>
            `;
            card.addEventListener('click', function() {
                document.querySelectorAll('.background-card').forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                this.querySelector('input[type="radio"]').checked = true;
                updateButtonState();
            });
            aiHistoryGrid.appendChild(card);
        });
    }
}

// Save AI background to history (for production use)
function saveToHistory(imageUrl, sport) {
    const history = JSON.parse(localStorage.getItem('aiBackgroundHistory') || '[]');
    history.unshift({
        image: imageUrl,
        sport: sport,
        date: new Date().toLocaleDateString('it-IT', { day: '2-digit', month: '2-digit' })
    });
    // Keep only last 5
    if (history.length > 5) history.pop();
    localStorage.setItem('aiBackgroundHistory', JSON.stringify(history));
    loadAiHistory();
}

// Background card selection
document.querySelectorAll('.background-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.background-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
        updateButtonState();
    });
});

// Initialize
updateButtonState();
loadAiHistory();
</script>

<style>
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes fadein {
    from { bottom: 0; opacity: 0; }
    to { bottom: 30px; opacity: 1; }
}

@keyframes fadeout {
    from { bottom: 30px; opacity: 1; }
    to { bottom: 0; opacity: 0; }
}
</style>
