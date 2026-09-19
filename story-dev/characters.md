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

## 候選人／失蹤兒童（案件核心）
| 姓名 | 殖民地 | LEDGER 狀態 | 真實結果（archive 揭露） |
|---|---|---|---|
| Eli Okafor | Eridanus II | Case Closed - Deceased | Augmentation failure, deceased |
| Talia Wren | Madrigal | Case Closed - Deceased | Augmentation successful, active service |
| Dominic Farrow | Skopje | Case Closed - Deceased | Augmentation failure, discharged, permanent disability |
| Samuel Voight | Eridanus II | （僅在 relay DB 背景資料出現，無 API record）Closed - Deceased | Augmentation successful, active service |
| Priya Anand | Eridanus II | Active（對照組，證明不是所有案件都異常） | 未涉入計畫，純粹作為「不是每筆資料都有問題」的對照 |

人物總數：LONGSHORE、T. Reyes、Dr. Castel、Cmdr. Petrov、CPO Kade + Halsey（克制引用）= 5 個原創 + 1 個 canon 引用，符合作品要求「5–7 個有名字角色」。
