<?php
session_start();

// Check authentication
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: index.php');
    exit;
}

// Initialize wizard data in session
if (!isset($_SESSION['wizard'])) {
    $_SESSION['wizard'] = [
        'step' => 1,
        'data' => []
    ];
}

// Function to generate banners using Python script
function generateBanners($wizardData) {
    // For demo, simulate generation
    // TODO: Call actual Python script with exec()

    $result = [
        'success' => true,
        'banners' => []
    ];

    foreach ($wizardData['templates'] ?? [] as $templateId) {
        $result['banners'][] = [
            'template_id' => $templateId,
            'svg_path' => "output/{$templateId}.svg",
            'generated' => false // Will be true when Python script runs
        ];
    }

    return $result;
}

// Get current step and wizard data
$currentStep = $_SESSION['wizard']['step'];
$wizardData = $_SESSION['wizard']['data'];

// Handle step navigation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';

    if ($action === 'next') {
        // Save current step data
        $_SESSION['wizard']['data'] = array_merge(
            $_SESSION['wizard']['data'],
            $_POST['data'] ?? []
        );

        // If moving from step 4 to 5, generate banners
        if ($currentStep == 4) {
            // Generate banners by calling Python script
            $wizardData = $_SESSION['wizard']['data']; // Update with new data
            $result = generateBanners($wizardData);
            $_SESSION['wizard']['generated_banners'] = $result;
        }

        $_SESSION['wizard']['step']++;
        $currentStep++; // Update local variable
    } elseif ($action === 'back') {
        if ($_SESSION['wizard']['step'] > 1) {
            $_SESSION['wizard']['step']--;
        }
    } elseif ($action === 'goto') {
        // Go to specific step (only if already visited)
        $targetStep = intval($_POST['target_step'] ?? 1);
        if ($targetStep >= 1 && $targetStep <= $_SESSION['wizard']['step']) {
            $_SESSION['wizard']['step'] = $targetStep;
        }
    } elseif ($action === 'reset') {
        $_SESSION['wizard'] = [
            'step' => 1,
            'data' => []
        ];
    }
}

// Update current step and wizard data after navigation
$currentStep = $_SESSION['wizard']['step'];
$wizardData = $_SESSION['wizard']['data'];

// Mock data per sviluppo (sarà sostituito da chiamate API)
$mockSports = ['Calcio', 'Tennis', 'Pallavolo/Volley', 'Ciclismo', 'Golf', 'Formula 1/Moto GP', 'Generico'];

