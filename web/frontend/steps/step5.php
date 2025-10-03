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
</script>
