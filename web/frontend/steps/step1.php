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
            <label>Stile Grafico *</label>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px;">
                <?php
                $selectedStyle = $wizardData['style'] ?? 'style1';
                ?>
                <label class="style-card <?= $selectedStyle === 'style1' ? 'selected' : '' ?>" style="border: 2px solid #e0e0e0; border-radius: 8px; padding: 20px; cursor: pointer; transition: all 0.3s ease;">
                    <input type="radio" name="data[style]" value="style1" <?= $selectedStyle === 'style1' ? 'checked' : '' ?> style="display: none;">
                    <div style="background: linear-gradient(135deg, #0f364c 0%, #1a4f6b 100%); padding: 30px; border-radius: 6px; margin-bottom: 12px; position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 10px; right: 10px; width: 40px; height: 40px; background: rgba(255, 215, 0, 0.2); border-radius: 50%;"></div>
                        <div style="color: #FFD700; font-size: 11px; font-weight: bold; margin-bottom: 8px;">EVENTO</div>
                        <div style="color: white; font-size: 16px; font-weight: bold; margin-bottom: 4px;">Titolo Banner</div>
                        <div style="color: rgba(255,255,255,0.8); font-size: 10px;">Sottotitolo esempio</div>
                    </div>
                    <div style="text-align: center; font-weight: 500; color: #333;">Stile 1</div>
                </label>

                <label class="style-card <?= $selectedStyle === 'style2' ? 'selected' : '' ?>" style="border: 2px solid #e0e0e0; border-radius: 8px; padding: 20px; cursor: pointer; transition: all 0.3s ease;">
                    <input type="radio" name="data[style]" value="style2" <?= $selectedStyle === 'style2' ? 'checked' : '' ?> style="display: none;">
                    <div style="background: white; border: 2px solid #0f364c; padding: 30px; border-radius: 6px; margin-bottom: 12px; position: relative;">
                        <div style="position: absolute; top: -10px; left: 20px; background: #FFD700; color: #0f364c; padding: 4px 12px; font-size: 9px; font-weight: bold; border-radius: 4px;">EVENTO</div>
                        <div style="color: #0f364c; font-size: 16px; font-weight: bold; margin-bottom: 4px; margin-top: 10px;">Titolo Banner</div>
                        <div style="color: #666; font-size: 10px;">Sottotitolo esempio</div>
                    </div>
                    <div style="text-align: center; font-weight: 500; color: #333;">Stile 2</div>
                </label>
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
                    $selected = ($wizardData['sport'] ?? '') === $sport;
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
        <div class="form-group" id="backgroundSection" style="margin-top: 30px; display: <?= isset($wizardData['sport']) ? 'block' : 'none' ?>;">
            <label>Sfondo per <span id="selectedSportName"><?= htmlspecialchars($wizardData['sport'] ?? 'Generico') ?></span> *</label>
            <div class="background-grid" id="backgroundGrid">
                <?php
                $selectedSport = $wizardData['sport'] ?? 'Generico';
                $sportBackgrounds = $mockBackgrounds[$selectedSport] ?? $mockBackgrounds['Generico'];
                foreach ($sportBackgrounds as $bg):
                    $selected = ($wizardData['background'] ?? '') === $bg['id'];
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

// Add click handler to style cards
document.querySelectorAll('.style-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.style-card').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
    });
});

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

// Initialize button state
updateButtonState();
</script>

<style>
.style-card:hover {
    border-color: #0f364c !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(15, 54, 76, 0.1);
}

.style-card.selected {
    border-color: #FFD700 !important;
    background: rgba(255, 215, 0, 0.05);
    box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2);
}
</style>
