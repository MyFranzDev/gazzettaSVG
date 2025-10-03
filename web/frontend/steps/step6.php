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

    <!-- Generated Banners List -->
    <div style="margin: 30px 0;">
        <h3 style="color: #0f364c; margin-bottom: 20px;">📦 Banner Generati</h3>
        <div style="display: grid; gap: 15px;">
            <?php foreach (($wizardData['templates'] ?? ['300x250']) as $templateId): ?>
                <?php
                $templateInfo = array_filter($mockTemplates, fn($t) => $t['id'] === $templateId)[0] ?? ['name' => $templateId, 'dimensions' => ''];
                ?>
                <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #333; display: block; margin-bottom: 5px;">
                            <?= htmlspecialchars($templateInfo['name']) ?>
                        </strong>
                        <span style="font-size: 12px; color: #666;">
                            <?= htmlspecialchars($templateInfo['dimensions']) ?> - SVG vettoriale
                        </span>
                    </div>
                    <button type="button" class="btn btn-primary" style="padding: 8px 20px;" onclick="alert('Download simulato: banner_<?= $templateId ?>.svg')">
                        📥 Download
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
