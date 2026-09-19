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
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_farrow.png'),
    array('name' => 'Priya Anand', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-12210',
          'status' => 'Active - standard dependent case', 'image' => 'case_anand.png'),
);

$NAV = array(
    'home' => 'Dashboard',
    'search' => 'Dependent Status Index',
    'upload' => 'Case File Intake',
    'ping' => 'Network Diagnostics',
    'notes' => 'Support Tickets',
);
$page_title = isset($NAV[$page]) ? $NAV[$page] : 'Not Found';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ROSTER :: OCPA Regional Terminal</title>
    <link rel="icon" type="image/png" href="assets/ocpa_seal.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
    <style>
        :root {
            --bg: #0a0d11;
            --surface: #131920;
            --surface-2: #1a212a;
            --surface-hover: #1f2731;
            --border: #232c36;
            --border-soft: #1a2129;
            --text: #d7dee4;
            --text-dim: #8a97a3;
            --text-faint: #55616c;
            --accent: #5fb3d1;
            --accent-soft: rgba(95, 179, 209, 0.12);
            --danger: #c96560;
            --danger-bg: #2a1414;
            --sans: 'IBM Plex Sans', -apple-system, 'Segoe UI', Roboto, sans-serif;
            --mono: 'IBM Plex Mono', 'Consolas', monospace;
        }
        * { box-sizing: border-box; }
        html { background: var(--bg); }
        body {
            font-family: var(--sans);
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-size: 14px;
            line-height: 1.5;
        }
        a { color: var(--accent); }
        .topbar {
            background: var(--danger-bg);
            color: var(--danger);
            text-align: center;
            padding: 6px 12px;
            font-size: 11.5px;
            letter-spacing: 0.4px;
            border-bottom: 1px solid #3a1d1d;
        }
        .shell { display: flex; min-height: calc(100vh - 27px); }

        /* Sidebar */
        .sidebar {
            width: 240px;
            flex-shrink: 0;
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 18px 16px;
            border-bottom: 1px solid var(--border-soft);
        }
        .brand img { width: 34px; opacity: 0.92; flex-shrink: 0; }
        .brand .name { font-weight: 600; font-size: 13.5px; letter-spacing: 0.3px; color: var(--text); }
        .brand .sub { font-size: 11px; color: var(--text-faint); letter-spacing: 0.5px; text-transform: uppercase; }
        .sidenav { padding: 10px 0; flex: 1; }
        .sidenav a {
            display: block;
            padding: 9px 18px;
            font-size: 13px;
            color: var(--text-dim);
            text-decoration: none;
            border-left: 2px solid transparent;
        }
        .sidenav a:hover { background: var(--surface-hover); color: var(--text); }
        .sidenav a.active { color: var(--accent); background: var(--accent-soft); border-left-color: var(--accent); font-weight: 500; }
        .sidefoot {
            padding: 12px 16px;
            border-top: 1px solid var(--border-soft);
            font-size: 10.5px;
            color: var(--text-faint);
            line-height: 1.6;
        }

        /* Main */
        .main { flex: 1; min-width: 0; }
        .pagebar {
            padding: 14px 28px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 8px;
        }
        .crumb { font-size: 11px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.5px; }
        .crumb b { color: var(--text-dim); }
        h1.page-title { font-size: 18px; font-weight: 600; margin: 2px 0 0 0; color: var(--text); }
        .content { padding: 22px 28px 40px; max-width: 980px; }
        h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.6px; color: var(--text-dim); font-weight: 600; margin: 26px 0 10px; }
        h2:first-child { margin-top: 0; }
        p { color: var(--text-dim); }

        /* Components */
        .dash-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 4px; }
        .stat { flex: 1 1 150px; background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 14px 16px; }
        .stat .num { font-family: var(--mono); font-size: 24px; font-weight: 500; color: var(--text); font-variant-numeric: tabular-nums; }
        .stat .lbl { font-size: 11px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.4px; margin-top: 3px; }
        .board { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; overflow: hidden; }
        .board-item { padding: 10px 14px; border-bottom: 1px solid var(--border-soft); font-size: 13px; display: flex; justify-content: space-between; gap: 14px; color: var(--text-dim); }
        .board-item:last-child { border-bottom: none; }
        .board-item .tag { color: var(--text-faint); font-family: var(--mono); font-size: 11.5px; white-space: nowrap; }
        .quicklinks { display: flex; gap: 8px; flex-wrap: wrap; }
        .quicklinks a { background: var(--surface); border: 1px solid var(--border); color: var(--text-dim); padding: 8px 14px; border-radius: 4px; text-decoration: none; font-size: 12.5px; }
        .quicklinks a:hover { color: var(--accent); border-color: var(--accent); background: var(--accent-soft); }

        .panel { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 18px 20px; }
        input[type="text"], input[type="file"] { font-family: var(--sans); padding: 8px 10px; width: 320px; max-width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 3px; color: var(--text); font-size: 13px; }
        input[type="submit"], button {
            font-family: var(--sans); padding: 8px 16px; background: var(--surface-2); color: var(--text);
            border: 1px solid var(--border); border-radius: 3px; cursor: pointer; font-size: 13px;
        }
        input[type="submit"]:hover, button:hover { border-color: var(--accent); color: var(--accent); }
        pre {
            font-family: var(--mono); font-size: 12.5px; background: #05070a; color: #9ad0c9;
            padding: 14px 16px; border: 1px solid var(--border); border-radius: 4px; overflow-x: auto; line-height: 1.6;
        }
        .warning { color: var(--danger); }
        .result-card { display: flex; gap: 14px; border: 1px solid var(--border); border-radius: 4px; padding: 12px; margin: 10px 0; background: var(--surface); }
        .result-card img { border: 1px solid var(--border-soft); border-radius: 3px; }
        .result-card .name { font-weight: 600; color: var(--text); margin-bottom: 2px; }
        .result-card .field { font-size: 12.5px; color: var(--text-dim); }
        ul.ticket-list { list-style: none; padding: 0; margin: 0 0 16px; }
        ul.ticket-list li { border: 1px solid var(--border); border-radius: 4px; margin-bottom: 6px; background: var(--surface); }
        ul.ticket-list a { display: block; padding: 10px 14px; font-size: 13px; text-decoration: none; color: var(--text-dim); }
        ul.ticket-list a:hover { color: var(--accent); }

        footer { font-size: 11px; color: var(--text-faint); margin-top: 30px; padding-top: 14px; border-top: 1px solid var(--border-soft); }

        @media (max-width: 720px) {
            .shell { flex-direction: column; }
            .sidebar { width: 100%; border-right: none; border-bottom: 1px solid var(--border); }
            .content { padding: 18px 16px 32px; }
            .pagebar { padding: 12px 16px; }
        }
    </style>
