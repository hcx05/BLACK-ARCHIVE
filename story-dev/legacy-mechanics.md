---
不進玩家發行版。內部開發參考文件。
---

# Legacy Mechanics Freeze — 原 VulnCastle 7-Host Attack Chain

> 目的：在 reskin 之前，把原本 7-host 版本「能動的東西」完整記錄下來，作為之後三個新 host 不可打破的技術基準。所有 credential / port / dependency 都必須在新架構裡找到對應位置，即使敘事外衣換掉。

## 完整攻擊鏈（原始版本）

1. **Recon (DMZ)**：nmap 掃到 `web-01:80`、`mail-01:8025`、`vpn-gw-01:22(2222)`。
2. **web-01 — 初始突破點（三選一都可）**
   - `?page=ping` → OS command injection（`shell_exec("ping -c 3 ".$host)`）→ RCE as www-data。
   - `?page=upload` → unrestricted upload（無型別檢查/無 rename）→ 上傳 webshell → RCE as www-data。
   - `?page=notes&file=` → LFI/path traversal → 讀取 `notes/welcome.txt`，內含 `db_user/S3cretDB!2024`（dev DB 憑證，非 root，僅示範用途，实际主要 lateral movement 靠 mail-01/db 洩漏）。
   - `?page=search&q=` → reflected XSS（僅示範用，非主線 progression）。
   - www-data 權限下：`/opt/backup.sh`（world-writable，root cron `*/5` 執行）→ 竄改腳本 → root privesc。另有 `sysadmin ALL=(ALL) NOPASSWD: /usr/bin/find` sudo misconfig 作為第二條 privesc 路徑（需先有 sysadmin shell，例如透過 SSH 憑證取得）。
3. **mail-01 — 憑證/情報來源**
   - `/debug` 洩漏環境變數：`SMTP_USER=admin / SMTP_PASS=MailP@ss2024 / SECRET_KEY=...`。
   - Webmail 帳密（弱到可猜或列在別處）：`admin/MailP@ss2024`、`sysadmin/admin123`、`devuser/devuser2024`。
   - Inbox 三封信是主要 credential 洩漏來源：
     - "VPN Credentials" → `vpnuser / Vpn$ecure99`，目標 `vpn-gw-01.internal`（**這是打到 pivot host 的關鍵信**）。
     - "DB Migration" → `root / S3cretDB!2024`，目標 `db-01.internal`。
     - "New Employee Onboarding" → 通用弱密碼 `Welcome2024!`（次要，非主線）。
   - `devuser ALL=(ALL) NOPASSWD: /usr/bin/python3` sudo misconfig（mail-01 專屬 privesc）。
4. **vpn-gw-01 — Pivot Point（dual-homed: DMZ 172.20.1.12 + Internal 10.10.0.12）**
   - SSH 用上一步取得的 `sysadmin/admin123`（base image 預設帳密）或 webmail 洩漏的 `vpnuser/Vpn$ecure99`（原始碼裡此帳號其實未真正建立在 base image — 是情報陷阱/紅鯡魚，實際登入仍靠 base 帳密 sysadmin/admin123, devuser/devuser2024, backup/backup, deploy/deploy!）。
   - `~/.ssh` 權限 777（可植入 authorized_keys 做持久化，非必要路徑）。
   - `sysadmin ALL=(ALL) NOPASSWD: /usr/bin/socat` + SUID `/usr/local/bin/python3-suid` → root privesc。
   - socat 已安裝 → 用於建立 internal network 的 port forward / SOCKS pivot，讓攻擊者從 Kali 觸及 10.10.0.0/24。
