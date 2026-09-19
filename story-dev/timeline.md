---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 時間線

- **2509–2512**：Eli Okafor、Talia Wren、Dominic Farrow、Samuel Voight 等候選人出生於不同殖民地（Eridanus II / Madrigal / Skopje）。
- **2516**：Section III 完成殖民地叛亂風險推估（archive 文件提及 "2516 revision"）。
- **2517**：正式 Candidate Acquisition Directive 發出，SPARTAN-II 作為暫定計畫代號首次出現（archive `acquisition_directive_excerpt.txt`）。同年 Halsey 與 Section III 的書信往來（CAIRN record 103）。候選人被帶走，flash-clone 死亡證明陸續簽發（Dr. Castel 涉入，CAIRN record 102）。
- **2517 之後（訓練期）**：CPO Kade 於 Reach 訓練候選人（CAIRN record 104 回顧視角）。
- **後續（augmentation 階段，年代未明確標註，留給正式內容再定）**：Eli Okafor、Dominic Farrow augmentation 失敗；Talia Wren、Samuel Voight augmentation 成功並進入現役。
- **人類—星盟戰爭爆發與結束**（依主線世界觀設定於 2550 年代中後期）：SPARTAN 成為公開英雄象徵，但起源仍列機密。
- **2547-02-11**：SPINDLE 系統正式退役，案件資料遷移至 LEDGER（一般案件）與 CAIRN（機密/歷史資料），Cmdr. Petrov 授權 Disposition Order 2547-014（relay `system_migration_log` / archive CAIRN record 101）。
- **2547-02-14**：內部提醒禁止將 SPINDLE transfer reference 與現行 dependent status 交叉比對（relay migration log 第三筆）。
- **現在（玩家行動時間點）**：LONGSHORE 聯絡玩家，提供一批看似普通的兒童死亡紀錄，聲稱其中至少幾筆是假的。

## 玩家實際會遇到的順序（技術面，非強制線性，但架構上大致如此）
1. FRONTIER：發現 Dependent Status Index 有異常、Support Tickets 提到 SPINDLE 這個名字、webmail 洩漏可能通往 RELAY 的線索（含一個過期/錯誤的帳密紅鯡魚，真正可行路徑是密碼重用：webmail `sysadmin/admin123` 同時是 RELAY 的 SSH 密碼）。
2. RELAY：透過 SSH 或 API exploit 進入，發現 case index 裡「已結案死亡」卻帶有 transfer reference 的紀錄，DB 洩漏 CAIRN 的服務憑證與 migration log（第一次出現 ONI Section III / Cmdr. Petrov 名字）。
3. ARCHIVE：透過 relay 洩漏的憑證 pivot 進入，SQLi 取得 records terminal 存取權，讀到 Halsey 書信片段、Medical Annex、Kade 備忘錄；Samba share 洩漏 acquisition directive（SPARTAN-II 首次正式出現）與遺留在 backups share 的 casualty log；root privesc 後讀到最終 `cairn_disposition_review.txt`，把所有線串起來。