</head>
<body>
<div class="topbar">UNSC OCPA NETWORK &mdash; AUTHORIZED PERSONNEL ONLY &mdash; ACTIVITY IS LOGGED (Reg. 4 Systems Directive 09)</div>
<div class="shell">
    <aside class="sidebar">
        <div class="brand">
            <img src="assets/unsc_insignia.png" alt="">
            <div>
                <div class="name">ROSTER Terminal</div>
                <div class="sub">OCPA &middot; Region 4</div>
            </div>
        </div>
        <nav class="sidenav">
<?php foreach ($NAV as $key => $label):
    $cls = ($key === $page) ? 'active' : ''; ?>
            <a class="<?php echo $cls; ?>" href="?page=<?php echo $key; ?>"><?php echo htmlspecialchars($label); ?></a>
<?php endforeach; ?>
        </nav>
        <div class="sidefoot">
            SESSION duty-terminal-04<br>
            LAST LOGIN 2547-02-19 06:12
        </div>
    </aside>

    <main class="main">
        <div class="pagebar">
            <div>
                <div class="crumb">OCPA &rsaquo; ROSTER &rsaquo; <b><?php echo htmlspecialchars($page_title); ?></b></div>
                <h1 class="page-title"><?php echo htmlspecialchars($page_title); ?></h1>
            </div>
        </div>
        <div class="content">
