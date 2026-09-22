# BLACK ARCHIVE — VulnCastle 改造計畫

> 開發用文件。包含劇情與關卡設計 spoiler。  
> 目標：將原本 VulnCastle 的 7-host 多主機靶場，重構為更接近單一 HTB Box 規模的 3-host Halo 同人 cyber-investigation scenario。
>
> 不在本文件中撰寫具體 exploit code，也不要求改變原本漏洞機制本身；優先保留可玩的 offensive progression，再把其重新包裝成調查敘事。

---

## 1. 專案定位

專案暫名：

**BLACK ARCHIVE — A Halo Cyber Investigation**

世界觀定位：

- 非官方 Halo fan project
- 時間背景位於人類－星盟戰爭結束後不久
- SPARTAN 已經是公眾熟知的英雄象徵
- SPARTAN-II 的真正起源、兒童徵召、flash-clone 掩蓋、早期 ONI 文件仍屬高度機密
- 玩家是民間獨立駭客／數位調查者
- 玩家一開始不知道案件與 SPARTAN-II 有關
- 最初委託只是驗證一批看似已經死亡的兒童紀錄是否造假
- 故事逐步從「失蹤兒童資料異常」轉化為「UNSC / ONI 黑色計畫調查」

核心體驗：

> 玩家不是來打 flag。  
> 玩家是因為想知道這些孩子發生了什麼，所以不得不侵入越來越深的系統。

---

# 2. 規模控制

## 原版問題

原版 VulnCastle 有 7 個 host：

### DMZ
- web-01
- mail-01
- vpn-gw-01

### Internal
- app-01
- db-01
- file-01
- admin-01

這個規模對完整企業靶場合理，但對本專案來說偏大。

本專案希望：

- 總遊玩時間接近 HTB Easy / 偏長 Easy
- 不讓玩家產生「要打一整個企業網路」的疲勞
- 主線不要分散到太多機器
- 每一次 compromise 都必須有明顯劇情意義
- 玩家最多只需要真正掌握 3 個 host

因此重構為：

# **3-host architecture**

---

# 3. 新架構總覽

```text
                     PLAYER / KALI
                          |
                          v
              ┌─────────────────────┐
              │ HOST 1              │
              │ FRONTIER            │
              │ Public / DMZ Node   │
              └──────────┬──────────┘
                         |
                         | progression
                         v
              ┌─────────────────────┐
              │ HOST 2              │
              │ RELAY               │
              │ Internal Access Hub │
              │ Dual-Homed          │
              └──────────┬──────────┘
                         |
                         | internal-only access
                         v
              ┌─────────────────────┐
              │ HOST 3              │
              │ ARCHIVE             │
              │ Restricted Records  │
              └─────────────────────┘
```

三台主機不是三個獨立 CTF box。

應該讓玩家感覺：

> 我只是一直往同一個 UNSC 系統更深處走。

---

# 4. 7 Hosts → 3 Hosts 合併方案

## HOST 1 — FRONTIER

### 來源
合併：

- `web-01`
- `mail-01`
- 部分 `app-01`

### 定位

一台公開可達的 UNSC Medical / Personnel Support Node。

玩家最初會把它理解為：

- 醫療後勤
- 人員紀錄
- 基礎研究行政
- 舊殖民地資料查詢
- 一般軍方公開或半公開入口

它不能一開始看起來像 ONI 黑站。

### 承擔內容

原本 web-01 的主要 Web attack surface 保留。

mail-01 不再獨立為一台主機。

mail / message / ticket 類內容改成：

- Webmail 子系統
- archived correspondence
- support tickets
- personnel notification system
- medical transfer notes

全部放在 FRONTIER 裡。

原本 app-01 的部分功能，如果只是簡單 Web/API 型功能，也可移入 FRONTIER，避免第二台主機功能過度分散。

### 故事功能

FRONTIER 的任務是讓玩家產生：

> 「這些兒童紀錄真的有問題。」

玩家在這一層得到的資訊不能證明完整陰謀。

