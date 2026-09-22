<?php
// English content pack for the ROSTER terminal. Selected at Docker build
// time (see Dockerfile ARG LANG) - the running app never branches on
// language, it just gets whichever content_*.php the image was built with.

$DEPENDENT_INDEX = array(
    array('name' => 'Eli Okafor', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-11902',
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_okafor.png',
          'transfer_ref' => 'SPINDLE-7-0119'),
    array('name' => 'Talia Wren', 'colony' => 'Madrigal', 'case_ref' => 'OCPA-R4-11944',
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_wren.png',
          'transfer_ref' => 'SPINDLE-7-0142'),
    array('name' => 'Dominic Farrow', 'colony' => 'Skopje', 'case_ref' => 'OCPA-R4-11887',
          'status' => 'Case Closed - Deceased (medical, age 6)', 'image' => 'case_farrow.png',
          'transfer_ref' => 'SPINDLE-7-0087'),
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

$STR = array(
    'page_title_not_found' => 'Not Found',
    'html_title' => 'ROSTER :: OCPA Regional Terminal',
    'topbar' => 'UNSC OCPA NETWORK &mdash; AUTHORIZED PERSONNEL ONLY &mdash; ACTIVITY IS LOGGED (Reg. 4 Systems Directive 09)',
    'brand_name' => 'ROSTER Terminal',
    'brand_sub' => 'OCPA &middot; Region 4',
    'sidefoot_session' => 'SESSION duty-terminal-04',
    'sidefoot_lastlogin' => 'LAST LOGIN 2555-03-19 07:45',
    'breadcrumb_root' => 'OCPA &rsaquo; ROSTER &rsaquo;',
    'footer' => 'ROSTER Terminal v2.1 &mdash; OCPA Region 4 &middot; Do not forward case material off-network.',
    'rail_regional_network' => 'Regional Network',
    'rail_region_alt' => 'OCPA Region 4 network reference',
    'rail_system_status' => 'System Status',
    'rail_terminal_tip' => 'Terminal Tip',
    'tip_label' => 'TIP&nbsp;&mdash;',

    // home
    'stat_active_cases' => 'Active dependent cases',
    'stat_closed_quarter' => 'Closed this quarter',
    'stat_pending_review' => 'Pending review',
    'stat_open_tickets' => 'Open support tickets',
    'system_notices' => 'System Notices',
    'notice_1' => 'Annual badge photo retake week - sign-up sheet at the Facilities desk, Building 2.',
    'notice_2' => 'Scheduled maintenance window, Sun 0200-0400 - terminal may be briefly unavailable.',
    'notice_3' => 'Cafeteria closed for deep clean, Thu 1100-1400. Vending machines on 2nd and 4th floor unaffected.',
    'notice_4' => 'Building 3 elevator inspection, Wed 0800-1200 - use the east stairwell during that window.',
    'notice_5' => 'Water shutoff, Building 4, Tue 0600-0900 - see Support Tickets for details.',
    'notice_6' => 'Lot C resurfacing complete. Standard permit parking resumes Monday.',
    'notice_7' => 'Reminder: Case File Intake is the only channel for adding or amending documentation on an existing case. Records cannot act on paperwork received any other way.',
    'notice_8' => 'Region 4 quarterly all-hands moved to the 25th, same time, same room.',
    'quick_links' => 'Quick Links',
    'quicklink_search' => 'Dependent Status Index',
    'quicklink_upload' => 'Case File Intake',
    'quicklink_notes' => 'Support Tickets',
    'quicklink_webmail' => 'Webmail',

    // search
    'search_back' => '&laquo; back to Dependent Status Index',
    'field_colony' => 'Colony of record:',
    'field_case_ref' => 'Case reference:',
    'field_status' => 'Status:',
    'field_transfer_ref' => 'Internal transfer ref:',
    'search_intro' => 'Search by dependent name, colony of record, or case reference number.',
    'search_placeholder' => 'Search records...',
    'search_submit' => 'Search',
    'search_results_for' => 'Results for:',
    'search_no_results' => 'No records found matching your query in the current index.',

    // upload
    'upload_intro' => 'Submit or resubmit intake material for a case file - scanned correspondence, medical transfer notes, or amended closure documentation. This is the only way anything gets added to a case record once it has been closed.',
    'upload_rejected' => "Intake rejected: file does not appear to be a valid scanned image.",
    'upload_indexed' => 'File indexed:',
    'upload_failed' => 'Intake failed.',
    'upload_submit' => 'Submit',

    // ping
    'ping_intro' => 'Legacy tool left over from the ROSTER migration. Reach out to Systems if it misbehaves.',
    'ping_placeholder' => 'Enter hostname or IP',
    'ping_submit' => 'Ping',
    'ping_invalid' => 'Invalid hostname or IP.',

    // notes
    'notes_link_welcome' => 'Onboarding Note (T. Reyes)',
    'notes_link_todo' => 'Open Items &mdash; Systems',
    'notes_reyes_name' => 'T. Reyes',
    'notes_reyes_dept' => 'Systems &middot; ROSTER / LEDGER',
    'notes_not_found' => 'File not found.',

    'page_not_found' => 'Page not found.',
);
