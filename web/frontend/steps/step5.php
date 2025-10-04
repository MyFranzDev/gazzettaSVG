<div class="step-container">
    <h2 class="step-title">🎉 Step 5: Banner Generati</h2>
    <p class="step-subtitle">I tuoi banner sono pronti! Puoi modificarli e rigenerarli</p>

    <?php
    $generatedBanners = $_SESSION['wizard']['generated_banners'] ?? ['banners' => []];
    $banners = $generatedBanners['banners'] ?? [];
    ?>

    <!-- Processing Status -->
    <div style="background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 30px 0; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
        <h3 style="color: #2e7d32; margin-bottom: 10px;">Generazione Completata!</h3>
        <p style="color: #666; margin: 0;">
            <?= count($banners) ?> banner SVG generati con successo
        </p>
    </div>

    <!-- Generated Banners List with Editing -->
    <div style="margin: 30px 0;">
        <h3 style="color: #0f364c; margin-bottom: 20px;">📦 Banner Generati - Modifica e Rigenera</h3>
        <div style="display: grid; gap: 30px;">
            <?php foreach ($banners as $banner): ?>
                <?php
                $templateId = $banner['template_id'];
                $templateInfo = array_filter($mockTemplates, fn($t) => $t['id'] === $templateId);
                $templateInfo = !empty($templateInfo) ? array_values($templateInfo)[0] : ['name' => $templateId, 'dimensions' => ''];
                ?>
                <div style="border: 2px solid #e0e0e0; border-radius: 12px; padding: 25px; background: #fafafa;">
                    <!-- Banner Header -->
                    <div style="margin-bottom: 20px;">
                        <strong style="color: #333; font-size: 18px;">
                            <?= htmlspecialchars($templateInfo['name']) ?> - <?= htmlspecialchars($templateInfo['dimensions']) ?>
                        </strong>
                    </div>

                    <!-- Banner Preview -->
                    <div id="preview-<?= $templateId ?>" style="background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; overflow-x: auto; text-align: center;">
                        <?php
                        $pngPath = __DIR__ . '/../generated/' . $templateId . '.png';
                        $svgPath = __DIR__ . '/../generated/' . $templateId . '.svg';

                        if ($banner['generated'] && file_exists($pngPath)):
                            // Show PNG preview
                            $pngData = base64_encode(file_get_contents($pngPath));
                        ?>
                            <img src="data:image/png;base64,<?= $pngData ?>" style="max-width: 100%; height: auto;">
                        <?php elseif ($banner['generated'] && file_exists($svgPath)): ?>
                            <!-- Fallback to SVG if PNG doesn't exist -->
                            <?= file_get_contents($svgPath) ?>
                        <?php else: ?>
                            <div style="color: #f44336; padding: 40px;">
                                ❌ Errore nella generazione
                            </div>
                        <?php endif; ?>
                    </div>

                    <!-- Editing Fields -->
                    <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                        <div style="display: grid; gap: 12px;">
                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Header:</label>
                                <input type="text" id="header-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['header'] ?? 'PROMO') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>

                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Titolo Principale:</label>
                                <input type="text" id="title-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['main_title'] ?? 'TITOLO') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>

                            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px;">
                                <div>
                                    <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Pulsante CTA:</label>
                                    <input type="text" id="cta-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['cta'] ?? 'ABBONATI') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                </div>
                                <div>
                                    <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Prezzo:</label>
                                    <input type="text" id="price-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['prezzo'] ?? '0,99€') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                                </div>
                            </div>

                            <div>
                                <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Periodicità:</label>
                                <input type="text" id="period-<?= $templateId ?>" value="<?= htmlspecialchars($wizardData['periodicita'] ?? '/mese') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                            </div>
                        </div>

                        <button type="button" class="btn btn-primary" style="margin-top: 15px; width: 100%;" onclick="regenerateBanner('<?= $templateId ?>')">
                            🔄 Rigenera Banner
                        </button>
                    </div>

                    <!-- Download Button -->
                    <a href="generated/<?= $templateId ?>.png" download="banner_<?= $templateId ?>.png" class="btn btn-success" style="width: 100%; padding: 12px; text-decoration: none; display: block; text-align: center;">
                        📥 Scarica Banner
                    </a>
                </div>
            <?php endforeach; ?>
        </div>
    </div>

    <form method="POST">
        <div class="wizard-actions">
            <button type="submit" name="action" value="back" class="btn btn-secondary">
                ← Indietro
            </button>
            <button type="submit" name="action" value="reset" class="btn btn-secondary">
                🔄 Nuova Generazione
            </button>
        </div>
    </form>
</div>

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
    previewDiv.innerHTML = '<div style="color: #666; padding: 40px; text-align: center;">⏳ Rigenerazione in corso...</div>';

    // Prepare data
    const data = {
        template: templateId,
        header_text: header,
        main_title: title,
        cta_text: cta,
        price: price,
        price_period: period,
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
            previewDiv.innerHTML = '<div style="color: #f44336; padding: 40px; text-align: center;">❌ Errore: ' + result.error + '</div>';
            showNotification('❌ Errore nella rigenerazione', 'error');
        }
    })
    .catch(error => {
        previewDiv.innerHTML = '<div style="color: #f44336; padding: 40px; text-align: center;">❌ Errore di connessione</div>';
        console.error('Error:', error);
    });
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
