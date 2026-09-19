<?php
// UNSC OCPA — ROSTER Terminal
// Colonial Dependent & Personnel Records Access

$page = isset($_GET['page']) ? $_GET['page'] : 'home';

// Dependent Status Index - real (if limited) backing data, not a static
// placeholder. This is the same batch of closed cases OCPA can legally
// disclose the existence of; internal transfer/disposition detail lives
// on other systems entirely.
$DEPENDENT_INDEX = array(
    array('name' => 'Eli Okafor', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-11902',
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_okafor.png'),
    array('name' => 'Talia Wren', 'colony' => 'Madrigal', 'case_ref' => 'OCPA-R4-11944',
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_wren.png'),
    array('name' => 'Dominic Farrow', 'colony' => 'Skopje', 'case_ref' => 'OCPA-R4-11887',
          'status' => 'Case Closed - Deceased (medical, age 7)', 'image' => 'case_farrow.png'),
    array('name' => 'Priya Anand', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-12210',
          'status' => 'Active - standard dependent case', 'image' => 'case_anand.png'),
);
?>
<!DOCTYPE html>
<html>
<head>
    <title>ROSTER :: OCPA Regional Terminal</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Consolas', 'DejaVu Sans Mono', monospace; margin: 0; background: #0b0f14; color: #c9d6df; }
        .banner { background: #2a1010; color: #ff6b5e; text-align: center; padding: 6px; font-size: 0.75em; letter-spacing: 1px; border-bottom: 1px solid #ff6b5e; }
        .container { max-width: 860px; margin: 30px auto; background: #10161d; padding: 20px 25px; border: 1px solid #1f2b38; box-shadow: 0 0 0 1px #050708; }
        h1 { color: #7fd1e0; font-size: 1.05em; letter-spacing: 0.5px; border-bottom: 1px solid #1f2b38; padding-bottom: 10px; margin-top: 0; text-transform: uppercase; }
        h2 { color: #7fd1e0; font-size: 1em; text-transform: uppercase; letter-spacing: 0.5px; }
        nav { background: #131b23; padding: 10px; margin-bottom: 20px; border: 1px solid #1f2b38; }
        nav a { color: #7fd1e0; margin-right: 18px; text-decoration: none; font-size: 0.85em; }
        nav a:hover { text-decoration: underline; }
        .upload-form { background: #131b23; padding: 15px; border: 1px solid #1f2b38; }
        .search-form { margin: 15px 0; }
        input[type="text"] { padding: 8px; width: 300px; background: #0b0f14; border: 1px solid #2a3b4a; color: #c9d6df; font-family: inherit; }
        input[type="submit"], button { padding: 8px 16px; background: #1f2b38; color: #7fd1e0; border: 1px solid #2a3b4a; cursor: pointer; font-family: inherit; }
        pre { background: #05070a; color: #9adfc2; padding: 15px; border: 1px solid #1f2b38; overflow-x: auto; }
        .warning { color: #ff6b5e; }
        footer { font-size: 0.7em; color: #4c5a68; margin-top: 20px; border-top: 1px solid #1f2b38; padding-top: 10px; }
    </style>
</head>
<body>
<div class="banner">UNSC OCPA NETWORK -- AUTHORIZED PERSONNEL ONLY -- ACTIVITY IS LOGGED (Reg. 4 Systems Directive 09)</div>
<div class="container">
    <h1><img src="assets/ocpa_seal.png" width="28" style="vertical-align:middle;margin-right:8px"> ROSTER :: Office of Colonial Personnel Affairs -- Regional Support Terminal</h1>
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
            // Vulnerable: no output encoding on the echoed query itself
            echo "<p>Results for: " . $query . "</p>";
            $needle = strtolower($query);
            $hits = array();
            foreach ($DEPENDENT_INDEX as $rec) {
                $haystack = strtolower($rec['name'] . ' ' . $rec['colony'] . ' ' . $rec['case_ref']);
                if ($needle !== '' && strpos($haystack, $needle) !== false) {
                    $hits[] = $rec;
                }
            }
            if (count($hits) > 0) {
                foreach ($hits as $rec) {
                    echo '<div style="display:flex;gap:15px;border:1px solid #1f2b38;padding:10px;margin:10px 0;background:#0e141a">';
                    echo '<img src="assets/' . $rec['image'] . '" width="90" style="border:1px solid #2a3b4a">';
                    echo '<div>';
                    echo '<b>' . htmlspecialchars($rec['name']) . '</b><br>';
                    echo 'Colony of record: ' . htmlspecialchars($rec['colony']) . '<br>';
                    echo 'Case reference: ' . htmlspecialchars($rec['case_ref']) . '<br>';
                    echo 'Status: ' . htmlspecialchars($rec['status']);
                    echo '</div></div>';
                }
            } else {
                echo "<p>No records found matching your query in the current index.</p>";
            }
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
        $filepath = '/var/www/html/portal/notes/' . $file;
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
