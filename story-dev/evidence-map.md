---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 證據地圖

依照作品核心要求 §證據設計原則，每份證據至少滿足一項功能。以下對照目前已寫入環境的證據檔案：

| 位置 | 證據 | 功能 |
|---|---|---|
| frontier `notes/welcome.txt` | T.R. onboarding note | 建立人物（T. Reyes）、首次出現「SPINDLE」代號、暗示 LEDGER 需要特定憑證 |
| frontier `notes/todo.txt` | T.R. 待辦清單 | 暗示異常案件被系統性地忽略／壓下（"probably nothing... probably a batch import artifact"）——建立第一層懷疑 |
| frontier `notes/credential_rotation_status.txt`（不在導覽列，只能靠 `/notes/` 目錄列出或 LFI 猜到） | T.R. 帳號稽核記錄，**內含「不小心貼上」的原始 provisioning script**（`useradd`/`chpasswd` 指令，含四組明文密碼） | **合法、非暴力破解**取得 `sysadmin/admin123` 等四組密碼的唯一正式管道。原本這份文件只寫「NOT rotated」卻沒給任何密碼值，玩家其實還是得用猜的——已修正為「T.R. 不小心把舊 provisioning script 貼進工單」的框架，讓密碼以貼近真實世界（shell history/貼錯內容）的方式洩漏，而不是乾淨表格 |
| frontier webmail Inbox #1 | LEDGER access note | 紅鯡魚帳密（svc-relay），但正確指出目標主機，訓練玩家「不是每個線索都直接可用」 |
| frontier webmail Inbox #2 | Sandbox DB migration note | 與 relay DB 的 root 密碼互相驗證（多來源交叉確認同一組密碼） |
| frontier webmail Inbox #3 | 新人上工信 | 定調「異常紀錄是正常的」官方說法，建立後續反差 |
| relay API `/api/cases/:id` (IDOR) | 候選人案件記錄（含 transfer_ref 異常） | 證明先前假設（死亡紀錄有問題）成立；引入「候選人」概念 |
| relay API record id 5 | LEDGER-CAIRN sync 服務帳號 | 首次讓玩家知道存在 CAIRN，但不直接說「archive」；這筆記錄現在會在 `/etc/ledger/sync.conf`（見下）得到真正的憑證印證，而不是自己就直接給密碼 |
| relay `dependent_case_index` 表 | 背景案件資料 | 提供更多同模式案例（Samuel Voight），強化「這不是單一個案」 |
| relay `service_accounts` 表 | CAIRN Fileshare（密碼重用印證）+ Redis + relay 自身備份帳號 + 印表機死線索 | lateral movement 的一部分，但**不再是「SELECT * 拿到下一關全部鑰匙」**——CAIRN Records Terminal 的帳密已經移出這張表，改成要在 relay 檔案系統找 `/etc/ledger/sync.conf` 才能拿到（見下方 bug 修正） |
| relay `/etc/ledger/sync.conf`（檔案系統，非 DB） | `ledger-cairn-sync` 服務的真實設定檔，內含 CAIRN Records Terminal 的帳密 | 把「下一關鑰匙」從一次乾淨的 SQL SELECT 改成「environment relationship → 找 config 檔 → 才發現憑證」，更貼近真實 pentest 的 credential discovery，也呼應 API record id 5 已經先告訴玩家這個 sync 服務存在 |
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
| archive CAIRN record 106（新增） | Cryogenic Recovery Transfer Authorization - Subject 07-B | Farrow 矛盾的**第三個來源**：官方 casualty log 說「殘障除役」、Kade 說「我看他死了」、這份 2525 年的轉移授權說「臨床無法存活、轉入低溫懸置、之後無追蹤紀錄」——三份都不完整也互相牴觸，遊戲永遠不解答，讓矛盾從「兩份資料一真一假」升級成真正的 forensic ambiguity |
| archive Samba `backups/training_roster_fragment.txt` | 訓練代號對照表（只有代號+殖民地+年齡，沒有姓名） | 逼玩家做真正的跨文件身分還原（代號 → 殖民地/年齡 → 交叉比對 relay 的 case index → 還原成真名），而不是單純複製貼上同一個字串；年齡已修正為 6-7 歲區間（貼近 canon「約六歲」設定） |
| archive `/root/cairn_disposition_review.txt`（root only，已改名+**大幅改寫**，見下方 bug 修正） | 最終處置決定書（Petrov 親筆） | **不再重講整個陰謀**，只回答「ONI 為什麼沒有銷毀這批資料」——這是 root 之後唯一新增的資訊，acquisition/flash-clone/augmentation 結果玩家此時應該已經從其他文件自己拼出來了 |
| relay `system_migration_log` 新增一列（2540 稽核回應） | Records Compliance Office 的官方結案回應 | **主動推理節點**：玩家已經從 API IDOR 親眼看過 transfer_ref 異常，這裡卻是官方「查過了，沒問題，是批次匯入的假影」的正式結論——玩家要自己判斷這份官方紀錄是失職還是刻意淡化，遊戲不給答案 |
| frontier `?page=search`（改版） | 真正查得到資料的 Dependent Status Index（4 筆真實記錄 + 對應照片欄位圖片） | 修正「網站內容只是為了塞漏洞存在」的問題：查 LONGSHORE 信裡給的名字會回傳真的案件卡（含 case_ref，供之後跨系統比對），查不到的名字（如 Voight）也會誠實回「查無資料」，不再是萬用的假回應 |
| frontier / archive 圖片（`assets/*.png`、`acquisition_directive_scan.pdf`、`disposition_order_2547-014.pdf`） | 案件卡（照片欄位標示「IMAGE CORRUPTED」）、OCPA 徽記、掃描版徵召指令、Petrov 簽署的處置令掃描件 | 補上真實感缺口：舊系統的照片欄位損毀是合理的世界觀理由，避免需要生成兒童肖像這種不恰當的內容，同時掃描版文件讓「這是紙本舊紀錄」的設定更可信 |
| `briefing/00_longshore_contact.html` | LONGSHORE 開場委託信的正式版本 | 玩家實際會打開的檔案不再只是純文字 `.md`，而是一個風格化的「加密通訊擷取」靜態網頁（深色終端機美術風格，JetBrains Mono + Chakra Petch），跟 `.md` 內容一致但呈現更真實；`.md` 保留作為純文字備份。**先試過 PDF（Pillow 生圖轉 PDF），使用者覺得效果不好，改成純 HTML** —— 純靜態檔案不需要架任何伺服器，直接用瀏覽器開 `file://` 路徑即可，也另外發布了一份線上版本（Claude Artifact，預設 private）方便分享連結而不用自己維護站台。 |

