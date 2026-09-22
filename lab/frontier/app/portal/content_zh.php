<?php
// 中文版內容包（ROSTER terminal）。由 Docker build ARG LANG 在建置時選擇，
// 執行中的程式碼完全不判斷語言，只是照著建置出來的 content.php 顯示。

$DEPENDENT_INDEX = array(
    array('name' => 'Eli Okafor', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-11902',
          'status' => '結案 - 死亡（醫療原因，6 歲）', 'image' => 'case_okafor.png'),
    array('name' => 'Talia Wren', 'colony' => 'Madrigal', 'case_ref' => 'OCPA-R4-11944',
          'status' => '結案 - 死亡（醫療原因，6 歲）', 'image' => 'case_wren.png'),
    array('name' => 'Dominic Farrow', 'colony' => 'Skopje', 'case_ref' => 'OCPA-R4-11887',
          'status' => '結案 - 死亡（醫療原因，6 歲）', 'image' => 'case_farrow.png'),
    array('name' => 'Priya Anand', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-12210',
          'status' => '在案 - 一般被扶養人案件', 'image' => 'case_anand.png'),
    array('name' => 'Marcus Webb', 'colony' => 'Tribute', 'case_ref' => 'OCPA-R4-12551',
          'status' => '在案 - 一般被扶養人案件', 'image' => 'case_webb.png'),
    array('name' => 'Dana Song', 'colony' => 'Coral', 'case_ref' => 'OCPA-R4-12608',
          'status' => '在案 - 一般被扶養人案件', 'image' => 'case_song.png'),
    array('name' => 'Theo Alvarez', 'colony' => 'Eridanus II', 'case_ref' => 'OCPA-R4-12439',
          'status' => '結案 - 家屬已遷離殖民地', 'image' => 'case_alvarez.png'),
);

$NAV = array(
    'home' => '主控台',
    'search' => '被扶養人狀態索引',
    'upload' => '案件檔案收件',
    'ping' => '網路診斷',
    'notes' => '支援工單',
);

$SERVICES = array(
    array('name' => 'ROSTER Terminal', 'status' => 'ok'),
    array('name' => 'Webmail Gateway', 'status' => 'ok'),
    array('name' => 'LEDGER Sync', 'status' => 'ok'),
    array('name' => '案件檔案收件', 'status' => 'degraded'),
);

$TIPS = array(
    '案件編號格式為 OCPA-R{區域}-{5 位數字}。常用查詢建議加入書籤，不用每次重新搜尋。',
    '終端機閒置 20 分鐘後 session 會過期。離開座位前請先儲存案件筆記。',
    '支援工單只在平日上班時間由 Systems 監看。緊急存取問題請直接到 Building 2 服務台。',
    '掃描檔超過 25MB 上傳可能會逾時。大型案件檔案請先拆分再送出。',
);

$STR = array(
    'page_title_not_found' => '找不到頁面',
    'html_title' => 'ROSTER :: OCPA 區域終端機',
    'topbar' => 'UNSC OCPA 網路 &mdash; 僅限授權人員 &mdash; 所有活動均予記錄（Reg. 4 系統指令 09）',
    'brand_name' => 'ROSTER Terminal',
    'brand_sub' => 'OCPA &middot; 第四區',
    'sidefoot_session' => 'SESSION duty-terminal-04',
    'sidefoot_lastlogin' => '上次登入 2555-03-19 07:45',
    'breadcrumb_root' => 'OCPA &rsaquo; ROSTER &rsaquo;',
    'footer' => 'ROSTER Terminal v2.1 &mdash; OCPA 第四區 &middot; 案件資料請勿轉發至網外。',
    'rail_regional_network' => '區域網路',
    'rail_region_alt' => 'OCPA 第四區網路示意圖',
    'rail_system_status' => '系統狀態',
    'rail_terminal_tip' => '終端機小提示',
    'tip_label' => 'TIP&nbsp;&mdash;',

    // home
    'stat_active_cases' => '在案被扶養人案件',
    'stat_closed_quarter' => '本季結案數',
    'stat_pending_review' => '待審核案件',
    'stat_open_tickets' => '未結支援工單',
    'system_notices' => '系統公告',
    'notice_1' => '年度識別證重拍週 - 報名表在 Building 2 設施服務台。',
    'notice_2' => '排定維護時段，週日 0200-0400 - 終端機可能短暫無法使用。',
    'notice_3' => '員工餐廳週四 1100-1400 深度清潔暫停開放。二樓、四樓自動販賣機不受影響。',
    'notice_4' => 'Building 3 電梯檢查，週三 0800-1200 - 該時段請改走東側樓梯。',
    'notice_5' => 'Building 4 停水，週二 0600-0900 - 詳情請見支援工單。',
    'notice_6' => 'C 停車場路面整修完工。標準核可停車證即日恢復使用。',
    'notice_7' => '提醒：案件檔案收件僅接受掃描信件與轉移紀錄。',
    'notice_8' => '第四區季度全體會議改到 25 日，時間地點不變。',
    'quick_links' => '快速連結',
    'quicklink_search' => '被扶養人狀態索引',
    'quicklink_upload' => '案件檔案收件',
    'quicklink_notes' => '支援工單',
    'quicklink_webmail' => 'Webmail',

    // search
    'search_back' => '&laquo; 返回被扶養人狀態索引',
    'field_colony' => '登記殖民地：',
    'field_case_ref' => '案件編號：',
    'field_status' => '狀態：',
    'search_intro' => '可依被扶養人姓名、登記殖民地或案件編號查詢。',
    'search_placeholder' => '搜尋紀錄...',
    'search_submit' => '搜尋',
    'search_results_for' => '搜尋結果：',
    'search_no_results' => '目前索引裡查無符合條件的紀錄。',

    // upload
    'upload_intro' => '上傳掃描信件、醫療轉移紀錄，或需要建檔的案件資料。',
    'upload_rejected' => '收件被拒：這個檔案看起來不是有效的掃描影像。',
    'upload_indexed' => '檔案已建檔：',
    'upload_failed' => '收件失敗。',
    'upload_submit' => '送出',

    // ping
    'ping_intro' => 'ROSTER 舊系統遷移時留下的工具。如果異常請聯絡 Systems。',
    'ping_placeholder' => '輸入主機名稱或 IP',
    'ping_submit' => 'Ping',
    'ping_invalid' => '主機名稱或 IP 格式不正確。',

    // notes
    'notes_link_welcome' => '新人須知（T. Reyes）',
    'notes_link_todo' => '待辦事項 &mdash; Systems',
    'notes_reyes_name' => 'T. Reyes',
    'notes_reyes_dept' => 'Systems &middot; ROSTER / LEDGER',
    'notes_not_found' => '找不到檔案。',

    'page_not_found' => '找不到頁面。',
);
