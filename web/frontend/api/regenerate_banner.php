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

// TODO: Call Python backend to generate SVG
// For now, return a mock response

try {
    // Mock SVG generation - replace with actual Python call
    $svg_content = generateMockSVG($template, $header_text, $main_title, $cta_text, $price, $price_period);

    // Return success with SVG HTML
    echo json_encode([
        'success' => true,
        'svg_html' => $svg_content,
        'template' => $template
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Errore nella generazione: ' . $e->getMessage()
    ]);
}

function generateMockSVG($template, $header, $title, $cta, $price, $period) {
    // Mock SVG - in production this would call the Python template engine
    list($width, $height) = explode('x', $template);

    $svg = <<<SVG
<svg width="{$width}" height="{$height}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {$width} {$height}">
    <!-- Background -->
    <rect width="{$width}" height="{$height}" fill="#1a1a2e"/>

    <!-- Header -->
    <text x="10" y="25" font-family="Arial" font-size="14" fill="#FFD700">{$header}</text>

    <!-- Title -->
    <text x="10" y="50" font-family="Arial" font-size="20" fill="#FFFFFF" font-weight="bold">{$title}</text>

    <!-- Price -->
    <text x="10" y="80" font-family="Arial" font-size="24" fill="#FFD700">{$price} {$period}</text>

    <!-- CTA Button -->
    <rect x="10" y="100" width="120" height="35" rx="8" fill="#FFD700"/>
    <text x="70" y="123" font-family="Arial" font-size="16" fill="#000" text-anchor="middle" font-weight="bold">{$cta}</text>

    <!-- Watermark -->
    <text x="{$width}" y="{$height}" font-family="Arial" font-size="10" fill="#666" text-anchor="end">Gazzetta Banner Generator</text>
</svg>
SVG;

    return '<div style="overflow-x: auto;">' . $svg . '</div>';
}
?>