**格式多樣性說明**：不是所有文件都改成 PDF/HTML——保留 `.txt` 的地方（`legacy_service_credentials.txt`、`casualty_log_partial.txt`、`training_roster_fragment.txt`、frontier notes、CAIRN admin panel 內文）都是因為那些情境下純文字本身就更真實（內部日誌、備份殘留、支援工單、web app 動態內容），只有「正式簽署的官方文件」轉成 PDF、「玩家會實際打開閱讀的委託信」轉成風格化網頁，避免為了多樣性而多樣性。

## 網站真實感翻修（讓一般人看不出來這是靶機）
使用者的標準：「一般人根本看不出來是靶機的網站」。原本 frontier 的設計雖然有 UNSC 風格外皮，但骨子裡還是「一個頁面對應一個漏洞」的典型靶機結構，首頁只有兩句話 + `php_uname()`，webmail 是單欄純列表。修改內容：
- **frontier 首頁改成真的 dashboard**：案件統計數字（active/closed/pending，純假數據，非安全相關）、System Notices 公告板（重用已建立的世界觀細節：SPINDLE 清理公告、停水通知）、Quick Links。拿掉了 `php_uname()` 這種一眼就會被辨識成「測試機」的資訊洩漏。
- **加了 session/utility bar**（`SESSION: duty-terminal-04 · REGION 4` + 假的 last login 時間）、favicon（用 OCPA 徽記）、細微的網格紋理背景——這些是真實內部系統會有、但原本完全沒做的視覺細節。
- **webmail 從單欄列表改成真的信箱介面**：左側資料夾側邊欄（Inbox/Sent/Drafts/Trash，只有 Inbox 有內容）、寄件人姓名縮寫頭像、主旨/日期欄位對齊，信件補上日期並依時間排序。
- **修掉一個真的 encoding bug**：webmail 原本沒有在 `Content-Type` 宣告 `charset=utf-8`，導致內文的 em dash（—）在瀏覽器裡顯示成亂碼 `â€"`——這種亂碼本身就是「這是隨手寫的測試程式」的破綻，已修正所有 response header。
- 所有修改都用 headless Chromium 實際截圖驗證過畫面，不是憑空猜測 CSS 效果。
- **關於「上網找 Halo 素材」**：沒有採用，改用一直在用的方式（Pillow 生成原創圖片）。真人拍攝/遊戲擷取的 Halo 美術資源是 Microsoft/343 的著作權本體，跟本專案的原創同人散文性質不同，直接下載嵌入公開 repo 的風險明顯更高，所以維持「原創但風格致敬」的做法。