只能建立：

- 死亡紀錄彼此存在共通模式
- 某些人員號碼或 transfer references 不合理
- 一些舊資料被後來修改
- 某個已退役的系統名稱重複出現
- 少量檔案指向一個玩家尚未理解的內部代號

### 敘事目標

第一階段不出現：

- SPARTAN-II
- John-117
- Halsey 的完整角色
- 明確 kidnapping 描述
- flash clone 完整說明

玩家只能知道：

**官方故事有問題。**

---

# 5. HOST 2 — RELAY

### 來源
合併：

- `vpn-gw-01`
- `app-01` 剩餘部分
- `db-01`

### 定位

一個舊式 UNSC internal operations / relay node。

此 host 是整個遊戲的中段。

它同時負責：

- 內外網橋接
- 舊系統 routing
- internal API
- service database
- internal authentication / service accounts
- legacy operational records

### 網路角色

RELAY 必須 dual-homed：

```text
DMZ / Public-side network
        |
      RELAY
        |
Internal restricted network
```

ARCHIVE 只能從 RELAY 所在的 internal network 存取。

玩家不能從自己的 Kali 直接碰到 ARCHIVE。

這保留 VulnCastle 最有價值的：

**pivot / network discovery**

但不需要保留 4 台 internal hosts。

### 故事功能

RELAY 是玩家第一次真正意識到：

> 這件事比資料造假嚴重得多。

這一層可以逐步讓玩家確認：

- 兒童被系統性地挑選
- 不同殖民地的案例其實屬於同一個 classified pipeline
- 所謂「死亡」與後續 military records 有重疊
- 有一批資料被刻意從一般醫療系統移往封閉網段
- 一些研究 / 訓練 / transfer 記錄存在非正常分類
- ONI / Section III 的存在開始出現，但不應一次把所有答案丟出來

### DB 整合

原本 `db-01` 不需要再做成一台玩家需要獨立 compromise 的 host。

資料庫作為 RELAY 的 backend service 即可。

它可以承載：

- candidate indexes
- old medical records
- personnel aliases
- transfer records
- project references
- internal service credentials
- system migration history

玩家可以需要取得 DB 裡的重要資訊，但不需要感覺自己又「打了一台 db box」。

---

# 6. HOST 3 — ARCHIVE

### 來源
合併：

- `file-01`
- `admin-01`
- 原 `db-01` 中最機密的資料層

### 定位

ARCHIVE 是高度受限的 classified records node。

它不是普通「最終主機」。

它代表：

**被刻意留下但從正式紀錄中消失的歷史。**

可以設定為：

- ONI legacy archive
- decommissioned Section III records repository
- protected legal / medical / operational archive
- 黑色預算計畫退役資料庫

### 服務內容

不需要每種服務都有一台主機。

可以在 ARCHIVE 上同時存在：

- internal admin interface
- file shares
- protected archives
- logs
- backups
- classified correspondence
- historical records

### 故事功能

ARCHIVE 才開始完整接近 SPARTAN-II 真相。

在這裡可以出現：

- SPARTAN-II designation
- candidate program
- abduction / acquisition terminology
- flash-clone substitution
- training records
- augmentation records
- early casualty / failure records
- ONI authorization
- Halsey 的相關文件或通訊
- 後續資料清理與 narrative management

但仍然不能只放一份：

`THE_TRUTH.txt`

然後全部講完。

玩家應該從數份不同來源拼出完整事件。

---

# 7. 哪些原 Host 刪除

以下 host 不再獨立存在：

## mail-01
### 處理方式
刪除為獨立 host。

其內容整合進 FRONTIER：

- webmail
- archived messages
- support tickets
- notification queue
- personnel correspondence

理由：

郵件是故事載體，不值得單獨增加一個 compromise cycle。

---

## db-01
### 處理方式
刪除為獨立 host。

資料庫服務整合進 RELAY。

最機密歷史資料可以另外在 ARCHIVE 以 archive database / dump / records 的形式存在。

