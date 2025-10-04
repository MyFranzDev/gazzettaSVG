<div class="step-container">
    <h2 class="step-title">🎉 Step 5: Banner Generati</h2>
    <p class="step-subtitle">I tuoi banner sono pronti! Clicca su un banner per modificarlo</p>

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

    <!-- Generated Banners Grid -->
    <div style="margin: 30px 0;">
        <h3 style="color: #0f364c; margin-bottom: 20px;">📦 Banner Generati</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <?php foreach ($banners as $banner): ?>
                <?php
                $templateId = $banner['template_id'];
                $templateInfo = array_filter($mockTemplates, fn($t) => $t['id'] === $templateId);
                $templateInfo = !empty($templateInfo) ? array_values($templateInfo)[0] : ['name' => $templateId, 'dimensions' => ''];
                ?>
                <div class="banner-card" onclick="openBannerModal('<?= $templateId ?>')" style="border: 2px solid #e0e0e0; border-radius: 12px; padding: 15px; background: white; cursor: pointer; transition: all 0.3s ease;">
                    <!-- Banner Preview -->
                    <div style="background: #f5f5f5; border-radius: 8px; padding: 15px; margin-bottom: 12px; overflow: hidden; display: flex; align-items: center; justify-content: center; min-height: 150px;">
                        <?php
                        $pngPath = __DIR__ . '/../generated/' . $templateId . '.png';
                        $svgPath = __DIR__ . '/../generated/' . $templateId . '.svg';

                        if ($banner['generated'] && file_exists($pngPath)):
                            $pngData = base64_encode(file_get_contents($pngPath));
                        ?>
                            <img src="data:image/png;base64,<?= $pngData ?>" style="max-width: 100%; max-height: 200px; height: auto;">
                        <?php elseif ($banner['generated'] && file_exists($svgPath)): ?>
                            <div style="max-width: 100%; max-height: 200px; overflow: hidden;">
                                <?= file_get_contents($svgPath) ?>
                            </div>
                        <?php else: ?>
                            <div style="color: #f44336; padding: 20px;">❌ Errore</div>
                        <?php endif; ?>
                    </div>

                    <!-- Banner Info -->
                    <div style="text-align: center;">
                        <strong style="color: #333; font-size: 14px; display: block; margin-bottom: 5px;">
                            <?= htmlspecialchars($templateInfo['name']) ?>
                        </strong>
                        <span style="color: #666; font-size: 12px;">
                            <?= htmlspecialchars($templateInfo['dimensions']) ?>
                        </span>
                    </div>
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

<!-- Modal for Banner Details -->
<div id="bannerModal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 1000; align-items: center; justify-content: center; padding: 20px;">
    <div style="background: white; border-radius: 12px; max-width: 900px; max-height: 90vh; overflow-y: auto; width: 100%;">
        <!-- Modal Header -->
        <div style="padding: 20px; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; color: #0f364c;" id="modalTitle">Banner Details</h3>
            <button onclick="closeBannerModal()" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #666;">×</button>
        </div>

        <!-- Modal Content -->
        <div style="padding: 30px;">
            <!-- Banner Preview -->
            <div id="modalPreview" style="background: #f5f5f5; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; overflow-x: auto; text-align: center;">
                <!-- Preview will be inserted here -->
            </div>

            <!-- Banner Info -->
            <div style="margin-bottom: 20px; padding: 15px; background: #f0f7ff; border-radius: 8px;">
                <strong style="color: #0f364c;">Dimensioni:</strong> <span id="modalDimensions"></span>
            </div>

            <!-- Editing Fields -->
            <div style="background: #fafafa; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                <h4 style="color: #0f364c; margin-bottom: 15px;">✏️ Modifica Contenuti</h4>
                <div style="display: grid; gap: 12px;">
                    <div>
                        <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Header:</label>
                        <input type="text" id="modal-header" value="<?= htmlspecialchars($wizardData['header'] ?? 'PROMO') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                    </div>

                    <div>
                        <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Titolo Principale:</label>
                        <input type="text" id="modal-title" value="<?= htmlspecialchars($wizardData['main_title'] ?? 'TITOLO') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                    </div>

                    <div>
                        <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Sottotitolo:</label>
                        <input type="text" id="modal-subtitle" value="<?= htmlspecialchars($wizardData['subtitle'] ?? '') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                    </div>

                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 10px;">
                        <div>
                            <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Pulsante CTA:</label>
                            <input type="text" id="modal-cta" value="<?= htmlspecialchars($wizardData['cta'] ?? 'ABBONATI') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                        </div>
                        <div>
                            <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Prezzo:</label>
                            <input type="text" id="modal-price" value="<?= htmlspecialchars($wizardData['prezzo'] ?? '0,99€') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                        </div>
                    </div>

                    <div>
                        <label style="display: block; font-size: 13px; color: #555; margin-bottom: 5px;">Periodicità:</label>
                        <input type="text" id="modal-period" value="<?= htmlspecialchars($wizardData['periodicita'] ?? '/mese') ?>" style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px;">
                    </div>
                </div>

                <button type="button" class="btn btn-primary" style="margin-top: 15px; width: 100%;" onclick="regenerateCurrentBanner()">
                    🔄 Rigenera Banner
                </button>
            </div>

            <!-- Download Button -->
            <a id="modalDownload" href="#" download class="btn btn-success" style="width: 100%; padding: 12px; text-decoration: none; display: block; text-align: center;">
                📥 Scarica Banner
            </a>
        </div>
    </div>
