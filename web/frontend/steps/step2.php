<div class="step-container">
    <h2 class="step-title">🤖 Step 2: Testi Generati da AI</h2>
    <p class="step-subtitle">L'AI ha generato 3 varianti di testi per il tuo evento</p>

    <div style="background: #f0f7ff; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
        <p style="margin: 0; color: #0f364c;">
            <strong>ℹ️ Nota:</strong> I testi sono stati generati automaticamente da GPT-4 in base all'evento "<?= htmlspecialchars($wizardData['evento'] ?? 'Tennis - US Open') ?>".
            Nel prossimo step potrai scegliere quale variante usare per ogni elemento.
        </p>
    </div>

    <?php foreach ($mockTextVariants as $variantKey => $variant): ?>
        <div class="text-variant">
            <div class="variant-header">
                <?php
                $variantTitles = [
                    'variant_1_fomo' => '🔥 Variante 1: FOMO (Urgenza, occasione limitata)',
                    'variant_2_esclusiva' => '👑 Variante 2: ESCLUSIVA (Premium, riservata)',
                    'variant_3_soft' => '😊 Variante 3: SOFT (Amichevole, inclusiva)'
                ];
                echo $variantTitles[$variantKey];
                ?>
            </div>
            <div class="variant-content">
                <div>
                    <strong>Header:</strong>
                    <?= htmlspecialchars($variant['header']) ?>
                </div>
                <div>
                    <strong>Main Title:</strong>
                    <?= htmlspecialchars($variant['main_title']) ?>
                </div>
                <div>
                    <strong>Subtitle:</strong>
                    <?= htmlspecialchars($variant['subtitle']) ?>
                </div>
                <div>
                    <strong>CTA:</strong>
                    <?= htmlspecialchars($variant['cta']) ?>
                </div>
            </div>
        </div>
    <?php endforeach; ?>

    <form method="POST">
        <?php
        // Save generated variants in session
        $_SESSION['wizard']['text_variants'] = $mockTextVariants;
        ?>
        <div class="wizard-actions">
            <button type="submit" name="action" value="back" class="btn btn-secondary">
                ← Indietro
            </button>
            <button type="submit" name="action" value="next" class="btn btn-primary">
                Avanti: Selezione Testi →
            </button>
        </div>
    </form>
</div>