理由：

玩家不需要為「有一台 MariaDB」再打完整一台機器。

---

## file-01
### 處理方式
刪除為獨立 host。

檔案服務整合進 ARCHIVE。

理由：

SMB / file-share 可以保留作為 service，但不是一台獨立劇情節點。

---

## app-01
### 處理方式
拆分。

- 公開 / 半公開 application 功能 → FRONTIER
- internal application / service API → RELAY

理由：

避免多一台純粹為了 API 而存在的 host。

---

# 8. 保留 / 重新命名 Host 對照

| 原 VulnCastle | 新架構 |
|---|---|
| web-01 | FRONTIER |
| mail-01 | 併入 FRONTIER |
| vpn-gw-01 | RELAY |
| app-01 | 拆分到 FRONTIER / RELAY |
| db-01 | 併入 RELAY |
| file-01 | 併入 ARCHIVE |
| admin-01 | ARCHIVE |

---

# 9. 網路拓撲

## Network A — External / DMZ

玩家可直接存取：

- FRONTIER

> **後續修正**：原計畫這裡寫的是「RELAY 的極少數必要入口」，實際後來覺得連這個極少數入口（RELAY 的 SSH）都不該對外開——一開始的 `nmap -p- TARGET` 就會同時看到 FRONTIER 跟 RELAY，破壞「先攻破 DMZ 才發現內部還有一台」的真實感。最終定案：**RELAY 完全不對外開任何 port**，跟 ARCHIVE 一致，玩家必須先在 FRONTIER 拿到執行權限、升級成真正的互動式 shell，才能從 container 內部 pivot 進 RELAY。細節見 `story-dev/attack_chain_design.md` §0、§3.1，`Answer/evidence-map.md` 第十輪。

---

## Network B — Restricted Internal

只有：

- RELAY
- ARCHIVE

ARCHIVE 不 publish port 到 host machine。

ARCHIVE 只能：

- 由 RELAY
- 或透過玩家建立的 tunnel / pivot

進入。

---

# 10. 玩家感受到的三階段結構

## ACT I — The Dead Children

主機：
**FRONTIER**

問題：

> 為什麼這些來自不同殖民地的孩子，死亡紀錄有同樣的異常？

氣氛：

- mundane
- bureaucratic
- old military infrastructure
- initially boring
- gradually unsettling

玩家開始時不應感覺自己已經碰到巨大陰謀。

---

## ACT II — The Missing Records

主機：
**RELAY**

玩家開始知道：

> 這些紀錄不是單純造假，而是被刻意搬離普通系統。

故事從：

**data inconsistency**

升級成：

**classified operation**

玩家逐步意識到這些 children 被視為：

- candidates
- assets
- subjects

而不是病患。

這裡開始讓 Halo 玩家產生猜測。

但不要直接確認全部。

---

## ACT III — The Black Archive

主機：
**ARCHIVE**

ARCHIVE 是整個案件真正的核心。

玩家終於能把：

- childhood records
- UNSC medical data
- military transfer
- ONI records
- augmentation history
- personnel identities

連起來。

此時故事才正式揭示：

**玩家從一開始調查的，就是 SPARTAN-II 計畫留下來的歷史殘骸。**

---

# 11. 改編後劇情主體

## 開場

玩家是一個民間獨立駭客。

一名匿名委託者傳來數名兒童資料。

這些兒童：

- 出生於不同殖民地
- 家庭互不相關
- 官方紀錄顯示已死亡
- 死亡原因看似合理
- 時間集中在一個不尋常區段

委託人聲稱：

> 其中至少幾個孩子並沒有死。

並給出一個舊 UNSC Medical / Personnel 系統作為唯一線索。

---

# 12. 真正歷史背景

SPARTAN-II 計畫最初並非為了 Covenant。

其原始戰略背景是 UNSC 對日益惡化的殖民地叛亂與全面內戰風險的恐懼。

ONI Section III 與 Catherine Halsey 推動一個極度機密的計畫：

