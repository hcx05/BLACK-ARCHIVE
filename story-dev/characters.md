---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 人物表

## 玩家
獨立駭客／數位調查者。無代號固定名稱（由玩家自行想像），故事中以「你」稱呼。

## 委託人 — 代號 LONGSHORE
- 一開始只用加密通訊代號 LONGSHORE 聯絡玩家，語氣簡短、謹慎。
- 只提供一批兒童紀錄與一句話任務：「Find out what happened to them.」
- **真實身分（後期揭露，不強制玩家發現，可留在 story-dev 供未來內容使用）**：Naomi Okafor，殖民地記錄職員，Eli Okafor 的母親。她從未真正相信兒子是病死。
- 目前 repo 的技術內容（frontier/relay/archive）尚未直接置入 LONGSHORE 的訊息文本——這屬於 Phase 5 之後可以擴充的「委託對話」層，目前先確保環境內部證據自洽。

## Tobias Reyes（T.R.）— 系統管理員
- 維護 ROSTER（frontier）與 LEDGER（relay）的 sysadmin。
- 已在 frontier 的 support tickets（`welcome.txt` / `todo.txt`）留下痕跡：知道資料有異常但被要求別再問。
- 知道的資訊量：中等。知道系統層面的異常（重複的 transfer reference、SPINDLE 這個名字），但不知道 SPINDLE/SPARTAN-II 的完整意義。

## Dr. Miriam Castel — UNSC 醫療官
- 出現在 archive 的 CAIRN record 102（Flash-Clone Substitution Protocol — Medical Annex）。
- 曾親手簽署至少三份 flash-clone 死亡證明，簽署當時不完全理解用途。
- 態度：不是主謀，事後有悔意但沒有否認自己的責任（"I am not going to pretend I didn't have a choice."）。

## Cmdr. I. Petrov — ONI Section III 官員
- 在 relay 的 `system_migration_log` 表與 archive 的 CAIRN record 101（Disposition Order 2547-014）出現。
- 負責 SPINDLE 系統退役後的資料處置授權，決定「保留但列為限閱」而非銷毀。
- 態度：程序性、謹慎，代表 ONI 對這段歷史「不销毁但不公開」的官方立場。

## CPO M. Kade — 訓練教官（Mendez 類比角色，原創姓名）
- 出現在 archive 的 CAIRN record 104（Internal Memo）。
- 親自訓練過 SPINDLE 名單上的多數候選人，親眼見過死亡與存活。
- 態度：矛盾但不逃避——「I don't know if that makes it right. I know I'd do it again.」

## Dr. Catherine Halsey（canon 角色，克制引用）
- 只以一段書信片段出現（archive CAIRN record 103），不作為可互動角色、不寫她的完整心理描寫。
- 內容克制且道德複雜：承認代價，堅持必要性，不寫成反派台詞。

## Dr. R. Achebe — UNSC 醫療官（僅文件署名，不展開角色）
- 只出現在 archive CAIRN record 105（Medical Certification Log Fragment）的一行署名：Samuel Voight（case_ref OCPA-R4-10733）的死亡證明是他/她簽的，不是 Dr. Castel。
- 存在目的：讓玩家發現「Castel 說她簽了三份，但案件明明有四份」的落差有一個具體、可查證的解答——不只 Castel 一個人涉入，這件事牽涉的醫療人員比她的自白信讓人以為的更多。
- 不需要展開背景故事，維持「一個名字」的份量即可，避免人物數量膨脹。

## 候選人／失蹤兒童（案件核心）
| 姓名 | 殖民地 | LEDGER 狀態 | 官方紀錄結果 | 有爭議的第二來源 |
|---|---|---|---|---|
| Eli Okafor | Eridanus II | Case Closed - Deceased | Augmentation failure, deceased | 無爭議 |
| Talia Wren | Madrigal | Case Closed - Deceased | Augmentation successful, active service | 無爭議 |
| Dominic Farrow | Skopje | Case Closed - Deceased | 官方 casualty log：discharged, permanent disability | CPO Kade 備忘錄（CAIRN record 104）暗示他其實死於 augmentation，官方紀錄被動過手腳——**兩份來源互相矛盾，遊戲不解答哪個對**，玩家要自己判斷 |
| Samuel Voight | Eridanus II | （僅在 relay DB 背景資料出現，無 API record）Closed - Deceased | Augmentation successful, active service | 無爭議，但死亡證明簽署人是 Dr. Achebe 而非 Castel（見上） |
| Priya Anand | Eridanus II | Active（對照組，證明不是所有案件都異常） | 未涉入計畫 | 純粹作為「不是每筆資料都有問題」的對照 |

Farrow 案是目前唯一一個刻意設計成「兩份可信來源互相矛盾、遊戲不裁決真假」的節點，對應作品核心要求「有些 evidence 可以…看似矛盾…玩家應該會建立 hypothesis，再用 hacking 去驗證」。線索鏈：archive backups share 的 `training_roster_fragment.txt`（只給訓練代號 07-A~07-D + 殖民地 + 年齡，不給姓名）→ CPO Kade 備忘錄提到「07-B」的親眼見聞 → 玩家要自己用殖民地（Skopje 只有 Farrow 一筆）交叉比對回真實姓名，才能發現這條反駁官方紀錄的線索——不是單純字串比對，是要跨兩份文件做身分還原。

人物總數：LONGSHORE、T. Reyes、Dr. Castel、Cmdr. Petrov、CPO Kade、Dr. Achebe + Halsey（克制引用）= 6 個原創 + 1 個 canon 引用，仍在作品要求「5–7 個有名字角色」範圍內。
