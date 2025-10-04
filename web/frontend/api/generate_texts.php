<?php
session_start();

// Check authentication
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Non autenticato']);
    exit;
}

// Get event from session
$wizardData = $_SESSION['wizard']['data'] ?? [];
$evento = $wizardData['evento'] ?? 'Evento sportivo';

// Call Python script to generate texts
try {
    $baseDir = __DIR__ . '/../../..';
    $pythonScript = $baseDir . '/generate_texts.py';

    // Execute Python script
    $command = "cd " . escapeshellarg($baseDir) . " && python3 " . escapeshellarg($pythonScript) . " " . escapeshellarg($evento) . " 2>&1";

    exec($command, $output, $returnCode);

    if ($returnCode === 0) {
        // Parse JSON output from Python
        $jsonOutput = implode("\n", $output);
        $variants = json_decode($jsonOutput, true);

        if ($variants && json_last_error() === JSON_ERROR_NONE) {
            // Save to session
            $_SESSION['wizard']['text_variants'] = $variants;

            echo json_encode([
                'success' => true,
                'variants' => $variants
            ]);
        } else {
            throw new Exception("Invalid JSON from Python script: " . json_last_error_msg());
        }
    } else {
        throw new Exception("Python script failed: " . implode("\n", $output));
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
?>
