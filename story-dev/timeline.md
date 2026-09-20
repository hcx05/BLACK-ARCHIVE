---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 時間線

遊戲「現在」的年份**定死為 2555 年**（星盟戰爭主要戰事 2552 年結束，UNSC 2553 年起進入戰後時期；SPARTAN-II 真正起源要到 2558 年《Hunt the Truth》才首次被公眾挖出——遊戲設定在那之前，玩家挖出的東西仍然是真正意義上「還沒被任何人證實過」的秘密，不要不小心把故事日期挪到 2558 之後）。

- **2510–2511**：Eli Okafor、Talia Wren、Dominic Farrow、Samuel Voight 出生於不同殖民地（Eridanus II / Madrigal / Skopje）。四人在 2517 年徵召時都是 **6 歲左右**（貼近 canon「75 名約六歲兒童」的設定，不要讓任何一個候選人的年齡明顯偏離這個區間）。
- **2516**：Section III 完成殖民地叛亂風險推估（archive 文件提及 "2516 revision"）。
- **2517**：正式 Candidate Acquisition Directive 發出，SPARTAN-II 作為暫定計畫代號首次出現（archive `acquisition_directive_excerpt.txt`）。同年 Halsey 與 Section III 的書信往來（CAIRN record 103）。候選人被帶走，flash-clone 死亡證明陸續簽發（Dr. Castel 涉入，CAIRN record 102；至少一份由 Dr. R. Achebe 簽署，見 record 105）。
- **2517 之後（訓練期）**：CPO Kade 於 Reach 訓練候選人（CAIRN record 104 回顧視角）。
- **2525：augmentation 階段**（候選人約 14 歲，貼近 canon 時間點）。Eli Okafor augmentation 失敗死亡；Talia Wren、Samuel Voight augmentation 成功並進入現役；Dominic Farrow 的結果**有爭議**——官方 casualty log 記為「augmentation 失敗、永久殘障、除役」，但 Kade 的備忘錄聲稱他親眼看到 Farrow 死亡，另外還有一份 2525 年的「07-B 低溫恢復艙轉移授權」（CAIRN record 106）記載他當時被判定「臨床上無法存活」而轉入低溫懸置、後續無追蹤記錄。三份來源互相不完全一致，遊戲**刻意不解答**哪一份才是真的。
- **人類—星盟戰爭**：2552 年主要戰事結束，2553 年起 UNSC 進入戰後重建期。SPARTAN 公開成為英雄象徵，但起源仍列機密。
- **約 2547（SPINDLE 退役／migration 前後）**：LONGSHORE（真實身分 Naomi Okafor，殖民地 records clerk）在協助處理 SPINDLE 系統退役的資料遷移作業時，意外看到 Eli 的舊 case 被重新索引，且帶有一個不應存在的 `transfer_ref`。她沒有辦法直接存取限閱系統，但利用自己的 records 工作權限，花了數年時間安靜地用同樣的 pattern 交叉搜尋，才逐步找到 Wren、Farrow 的案例（Voight 的案例她並未查到，這也是為什麼 LONGSHORE 一開始只給玩家三個名字，不是四個）。
- **2547-02-11**：SPINDLE 系統正式退役，案件資料遷移至 LEDGER（一般案件）與 CAIRN（機密/歷史資料，此節點實際上是待轉移的 staging mirror，正式除役排程後來沒有真的執行完），Cmdr. Petrov 授權 Disposition Order 2547-014（relay `system_migration_log` / archive CAIRN record 101）。
- **2547-02-11（同一天）**：SPINDLE 除役的標準檔案檢查把 07-B（Farrow）的低溫懸置單位列入「繼續保管或最終處置」審查清單。Cmdr. Petrov 在正式審查觸發前，私自把該案的保管狀態改成「繼續、無需處理」，跳過審查——這是玩家在 Act I/II 看到的 Farrow transfer_ref 異常「在 2547 年被重新處理過」的真正原因，也是 root 文件揭露的具體事件（見 `truth-map.md` 第 9 點）。這個動作本身沒有任何正式授權文書（root 文件明講「no authorization attached」），但 CAIRN 的系統存取紀錄剛好留下一筆技術性的 audit trail（`cairn_access_log_extract.txt`：`i.petrov CUSTODY_STATUS_SET 07-B`）——這不是一份正式決策紀錄，只是系統照樣記錄了「誰、什麼時候、動了哪個保管狀態欄位」，沒有解釋原因。同一天，records clerk N. Okafor（真實身分 Naomi Okafor，Eli 的母親）在處理同一批 migration 的 Eridanus II／Madrigal 案件重新索引時，意外看到 Eli 的舊 case 也帶有類似的異常 transfer_ref。
- **2547-02-14**：內部提醒禁止將 SPINDLE transfer reference 與現行 dependent status 交叉比對（relay migration log 第三筆）。
- **2555（現在／玩家行動時間點）**：Naomi 花了約 8 年謹慎累積出三個案例、確認系統性 pattern 後，終於透過 LONGSHORE 這個代號聯絡玩家，提供這批看似普通的兒童死亡紀錄，聲稱其中至少幾筆是假的。她沒有提到自己是誰、也沒有提到 Eli 是她兒子。

## 玩家實際會遇到的順序（技術面，非強制線性，但架構上大致如此）
1. FRONTIER：發現 Dependent Status Index 有異常、Support Tickets 提到 SPINDLE 這個名字、webmail 洩漏可能通往 RELAY 的線索（含一個過期/錯誤的帳密紅鯡魚，真正可行路徑是密碼重用：webmail `sysadmin/admin123` 同時是 RELAY 的 SSH 密碼）。
2. RELAY：透過 SSH 或 API exploit 進入，發現 case index 裡「已結案死亡」卻帶有 transfer reference 的紀錄，找到通往 CAIRN 的 sync service 設定檔與 migration log（第一次出現 ONI Section III / Cmdr. Petrov 名字，以及一則跟玩家自己發現互相矛盾的官方稽核結論）。
3. ARCHIVE：透過 relay 洩漏的憑證 pivot 進入，SQLi 或合法密碼取得 records terminal 存取權，讀到 Halsey 書信片段、Medical Annex、Kade 備忘錄、醫療簽署紀錄、低溫轉移授權；Samba share 洩漏 acquisition directive（**SPARTAN-II 首次正式出現，重大世界觀 reveal，但不是最終答案**）與遺留在 backups share 的 casualty log、訓練名冊；root privesc 後讀到的最終文件回答 LONGSHORE 真正委託的具體問題——**誰在 2547 年重新碰過 Farrow 的案件、為什麼**——而不是重述整個 acquisition/掩蓋陰謀，玩家此時應該已經自己從其他文件拼出那部分了。
