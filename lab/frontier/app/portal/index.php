<?php
// UNSC OCPA — ROSTER Terminal
// Colonial Dependent & Personnel Records Access

$page = isset($_GET['page']) ? $_GET['page'] : 'home';

// Dependent Status Index - real (if limited) backing data, not a static
// placeholder. This is the same batch of closed cases OCPA can legally
// disclose the existence of; internal transfer/disposition detail lives
// on other systems entirely.
require __DIR__ . '/content.php';

$page_title = isset($NAV[$page]) ? $NAV[$page] : $STR['page_title_not_found'];
$tip = $TIPS[intval(date('j')) % count($TIPS)];
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?php echo htmlspecialchars($STR['html_title']); ?></title>
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
<div class="topbar"><?php echo $STR['topbar']; ?></div>
<div class="shell">
    <aside class="sidebar">
        <div class="brand">
            <img src="assets/unsc_insignia.png" alt="">
            <div>
                <div class="name"><?php echo htmlspecialchars($STR['brand_name']); ?></div>
                <div class="sub"><?php echo $STR['brand_sub']; ?></div>
            </div>
        </div>
        <nav class="sidenav">
<?php foreach ($NAV as $key => $label):
    $cls = ($key === $page) ? 'active' : ''; ?>
            <a class="<?php echo $cls; ?>" href="?page=<?php echo $key; ?>"><?php echo htmlspecialchars($label); ?></a>
<?php endforeach; ?>
        </nav>
        <div class="sidefoot">
            <?php echo htmlspecialchars($STR['sidefoot_session']); ?><span class="cursor-blink"></span><br>
            <?php echo htmlspecialchars($STR['sidefoot_lastlogin']); ?>
        </div>
    </aside>

    <main class="main">
        <div class="pagebar">
            <div>
                <div class="crumb"><?php echo $STR['breadcrumb_root']; ?> <b><?php echo htmlspecialchars($page_title); ?></b></div>
                <h1 class="page-title"><?php echo htmlspecialchars($page_title); ?></h1>
            </div>
        </div>
        <div class="body-row">
        <div class="content">