## 無關緊要的填充內容（增加真實感，不是線索）
刻意加了幾筆跟案件完全無關的雜訊，讓「找線索」不是無腦把每個檔案都當成有意義的提示：
- frontier webmail 多兩封信：Building 4 停水通知、二樓印表機缺碳粉的閒聊回覆。
- frontier `/notes/` 多一份 `parking_permit_renewal.txt`（停車證續約通知）——現在 `/notes/` autoindex 列出來的檔案不是每個都重要，玩家要自己判斷。
- archive Samba `public` share 多一份 `it_policy_reminder.txt`（IT 使用規範，制式公告）。
- relay `service_accounts` 多一筆「Floor Print Server」，`printsvc.internal` 這個主機名稱根本不會 resolve/回應——一個看起來像線索、實際上是死路的憑證，訓練玩家不要每組帳密都無條件深挖。

## 目前刻意留白／可在後續內容擴充
- Priya Anand（對照組案例）目前只在 relay API + frontier search 出現，尚無對應 archive 端資料——刻意保留「不是每筆資料都異常」的訊號，不需要額外揭露。

## 已修正的攻擊鏈 bug（依 OSCP/CPTS/eJPT 方法論覆盤時發現）
- **LONGSHORE 開場委託信**已補上：`briefing/00_longshore_contact.md`，玩家介面層，比對三個案例（Eli Okafor / Talia Wren / Dominic Farrow）作為唯一初始線索，不劇透、不給登入資訊。
- **frontier 的 LFI 讀不到任何 notes 檔案**：`index.php` 的 `$filepath` 寫死 `/var/www/html/notes/`，但 nginx `root` 實際指到 `/var/www/html/portal/`，兩者對不起來，導致 welcome.txt / todo.txt 從一開始就是死路。已修正為 `/var/www/html/portal/notes/`。
- **archive confidential share 的密碼永遠對不起來**：relay DB 洩漏的 CAIRN Fileshare 帳密是 `smbadmin/Cairn#Records24`，但 smb.conf 的 `confidential` share 限定 `valid users = sysadmin`，且 Samba 只幫 `sysadmin` 設過完全不同的密碼——玩家不可能用洩漏的憑證登入，等於 `acquisition_directive_excerpt.txt`（SPARTAN-II 名稱正式出現的地方）永久拿不到。已改成密碼重用同一套（`sysadmin/admin123`，跟 SSH/webmail 共用），同時更貼合「同一批人到處重複用密碼」這個核心主題。
- **webmail/SSH 憑證重用路徑原本沒有合法發現管道**：玩家要嘗試 `sysadmin/admin123` 登入 webmail、進而重用到 relay SSH，原本沒有任何線索指向這組帳密，等於逼玩家 brute force。已透過上面的 `credential_rotation_status.txt` + `/notes/` autoindex 補上合法發現路徑。
- **relay 的 MariaDB 從來沒有真正初始化過（嚴重）**：`run-mariadb.sh` 用 `/var/lib/mysql/mysql` 是否存在來判斷「要不要跑 init.sql」，但 `mariadb-server` 這個 apt 套件在 image build 階段的 postinst 就已經自己建好這個目錄了——導致每次 container 啟動都判斷成「已經初始化過」，直接跳過 `init.sql`，`ledger` 資料庫（`dependent_case_index`／`service_accounts`／`system_migration_log`，也就是通往 CAIRN 的憑證洩漏跟稽核矛盾紀錄）從來沒有真的建立過。這是在幫 relay 補測試時才發現的，之前所有「relay 資料庫驗證過」的說法都只驗證到 Node API 的記憶體資料，沒碰到真正的 DB。已改成檢查 `/var/lib/mysql/ledger`（我們自己的資料庫）而不是系統的 `mysql` 目錄，重建後確認四張表都正確建立、資料筆數正確。
- **檔名 `disposition_summary_final.txt` 直接寫著「final」**，違反「檔名不要暗示這是最終答案」的要求，已改名為 `cairn_disposition_review.txt`（跟其他 CAIRN 文件的命名風格一致），Dockerfile 與所有 story-dev 引用都同步更新。