<?php
switch($page) {
    case 'home':
        echo '<div class="dash-grid">';
        echo '<div class="stat"><div class="num">142</div><div class="lbl">Active dependent cases</div></div>';
        echo '<div class="stat"><div class="num">38</div><div class="lbl">Closed this quarter</div></div>';
        echo '<div class="stat"><div class="num">6</div><div class="lbl">Pending review</div></div>';
        echo '<div class="stat"><div class="num">3</div><div class="lbl">Open support tickets</div></div>';
        echo '</div>';

        echo '<h2>System Notices</h2>';
        echo '<div class="board">';
        echo '<div class="board-item"><span>Scheduled maintenance window, Sun 0200-0400 - terminal may be briefly unavailable.</span><span class="tag">2547-02-18</span></div>';
        echo '<div class="board-item"><span>SPINDLE migration cleanup ongoing. Report stale references to Systems, do not self-correct case data.</span><span class="tag">2547-02-11</span></div>';
        echo '<div class="board-item"><span>Water shutoff, Building 4, Tue 0600-0900 - see Support Tickets for details.</span><span class="tag">2547-02-09</span></div>';
        echo '<div class="board-item"><span>Reminder: case file intake accepts scanned correspondence and transfer notes only.</span><span class="tag">2547-01-30</span></div>';
        echo '</div>';

        echo '<h2>Quick Links</h2>';
        echo '<div class="quicklinks">';
        echo '<a href="?page=search">Dependent Status Index</a>';
        echo '<a href="?page=upload">Case File Intake</a>';
        echo '<a href="?page=notes">Support Tickets</a>';
        echo '<a href="http://localhost:8025">Webmail</a>';
        echo '</div>';
        break;

    case 'search':
        // Reflected XSS vulnerability
        $query = isset($_GET['q']) ? $_GET['q'] : '';
        echo '<p>Search by dependent name, colony of record, or case reference number.</p>';
        echo '<form method="GET">';
        echo '<input type="hidden" name="page" value="search">';
        echo '<input type="text" name="q" placeholder="Search records..." value="' . $query . '">';
        echo ' <input type="submit" value="Search">';
        echo '</form>';
        if ($query) {
            // Vulnerable: no output encoding on the echoed query itself
            echo "<p style='margin-top:16px'>Results for: " . $query . "</p>";
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
                    echo '<div class="result-card">';
                    echo '<img src="assets/' . $rec['image'] . '" width="90">';
                    echo '<div>';
                    echo '<div class="name">' . htmlspecialchars($rec['name']) . '</div>';
                    echo '<div class="field">Colony of record: ' . htmlspecialchars($rec['colony']) . '</div>';
                    echo '<div class="field">Case reference: ' . htmlspecialchars($rec['case_ref']) . '</div>';
                    echo '<div class="field">Status: ' . htmlspecialchars($rec['status']) . '</div>';
                    echo '</div></div>';
                }
            } else {
                echo "<p>No records found matching your query in the current index.</p>";
            }
        }
        break;

    case 'upload':
        echo '<div class="panel">';
        echo '<p style="margin-top:0">Upload scanned correspondence, medical transfer notes, or archived case material for indexing.</p>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
            $target = '/var/www/html/portal/uploads/' . basename($_FILES['file']['name']);
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
        echo '<p>Legacy tool left over from the ROSTER migration. Reach out to Systems if it misbehaves.</p>';
        echo '<form method="POST">';
        echo '<input type="text" name="host" placeholder="Enter hostname or IP">';
        echo ' <input type="submit" value="Ping">';
        echo '</form>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['host'])) {
            $host = $_POST['host'];
            // Vulnerable: direct command injection
            $output = shell_exec("ping -c 3 " . $host);
            echo '<pre style="margin-top:16px">' . $output . '</pre>';
        }
        break;

    case 'notes':
        // Local File Inclusion vulnerability
        $file = isset($_GET['file']) ? $_GET['file'] : 'welcome.txt';
        echo '<ul class="ticket-list">';
        echo '<li><a href="?page=notes&file=welcome.txt">Onboarding Note (T. Reyes)</a></li>';
        echo '<li><a href="?page=notes&file=todo.txt">Open Items &mdash; Systems</a></li>';
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
            <footer>ROSTER Terminal v2.1 &mdash; OCPA Region 4 &middot; Do not forward case material off-network.</footer>
        </div>
    </main>
</div>
</body>
</html>
