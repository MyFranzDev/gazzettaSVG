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
            <input type="text" id="prezzo" name="data[prezzo]"
                   value="<?= htmlspecialchars($wizardData['prezzo'] ?? '0,99€ / mese') ?>"
                   placeholder="es. 0,99€ / mese" required>
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
                    <label class="sport-card <?= $selected ? 'selected' : '' ?>">
                        <input type="radio" name="data[sport]" value="<?= htmlspecialchars($sport) ?>"
                               <?= $selected ? 'checked' : '' ?> required>
                        <div class="sport-icon"><?= $sportIcons[$sport] ?? '🏅' ?></div>
                        <div class="sport-name"><?= htmlspecialchars($sport) ?></div>
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

// Check if sport is already selected
function updateButtonState() {
    const sportSelected = document.querySelector('input[name="data[sport]"]:checked');
    nextBtn.disabled = !sportSelected;

    if (sportSelected) {
        nextBtn.style.opacity = '1';
        nextBtn.style.cursor = 'pointer';
    } else {
        nextBtn.style.opacity = '0.5';
        nextBtn.style.cursor = 'not-allowed';
    }
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