- 尋找具有特定遺傳與認知特質的兒童
- 將其帶離原家庭
- 用 flash clones 掩蓋失蹤
- 將真正的孩子送往秘密訓練設施
- 從童年開始軍事化
- 在青少年期接受高風險 augmentation
- 最終成為 SPARTAN-II

不少候選人在 augmentation 中：

- 死亡
- 永久殘障
- 無法繼續服役

成功者成為後來的人類英雄。

---

# 13. 主題

本專案不能把故事簡化成：

> ONI 壞  
> Halsey 壞  
> Spartans 是受害者  
> End

核心應該是矛盾。

SPARTAN-II 的產生方式是不可接受的。

但這些人後來又確實：

- 阻止災難
- 保護殖民地
- 對抗 Covenant
- 成為人類存續的重要力量

因此玩家最後面對的不只是：

**What happened?**

還有：

**Who gets to decide whether this history should remain buried?**

---

# 14. 人物配置原則

正式 implementation 時，建議只設：

- 1 名匿名委託人
- 1–2 名 ONI / UNSC 官員
- 1 名醫療 / 研究人員
- 1 名技術 / 系統人員
- 1–2 名與候選人歷史直接相關的人

總共約 5–7 名有名字的人物。

不要塞 20 個名字。

玩家應該能記住：

- 誰知道什麼
- 誰參與了什麼
- 誰在掩蓋什麼

---

# 15. 證據設計原則

每份重要資料至少應完成以下之一：

1. 證明先前假設錯誤
2. 建立人物關係
3. 連接兩個時間點
4. 證明某個官方紀錄遭修改
5. 證明某人其實不知道全部真相
6. 揭露一個新的 project layer
7. 解釋某個早期異常

避免：

- 「下一個密碼是 xxx」
- 「去 host X」
- 「下一步打 port Y」
- 明顯 CTF hint
- 文件只為提供下一個 exploit 而存在

---

# 16. Flag 改造

可以保留原本的 flag progression 機制，但玩家不看到 flag 格式。

所有：

```text
flag.txt
user.txt
root.txt
```

都重新包裝。

例如類型可改成：

- medical transfer memo
- archive index
- correspondence fragment
- subject roster
- approval order
- audit export
- deleted report
- classified directive

但 filename 本身不能過度劇透。

---

# 17. 最終證據設計

最後的最高權限內容不應是一句：

> SPARTAN-II kidnapped children.

這件事玩家到後段應該已經知道。

最終內容應該是：

**能讓玩家完成整個案件判斷的最後拼圖。**

它需要把前面分散的幾條線：

- candidate selection
- false death records
- flash clones
- military transfer
- training
- augmentation
- ONI authorization

真正關聯起來。

玩家取得最終資料後，應該有：

> 「原來前面那幾份看似互相矛盾的資料，其實是這樣連起來的。」

的感覺。

---

# 18. 難度目標

整體 hacking 難度：

**HTB Easy ～ 偏難 Easy**

不追求 Medium 的 obscure 技巧。

玩家如果卡住，理想原因應該是：

> 我還沒理解環境。

而不是：

> 我不知道作者腦中那個冷門 exploit。

---

# 19. Technical Progression 原則

本次重構不要重新發明整條 exploit chain。

優先策略：

1. 保留原 VulnCastle 中已經能工作的 exploit mechanics
2. 合併 host 時調整 dependency
3. 不主動修復 intentional vulnerabilities
4. 不增加 kernel / binary / reverse engineering
5. 不增加純 CTF puzzle
6. 不依靠 stego / Base64 / ROT / trivia
7. network pivot 保留
8. Linux privilege escalation 保留
9. credentials / auth abuse 保留
10. Web exploitation 保留

---

# 20. 目標遊玩時間

預期 blind play：

**約 2.5–4 小時**

熟練玩家：

**約 1.5–2.5 小時**

初次接觸 pivoting 的玩家可能更久。

不得膨脹成：

