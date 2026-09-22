# -*- coding: utf-8 -*-
"""中文版內容包（CAIRN Records Terminal）。由 Docker build ARG LANG 在建置時
選擇，admin_panel.py 完全不判斷語言。這裡的關鍵引言盡量沿用
Answer/truth-zh.md 已經確立的譯法，保持全專案用詞一致。"""

RECORDS = [
    (101, "ONI Section III - 處置令 2547-014",
     "//機密 - ONI SECTION III - 限閱//\n"
     "處置令 2547-014\n"
     "FROM: Cmdr. I. Petrov, ONI Section III\n"
     "TO: CAIRN Records Custodian\n"
     "DATE: 2547-02-11\n"
     "RE: SPINDLE 除役 - 紀錄處置\n\n"
     "依據 SPINDLE 除役審查結果，所有早於 2547 年遷移的案件資料重新分類為\n"
     "「限制 - 待處置保留」，等候後續審查。在案被扶養人案件維持留在 LEDGER。\n"
     "所有徵召年代的資料，包括對象轉移紀錄與計畫往來信件，應保留在本節點，\n"
     "等待完整轉移至永久檔案保管單位，期間不得在任何在案 OCPA 案件檔案中\n"
     "引用。\n\n"
     "給保管人的備註：這是一個 staging mirror，不是永久檔案庫。這個節點的\n"
     "完整除役排程訂在轉移完成之後。請不要把這套系統當成正式生產環境。\n\n"
     "本令不授權銷毀資料。僅授權保留。"),

    (102, "Flash-Clone 替代協議 - 醫療附件",
     "//機密 - ONI SECTION III - 限閱//\n"
     "醫療附件 - FLASH-CLONE 替代協議\n"
     "REVIEWED BY: Dr. M. Castel, ONI Section III 醫療督導\n"
     "RE: 候選人徵召 - 案件結案程序\n\n"
     "標準候選人徵召程序需要一份替代生物紀錄，用以結掉原始案件檔案，\n"
     "同時不會引起家屬或殖民地行政單位的疑問。替代品是加速培養、存活期限\n"
     "被縮短的複製體，刻意設計成在任何主治醫師眼中都會判定為普通的自然/\n"
     "醫療死亡——這樣負責結案的當地醫師才不會有任何理由起疑，也不需要\n"
     "被告知這個計畫的存在。\n\n"
     "本處的角色僅限於計畫端的醫療督導：在當地結案之後審核案件檔案，\n"
     "確認替代結果經得起一般查核，並維護複製體規格紀錄。本處沒有親自\n"
     "到場參與任何一次結案。\n\n"
     "交叉參照備註（後來補上，筆跡不同）：我事後審核並簽核了 OCPA-R4-\n"
     "11902、11944、11887 這三份案件檔案，確認結案沒有問題。我做這件事\n"
     "的時候，還不知道自己確認的其實是什麼。我不覺得那樣就沒事，我也不\n"
     "打算假裝自己沒有選擇。\n"
     "- M.C."),

    (103, "書信片段 - C. Halsey 致 Section III，2517",
     "//機密 - ONI SECTION III - 限閱//\n"
     "書信片段（復原，殘缺）\n"
     "FROM: Dr. C. Halsey\n"
     "TO: ONI Section III\n"
     "DATE: 2517（確切日期未能復原）\n\n"
     "……你問我能不能接受這件事。我不覺得那是對的問題。對的問題是，殖民地\n"
     "能不能撐到有資格問我任何問題的那一天。我已經在我們談過之後又跑了\n"
     "三次推估，結果沒有改善。\n\n"
     "我不會假裝這是別的什麼。我在請求你們讓我把孩子從他們的人生裡帶走，\n"
     "不經過他們的同意，也不經過他們父母的同意。我同時也在告訴你們，我\n"
     "相信這是必要的。這兩件事同時為真，我不指望我們任何一個人會因此覺得\n"
     "心安。\n\n"
     "依原送候選人名單繼續進行。"),

    (104, "內部備忘錄 - CPO M. Kade 致 Records，2540",
     "//機密 - ONI SECTION III - 限閱//\n"
     "內部備忘錄\n"
     "FROM: CPO M. Kade, UNSC Training Command (Reach)\n"
     "TO: Records\n"
     "DATE: 2540\n\n"
     "寫給最終真的會讀這份檔案、而不只是蓋章存檔的人——\n\n"
     "我是 Chief Mendez 在 Reach 的訓練幹部之一，不是負責整個計畫的人——\n"
     "那從頭到尾都是他的計畫。我自己負責的只是 SPINDLE 名單裡一小群，\n"
     "不是整個梯隊。我帶到的這些，是我親自從頭訓練到底的。有些人我看著\n"
     "他們沒能撐過強化手術。剩下的人，我看著他們變成這個物種比自己承認\n"
     "的更需要的東西。\n\n"
     "我不知道這樣算不算對。我知道如果重來一次我還是會做同樣的事，我也\n"
     "知道這個念頭比星盟丟到我們身上的任何東西都更讓我害怕。留著這份檔案。\n"
     "不要讓它消失。以後應該要有人能問這個問題，就算我們現在回答不了。\n\n"
     "還有一件事，反正這是要進封存檔案、不是要給人審閱的報告。我還是會\n"
     "想起 07-B。Skopje 來的，我帶過最凶的六歲小孩，第二年就是整個梯隊\n"
     "反應最快的。官方紀錄上那一筆寫的是醫療除役。我在強化艙親眼看到的\n"
     "不是那樣，我當時就站在旁邊。那份紀錄不是我寫的。我不知道是誰寫的，\n"
     "也不知道為什麼。\n\n"
     "- M. Kade, CPO"),

    (105, "醫療證明紀錄片段 - 2517 年結案",
     "//機密 - ONI SECTION III - 限閱//\n"
     "醫療證明紀錄（片段）\n"
     "RE: 替代協議下開立的死亡證明，2517 年批次\n\n"
     "  案件編號          當地簽署醫師                  ONI 檔案審核\n"
     "  OCPA-R4-11902    Dr. H. Idowu（Eridanus II）      M. Castel\n"
     "  OCPA-R4-11944    Dr. A. Petrides（Madrigal）      M. Castel\n"
     "  OCPA-R4-11887    Dr. T. Marlow（Skopje）          M. Castel\n"
     "  OCPA-R4-10733    Dr. H. Idowu（Eridanus II）      R. Achebe\n\n"
     "當地簽署醫師完全無法接觸徵召計畫的資料，依設計把每一筆都當成一般\n"
     "案件結案。僅存此片段 - 其餘紀錄在 SPINDLE 遷移過程中遺失。"),

    (106, "低溫恢復轉移授權書 - 07-B 對象",
     "//機密 - ONI SECTION III - 限閱//\n"
     "轉移授權書（醫療）\n"
     "RE: 強化後恢復轉移，對象 07-B\n"
     "DATE: 2525（強化週期）\n\n"
     "對象 07-B 獲授權轉入長期低溫恢復艙，等候重新評估。存檔的強化艙報告\n"
     "記載對象於轉移當時臨床上判定「無法存活」；恢復小組選擇直接進入懸置\n"
     "程序，未記錄正式的現場判定結果。\n\n"
     "本授權書不取代或修改任何既有案件結案紀錄，依標準醫療程序另行存檔，\n"
     "適用於懸置待評估案例。\n\n"
     "本檔案庫未能找到任何後續重新評估紀錄。"),
]

UI = {
    "login_title": "CAIRN Records Terminal",
    "classbar": "機密 // ONI SECTION III // 限閱",
    "login_seal_h1": "CAIRN RECORDS TERMINAL",
    "login_warning": "僅限保留處置權限存取 -- 未經授權存取即違反 UNSC 軍事法典第 12 條",
    "placeholder_user": "帳號",
    "placeholder_pass": "密碼",
    "access_button": "存取",
    "dashboard_title": "CAIRN Dashboard",
    "dashboard_h1": "保留處置 -- 紀錄索引",
    "terminal_status": "終端機狀態",
    "status_hostname": "主機名稱：",
    "status_user": "使用者：",
    "status_role": "角色：staging mirror（SPINDLE 遷移後留下，轉移未完成）",
    "status_decommission": "除役狀態：已排定，尚未完成",
    "back_to_index": "&laquo; 返回索引",
    "record_not_found": "查無此紀錄 / 超出範圍。",
    "access_denied": "存取遭拒",
    "back_link": "返回",
    "photo_on_file": "存檔人員照片",
}
