<div class="step-container">
    <h2 class="step-title">✍️ Step 3: Testi</h2>
    <p class="step-subtitle">Scegli i testi generati dall'AI o personalizzali manualmente</p>

    <form method="POST">
        <?php
        $textVariants = $_SESSION['wizard']['text_variants'] ?? $mockTextVariants;
        $fields = ['header', 'main_title', 'subtitle', 'cta'];
        $fieldLabels = [
            'header' => 'Header',
            'main_title' => 'Titolo Principale',
            'subtitle' => 'Sottotitolo',
            'cta' => 'Call to Action (CTA)'
        ];

        foreach ($fields as $field):
        ?>
            <div class="form-group" style="margin-bottom: 60px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <label style="font-size: 18px; color: #0f364c; margin: 0;">
                        <?= $fieldLabels[$field] ?> *
                    </label>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 13px; color: #666;">Font:</span>
                        <?php
                        // Default fonts per field based on templates
                        $defaultFonts = [
                            'header' => 'roboto',
                            'main_title' => 'oswald',
                            'subtitle' => 'oswald',
                            'cta' => 'roboto-bold'
                        ];
                        $selectedFont = $wizardData['font_' . $field] ?? $defaultFonts[$field];
                        ?>
                        <select name="data[font_<?= $field ?>]" style="padding: 6px 12px; border: 2px solid #e0e0e0; border-radius: 6px; font-size: 14px; font-family: 'Alata', sans-serif; cursor: pointer;">
                            <option value="oswald" <?= $selectedFont === 'oswald' ? 'selected' : '' ?>>Oswald Bold</option>
                            <option value="roboto-bold" <?= $selectedFont === 'roboto-bold' ? 'selected' : '' ?>>Roboto Bold</option>
                            <option value="roboto" <?= $selectedFont === 'roboto' ? 'selected' : '' ?>>Roboto Regular</option>
                        </select>
                    </div>
                </div>

                <!-- AI Generated Options -->
                <div style="display: grid; gap: 10px; margin-bottom: 15px;">
                    <?php foreach ($textVariants as $variantKey => $variant): ?>
                        <?php
                        $variantNum = substr($variantKey, 8, 1);
                        $selected = ($wizardData['selected_' . $field] ?? '1') === $variantNum;
                        ?>
                        <label class="text-variant <?= $selected ? 'selected' : '' ?>"
                               style="cursor: pointer; padding: 15px; display: flex; align-items: center;">
                            <input type="radio"
                                   name="selected_<?= $field ?>"
                                   value="<?= $variantNum ?>"
                                   data-text="<?= htmlspecialchars($variant[$field]) ?>"
                                   <?= $selected ? 'checked' : '' ?>
                                   style="margin-right: 12px; width: 18px; height: 18px; cursor: pointer;">
                            <span style="flex: 1; font-size: 15px;">
                                <?= htmlspecialchars($variant[$field]) ?>
                            </span>
                        </label>
                    <?php endforeach; ?>

                </div>

                <!-- Custom text input (disabled in demo) -->
                <div class="custom-text-input" style="margin-top: 15px;">
                    <input type="text"
                           name="data[custom_<?= $field ?>]"
                           id="input_<?= $field ?>"
                           value="<?= htmlspecialchars($wizardData['custom_' . $field] ?? '') ?>"
                           placeholder="Testo personalizzato (disabilitato in demo)"
                           readonly
                           class="demo-disabled"
                           style="width: 100%; padding: 12px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 15px; font-family: 'Alata', sans-serif; background: #f5f5f5; cursor: not-allowed;">
                </div>

                <!-- Hidden fields for tracking selection and final text value -->
                <input type="hidden" name="data[selected_<?= $field ?>]" id="selected_<?= $field ?>" value="<?= $wizardData['selected_' . $field] ?? '1' ?>">
                <input type="hidden" name="data[<?= $field ?>]" id="final_<?= $field ?>" value="<?= htmlspecialchars($wizardData[$field] ?? '') ?>">
            </div>
        <?php endforeach; ?>

        <div class="wizard-actions">
            <button type="submit" name="action" value="back" class="btn btn-secondary">
                ← Indietro
            </button>
            <button type="submit" name="action" value="next" class="btn btn-primary">
                Avanti: Selezione Formato →
            </button>
        </div>
    </form>
</div>

<script>
const fields = ['header', 'main_title', 'subtitle', 'cta'];

fields.forEach(field => {
    const radios = document.querySelectorAll(`input[name="selected_${field}"]`);
    const customTextInput = document.getElementById(`input_${field}`);
    const selectedInput = document.getElementById(`selected_${field}`);
    const finalInput = document.getElementById(`final_${field}`);

    // Function to update final value based on custom text or selected radio
    function updateFinalValue() {
        if (customTextInput.value.trim()) {
            // User has typed custom text - use it
            finalInput.value = customTextInput.value;
            selectedInput.value = 'custom';
        } else {
            // Use selected radio button text
            const selectedRadio = document.querySelector(`input[name="selected_${field}"]:checked`);
            if (selectedRadio) {
                finalInput.value = selectedRadio.getAttribute('data-text');
                selectedInput.value = selectedRadio.value;
            }
        }
    }

    // Radio button selection
    radios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Update visual selection
            document.querySelectorAll(`input[name="selected_${field}"]`).forEach(r => {
                r.closest('.text-variant').classList.remove('selected');
            });
            this.closest('.text-variant').classList.add('selected');

            // Update final value
            updateFinalValue();
        });
    });

    // Initialize on page load
    updateFinalValue();

    // Custom text input (disabled in demo - show snackbar on click)
    if (customTextInput) {
        customTextInput.addEventListener('click', function() {
            showSnackbar('🚧 Funzionalità disponibile nella versione completa');
        });

        customTextInput.addEventListener('input', function() {
            // Prevent input in demo mode
            this.value = '';
            showSnackbar('🚧 Funzionalità disponibile nella versione completa');
        });
    }

    // Click on variant card
    document.querySelectorAll('.text-variant').forEach(variant => {
        variant.addEventListener('click', function(e) {
            if (e.target.tagName !== 'INPUT') {
                const radio = this.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                    radio.dispatchEvent(new Event('change'));
                }
            }
        });
    });
});
</script>