</div>

<style>
.banner-card:hover {
    border-color: #0f364c;
    box-shadow: 0 4px 12px rgba(15, 54, 76, 0.15);
    transform: translateY(-2px);
}

#bannerModal {
    display: none;
}

#bannerModal.active {
    display: flex !important;
}
</style>

<script>
let currentTemplateId = null;

function openBannerModal(templateId) {
    currentTemplateId = templateId;
    const modal = document.getElementById('bannerModal');

    // Get template info
    const templates = <?= json_encode($mockTemplates) ?>;
    const template = templates.find(t => t.id === templateId);

    // Update modal title and dimensions
    document.getElementById('modalTitle').textContent = template.name;
    document.getElementById('modalDimensions').textContent = template.dimensions + ' px';

    // Update preview by fetching the latest PNG
    const previewDiv = document.getElementById('modalPreview');
    previewDiv.innerHTML = '<div style="color: #666; padding: 40px; text-align: center;">⏳ Caricamento...</div>';

    fetch('generated/' + templateId + '.png?t=' + Date.now())
        .then(response => response.blob())
        .then(blob => {
            const reader = new FileReader();
            reader.onloadend = function() {
                const base64data = reader.result;
                previewDiv.innerHTML = '<img src="' + base64data + '" style="max-width: 100%; height: auto;">';
            };
            reader.readAsDataURL(blob);
        })
        .catch(err => {
            console.error('Error loading banner:', err);
            previewDiv.innerHTML = '<div style="color: #f44336; padding: 40px; text-align: center;">❌ Errore caricamento</div>';
        });

    // Update download link
    document.getElementById('modalDownload').href = 'generated/' + templateId + '.png';
    document.getElementById('modalDownload').download = 'banner_' + templateId + '.png';

    // Show modal
    modal.classList.add('active');
}

function closeBannerModal() {
    const modal = document.getElementById('bannerModal');
    modal.classList.remove('active');
    currentTemplateId = null;
}

function regenerateCurrentBanner() {
    if (!currentTemplateId) return;

    // Get field values
    const header = document.getElementById('modal-header').value;
    const title = document.getElementById('modal-title').value;
    const subtitle = document.getElementById('modal-subtitle').value;
    const cta = document.getElementById('modal-cta').value;
    const price = document.getElementById('modal-price').value;
    const period = document.getElementById('modal-period').value;

    // Show loading state
    const previewDiv = document.getElementById('modalPreview');
    previewDiv.innerHTML = '<div style="color: #666; padding: 40px; text-align: center;">⏳ Rigenerazione in corso...</div>';

    // Prepare data
    const data = {
        template: currentTemplateId,
        header_text: header,
        main_title: title,
        description_text: subtitle,
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
            // Update preview with new content
            previewDiv.innerHTML = result.svg_html;

            // Update the grid thumbnail by fetching the new PNG
            fetch('generated/' + currentTemplateId + '.png?t=' + Date.now())
                .then(response => response.blob())
                .then(blob => {
                    const reader = new FileReader();
                    reader.onloadend = function() {
                        const base64data = reader.result;
                        // Find and update the grid card image
                        const gridCards = document.querySelectorAll('.banner-card');
                        gridCards.forEach(card => {
                            if (card.getAttribute('onclick').includes(currentTemplateId)) {
                                const img = card.querySelector('img');
                                if (img) {
                                    img.src = base64data;
                                }
                            }
                        });
                    };
                    reader.readAsDataURL(blob);
                })
                .catch(err => console.error('Error updating thumbnail:', err));

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

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Close modal on outside click
document.getElementById('bannerModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeBannerModal();
    }
});

// Close modal on ESC key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeBannerModal();
    }
});

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
