---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 證據地圖

依照作品核心要求 §證據設計原則，每份證據至少滿足一項功能。以下對照目前已寫入環境的證據檔案：

| 位置 | 證據 | 功能 |
|---|---|---|
| frontier `notes/welcome.txt` | T.R. onboarding note | 建立人物（T. Reyes）、首次出現「SPINDLE」代號、暗示 LEDGER 需要特定憑證 |
| frontier `notes/todo.txt` | T.R. 待辦清單 | 暗示異常案件被系統性地忽略／壓下（"probably nothing... probably a batch import artifact"）——建立第一層懷疑 |
| frontier `notes/credential_rotation_status.txt`（不在導覽列，只能靠 `/notes/` 目錄列出或 LFI 猜到） | T.R. 帳號稽核記錄 | **合法、非暴力破解**取得 `sysadmin/admin123` 的唯一正式管道——沒有這份文件，玩家只能硬猜或 brute force 才能拿到 relay SSH 與 archive SMB 用的密碼，違反「不要讓 brute force 成為主要 progression」的要求，故補上此檔並在 nginx 開 `/notes/` autoindex |
| frontier webmail Inbox #1 | LEDGER access note | 紅鯡魚帳密（svc-relay），但正確指出目標主機，訓練玩家「不是每個線索都直接可用」 |
| frontier webmail Inbox #2 | Sandbox DB migration note | 與 relay DB 的 root 密碼互相驗證（多來源交叉確認同一組密碼） |
| frontier webmail Inbox #3 | 新人上工信 | 定調「異常紀錄是正常的」官方說法，建立後續反差 |
| relay API `/api/cases/:id` (IDOR) | 候選人案件記錄（含 transfer_ref 異常） | 證明先前假設（死亡紀錄有問題）成立；引入「候選人」概念 |
| relay API record id 5 | LEDGER-CAIRN sync 服務帳號 | 首次讓玩家知道存在 CAIRN，但不直接說「archive」 |
| relay `dependent_case_index` 表 | 背景案件資料 | 提供更多同模式案例（Samuel Voight），強化「這不是單一個案」 |
| relay `service_accounts` 表 | CAIRN 憑證 + relay 自身備份帳號 | 主要 lateral movement 入口 |
| relay `system_migration_log` 表 | SPINDLE 退役紀錄 | 第一次點名 ONI Section III / Cmdr. Petrov，把「資料異常」升級成「classified operation」 |
| archive Samba `public/welcome.txt` | CAIRN 使用須知 | 建立場景真實感，非關鍵 |
| archive Samba `confidential/legacy_service_credentials.txt` | 舊帳密清單 | 對照 base 帳號，強化「憑證重複使用」主題 |
| archive Samba `confidential/acquisition_directive_excerpt.txt` | 2517 徵召指令 | **SPARTAN-II 名稱正式出現**；揭露原始動機（殖民地叛亂風險，非星盟） |
| archive Samba `backups/casualty_log_partial.txt` | augmentation 傷亡紀錄（意外留在 backups） | 連結案件姓名與真實結果（部分死亡/部分成為現役 Spartan）；示範「不安全備份習慣」 |
| archive CAIRN record 101 (admin panel) | Disposition Order 2547-014 | 解釋 LEDGER/CAIRN 分層的官方理由；确认 Petrov 的角色 |
| archive CAIRN record 102 | Medical Annex（Dr. Castel） | 解釋 flash-clone 掩蓋機制；直接連結四個 case_ref |
| archive CAIRN record 103 | Halsey 書信片段 | 呈現道德複雜性，非反派台詞 |
| archive CAIRN record 104 | CPO Kade 備忘錄 | 人性視角：訓練者本人的矛盾情感；**追加段落引入「07-B」訓練代號**，需要玩家自己跟 backups share 的訓練名冊交叉比對才能還原成 Dominic Farrow，並發現他跟官方 casualty log 的紀錄互相矛盾 |
| archive CAIRN record 105 | Medical Certification Log Fragment | **主動推理節點**：解答「Castel 說簽了三份，但案件有四份」的落差——第四份是 Dr. Achebe 簽的，證明涉入的醫療人員不只 Castel 一人 |
| archive Samba `backups/training_roster_fragment.txt` | 訓練代號對照表（只有代號+殖民地+年齡，沒有姓名） | 逼玩家做真正的跨文件身分還原（代號 → 殖民地/年齡 → 交叉比對 relay 的 case index → 還原成真名），而不是單純複製貼上同一個字串 |
| archive `/root/cairn_disposition_review.txt`（root only，已改名，見下方 bug 修正） | 最終整合摘要 | 把 acquisition → flash-clone → augmentation → ONI 授權 → 現狀處置串成完整事件，並提出核心主題問句 |
| relay `system_migration_log` 新增一列（2540 稽核回應） | Records Compliance Office 的官方結案回應 | **主動推理節點**：玩家已經從 API IDOR 親眼看過 transfer_ref 異常，這裡卻是官方「查過了，沒問題，是批次匯入的假影」的正式結論——玩家要自己判斷這份官方紀錄是失職還是刻意淡化，遊戲不給答案 |
| frontier `?page=search`（改版） | 真正查得到資料的 Dependent Status Index（4 筆真實記錄 + 對應照片欄位圖片） | 修正「網站內容只是為了塞漏洞存在」的問題：查 LONGSHORE 信裡給的名字會回傳真的案件卡（含 case_ref，供之後跨系統比對），查不到的名字（如 Voight）也會誠實回「查無資料」，不再是萬用的假回應 |
| frontier / archive 圖片（`assets/*.png`、`acquisition_directive_scan.jpg`） | 案件卡（照片欄位標示「IMAGE CORRUPTED」）、OCPA 徽記、掃描版徵召指令 | 補上真實感缺口：舊系統的照片欄位損毀是合理的世界觀理由，避免需要生成兒童肖像這種不恰當的內容，同時掃描版文件讓「這是紙本舊紀錄」的設定更可信 |