## 第二輪外部 review 修正（劇情/世界觀一致性，非攻擊鏈 bug）
使用者拿了另一個 AI 對全部劇情文件 + 實際 lab 內容做的逐項 review，以下是採納並修正的項目：

- **root 檔案的數學錯誤（真 bug）**：`cairn_disposition_review.txt` 原本寫「兩死一殘兩現役」，但候選人一共只有四個（Okafor/Wren/Farrow/Voight），那是五個 outcome，多算了一個。已整個重寫這份文件，不再重述 outcome 統計（也不再重述整個陰謀），只回答「Petrov 為什麼決定保留而不銷毀」。真正的四人結果只存在 `casualty_log_partial.txt`（1死/2現役/1爭議），本來就沒有算錯，錯的只有 root 文件自己重新統計時的敘述。
- **root 文件本身變成 `THE_TRUTH.txt`（設計原則牴觸）**：原本逐項列出 Origin/Concealment/Outcome/Program continuation/Disposition，等於幫玩家把全部劇情總結一遍，跟「玩家應該自己拼線索」的核心原則衝突。已縮成只回答一個問題：ONI 為什麼沒銷毀這批資料。
- **遊戲年份定死為 2555**：原本只寫「2550 年代中後期」。根據 canon，星盟戰爭 2552 年結束、UNSC 2553 年進入戰後；SPARTAN-II 起源要到 2558 年《Hunt the Truth》才首次被公眾挖出。定在 2558 之前（2555）能確保玩家挖到的東西仍然是「還沒被任何人證實過」的真正秘密，不會變成「駭進去發現新聞早就報過的事」。`故事劇情`、`timeline.md`、`truth-map.md` 已同步更新。
- **候選人年齡跟 canon 有落差**：Canon 是 75 名「約六歲」兒童在 2517 年被徵召。原本 Dominic Farrow（2517 年時 7 歲）、Samuel Voight（8 歲）偏離區間；Voight 尤其明顯。已改成全員 6-7 歲（Okafor/Wren/Farrow 6 歲，Voight 7 歲，保留一點年齡差異以維持 training roster 的次要身分還原機制），同步修正 `relay/sql/init.sql`、`relay/app/api/server.js`、`frontier/index.php`、`training_roster_fragment.txt`，並重新生成 Farrow 的案件卡圖片（DOB 欄位）。也把 augmentation 階段明確定在 **2525 年**（約 14 歲，貼近 canon），寫進 `timeline.md`/`truth-map.md` 與 `casualty_log_partial.txt`/CAIRN record 106 的標題。
- **`credential_rotation_status.txt` 沒有真的給密碼（真 bug）**：文件原本只寫「NOT rotated」，沒有任何密碼值，玩家其實還是得用猜的，違反「不要讓 brute force 成為主要 progression」。已改成 T.R. 「不小心把舊 provisioning script 貼進工單」的框架，內容是實際的 `useradd`/`chpasswd` 指令（跟 `lab/base/Dockerfile` 的真實內容一致），密碼以貼近真實世界的方式（誤貼、shell 歷史紀錄）洩漏，不是一張乾淨的帳密表。
- **`welcome.txt` 的 sandbox 憑證其實能打正式資料庫（真 bug）**：`app_svc/S3cretDB!2024` 被說成「sandbox copy only」，但 `init.sql` 原本的 `GRANT ALL PRIVILEGES ON *.*` 讓它其實對 `ledger`（正式資料庫）有完整權限，玩家看完 `welcome.txt` 可以直接跳過大半 Act I/II 設計。已新增真正獨立的 `ledger_sandbox` 資料庫（只有兩筆無意義的 demo 資料），`app_svc` 的 GRANT 改成只能碰 `ledger_sandbox.*`，`welcome.txt` 的說法現在是真的。`root` 帳號的 `*.*` 權限維持不變（那是 webmail Inbox #2 洩漏的 Act II 正式管道，本來就該是真的能打正式庫）。
- **CAIRN 的資安爛得不像 ONI Section III 最高機密系統**：guest SMB、明文憑證、SQLi、無 session check、Redis 無認證全部疊在同一台「TOP SECRET」系統上，會讓人覺得「ONI 資安比電腦教室還爛」。不減漏洞，改身分：CAIRN 現在明確定位成「2547 SPINDLE decommission 時的 staging mirror／recovery node，正式除役排程沒有真的執行完」——CAIRN record 101（Disposition Order）與 admin panel dashboard 的 Terminal Status 都已經明講這件事。所有誤設變成「四十年前一具沒清乾淨的數位屍體」的合理殘留，而不是現役最高機密資料中心的荒謬弱點。
- **LONGSHORE = Naomi Okafor 缺一個「為什麼是現在」**：原本的設定是「不相信兒子病死的母親，38 年後突然找上駭客」，動機薄弱。已改成：Naomi 是殖民地 records clerk，2547 年 SPINDLE 退役／資料遷移時，因工作接觸意外看到 Eli 的舊 case 被重新索引、帶有不該存在的 transfer_ref；她沒有系統存取權限，只能用自己的職權花約 8 年時間安靜交叉搜尋同樣的 pattern，找到 Wren、Farrow（沒找到 Voight，這也是她一開始只給玩家三個名字的原因）。2555 年她終於累積夠了才聯絡玩家。觸發點是系統遷移意外露出痕跡，不是單純的母親直覺，時間差也從「38 年」縮小成「發現異常後又謹慎查證了 8 年」，合理很多。
- **`service_accounts` 表太像「下一關鑰匙箱」**：原本 CAIRN Fileshare 跟 CAIRN Records Terminal 的帳密都乾淨地放在同一張 DB 表裡，玩家 `SELECT *` 就一次拿到全部。CAIRN Fileshare 那筆本身只是「跟已知密碼重用」的印證，保留；CAIRN Records Terminal 的帳密已經移出 DB，改成要在 relay 檔案系統找到 `/etc/ledger/sync.conf`（ledger-cairn-sync 服務的真實設定檔，呼應 API record id 5 早就提過這個服務存在）才能拿到——從「SELECT * FROM next_level_passwords」變成「environment relationship → 找 config 檔 → credential discovery」。
- **Farrow 矛盾追加第三個來源**：原本只有官方 casualty log vs. Kade 備忘錄兩份互相矛盾的來源。新增 CAIRN record 106「07-B 低溫恢復艙轉移授權」，記載他被判定臨床無法存活、轉入懸置、之後無追蹤紀錄——三份來源都不完整，讓矛盾從「一真一假」升級成真正的 forensic ambiguity，永遠不解答。