<?php
switch($page) {
    case 'home':
        echo '<div class="dash-grid">';
        echo '<div class="stat"><div class="num">142</div><div class="lbl">' . htmlspecialchars($STR['stat_active_cases']) . '</div></div>';
        echo '<div class="stat"><div class="num">38</div><div class="lbl">' . htmlspecialchars($STR['stat_closed_quarter']) . '</div></div>';
        echo '<div class="stat"><div class="num">6</div><div class="lbl">' . htmlspecialchars($STR['stat_pending_review']) . '</div></div>';
        echo '<div class="stat"><div class="num">3</div><div class="lbl">' . htmlspecialchars($STR['stat_open_tickets']) . '</div></div>';
        echo '</div>';

        echo '<h2>' . htmlspecialchars($STR['system_notices']) . '</h2>';
        echo '<div class="board">';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_1']) . '</span><span class="tag">2555-03-19</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_2']) . '</span><span class="tag">2555-03-18</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_3']) . '</span><span class="tag">2555-03-14</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_4']) . '</span><span class="tag">2555-03-11</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_5']) . '</span><span class="tag">2555-03-09</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_6']) . '</span><span class="tag">2555-03-06</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_7']) . '</span><span class="tag">2555-02-27</span></div>';
        echo '<div class="board-item"><span>' . htmlspecialchars($STR['notice_8']) . '</span><span class="tag">2555-02-19</span></div>';
        echo '</div>';

        echo '<h2>' . htmlspecialchars($STR['quick_links']) . '</h2>';
        echo '<div class="quicklinks">';
        echo '<a href="?page=search">' . htmlspecialchars($STR['quicklink_search']) . '</a>';
        echo '<a href="?page=upload">' . htmlspecialchars($STR['quicklink_upload']) . '</a>';
        echo '<a href="?page=notes">' . htmlspecialchars($STR['quicklink_notes']) . '</a>';
        $request_host = explode(':', $_SERVER['HTTP_HOST'])[0];
        $webmail_port = getenv('WEBMAIL_PORT') ?: '8025';
        echo '<a href="http://' . htmlspecialchars($request_host) . ':' . htmlspecialchars($webmail_port) . '">' . htmlspecialchars($STR['quicklink_webmail']) . '</a>';
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
            echo '<a class="detail-back" href="?page=search">' . $STR['search_back'] . '</a>';
            echo '<div class="detail-card">';
            echo '<img src="assets/' . htmlspecialchars($detail_rec['image']) . '" width="280">';
            echo '<div>';
            echo '<h2>' . htmlspecialchars($detail_rec['name']) . '</h2>';
            echo '<div class="field">' . htmlspecialchars($STR['field_colony']) . ' ' . htmlspecialchars($detail_rec['colony']) . '</div>';
            echo '<div class="field">' . htmlspecialchars($STR['field_case_ref']) . ' ' . htmlspecialchars($detail_rec['case_ref']) . '</div>';
            echo '<div class="field">' . htmlspecialchars($STR['field_status']) . ' ' . htmlspecialchars($detail_rec['status']) . '</div>';
            if (isset($detail_rec['transfer_ref'])) {
                echo '<div class="field">' . htmlspecialchars($STR['field_transfer_ref']) . ' ' . htmlspecialchars($detail_rec['transfer_ref']) . '</div>';
            }
            echo '</div></div>';
            break;
        }

        $query = isset($_GET['q']) ? $_GET['q'] : '';
        echo '<p>' . htmlspecialchars($STR['search_intro']) . '</p>';
        echo '<form method="GET">';
        echo '<input type="hidden" name="page" value="search">';
        echo '<input type="text" name="q" placeholder="' . htmlspecialchars($STR['search_placeholder']) . '" value="' . htmlspecialchars($query) . '">';
        echo ' <input type="submit" value="' . htmlspecialchars($STR['search_submit']) . '">';
        echo '</form>';
        if ($query) {
            echo "<p style='margin-top:16px'>" . htmlspecialchars($STR['search_results_for']) . " " . htmlspecialchars($query) . "</p>";
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
                    echo '<div class="field">' . htmlspecialchars($STR['field_colony']) . ' ' . htmlspecialchars($rec['colony']) . '</div>';
                    echo '<div class="field">' . htmlspecialchars($STR['field_case_ref']) . ' ' . htmlspecialchars($rec['case_ref']) . '</div>';
                    echo '<div class="field">' . htmlspecialchars($STR['field_status']) . ' ' . htmlspecialchars($rec['status']) . '</div>';
                    if (isset($rec['transfer_ref'])) {
                        echo '<div class="field">' . htmlspecialchars($STR['field_transfer_ref']) . ' ' . htmlspecialchars($rec['transfer_ref']) . '</div>';
                    }
                    echo '</div></div></a>';
                }
            } else {
                echo "<p>" . htmlspecialchars($STR['search_no_results']) . "</p>";
            }
        }
        break;

    case 'upload':
        echo '<div class="panel">';
        echo '<p style="margin-top:0">' . htmlspecialchars($STR['upload_intro']) . '</p>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
            $target = '/var/www/html/portal/uploads/' . basename($_FILES['file']['name']);
            // Post-finding patch (SEC-1188): reject anything that isn't a
            // decodable image. Still no extension allowlist or rename -
            // that part of the finding was marked "won't fix" (see todo.txt).
            if (@getimagesize($_FILES['file']['tmp_name']) === false) {
                echo "<p class='warning'>" . htmlspecialchars($STR['upload_rejected']) . "</p>";
            } elseif (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
                echo "<p>" . htmlspecialchars($STR['upload_indexed']) . " <a href='/uploads/" . basename($_FILES['file']['name']) . "'>" . htmlspecialchars($_FILES['file']['name']) . "</a></p>";
            } else {
                echo "<p class='warning'>" . htmlspecialchars($STR['upload_failed']) . "</p>";
            }
        }
        echo '<form method="POST" enctype="multipart/form-data">';
        echo '<input type="file" name="file"><br><br>';
        echo '<input type="submit" value="' . htmlspecialchars($STR['upload_submit']) . '">';
        echo '</form>';
        echo '</div>';
        break;

    case 'ping':
        echo '<p>' . htmlspecialchars($STR['ping_intro']) . '</p>';
        echo '<form method="POST">';
        echo '<input type="text" name="host" placeholder="' . htmlspecialchars($STR['ping_placeholder']) . '">';
        echo ' <input type="submit" value="' . htmlspecialchars($STR['ping_submit']) . '">';
        echo '</form>';
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['host'])) {
            $host = $_POST['host'];
            // Re-done properly after SEC-1188 flagged the old semicolon-only
            // filter: validate against a hostname/IP shape instead of
            // blacklisting separators, then still pass through escapeshellarg.
            if (preg_match('/^[a-zA-Z0-9.\-]+$/', $host)) {
                $output = shell_exec("ping -c 3 " . escapeshellarg($host));
                echo '<pre style="margin-top:16px">' . htmlspecialchars($output) . '</pre>';
            } else {
                echo '<p class="warning">' . htmlspecialchars($STR['ping_invalid']) . '</p>';
            }
        }
        break;

    case 'notes':
        $file = isset($_GET['file']) ? $_GET['file'] : 'welcome.txt';
        echo '<ul class="ticket-list">';
        echo '<li><a href="?page=notes&file=welcome.txt">' . htmlspecialchars($STR['notes_link_welcome']) . '</a></li>';
        echo '<li><a href="?page=notes&file=todo.txt">' . $STR['notes_link_todo'] . '</a></li>';
        echo '</ul>';
        // basename() strips any directory component, so ../ traversal
        // collapses to a lookup inside notes/ instead of escaping it.
        $filepath = '/var/www/html/portal/notes/' . basename($file);
        $reyes_files = array('welcome.txt', 'todo.txt', 'credential_rotation_status.txt', 't_reyes_annual_review_2546.txt');
        if (in_array($file, $reyes_files, true)) {
            echo '<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">';
            echo '<a href="assets/t_reyes.jpg" target="_blank" rel="noopener"><img src="assets/t_reyes.jpg" width="60" style="border-radius:0;border:1px solid var(--border)"></a>';
            echo '<div><div style="font-size:14.5px;font-weight:600;color:var(--text)">' . htmlspecialchars($STR['notes_reyes_name']) . '</div><div style="font-size:12px;color:var(--text-faint)">' . $STR['notes_reyes_dept'] . '</div></div>';
            echo '</div>';
        }
        if (file_exists($filepath)) {
            echo "<pre>" . htmlspecialchars(file_get_contents($filepath)) . "</pre>";
        } else {
            echo "<p>" . htmlspecialchars($STR['notes_not_found']) . "</p>";
        }
        break;

    default:
        echo "<p>" . htmlspecialchars($STR['page_not_found']) . "</p>";
}
?>
            <footer><?php echo $STR['footer']; ?></footer>
        </div>
        <aside class="rail">
            <div class="rail-card">
                <h3><?php echo htmlspecialchars($STR['rail_regional_network']); ?></h3>
                <img src="assets/region_map.png" alt="<?php echo htmlspecialchars($STR['rail_region_alt']); ?>">
            </div>
            <div class="rail-card">
                <h3><?php echo htmlspecialchars($STR['rail_system_status']); ?></h3>
                <div class="body" style="padding:6px 0">
<?php foreach ($SERVICES as $svc): ?>
                    <div class="status-row"><span class="dot <?php echo $svc['status']; ?>"></span><?php echo htmlspecialchars($svc['name']); ?></div>
<?php endforeach; ?>
                </div>
            </div>
            <div class="rail-card tip-card">
                <h3><?php echo htmlspecialchars($STR['rail_terminal_tip']); ?></h3>
                <div class="body"><span class="tip-label"><?php echo $STR['tip_label']; ?></span> <?php echo htmlspecialchars($tip); ?></div>
            </div>
        </aside>
        </div>
    </main>
</div>
</body>
</html>