5. **Internal Network（僅能透過 vpn-gw-01 pivot 到達，10.10.0.0/24 標記 `internal: true`，無 host port 映射）**
   - **app-01 (10.10.0.13:3000)**：
     - `/api/users/:id` IDOR → 任意 user id 洩漏 PII（含 service account #4 的 `api_key` 與 `internal_notes: "Has access to db-01 and file-01"`）。
     - `/api/fetch?url=` SSRF → 可探測 internal 服務（例如打 `admin-01:6379` 或 `db-01:3306` 探測開放狀態）。
     - `/api/diagnostics` command injection（`nslookup ${target}`）→ RCE。
     - `/api/files?name=` path traversal → 讀 `/opt/api/data/readme.txt`（洩漏 `admin-01:6379 無認證` + `file-01 guest access`）。
     - `/api/health` 洩漏 internal_services 對照表（db-01/file-01/admin-01 主機名稱與 port）。
   - **db-01 (10.10.0.14:3306, MariaDB)**：
     - `root / S3cretDB!2024`（遠端可登入，`root@%`）、`app_user / S3cretDB!2024`。
     - `customers` 表：PII/信用卡/SSN（次要，flavor data，非主線關鍵）。
     - `service_accounts` 表：**核心 lateral movement 資料** → Samba (`smbadmin/FileShare#2024`)、Redis（無認證備註）、Backup SSH (`backup/backup`，對應 vpn-gw-01)、Admin Panel (`administrator/Admin!Panel99`，對應 admin-01)。
   - **file-01 (10.10.0.15:445, Samba)**：
     - `public` share：guest 可讀寫。`confidential` share：宣稱需認證但 `create mask 0644` 導致世界可讀；內含 `passwords.txt`（sysadmin/devuser/backup/deploy 明文密碼，等同 base image 帳密清單，可與 SSH 對照驗證）、`id_rsa_deploy`（假私鑰，flavor）、`budget_q4.txt`（flavor）。`backups` share guest 可寫（可用於植入 payload 若有排程讀取，目前無排程消費此目錄，是留白 hook）。
     - `server min protocol = NT1`（SMBv1 可用，next-CVE hook，未指定具體 CVE，僅作為 misconfig flavor）。
   - **admin-01 (10.10.0.16:8080 admin panel, 6379 Redis)**：
     - SQL Injection（f-string 拼接）→ `' OR '1'='1` 類 payload 繞過登入 → `/dashboard`。
     - `/dashboard` 直接洩漏 DB root 密碼 `S3cretDB!2024`、Redis/Samba/API 位置（等同 db-01.service_accounts 的重複來源，用於「多來源互相驗證」設計）。
     - Redis 無認證（6379）→ 可用 SSRF（app-01 `/api/fetch`）或直連（pivot 後）操作，作為次要 flavor（原版無關鍵資料存在 Redis 內，僅示範 misconfig）。
     - Writable cron `/opt/healthcheck.sh`（777，root `* * * * *` 執行）→ root privesc（第三條 privesc 路徑，internal 網段版本）。

## 必須保留到新架構的依賴關係表

| 原始依賴 | 新架構對應 | 備註 |
|---|---|---|
| mail-01 inbox → vpn-gw-01 SSH 憑證 | frontier webmail inbox → relay SSH 憑證 | 核心 pivot 觸發信，敘事外衣換掉即可 |
| web-01 notes → dev DB 憑證 | frontier notes → relay MariaDB 憑證（次要） | 保留但降低權重，主線走 relay 內部發現 |
| vpn-gw-01 dual-homed + socat | relay dual-homed + socat（container 內建） | relay 必須同時在 dmz + internal 兩個 docker network |
| app-01 IDOR/SSRF/CMDi/health | relay 內 API process（同 container，port 不變 3000） | 邏輯 1:1 搬移 |
| db-01 service_accounts → Samba/Redis/backup SSH/admin panel 密碼 | relay 內 MariaDB（同 container） → 密碼指向 archive 內服務 | 表結構/欄位保留，內容 reskin |
| admin-01 SQLi → dashboard 洩漏 DB root 密碼 | archive 內 admin panel（SQLite 邏輯不變，資料庫內容擴充成案件證據） | SQLi payload 手法不變 |
| file-01 confidential share 明文密碼檔 | archive 內 Samba share（同 container） | 對應 base 帳密清單，換成劇情用帳密 |
| admin-01 writable cron / vpn-gw-01 SUID+sudo / web-01 writable cron+sudo find / mail-01 sudo python3 | 三個新 host 各保留至少一條 privesc 路徑 | frontier 保留 web-01 兩條（cron+sudo find）；relay 保留 vpn-gw-01 兩條（SUID+sudo socat）；archive 保留 admin-01 一條（writable cron） |

## 三個新 host 各自「必須可達」的驗收基準

- **frontier**：未認證即可從 host machine 打到（command injection / upload / LFI 三選一皆可取得 shell），並能從 frontier 取得指向 relay 的憑證。
- **relay**：需要 frontier 取得的憑證才能 SSH 登入（或透過 frontier 上傳的手法直接取得 shell 後再橫向到 relay，兩條路徑都保留彈性）；relay 對外只開 SSH，API/DB 只在 container 內部（不對 host machine 開 port）；relay 必須能建立到 internal network 的 pivot（socat 或 SSH dynamic forward）。
- **archive**：只能從 relay 所在的 internal network 存取（不映射任何 host port），需要 relay 內 MariaDB 洩漏的憑證或路徑資訊才能定位；archive 的 SQLi + writable cron 兩條路徑都保留。