## 目前刻意留白／可在後續內容擴充
- Priya Anand（對照組案例）目前只在 relay API + frontier search 出現，尚無對應 archive 端資料——刻意保留「不是每筆資料都異常」的訊號，不需要額外揭露。

## 已修正的攻擊鏈 bug（依 OSCP/CPTS/eJPT 方法論覆盤時發現）
- **LONGSHORE 開場委託信**已補上：`briefing/00_longshore_contact.md`，玩家介面層，比對三個案例（Eli Okafor / Talia Wren / Dominic Farrow）作為唯一初始線索，不劇透、不給登入資訊。
- **frontier 的 LFI 讀不到任何 notes 檔案**：`index.php` 的 `$filepath` 寫死 `/var/www/html/notes/`，但 nginx `root` 實際指到 `/var/www/html/portal/`，兩者對不起來，導致 welcome.txt / todo.txt 從一開始就是死路。已修正為 `/var/www/html/portal/notes/`。
- **archive confidential share 的密碼永遠對不起來**：relay DB 洩漏的 CAIRN Fileshare 帳密是 `smbadmin/Cairn#Records24`，但 smb.conf 的 `confidential` share 限定 `valid users = sysadmin`，且 Samba 只幫 `sysadmin` 設過完全不同的密碼——玩家不可能用洩漏的憑證登入，等於 `acquisition_directive_excerpt.txt`（SPARTAN-II 名稱正式出現的地方）永久拿不到。已改成密碼重用同一套（`sysadmin/admin123`，跟 SSH/webmail 共用），同時更貼合「同一批人到處重複用密碼」這個核心主題。
- **webmail/SSH 憑證重用路徑原本沒有合法發現管道**：玩家要嘗試 `sysadmin/admin123` 登入 webmail、進而重用到 relay SSH，原本沒有任何線索指向這組帳密，等於逼玩家 brute force。已透過上面的 `credential_rotation_status.txt` + `/notes/` autoindex 補上合法發現路徑。
- **relay 的 MariaDB 從來沒有真正初始化過（嚴重）**：`run-mariadb.sh` 用 `/var/lib/mysql/mysql` 是否存在來判斷「要不要跑 init.sql」，但 `mariadb-server` 這個 apt 套件在 image build 階段的 postinst 就已經自己建好這個目錄了——導致每次 container 啟動都判斷成「已經初始化過」，直接跳過 `init.sql`，`ledger` 資料庫（`dependent_case_index`／`service_accounts`／`system_migration_log`，也就是通往 CAIRN 的憑證洩漏跟稽核矛盾紀錄）從來沒有真的建立過。這是在幫 relay 補測試時才發現的，之前所有「relay 資料庫驗證過」的說法都只驗證到 Node API 的記憶體資料，沒碰到真正的 DB。已改成檢查 `/var/lib/mysql/ledger`（我們自己的資料庫）而不是系統的 `mysql` 目錄，重建後確認四張表都正確建立、資料筆數正確。
- **檔名 `disposition_summary_final.txt` 直接寫著「final」**，違反「檔名不要暗示這是最終答案」的要求，已改名為 `cairn_disposition_review.txt`（跟其他 CAIRN 文件的命名風格一致），Dockerfile 與所有 story-dev 引用都同步更新。
