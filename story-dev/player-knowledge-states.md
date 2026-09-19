---
不進玩家發行版。內部開發參考文件。
---

# BLACK ARCHIVE — Player Knowledge States

用來檢查「玩家在拿到某份證據之後，應該知道什麼、還不應該知道什麼」，避免某個 host 過早劇透。

## 開場（拿到 LONGSHORE 的委託後）
知道：一批兒童紀錄、官方顯示已死亡、委託人懷疑造假。
不知道：SPINDLE / LEDGER / CAIRN 這些名字、ONI、SPARTAN-II、Halsey。

## FRONTIER 攻破後
新增知道：
- Support ticket 提到「SPINDLE」是一個舊系統名稱，多筆案件在遷移時出現異常。
- 有一個內部系統叫 LEDGER，可能保存更完整的紀錄。
- 一組可能有效的憑證（webmail `sysadmin/admin123`，實際上是密碼重用，不是信裡寫的那組）。
仍不知道：候選人／transfer reference 的意義、ONI、SPARTAN-II。

## RELAY 攻破後
新增知道：
- 「已結案死亡」的案件带有不該存在的 transfer reference（SPINDLE-7-xxxx）。
- 這些孩子在系統內被稱為某種「candidate」，且與一般案件分開處理。
- 存在一個叫 CAIRN 的更高機密系統，以及一次由 ONI Section III（Cmdr. Petrov）授權的資料遷移/限閱決定。
- CAIRN 的服務憑證。
仍不知道：SPARTAN-II 這個名稱本身、flash-clone 機制細節、候選人的最終命運、Halsey 的角色。

## ARCHIVE 攻破後（SQLi / Samba 取得，未 root）
新增知道：
- SPARTAN-II 正式名稱與 2517 徵召指令的動機（殖民地叛亂風險，不是為了星盟）。
- flash-clone 死亡掩蓋機制，以及 Dr. Castel 的直接涉入。
- Halsey 與 Section III 之間的書信片段（道德複雜性）。
- CPO Kade 的訓練者視角與情感矛盾。
- 部分候選人的 augmentation 結果（backups share 的傷亡紀錄）。
仍不知道：官方最終處置決定的完整脈絡與明確的「保留但不公開」授權文字（Disposition Order 已知，但尚未有把所有線串起來的單一文件）。

## ARCHIVE root 之後（讀到 disposition_summary_final.txt）
新增知道：完整事件脈絡——起源、掩蓋手法、訓練與 augmentation 結果、程序性授權決定，以及案件最終停在「保留但等待未來處置」。
玩家此時應該能自己回答「這些孩子發生了什麼」，並面對主題問句，而不是被文件直接告知結論。