$mockBackgrounds = [
    'Calcio' => [
        ['id' => 'bg15', 'name' => 'Champions League 1', 'thumb' => 'backgrounds/bg15.png'],
        ['id' => 'bg16', 'name' => 'Champions League 2', 'thumb' => 'backgrounds/bg16.png'],
        ['id' => 'bg17', 'name' => 'Champions League 3', 'thumb' => 'backgrounds/bg17.png'],
        ['id' => 'bg18', 'name' => 'Generico 1', 'thumb' => 'backgrounds/bg18.png'],
        ['id' => 'bg19', 'name' => 'Generico 2', 'thumb' => 'backgrounds/bg19.png'],
        ['id' => 'bg20', 'name' => 'Calcio 1', 'thumb' => 'backgrounds/bg20.png'],
        ['id' => 'bg22', 'name' => 'Calcio 2', 'thumb' => 'backgrounds/bg22.png'],
        ['id' => 'bg23', 'name' => 'Calcio 3', 'thumb' => 'backgrounds/bg23.png'],
        ['id' => 'bg24', 'name' => 'Calcio 4', 'thumb' => 'backgrounds/bg24.png'],
        ['id' => 'bg30', 'name' => 'Calcio 5', 'thumb' => 'backgrounds/bg30.png'],
        ['id' => 'bg31', 'name' => 'Calcio 6', 'thumb' => 'backgrounds/bg31.png'],
        ['id' => 'bg32', 'name' => 'Calcio 7', 'thumb' => 'backgrounds/bg32.png'],
        ['id' => 'bg33', 'name' => 'Calcio 8', 'thumb' => 'backgrounds/bg33.png'],
        ['id' => 'bg34', 'name' => 'Calcio 9', 'thumb' => 'backgrounds/bg34.png'],
        ['id' => 'bg35', 'name' => 'Calcio 10', 'thumb' => 'backgrounds/bg35.png'],
        ['id' => 'bg36', 'name' => 'Calcio 11', 'thumb' => 'backgrounds/bg36.png'],
        ['id' => 'bg37', 'name' => 'Calcio 12', 'thumb' => 'backgrounds/bg37.png'],
        ['id' => 'bg38', 'name' => 'Calcio 13', 'thumb' => 'backgrounds/bg38.png'],
        ['id' => 'bg39', 'name' => 'Calcio 14', 'thumb' => 'backgrounds/bg39.png'],
        ['id' => 'bg40', 'name' => 'Calcio 15', 'thumb' => 'backgrounds/bg40.png'],
        ['id' => 'bg41', 'name' => 'Calcio 16', 'thumb' => 'backgrounds/bg41.png'],
    ],
    'Tennis' => [
        ['id' => 'bg11', 'name' => 'Wimbledon', 'thumb' => 'backgrounds/bg11.png'],
        ['id' => 'bg12', 'name' => 'US Open', 'thumb' => 'backgrounds/bg12.png'],
        ['id' => 'bg42', 'name' => 'Tennis 1', 'thumb' => 'backgrounds/bg42.png'],
        ['id' => 'bg43', 'name' => 'Tennis 2', 'thumb' => 'backgrounds/bg43.png'],
        ['id' => 'bg44', 'name' => 'Tennis 3', 'thumb' => 'backgrounds/bg44.png'],
        ['id' => 'bg45', 'name' => 'Australian Open', 'thumb' => 'backgrounds/bg45.png'],
    ],
    'Pallavolo/Volley' => [
        ['id' => 'bg06', 'name' => 'Volley 1', 'thumb' => 'backgrounds/bg06.png'],
        ['id' => 'bg07', 'name' => 'Volley 2', 'thumb' => 'backgrounds/bg07.png'],
        ['id' => 'bg08', 'name' => 'Volley 3', 'thumb' => 'backgrounds/bg08.png'],
        ['id' => 'bg09', 'name' => 'Volley 4', 'thumb' => 'backgrounds/bg09.png'],
        ['id' => 'bg10', 'name' => 'Volley 5', 'thumb' => 'backgrounds/bg10.png'],
        ['id' => 'bg46', 'name' => 'Volley 6', 'thumb' => 'backgrounds/bg46.png'],
        ['id' => 'bg47', 'name' => 'Volley 7', 'thumb' => 'backgrounds/bg47.png'],
    ],
    'Ciclismo' => [
        ['id' => 'bg20', 'name' => 'Ciclismo 1', 'thumb' => 'backgrounds/bg20.png'],
        ['id' => 'bg21', 'name' => 'Ciclismo 2', 'thumb' => 'backgrounds/bg21.png'],
        ['id' => 'bg22', 'name' => 'Ciclismo 3', 'thumb' => 'backgrounds/bg22.png'],
    ],
    'Golf' => [
        ['id' => 'bg13', 'name' => 'Golf 1', 'thumb' => 'backgrounds/bg13.png'],
        ['id' => 'bg14', 'name' => 'Golf 2', 'thumb' => 'backgrounds/bg14.png'],
    ],
    'Formula 1/Moto GP' => [
        ['id' => 'bg23', 'name' => 'F1/MotoGP 1', 'thumb' => 'backgrounds/bg23.png'],
        ['id' => 'bg24', 'name' => 'F1/MotoGP 2', 'thumb' => 'backgrounds/bg24.png'],
        ['id' => 'bg25', 'name' => 'F1/MotoGP 3', 'thumb' => 'backgrounds/bg25.png'],
        ['id' => 'bg26', 'name' => 'F1/MotoGP 4', 'thumb' => 'backgrounds/bg26.png'],
        ['id' => 'bg27', 'name' => 'F1/MotoGP 5', 'thumb' => 'backgrounds/bg27.png'],
    ],
    'Generico' => [
        ['id' => 'bg01', 'name' => 'Sfondo 1', 'thumb' => 'backgrounds/bg01.png'],
        ['id' => 'bg02', 'name' => 'Sfondo 2', 'thumb' => 'backgrounds/bg02.png'],
        ['id' => 'bg03', 'name' => 'Sfondo 3', 'thumb' => 'backgrounds/bg03.png'],
    ]
];

