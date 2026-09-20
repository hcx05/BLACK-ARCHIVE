---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — 人物表

## 玩家
獨立駭客／數位調查者。無代號固定名稱（由玩家自行想像），故事中以「你」稱呼。

## 委託人 — 代號 LONGSHORE
- 一開始只用加密通訊代號 LONGSHORE 聯絡玩家，語氣簡短、謹慎（開場委託信現在只存在於線上 artifact，不是本機檔案，見 README）。
- 提供三個名字（Eli Okafor / Talia Wren / Dominic Farrow），並明確要求玩家查出「誰授權了轉移、原始紀錄送去哪裡、為什麼 Farrow 案在死後三十年被重新開啟」，收尾一句「I don't need a theory. I need the record that made them change his file.」——**只有三個名字，不是四個**：她自己也沒查到 Samuel Voight，這是刻意的（見下方「為什麼是現在」）。
- **真實身分（後期揭露，不強制玩家發現）**：Naomi Okafor，殖民地 records clerk，Eli Okafor 的母親。她從未真正相信兒子是病死。
- **為什麼是現在**（解決「等了將近 40 年才找 hacker」這個動機漏洞）：Naomi 不是在 Eli 消失 38 年後突然心血來潮。約 2547 年 SPINDLE 系統退役／資料遷移時，她因為工作關係接觸到 Eli 的舊 case 被重新索引，意外看到一個不該存在的 `transfer_ref`。她沒有權限進入限閱系統，只能用自己的 records 職權，花了約 8 年時間安靜地用同樣的 pattern 交叉搜尋，才陸續找到 Wren、Farrow 的案例（沒找到 Voight——她的搜尋管道本來就有限）。2555 年她終於累積到足夠信心，透過 LONGSHORE 這個代號找上玩家。真正的觸發點是**系統遷移意外讓一個不該存在的痕跡露出來**，不是單純的母親直覺。
- 身分線索現在確實存在於環境內：relay `system_migration_log` 有一筆由「N. Okafor, Colonial Records Clerk」處理 2547 批次重新索引的紀錄；archive backups share 有一份列出「Naomi Okafor」為 Eli 監護人全名的通知記錄殘檔。兩者都用行政語氣寫成，不強調、不加粗、不特別標示——細心玩家自己把姓氏跟職務連起來就能推出身分，遊戲不會直接講。

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
- **root-only 文件的真正作者**：`cairn_disposition_review.txt` 現在是他對 07-B（Farrow）個案的私人揭露——SPINDLE 除役檔案檢查把 07-B 的低溫懸置單位列入審查清單時，他在正式審查觸發前私自改寫保管狀態、跳過審查，並在文件裡承認自己沒有這個授權。這是他個人道德立場（「我沒有資格決定」）第一次不再是抽象的行政哲學，而是一個具體、他自己承認越權的個人行為——也是整個遊戲的最終答案。

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

## 候選人／失蹤兒童（案件核心，四人在 2517 徵召時皆約 6 歲，貼近 canon 設定）
| 姓名 | 殖民地 | LEDGER 狀態 | 官方紀錄結果 | 其他來源 |
|---|---|---|---|---|
| Eli Okafor | Eridanus II | Case Closed - Deceased | Augmentation failure, deceased | 無爭議 |
| Talia Wren | Madrigal | Case Closed - Deceased | Augmentation successful, active service | 無爭議 |
| Dominic Farrow | Skopje | Case Closed - Deceased | 官方 casualty log：discharged, permanent disability | 三份來源互相牴觸，**遊戲永遠不解答哪個對**：(1) CPO Kade 備忘錄（CAIRN 104）聲稱親眼看到他死於 augmentation；(2) CAIRN 106「07-B 低溫恢復艙轉移授權」記載他被判定臨床無法存活、轉入懸置、之後無追蹤紀錄 |
| Samuel Voight | Eridanus II | （僅在 relay DB 背景資料出現，無 API record）Closed - Deceased | Augmentation successful, active service | 無爭議，但死亡證明簽署人是 Dr. Achebe 而非 Castel（見上） |
| Priya Anand | Eridanus II | Active（對照組，證明不是所有案件都異常） | 未涉入計畫 | 純粹作為「不是每筆資料都有問題」的對照 |

Farrow 案是目前唯一一個刻意設計成「多份可信來源互相矛盾、遊戲不裁決真假」的節點，對應作品核心要求「有些 evidence 可以…看似矛盾…玩家應該會建立 hypothesis，再用 hacking 去驗證」。線索鏈：archive backups share 的 `training_roster_fragment.txt`（只給訓練代號 07-A~07-D + 殖民地 + 年齡，不給姓名）→ CPO Kade 備忘錄提到「07-B」的親眼見聞 → 玩家要自己用殖民地（Skopje 只有 Farrow 一筆）交叉比對回真實姓名，才能發現這條反駁官方紀錄的線索；找到 CAIRN record 106 後，矛盾從「兩份資料一真一假」升級成「三份都不完整、可能都對也可能都不對」的真正 forensic ambiguity——不是單純字串比對，是要跨三份文件做身分還原與判斷。

## CAIRN 的定位（世界觀 immersion 修正）
CAIRN 不是「現役 ONI 最高機密資料中心」，而是 **2547 SPINDLE decommission 時留下的 staging mirror／recovery node**——正式資料應該全部轉移到別處、這個節點應該被除役，但除役排程沒有真的執行完。CAIRN record 101（Disposition Order）與 admin panel 的 Terminal Status 都已經明講這件事。這個設定解釋了為什麼同一台「機密檔案庫」會同時存在 guest SMB、明文憑證、SQLi、無 session check、Redis 無認證：玩家攻破的不是「ONI 資安爛得像學校電腦教室」，而是「ONI 四十年前留下的一具數位屍體，沒有人真的清乾淨」。

人物總數：LONGSHORE、T. Reyes、Dr. Castel、Cmdr. Petrov、CPO Kade、Dr. Achebe + Halsey（克制引用）= 6 個原創 + 1 個 canon 引用，仍在作品要求「5–7 個有名字角色」範圍內。
