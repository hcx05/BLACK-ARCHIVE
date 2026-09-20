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
    array('name' => 'Marcus Webb', 'colony' => 'Tribute', 'case_ref' => 'OCPA-R4-12551',
          'status' => 'Active - standard dependent case', 'image' => 'case_webb.png'),
    array('name' => 'Dana Song', 'colony' => 'Coral', 'case_ref' => 'OCPA-R4-12608',
          'status' => 'Active - standard dependent case', 'image' => 'case_song.png'),
    array('name' => 'Theo Alvarez', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-12439',
          'status' => 'Case Closed - Family relocated off-colony', 'image' => 'case_alvarez.png'),
);

$NAV = array(
    'home' => 'Dashboard',
    'search' => 'Dependent Status Index',
    'upload' => 'Case File Intake',
    'ping' => 'Network Diagnostics',
    'notes' => 'Support Tickets',
);
$page_title = isset($NAV[$page]) ? $NAV[$page] : 'Not Found';

$SERVICES = array(
    array('name' => 'ROSTER Terminal', 'status' => 'ok'),
    array('name' => 'Webmail Gateway', 'status' => 'ok'),
    array('name' => 'LEDGER Sync', 'status' => 'ok'),
    array('name' => 'Case File Intake', 'status' => 'degraded'),
);
$TIPS = array(
    'Case reference numbers follow OCPA-R{region}-{5 digits}. Bookmark frequent lookups instead of re-searching each time.',
    'Terminal sessions expire after 20 minutes idle. Save case notes before stepping away.',
    'Support Tickets is monitored by Systems on business days only. For urgent access issues, use the Building 2 helpdesk in person.',
    'Scanned intake files over 25MB may time out on upload. Split large case files before submitting.',
);
$tip = $TIPS[intval(date('j')) % count($TIPS)];
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ROSTER :: OCPA Regional Terminal</title>
    <link rel="icon" type="image/png" href="assets/ocpa_seal.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap">
    <style>
        :root {
            --bg: #000000;
            --surface: #060d14;
            --surface-2: #0a1622;
            --surface-hover: #0d1c2a;
            --border: #1a3244;
            --border-soft: #101f2a;
            --text: #7ec4e8;
            --text-dim: #4f89ac;
            --text-faint: #2f5870;
            --accent: #bfe6f7;
            --accent-soft: rgba(191, 230, 247, 0.06);
            --danger: #d4685c;
            --danger-bg: #200d0b;
            --mono: 'IBM Plex Mono', 'Consolas', monospace;
        }
        * { box-sizing: border-box; }
        html { background: var(--bg); }
        body {
            font-family: var(--mono);
            margin: 0;
            color: var(--text);
            font-size: 15.5px;
            line-height: 1.55;
            background-color: var(--bg);
            background-image:
                repeating-linear-gradient(180deg, rgba(191,230,247,0.016) 0px, rgba(191,230,247,0.016) 1px, transparent 1px, transparent 3px),
                radial-gradient(ellipse at 50% 40%, rgba(191,230,247,0.02) 0%, rgba(0,0,0,0) 55%),
                radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.6) 100%);
            background-attachment: fixed;
        }
        a { color: var(--accent); }
        .cursor-blink { display: inline-block; width: 0.55em; height: 1em; background: var(--text); vertical-align: -0.15em; margin-left: 2px; animation: blink 1.1s steps(1) infinite; }
        @keyframes blink { 50% { opacity: 0; } }
        @media (prefers-reduced-motion: reduce) { .cursor-blink { animation: none; opacity: 0.6; } }
        .topbar {
            background: var(--danger-bg);
            color: var(--danger);
            text-align: center;
            padding: 7px 12px;
            font-size: 12px;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            border-bottom: 1px solid #3a1d1d;
        }
        .shell { display: flex; min-height: calc(100vh - 30px); }

        /* Sidebar */
        .sidebar {
            width: 260px;
            flex-shrink: 0;
            background: var(--surface);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px 16px;
            border-bottom: 1px solid var(--border-soft);
        }
        .brand img { width: 56px; opacity: 0.95; flex-shrink: 0; filter: grayscale(0.2); }
        .brand .name { font-weight: 600; font-size: 15px; letter-spacing: 0.3px; color: var(--text); }
        .brand .sub { font-size: 12px; color: var(--text-faint); letter-spacing: 0.5px; text-transform: uppercase; }
        .sidenav { padding: 10px 0; flex: 1; }
        .sidenav a {
            display: block;
            padding: 10px 18px;
            font-size: 14px;
            color: var(--text-dim);
            text-decoration: none;
            border-left: 3px solid transparent;
        }
        .sidenav a:hover { background: var(--surface-hover); color: var(--text); }
        .sidenav a.active { color: #051622; background: var(--text); border-left-color: var(--accent); font-weight: 600; }
        .sidefoot {
            padding: 14px 16px;
            border-top: 1px solid var(--border-soft);
            font-size: 11.5px;
            color: var(--text-faint);
            line-height: 1.6;
        }

        /* Main */
        .main { flex: 1; min-width: 0; }
        .pagebar {
            padding: 16px 28px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 8px;
        }
        .crumb { font-size: 12px; color: var(--text-faint); letter-spacing: 0.5px; }
        .crumb b { color: var(--text-dim); }
        h1.page-title { font-size: 20px; font-weight: 600; margin: 3px 0 0 0; color: var(--text); text-shadow: 0 0 6px rgba(126,196,232,0.35); }
        .body-row { display: flex; align-items: flex-start; }
        .content { flex: 1; min-width: 0; padding: 24px 28px 40px; }

        /* Right rail */
        .rail { width: 280px; flex-shrink: 0; padding: 24px 24px 40px 0; }
        .rail-card { background: var(--surface); border: 1px solid var(--border); border-radius: 0; margin-bottom: 16px; overflow: hidden; }
        .rail-card h3 { font-size: 12px; letter-spacing: 0.5px; color: var(--text-faint); font-weight: 600; margin: 0; padding: 10px 14px; border-bottom: 1px solid var(--border-soft); }
        .rail-card .body { padding: 12px 14px; }
        .rail-card img { width: 100%; display: block; }
        .status-row { display: flex; align-items: center; gap: 9px; padding: 8px 14px; font-size: 13px; color: var(--text-dim); }
        .status-row .dot { width: 10px; height: 10px; border-radius: 0; flex-shrink: 0; }
        .status-row .dot.ok { background: var(--text); }
        .status-row .dot.degraded { background: #d1a95f; }
        .tip-card .body { font-size: 13px; color: var(--text-dim); line-height: 1.6; }
        .tip-label { color: var(--accent); font-weight: 600; letter-spacing: 0.4px; }
        @media (max-width: 980px) {
            .rail { display: none; }
        }
        h2 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-dim); font-weight: 600; margin: 28px 0 10px; }
        h2:first-child { margin-top: 0; }
        p { color: var(--text-dim); }

        /* Components */
        .dash-grid { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 4px; }
        .stat { flex: 1 1 150px; background: var(--surface); border: 1px solid var(--border); border-radius: 0; padding: 16px 18px; }
        .stat .num { font-size: 28px; font-weight: 600; color: var(--text); font-variant-numeric: tabular-nums; text-shadow: 0 0 6px rgba(126,196,232,0.3); }
        .stat .lbl { font-size: 12px; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.4px; margin-top: 4px; }
        .board { background: var(--surface); border: 1px solid var(--border); border-radius: 0; overflow: hidden; }
        .board-item { padding: 11px 14px; border-bottom: 1px solid var(--border-soft); font-size: 14px; display: flex; justify-content: space-between; gap: 14px; color: var(--text-dim); }
        .board-item:last-child { border-bottom: none; }
        .board-item .tag { color: var(--text-faint); font-size: 12px; white-space: nowrap; }
        .quicklinks { display: flex; gap: 8px; flex-wrap: wrap; }
        .quicklinks a { background: var(--surface); border: 1px solid var(--border); color: var(--text-dim); padding: 9px 14px; border-radius: 0; text-decoration: none; font-size: 13.5px; }
        .quicklinks a:hover { color: #051622; border-color: var(--text); background: var(--text); }

        .panel { background: var(--surface); border: 1px solid var(--border); border-radius: 0; padding: 20px 22px; }
        input[type="text"], input[type="file"] { font-family: var(--mono); padding: 9px 10px; width: 320px; max-width: 100%; background: var(--bg); border: 1px solid var(--border); border-radius: 0; color: var(--text); font-size: 14px; }
        input[type="submit"], button {
            font-family: var(--mono); padding: 9px 18px; background: var(--surface-2); color: var(--text);
            border: 1px solid var(--border); border-radius: 0; cursor: pointer; font-size: 13.5px;
            letter-spacing: 0.4px; text-transform: uppercase;
        }
        input[type="submit"]:hover, button:hover { border-color: var(--text); background: var(--text); color: #051622; }
        pre {
            font-family: var(--mono); font-size: 13.5px; background: #030810; color: #8ed0ef;
            padding: 16px 18px; border: 1px solid var(--border); border-radius: 0; overflow-x: auto; line-height: 1.6;
        }
        .warning { color: var(--danger); }
        .result-card { display: flex; gap: 16px; border: 1px solid var(--border); border-radius: 0; padding: 14px; margin: 10px 0; background: var(--surface); }
        .result-card img { border: 1px solid var(--border-soft); border-radius: 0; }
        .result-card .name { font-weight: 600; color: var(--text); margin-bottom: 3px; font-size: 15px; }
        .result-card .field { font-size: 13px; color: var(--text-dim); }
        a.result-link { display: block; text-decoration: none; color: inherit; }
        a.result-link:hover .result-card { border-color: var(--text); }
        a.result-link:hover .name { color: var(--accent); }
        .detail-back { display: inline-block; margin-bottom: 14px; font-size: 13px; }
        .detail-card { display: flex; gap: 26px; border: 1px solid var(--border); background: var(--surface); padding: 22px; flex-wrap: wrap; }
        .detail-card img { border: 1px solid var(--border-soft); flex-shrink: 0; }
        .detail-card h2 { margin: 0 0 12px; font-size: 19px; color: var(--text); text-shadow: 0 0 6px rgba(126,196,232,0.3); }
        .detail-card .field { font-size: 14px; color: var(--text-dim); margin-bottom: 6px; }
        ul.ticket-list { list-style: none; padding: 0; margin: 0 0 16px; }
        ul.ticket-list li { border: 1px solid var(--border); border-radius: 0; margin-bottom: 6px; background: var(--surface); }
        ul.ticket-list a { display: block; padding: 11px 14px; font-size: 14px; text-decoration: none; color: var(--text-dim); }
        ul.ticket-list a:hover { color: var(--accent); }

        footer { font-size: 12px; color: var(--text-faint); margin-top: 30px; padding-top: 14px; border-top: 1px solid var(--border-soft); }

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
            SESSION duty-terminal-04<span class="cursor-blink"></span><br>
            LAST LOGIN 2555-03-19 07:45
        </div>
    </aside>

    <main class="main">
        <div class="pagebar">
            <div>
                <div class="crumb">OCPA &rsaquo; ROSTER &rsaquo; <b><?php echo htmlspecialchars($page_title); ?></b></div>
                <h1 class="page-title"><?php echo htmlspecialchars($page_title); ?></h1>
            </div>
        </div>
        <div class="body-row">
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
        echo '<div class="board-item"><span>Annual badge photo retake week - sign-up sheet at the Facilities desk, Building 2.</span><span class="tag">2555-03-19</span></div>';
        echo '<div class="board-item"><span>Scheduled maintenance window, Sun 0200-0400 - terminal may be briefly unavailable.</span><span class="tag">2555-03-18</span></div>';
        echo '<div class="board-item"><span>Cafeteria closed for deep clean, Thu 1100-1400. Vending machines on 2nd and 4th floor unaffected.</span><span class="tag">2555-03-14</span></div>';
        echo '<div class="board-item"><span>Building 3 elevator inspection, Wed 0800-1200 - use the east stairwell during that window.</span><span class="tag">2555-03-11</span></div>';
        echo '<div class="board-item"><span>Water shutoff, Building 4, Tue 0600-0900 - see Support Tickets for details.</span><span class="tag">2555-03-09</span></div>';
        echo '<div class="board-item"><span>Lot C resurfacing complete. Standard permit parking resumes Monday.</span><span class="tag">2555-03-06</span></div>';
        echo '<div class="board-item"><span>Reminder: case file intake accepts scanned correspondence and transfer notes only.</span><span class="tag">2555-02-27</span></div>';
        echo '<div class="board-item"><span>Region 4 quarterly all-hands moved to the 25th, same time, same room.</span><span class="tag">2555-02-19</span></div>';
        echo '</div>';

        echo '<h2>Quick Links</h2>';
        echo '<div class="quicklinks">';
        echo '<a href="?page=search">Dependent Status Index</a>';
        echo '<a href="?page=upload">Case File Intake</a>';
        echo '<a href="?page=notes">Support Tickets</a>';
        $request_host = explode(':', $_SERVER['HTTP_HOST'])[0];
        echo '<a href="http://' . htmlspecialchars($request_host) . ':8025">Webmail</a>';
        echo '</div>';
        break;

    case 'search':
        // Detail view: exact case_ref lookup against the known index only
        // (no filesystem/DB access, no substring match) - safe regardless
        // of what's in $_GET['case'].
        $detail_ref = isset($_GET['case']) ? $_GET['case'] : '';
        $detail_rec = null;
        if ($detail_ref !== '') {
            foreach ($DEPENDENT_INDEX as $rec) {
                if ($rec['case_ref'] === $detail_ref) {
                    $detail_rec = $rec;
                    break;
                }
            }
        }
        if ($detail_rec) {
            echo '<a class="detail-back" href="?page=search">&laquo; back to Dependent Status Index</a>';
            echo '<div class="detail-card">';
            echo '<img src="assets/' . htmlspecialchars($detail_rec['image']) . '" width="280">';
            echo '<div>';
            echo '<h2>' . htmlspecialchars($detail_rec['name']) . '</h2>';
            echo '<div class="field">Colony of record: ' . htmlspecialchars($detail_rec['colony']) . '</div>';
            echo '<div class="field">Case reference: ' . htmlspecialchars($detail_rec['case_ref']) . '</div>';
            echo '<div class="field">Status: ' . htmlspecialchars($detail_rec['status']) . '</div>';
            echo '</div></div>';
            break;
        }

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
                    echo '<a class="result-link" href="?page=search&case=' . urlencode($rec['case_ref']) . '">';
                    echo '<div class="result-card">';
                    echo '<img src="assets/' . $rec['image'] . '" width="140">';
                    echo '<div>';
                    echo '<div class="name">' . htmlspecialchars($rec['name']) . '</div>';
                    echo '<div class="field">Colony of record: ' . htmlspecialchars($rec['colony']) . '</div>';
                    echo '<div class="field">Case reference: ' . htmlspecialchars($rec['case_ref']) . '</div>';
                    echo '<div class="field">Status: ' . htmlspecialchars($rec['status']) . '</div>';
                    echo '</div></div></a>';
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
            // Post-finding patch (SEC-1188): reject anything that isn't a
            // decodable image. Still no extension allowlist or rename -
            // that part of the finding was marked "won't fix" (see todo.txt).
            if (@getimagesize($_FILES['file']['tmp_name']) === false) {
                echo "<p class='warning'>Intake rejected: file does not appear to be a valid scanned image.</p>";
            } elseif (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
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
            // Post-finding patch (SEC-1188): strips the separator from the
            // last incident report. Nobody checked for other separators.
            $host = str_replace(';', '', $_POST['host']);
            // Vulnerable: direct command injection (semicolons only, see above)
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
        $reyes_files = array('welcome.txt', 'todo.txt', 'credential_rotation_status.txt', 't_reyes_annual_review_2546.txt');
        if (in_array($file, $reyes_files, true)) {
            echo '<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">';
            echo '<a href="assets/t_reyes.jpg" target="_blank" rel="noopener"><img src="assets/t_reyes.jpg" width="60" style="border-radius:0;border:1px solid var(--border)"></a>';
            echo '<div><div style="font-size:14.5px;font-weight:600;color:var(--text)">T. Reyes</div><div style="font-size:12px;color:var(--text-faint)">Systems &middot; ROSTER / LEDGER</div></div>';
            echo '</div>';
        }
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
        <aside class="rail">
            <div class="rail-card">
                <h3>Regional Network</h3>
                <img src="assets/region_map.png" alt="OCPA Region 4 network reference">
            </div>
            <div class="rail-card">
                <h3>System Status</h3>
                <div class="body" style="padding:6px 0">
<?php foreach ($SERVICES as $svc): ?>
                    <div class="status-row"><span class="dot <?php echo $svc['status']; ?>"></span><?php echo htmlspecialchars($svc['name']); ?></div>
<?php endforeach; ?>
                </div>
            </div>
            <div class="rail-card tip-card">
                <h3>Terminal Tip</h3>
                <div class="body"><span class="tip-label">TIP&nbsp;&mdash;</span> <?php echo htmlspecialchars($tip); ?></div>
            </div>
        </aside>
        </div>
    </main>
</div>
</body>
</html>
