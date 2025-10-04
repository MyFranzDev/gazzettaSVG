<div class="step-container">
    <h2 class="step-title">🚀 Step 4: Genera</h2>
    <p class="step-subtitle">Scegli quali formati di banner generare</p>

    <form method="POST">
        <div style="background: #f0f7ff; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
            <label style="display: flex; align-items: center; cursor: pointer; margin: 0;">
                <input type="checkbox" id="selectAll" style="margin-right: 10px; width: 20px; height: 20px;">
                <strong style="color: #0f364c;">Seleziona tutti i formati</strong>
            </label>
        </div>

        <div class="template-grid">
            <?php foreach ($mockTemplates as $template): ?>
                <?php
                $selected = in_array($template['id'], $wizardData['templates'] ?? []);
                ?>
                <label class="template-card <?= $selected ? 'selected' : '' ?>">
                    <input type="checkbox"
                           name="data[templates][]"
                           value="<?= htmlspecialchars($template['id']) ?>"
                           class="template-checkbox"
                           <?= $selected ? 'checked' : '' ?>>
                    <div class="template-name"><?= htmlspecialchars($template['name']) ?></div>
                    <div class="template-dimensions"><?= htmlspecialchars($template['dimensions']) ?></div>
                </label>
            <?php endforeach; ?>
        </div>

        <div class="wizard-actions">
            <button type="submit" name="action" value="back" class="btn btn-secondary">
                ← Indietro
            </button>
            <button type="submit" name="action" value="next" class="btn btn-primary" id="generateBtn" disabled>
                Genera Banner →
            </button>
        </div>
    </form>
</div>

<script>
const selectAll = document.getElementById('selectAll');
const checkboxes = document.querySelectorAll('.template-checkbox');
const generateBtn = document.getElementById('generateBtn');

// Select all functionality
selectAll.addEventListener('change', function() {
    checkboxes.forEach(cb => {
        cb.checked = this.checked;
        updateCardSelection(cb);
    });
    updateButtonState();
});

// Individual checkbox handling
checkboxes.forEach(cb => {
    cb.addEventListener('change', function() {
        updateCardSelection(this);
        updateSelectAllState();
        updateButtonState();
    });
});

// Card click handling
document.querySelectorAll('.template-card').forEach(card => {
    card.addEventListener('click', function(e) {
        if (e.target.tagName !== 'INPUT') {
            const checkbox = this.querySelector('input[type="checkbox"]');
            checkbox.checked = !checkbox.checked;
            updateCardSelection(checkbox);
            updateSelectAllState();
            updateButtonState();
        }
    });
});

function updateCardSelection(checkbox) {
    const card = checkbox.closest('.template-card');
    if (checkbox.checked) {
        card.classList.add('selected');
    } else {
        card.classList.remove('selected');
    }
}

function updateSelectAllState() {
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    const someChecked = Array.from(checkboxes).some(cb => cb.checked);
    selectAll.checked = allChecked;
    selectAll.indeterminate = someChecked && !allChecked;
}

function updateButtonState() {
    const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;

    // Enable/disable button based on selection
    if (selectedCount > 0) {
        generateBtn.disabled = false;
        generateBtn.style.opacity = '1';
        generateBtn.style.cursor = 'pointer';
        generateBtn.textContent = `Genera ${selectedCount} Banner →`;
    } else {
        generateBtn.disabled = true;
        generateBtn.style.opacity = '0.5';
        generateBtn.style.cursor = 'not-allowed';
        generateBtn.textContent = 'Genera Banner →';
    }
}

// Initialize state
updateSelectAllState();
updateButtonState();

// Show loader when generate button is clicked
generateBtn.addEventListener('click', function(e) {
    const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
    if (selectedCount > 0) {
        console.log('Showing loader for', selectedCount, 'banners');
        showLoader(selectedCount);
    }
});

function showLoader(count) {
    // Create loader overlay
    const overlay = document.createElement('div');
    overlay.id = 'generation-loader';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease-out;
    `;

    overlay.innerHTML = `
        <div style="text-align: center; color: white;">
            <div class="spinner" style="
                width: 80px;
                height: 80px;
                border: 8px solid rgba(255, 255, 255, 0.3);
                border-top: 8px solid #FFD700;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 30px;
            "></div>
            <h2 style="font-size: 28px; margin-bottom: 15px;">🎨 Generazione in corso...</h2>
            <p style="font-size: 18px; color: rgba(255, 255, 255, 0.8);">
                Stiamo creando ${count} banner ad alta qualità
            </p>
            <p style="font-size: 14px; color: rgba(255, 255, 255, 0.6); margin-top: 20px;">
                Questo potrebbe richiedere alcuni secondi...
            </p>
        </div>
    `;

    document.body.appendChild(overlay);

    // Add animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}
</script>
