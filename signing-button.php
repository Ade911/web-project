<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank App - Sign In</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f2;
        }
        .sign-in-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .sign-in-button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .sign-in-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="sign-in-container">
        <form action="process_sign_in.php" method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit" class="sign-in-button">Sign In</button>
        </form>
    </div>
</body>
</html>
<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Example hardcoded credentials for demonstration
    $correctUsername = 'user';
    $correctPassword = 'password';

    if ($username === $correctUsername && $password === $correctPassword) {
        $_SESSION['loggedin'] = true;
        $_SESSION['username'] = $username;
        header('Location: dashboard.php');
    } else {
        echo "<script>alert('Invalid username or password');window.location.href='sign_in.php';</script>";
    }
} else {
    header('Location: sign_in.php');
}
?>
<?php
session_start();

if (!isset($_SESSION['loggedin'])) {
    header('Location: sign_in.php');
    exit;
}

echo "Welcome to your dashboard, " . htmlspecialchars($_SESSION['username']) . "!";
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank App - Dashboard</title>
</head>
<body>
    <h1>Dashboard</h1>
    <p>This is a protected area only accessible to authenticated users.</p>
    <a href="logout.php">Log Out</a>
</body>
</html>
<?php
session_start();
session_destroy();
header('Location: sign_in.php');
exit;
?>
