<?php
// UNSC OCPA — ROSTER Terminal
// Colonial Dependent & Personnel Records Access

$page = isset($_GET['page']) ? $_GET['page'] : 'home';
?>
<!DOCTYPE html>
<html>
<head>
    <title>ROSTER — OCPA Regional Terminal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #eef0f2; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; font-size: 1.3em; }
        nav { background: #34495e; padding: 10px; border-radius: 2px; margin-bottom: 20px; }
        nav a { color: #dfe6e9; margin-right: 15px; text-decoration: none; font-size: 0.9em; }
        .upload-form { background: #ecf0f1; padding: 15px; border-radius: 4px; }
        .search-form { margin: 15px 0; }
        input[type="text"] { padding: 8px; width: 300px; }
        input[type="submit"], button { padding: 8px 16px; background: #34495e; color: white; border: none; cursor: pointer; }
        pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 4px; overflow-x: auto; }
        .warning { color: #c0392b; }
        footer { font-size: 0.75em; color: #7f8c8d; margin-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <h1>ROSTER — Office of Colonial Personnel Affairs, Regional Support Terminal</h1>
    <nav>
        <a href="?page=home">Home</a>
        <a href="?page=search">Dependent Status Index</a>
        <a href="?page=upload">Case File Intake</a>
        <a href="?page=ping">Network Diagnostics</a>
        <a href="?page=notes">Support Tickets</a>
    </nav>

<?php
switch($page) {
    case 'home':
        echo "<h2>Welcome</h2>";
        echo "<p>Regional terminal for colonial personnel and dependent records. For onboarding, see Support Tickets.</p>";
        echo "<p>Host: " . php_uname() . "</p>";
        break;

    case 'search':
        // Reflected XSS vulnerability
        $query = isset($_GET['q']) ? $_GET['q'] : '';
        echo '<div class="search-form">';
        echo '<h2>Dependent Status Index</h2>';
        echo '<p>Search by dependent name, colony of record, or case reference number.</p>';
        echo '<form method="GET">';
        echo '<input type="hidden" name="page" value="search">';
        echo '<input type="text" name="q" placeholder="Search records..." value="' . $query . '">';
        echo ' <input type="submit" value="Search">';
        echo '</form>';
        if ($query) {
            // Vulnerable: no output encoding
            echo "<p>Results for: " . $query . "</p>";
            echo "<p>No records found matching your query in the current index.</p>";
        }
        echo '</div>';
        break;

    case 'upload':
        echo '<div class="upload-form">';
        echo '<h2>Case File Intake</h2>';
        echo '<p>Upload scanned correspondence, medical transfer notes, or archived case material for indexing.</p>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
            $target = '/var/www/html/uploads/' . basename($_FILES['file']['name']);
            // Vulnerable: no file type validation, no renaming
            if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
                echo "<p>File indexed: <a href='/uploads/" . basename($_FILES['file']['name']) . "'>" . htmlspecialchars($_FILES['file']['name']) . "</a></p>";
            } else {
                echo "<p class='warning'>Intake failed.</p>";
            }
        }
        echo '<form method="POST" enctype="multipart/form-data">';
        echo '<input type="file" name="file"><br><br>';
        echo '<input type="submit" value="Submit">';
        echo '</form>';
        echo '</div>';
        break;

    case 'ping':
        // OS Command Injection vulnerability
        echo '<h2>Network Diagnostics</h2>';
        echo '<p>Legacy tool left over from the ROSTER migration. Reach out to systems if it misbehaves.</p>';
        echo '<form method="POST">';
        echo '<input type="text" name="host" placeholder="Enter hostname or IP">';
        echo ' <input type="submit" value="Ping">';
        echo '</form>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['host'])) {
            $host = $_POST['host'];
            // Vulnerable: direct command injection
            $output = shell_exec("ping -c 3 " . $host);
            echo "<pre>" . $output . "</pre>";
        }
        break;

    case 'notes':
        // Local File Inclusion vulnerability
        $file = isset($_GET['file']) ? $_GET['file'] : 'welcome.txt';
        echo '<h2>Support Tickets</h2>';
        echo '<ul>';
        echo '<li><a href="?page=notes&file=welcome.txt">Onboarding Note (T. Reyes)</a></li>';
        echo '<li><a href="?page=notes&file=todo.txt">Open Items — Systems</a></li>';
        echo '</ul>';
        // Vulnerable: no path validation
        $filepath = '/var/www/html/notes/' . $file;
        if (file_exists($filepath)) {
            echo "<pre>" . htmlspecialchars(file_get_contents($filepath)) . "</pre>";
        } else {
            // Path traversal possible
            if (file_exists($file)) {
                echo "<pre>" . htmlspecialchars(file_get_contents($file)) . "</pre>";
            } else {
                echo "<p>File not found.</p>";
            }
        }
        break;

    default:
        echo "<p>Page not found.</p>";
}
?>
    <footer>ROSTER Terminal v2.1 — OCPA Region 4 | Do not forward case material off-network.</footer>
</div>
</body>
</html>
