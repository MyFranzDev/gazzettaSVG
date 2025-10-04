<?php
session_start();

// Check authentication
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Non autenticato']);
    exit;
}

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

if (!$input) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Dati non validi']);
    exit;
}

// Extract parameters
$template = $input['template'] ?? '';
$header_text = $input['header_text'] ?? '';
$main_title = $input['main_title'] ?? '';
$cta_text = $input['cta_text'] ?? '';
$price = $input['price'] ?? '';
$price_period = $input['price_period'] ?? '';
$sport = $input['sport'] ?? '';
$background = $input['background'] ?? '';

// Validate template
if (empty($template)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Template non specificato']);
    exit;
}

// Call Python backend to generate SVG
try {
    // Prepare paths
    $baseDir = __DIR__ . '/../../..';
    $pythonScript = $baseDir . '/generate_single_banner.py';
    $outputDir = $baseDir . '/web/frontend/generated';

    // Create output directory if not exists
    if (!file_exists($outputDir)) {
        mkdir($outputDir, 0755, true);
    }

    // Get wizard data for subtitle and background
    $wizardData = $_SESSION['wizard']['data'] ?? [];

    // Prepare template data
    $templateData = [
        'template' => $template,
        'header_text' => $header_text,
        'main_title' => $main_title,
        'description_text' => $wizardData['subtitle'] ?? '',
        'cta_text' => $cta_text,
        'price' => $price,
        'price_period' => $price_period,
        'background' => $background ?: ($wizardData['background'] ?? 'bg01')
    ];

    // Generate banner
    $outputPath = $outputDir . "/{$template}.svg";
    $pngPath = $outputDir . "/{$template}.png";

    $jsonData = json_encode($templateData);
    $escapedJson = escapeshellarg($jsonData);

    // Execute Python script to generate SVG
    $command = "cd " . escapeshellarg($baseDir) . " && python3 " . escapeshellarg($pythonScript) . " {$escapedJson} 2>&1 > " . escapeshellarg($outputPath);

    exec($command, $output, $returnCode);

    // Convert SVG to PNG using Node.js for better quality
    if ($returnCode === 0 && file_exists($outputPath)) {
        $nodeScript = $baseDir . '/svg_to_png.js';
        $pngCommand = "node " . escapeshellarg($nodeScript) . " " . escapeshellarg($outputPath) . " " . escapeshellarg($pngPath) . " 2>&1";
        exec($pngCommand, $pngOutput, $pngReturnCode);
    }

    if ($returnCode === 0 && file_exists($outputPath)) {
        // Return success with PNG preview (if available)
        $previewHtml = '';
        if (file_exists($pngPath)) {
            $pngData = base64_encode(file_get_contents($pngPath));
            $previewHtml = '<img src="data:image/png;base64,' . $pngData . '" style="max-width: 100%; height: auto;">';
        } else {
            // Fallback to SVG if PNG generation failed
            $svgContent = file_get_contents($outputPath);
            $previewHtml = $svgContent;
        }

        echo json_encode([
            'success' => true,
            'svg_html' => '<div style="overflow-x: auto; background: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center;">' . $previewHtml . '</div>',
            'template' => $template,
            'file_size' => filesize($outputPath)
        ]);
    } else {
        throw new Exception("Generazione fallita: " . implode("\n", $output));
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Errore nella generazione: ' . $e->getMessage()
    ]);
}
?>
