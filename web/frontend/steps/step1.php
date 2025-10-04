<div class="step-container">
    <h2 class="step-title">📋 Step 1: Parametri Evento e Sport</h2>
    <p class="step-subtitle">Inserisci i dettagli dell'evento e seleziona lo sport</p>

    <form method="POST">
        <div class="form-group">
            <label for="evento">Evento *</label>
            <input type="text" id="evento" name="data[evento]"
                   value="<?= htmlspecialchars($wizardData['evento'] ?? 'Calcio - Finale di Champions League') ?>"
                   placeholder="es. Calcio - Finale di Champions League" required>
        </div>

        <div class="form-group">
            <label for="prezzo">Prezzo *</label>
            <p style="font-size: 13px; color: #666; margin-bottom: 10px;">Inserisci il prezzo e la periodicità separatamente</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <label for="prezzo" style="font-size: 13px; color: #555; margin-bottom: 5px; display: block;">Prezzo</label>
                    <input type="text" id="prezzo" name="data[prezzo]"
                           value="<?= htmlspecialchars($wizardData['prezzo'] ?? '0,99€') ?>"
                           placeholder="es. 0,99€" required
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                </div>
                <div>
                    <label for="periodicita" style="font-size: 13px; color: #555; margin-bottom: 5px; display: block;">Periodicità</label>
                    <input type="text" id="periodicita" name="data[periodicita]"
                           value="<?= htmlspecialchars($wizardData['periodicita'] ?? '/mese') ?>"
                           placeholder="es. /mese, /anno"
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                    <small style="font-size: 11px; color: #999; margin-top: 3px; display: block;">Lascia vuoto se non applicabile</small>
                </div>
            </div>
        </div>

        <div class="form-group">
            <label>Sport *</label>
            <div class="sport-grid">
                <?php
                $sportIcons = [
                    'Calcio' => '⚽',
                    'Tennis' => '🎾',
                    'Pallavolo/Volley' => '🏐',
                    'Ciclismo' => '🚴',
                    'Golf' => '⛳',
                    'Formula 1/Moto GP' => '🏎️',
                    'Generico' => '🏆'
                ];

                foreach ($mockSports as $sport):
                    $selected = ($wizardData['sport'] ?? 'Calcio') === $sport;
                ?>
                    <label class="sport-card <?= $selected ? 'selected' : '' ?>" data-sport="<?= htmlspecialchars($sport) ?>">
                        <input type="radio" name="data[sport]" value="<?= htmlspecialchars($sport) ?>"
                               <?= $selected ? 'checked' : '' ?> required>
                        <div class="sport-icon"><?= $sportIcons[$sport] ?? '🏅' ?></div>
                        <div class="sport-name"><?= htmlspecialchars($sport) ?></div>
                    </label>
                <?php endforeach; ?>
            </div>
        </div>

        <!-- Background Selection (shown after sport selection) -->
        <div class="form-group" id="backgroundSection" style="margin-top: 30px; display: block;">
            <label>Sfondo per <span id="selectedSportName"><?= htmlspecialchars($wizardData['sport'] ?? 'Calcio') ?></span> *</label>
            <div class="background-grid" id="backgroundGrid">
                <?php
                $selectedSport = $wizardData['sport'] ?? 'Calcio';
                $sportBackgrounds = $mockBackgrounds[$selectedSport] ?? $mockBackgrounds['Generico'];
                foreach ($sportBackgrounds as $i => $bg):
                    $selected = isset($wizardData['background']) ? ($wizardData['background'] === $bg['id']) : ($i === 0);
                ?>
                    <label class="background-card <?= $selected ? 'selected' : '' ?>">
                        <input type="radio" name="data[background]" value="<?= htmlspecialchars($bg['id']) ?>"
                               <?= $selected ? 'checked' : '' ?>>
                        <img src="<?= htmlspecialchars($bg['thumb']) ?>" alt="<?= htmlspecialchars($bg['name']) ?>">
                        <div class="bg-name"><?= htmlspecialchars($bg['name']) ?></div>
                    </label>
                <?php endforeach; ?>
            </div>
        </div>

        <!-- Image Upload (Optional) -->
        <div class="form-group" style="margin-top: 30px;">
            <label>📱 Immagine nello smartphone / immagine libera (opzionale)</label>
            <div class="upload-area" id="uploadArea">
                <input type="file" id="imageUpload" name="image" accept="image/*" style="display: none;">
                <div class="upload-icon">📱</div>
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

        <div class="wizard-actions">
            <div></div>
            <button type="submit" name="action" value="next" class="btn btn-primary" id="nextBtn" disabled>
                Avanti: Caricamento Risorse →
            </button>
        </div>
    </form>
</div>

<script>
const nextBtn = document.getElementById('nextBtn');
const backgroundSection = document.getElementById('backgroundSection');
const selectedSportName = document.getElementById('selectedSportName');
const backgroundGrid = document.getElementById('backgroundGrid');

// Background data by sport
const backgroundsBySport = <?= json_encode($mockBackgrounds) ?>;

// Check if sport and background are selected
function updateButtonState() {
    const sportSelected = document.querySelector('input[name="data[sport]"]:checked');
    const backgroundSelected = document.querySelector('input[name="data[background]"]:checked');

    const isValid = sportSelected && backgroundSelected;
    nextBtn.disabled = !isValid;

    if (isValid) {
        nextBtn.style.opacity = '1';
        nextBtn.style.cursor = 'pointer';
    } else {
        nextBtn.style.opacity = '0.5';
        nextBtn.style.cursor = 'not-allowed';
    }
}

// Update backgrounds when sport changes
function updateBackgrounds(sport) {
    selectedSportName.textContent = sport;
    const backgrounds = backgroundsBySport[sport] || backgroundsBySport['Generico'];

    backgroundGrid.innerHTML = '';
    backgrounds.forEach(bg => {
        const label = document.createElement('label');
        label.className = 'background-card';
        label.innerHTML = `
            <input type="radio" name="data[background]" value="${bg.id}">
            <img src="${bg.thumb}" alt="${bg.name}">
            <div class="bg-name">${bg.name}</div>
        `;

        label.addEventListener('click', function() {
            document.querySelectorAll('.background-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            this.querySelector('input[type="radio"]').checked = true;
            updateButtonState();
        });

        backgroundGrid.appendChild(label);
    });

    // Show background section
    backgroundSection.style.display = 'block';
    updateButtonState();
}

// Add click handler to sport cards
document.querySelectorAll('.sport-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.sport-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;

        const sport = this.dataset.sport;
        updateBackgrounds(sport);
    });
});

// Add click handler to initial background cards (if sport already selected)
document.querySelectorAll('.background-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.background-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
        updateButtonState();
    });
});

// Image upload handlers
const uploadArea = document.getElementById('uploadArea');
const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const fileName = document.getElementById('fileName');
const removeImage = document.getElementById('removeImage');

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

// Initialize button state and select first background if Calcio is default
updateButtonState();

// Auto-select first background for default sport (Calcio)
const defaultSport = document.querySelector('input[name="data[sport]"]:checked');
if (defaultSport && !document.querySelector('input[name="data[background]"]:checked')) {
    const firstBackground = document.querySelector('.background-card input[type="radio"]');
    if (firstBackground) {
        firstBackground.checked = true;
        firstBackground.closest('.background-card').classList.add('selected');
        updateButtonState();
    }
}
</script>