- 8 小時企業 lab
- 7 台 box marathon
- 每個 service 都要求單獨 compromise

---

# 21. 每 Host 的大概份量

## FRONTIER
約 35%

- recon
- web
- initial foothold
- 第一層調查

## RELAY
約 35%

- Linux
- credentials
- network discovery
- pivot
- 第二層調查

## ARCHIVE
約 30%

- internal service
- privilege escalation
- restricted evidence
- 最終調查

---

# 22. UI / 世界觀視覺

避免整個網站一眼就是 Halo fan page。

FRONTIER 應該像：

- boring UNSC government portal
- logistics dashboard
- medical support system
- outdated military intranet

而不是：

- 巨大 SPARTAN logo
- Master Chief hero banner
- ONI SECRET DATABASE

秘密感來自：

**資料本身。**

不是 CSS 寫「TOP SECRET」。

---

# 23. Canon 使用策略

使用 Halo canon 的核心元素：

- UNSC
- ONI / Section III
- SPARTAN-II
- Dr. Catherine Halsey
- Reach
- candidate selection
- flash clones
- military training
- augmentation
- MJOLNIR
- Insurrection-era origins
- Human-Covenant War 後的英雄化

但遊戲中的：

- 小人物
- IT 系統
- 支援部門
- archival nodes
- 個別文件
- 調查事件
- 匿名委託人

可以原創。

這樣玩家既能感受到 Halo，又不只是重新朗讀小說。

---

# 24. Repo 結構改造目標

最終不需要維持 7 個 lab directory。

概念上應重構成：

```text
lab/
├── base/
├── frontier/
├── relay/
└── archive/
```

開發用 story 資料可另外放：

```text
story-dev/
├── timeline.md
├── characters.md
├── evidence-map.md
├── truth-map.md
└── player-knowledge-states.md
```

`story-dev/` 不應被打包進玩家發行版本。

---

# 25. 開發順序

## Phase 1 — Freeze Original Mechanics
- 紀錄原本 7-host attack progression
- 列出所有必須保留的 credential / permission / network dependencies
- 不改任何 story

## Phase 2 — Collapse to 3 Hosts
- web + mail + public app → FRONTIER
- gateway + internal app + DB → RELAY
- file + admin + restricted data → ARCHIVE
- 確認 ARCHIVE 不能直接從 attacker network access

## Phase 3 — Functional Test
- 完整走一次原本 technical progression
- 確認三台 host 全部可被合理到達
- 確認 pivot 正常
- 確認 privesc 正常

## Phase 4 — Halo Reskin
- UNSC visual identity
- military naming
- internal terminology
- believable service data

## Phase 5 — Story Injection
- characters
- timeline
- messages
- records
- archives
- contradictory evidence

## Phase 6 — Replace Flags
- 每個原 flag 替換為 story evidence
- 移除 flag-like wording

## Phase 7 — Blind Playtest
測試者只能得到最初委託。

觀察：

- 是否知道下一步但不是因為明示提示
- 是否能理解故事
- 是否太容易提前猜到 SPARTAN-II
- 是否有某 host 感覺只是多餘
- 是否有證據只是 password delivery device

---

# 26. 最終成功標準

成功版本應做到：

### 技術
- 3 hosts
- Docker Compose 可一次啟動
- Kali 可正常進行
- 不需要 AD
- 不需要 Windows
- 不需要 kernel exploit
- 不需要 binary exploitation
- 保留 Web / Linux / credentials / internal services / pivot / privesc

### 規模
- 接近一台偏長的 HTB Easy
- 不像完整 enterprise range

### 故事
- 玩家開始不知道案件與 SPARTAN-II 有關
- 玩家自己從資料中建立假設
- Halo lore 是調查結果，不是 opening exposition
- root / highest privilege 只是取得最後證據的工具
- 最終目標是回答「這些孩子發生了什麼」

### 氛圍
玩家最後應該感覺：

> 我不是攻破了三台靶機。
>
> 我闖進了一段 UNSC 不希望任何人重新找到的歷史。
