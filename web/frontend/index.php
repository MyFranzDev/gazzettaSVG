<?php
session_start();

// Password demo
define('DEMO_PASSWORD', 'touchlabs2');

// Check login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password'])) {
    if ($_POST['password'] === DEMO_PASSWORD) {
        $_SESSION['authenticated'] = true;
        header('Location: wizard.php');
        exit;
    } else {
        $error = "Password errata";
    }
}

// If already authenticated, redirect to wizard
if (isset($_SESSION['authenticated']) && $_SESSION['authenticated']) {
    header('Location: wizard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gazzetta Multi-Banner Generator - Demo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Alata&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Alata", sans-serif;
            background-color: #122e4d;
            background-image: url('https://www.newrality.com/gazzettaprototipo2/3070961.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 54, 76, 0.7);
            z-index: 1;
        }

        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
            position: relative;
            z-index: 2;
        }

        h1 {
            color: #0f364c;
            margin-bottom: 10px;
            font-size: 24px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .form-group {
            margin-bottom: 25px;
            text-align: left;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #333;
        }

        input[type="password"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
            font-family: "Alata", sans-serif;
        }

        input[type="password"]:focus {
            outline: none;
            border-color: #0f364c;
        }

        .login-btn {
            background: linear-gradient(135deg, #0f364c, #1a4f6b);
            color: white;
            border: none;
            padding: 16px 32px;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            font-family: "Alata", sans-serif;
        }

        .login-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(15, 54, 76, 0.3);
        }

        .error {
            color: #f44336;
            margin-top: 15px;
            font-size: 14px;
        }

        .logo {
            max-width: 200px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🏆 Gazzetta Multi-Banner Generator</h1>
        <p class="subtitle">Accesso Demo Riservato</p>

        <form method="POST">
            <div class="form-group">
                <label for="password">Password Demo:</label>
                <input type="password" id="password" name="password" required autofocus>
            </div>
            <button type="submit" class="login-btn">Accedi alla Demo</button>
        </form>

        <?php if (isset($error)): ?>
            <p class="error"><?= htmlspecialchars($error) ?></p>
        <?php endif; ?>
    </div>
</body>
</html>