$mockTextVariants = [
    'variant_1_fomo' => [
        'header' => 'Solo per poco!',
        'main_title' => 'L\'US Open ti aspetta!',
        'subtitle' => 'Non perdere l\'evento sportivo dell\'anno',
        'cta' => 'Agisci ora'
    ],
    'variant_2_esclusiva' => [
        'header' => 'Accesso Premium',
        'main_title' => 'US Open come mai prima',
        'subtitle' => 'Goditi l\'esperienza esclusiva riservata',
        'cta' => 'Accedi Ora'
    ],
    'variant_3_soft' => [
        'header' => 'Ama il Tennis?',
        'main_title' => 'Unisciti a noi all\'US Open',
        'subtitle' => 'Condividi l\'emozione del grande tennis',
        'cta' => 'Partecipa subito'
    ]
];

$mockTemplates = [
    ['id' => '728x90', 'name' => 'Leaderboard', 'dimensions' => '728x90'],
    ['id' => '1200x1200', 'name' => 'Square Social Media', 'dimensions' => '1200x1200'],
    ['id' => '1920x1080', 'name' => 'Full HD Landscape', 'dimensions' => '1920x1080'],
];
?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gazzetta Banner Generator - Wizard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Alata&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="wizard-container">
        <!-- Header -->
        <div class="wizard-header">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                <h1 style="margin: 0;">🏆 Gazzetta Multi-Banner Generator</h1>
                <a href="logout.php" style="font-size: 12px; color: rgba(255,255,255,0.5); text-decoration: none; transition: color 0.3s;" onmouseover="this.style.color='rgba(255,255,255,1)'" onmouseout="this.style.color='rgba(255,255,255,0.5)'">
                    Esci
                </a>
            </div>
            <div class="progress-bar">
                <?php for ($i = 1; $i <= 5; $i++): ?>
                    <div class="progress-step <?= $i <= $currentStep ? 'active' : '' ?> <?= $i == $currentStep ? 'current' : '' ?>">
                        <?php if ($i <= $currentStep): ?>
                            <form method="POST" style="display: inline;">
                                <input type="hidden" name="action" value="goto">
                                <input type="hidden" name="target_step" value="<?= $i ?>">
                                <button type="submit" class="step-number" style="border: none; cursor: pointer;">
                                    <?= $i ?>
                                </button>
                            </form>
                        <?php else: ?>
                            <div class="step-number"><?= $i ?></div>
                        <?php endif; ?>
                        <div class="step-label">
                            <?php
                            $labels = ['Evento', 'Risorse', 'Testi', 'Genera', 'Download'];
                            echo $labels[$i - 1];
                            ?>
                        </div>
                    </div>
                <?php endfor; ?>
            </div>
        </div>

        <!-- Step Content -->
        <div class="wizard-content">
            <?php if ($currentStep == 1): ?>
                <?php include 'steps/step1.php'; ?>
            <?php elseif ($currentStep == 2): ?>
                <?php include 'steps/step4.php'; ?>
            <?php elseif ($currentStep == 3): ?>
                <?php include 'steps/step3.php'; ?>
            <?php elseif ($currentStep == 4): ?>
                <?php include 'steps/step5.php'; ?>
            <?php elseif ($currentStep == 5): ?>
                <?php include 'steps/step6.php'; ?>
            <?php endif; ?>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
