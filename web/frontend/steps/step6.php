<div class="step-container">
    <h2 class="step-title">🎉 Step 5: Download</h2>
    <p class="step-subtitle">I tuoi banner sono pronti per il download</p>

    <!-- Summary -->
    <div class="summary-section">
        <div class="summary-title">📋 Riepilogo Configurazione</div>
        <div class="summary-item">
            <span class="summary-label">Evento:</span>
            <span class="summary-value"><?= htmlspecialchars($wizardData['evento'] ?? 'N/A') ?></span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Prezzo:</span>
            <span class="summary-value"><?= htmlspecialchars($wizardData['prezzo'] ?? 'N/A') ?></span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Sport:</span>
            <span class="summary-value"><?= htmlspecialchars($wizardData['sport'] ?? 'N/A') ?></span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Background:</span>
            <span class="summary-value"><?= htmlspecialchars($wizardData['background'] ?? 'N/A') ?></span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Template selezionati:</span>
            <span class="summary-value"><?= count($wizardData['templates'] ?? []) ?> formati</span>
        </div>
    </div>

    <!-- Processing Status (simulato) -->
    <div style="background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
        <h3 style="color: #2e7d32; margin-bottom: 10px;">Generazione Completata!</h3>
        <p style="color: #666; margin: 0;">
            <?= count($wizardData['templates'] ?? [0]) ?> banner SVG generati con successo
        </p>
    </div>

    <!-- Generated Banners List with Editing -->
    <div style="margin: 30px 0;">
        <h3 style="color: #0f364c; margin-bottom: 20px;">📦 Banner Generati - Modifica e Scarica</h3>
        <div style="display: grid; gap: 30px;">
            <?php foreach (($wizardData['templates'] ?? ['300x250']) as $index => $templateId): ?>
                <?php
                $templateInfo = array_filter($mockTemplates, fn($t) => $t['id'] === $templateId)[0] ?? ['name' => $templateId, 'dimensions' => ''];
                // Get text variant data (from step 3)
                $selectedVariant = $wizardData['text_variant'] ?? 'variant_1_fomo';
                $variantData = $mockTextVariants[$selectedVariant] ?? [];
                ?>
                <div style="border: 2px solid #e0e0e0; border-radius: 12px; padding: 25px; background: #fafafa;">
                    <!-- Banner Header -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <strong style="color: #333; display: block; margin-bottom: 5px; font-size: 18px;">
                                <?= htmlspecialchars($templateInfo['name']) ?>
                            </strong>
                            <span style="font-size: 13px; color: #666;">
                                <?= htmlspecialchars($templateInfo['dimensions']) ?> - SVG vettoriale
                            </span>
                        </div>
                    </div>

                    <!-- Banner Preview -->
                    <div id="preview-<?= $templateId ?>" style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; text-align: center;">
                        <div style="color: #999; padding: 40px;">
                            🖼️ Preview banner (mock)<br>
                            <small><?= htmlspecialchars($templateInfo['dimensions']) ?></small>
                        </div>
                    </div>

                    <!-- Editing Fields -->
                    <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                        <h4 style="color: #0f364c; margin-bottom: 15px; font-size: 14px;">✏️ Modifica Testi</h4>

                        <div style="display: grid; gap: 12px;">
                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Header:</label>
                                <input type="text" id="header-<?= $templateId ?>" value="<?= htmlspecialchars($variantData['header'] ?? 'PROMO FLASH') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>

                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Titolo Principale:</label>
                                <input type="text" id="title-<?= $templateId ?>" value="<?= htmlspecialchars($variantData['main_title'] ?? 'IMPRESA BOLOGNA') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>

                            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px;">
                                <div>
                                    <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Pulsante CTA:</label>
                                    <input type="text" id="cta-<?= $templateId ?>" value="<?= htmlspecialchars($variantData['cta'] ?? 'ABBONATI') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                </div>
                                <div>
                                    <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Prezzo:</label>
                                    <input type="text" id="price-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['prezzo'] ?? '14,99€') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                </div>
                            </div>

                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Periodicità (es. /ANNO, /MESE):</label>
                                <input type="text" id="period-<?= $templateId ?>" value="/ANNO" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>
                        </div>

                        <button type="button" class="btn btn-primary" style="margin-top: 15px; width: 100%;" onclick="regenerateBanner('<?= $templateId ?>')">
                            🔄 Rigenera Banner
                        </button>
                    </div>

                    <!-- Download Button -->
                    <button type="button" class="btn btn-success" style="width: 100%; padding: 12px;" onclick="downloadBanner('<?= $templateId ?>')">
                        📥 Scarica Banner
                    </button>
                </div>
            <?php endforeach; ?>
        </div>
    </div>

    <!-- Download All Button -->
    <div style="text-align: center; margin: 40px 0;">
        <button type="button" class="btn btn-success" style="padding: 16px 48px; font-size: 18px;" onclick="alert('Download ZIP simulato con tutti i banner')">
            📦 Scarica Tutti (ZIP)
        </button>
    </div>

    <form method="POST">
        <div class="wizard-actions">
            <button type="submit" name="action" value="reset" class="btn btn-secondary">
                🔄 Nuova Generazione
            </button>
            <a href="logout.php" class="btn btn-secondary" style="text-decoration: none; display: inline-block;">
                🚪 Esci
            </a>
        </div>
    </form>
</div>

<style>
.wizard-actions a.btn {
    line-height: 1.5;
}
</style>

<script>
function regenerateBanner(templateId) {
    // Get field values
    const header = document.getElementById('header-' + templateId).value;
    const title = document.getElementById('title-' + templateId).value;
    const cta = document.getElementById('cta-' + templateId).value;
    const price = document.getElementById('price-' + templateId).value;
    const period = document.getElementById('period-' + templateId).value;

    // Show loading state
    const previewDiv = document.getElementById('preview-' + templateId);
    previewDiv.innerHTML = '<div style="color: #666; padding: 40px;">⏳ Rigenerazione in corso...</div>';

    // Prepare data
    const data = {
        template: templateId,
        header_text: header,
        main_title: title,
        cta_text: cta,
        price: price,
        price_period: period,
        // Include other data from wizard session
        sport: '<?= htmlspecialchars($wizardData['sport'] ?? '') ?>',
        background: '<?= htmlspecialchars($wizardData['background'] ?? '') ?>'
    };

    // Call API to regenerate banner
    fetch('api/regenerate_banner.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Update preview with new SVG
            previewDiv.innerHTML = result.svg_html;

            // Show success message
            showNotification('✅ Banner rigenerato con successo!', 'success');
        } else {
            previewDiv.innerHTML = '<div style="color: #f44336; padding: 40px;">❌ Errore: ' + result.error + '</div>';
            showNotification('❌ Errore nella rigenerazione', 'error');
        }
    })
    .catch(error => {
        previewDiv.innerHTML = '<div style="color: #f44336; padding: 40px;">❌ Errore di connessione</div>';
        console.error('Error:', error);
    });
}

function downloadBanner(templateId) {
    // For now, simulate download
    // In production, this would call the backend to generate and download the SVG
    const filename = 'banner_' + templateId + '.svg';

    // TODO: Implement actual download
    showNotification('📥 Download di ' + filename + ' (da implementare)', 'info');
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
</script>
