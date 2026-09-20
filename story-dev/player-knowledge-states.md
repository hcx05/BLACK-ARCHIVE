# BLACK ARCHIVE — Player Knowledge States

> 不進玩家發行版。內部開發參考文件。

用來檢查「玩家在拿到某份證據之後，應該知道什麼、還不應該知道什麼」，避免某個 host 過早劇透。

實際的開場委託信現在只存在於線上 artifact（本機 `briefing/` 目錄已移除），內容是三個案例（Eli Okafor / Talia Wren / Dominic Farrow），加上明確的三個問題（誰授權轉移、原始紀錄去向、Farrow 案為何三十年後被重開）與收尾句「I don't need a theory. I need the record that made them change his file.」，不含任何登入資訊或下一步提示。遊戲現在時間點定死為 2555 年。

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
- CAIRN Fileshare 的憑證（密碼重用）；CAIRN Records Terminal 的憑證要另外在 relay 檔案系統的 `/etc/ledger/sync.conf` 才找得到，DB 裡不再直接給。
- relay 自己的官方稽核紀錄（2540 年）說這些異常「只是批次匯入的假影」——跟玩家自己看到的 transfer_ref 模式矛盾，玩家要自己判斷。
仍不知道：SPARTAN-II 這個名稱本身、flash-clone 機制細節、候選人的最終命運、Halsey 的角色、CAIRN 實際上是什麼樣的系統（現役還是廢棄）。

## ARCHIVE 攻破後（SQLi / Samba 取得，未 root）
新增知道：
- SPARTAN-II 正式名稱與 2517 徵召指令的動機（殖民地叛亂風險，不是為了星盟）。
- flash-clone 死亡掩蓋機制，Dr. Castel 的直接涉入，以及第四份證明其實是 Dr. Achebe 簽的（不只她一人涉入）。
- Halsey 與 Section III 之間的書信片段（道德複雜性）。
- CPO Kade 的訓練者視角與情感矛盾，以及他對「07-B」（需要跨文件還原成 Farrow）的親眼見聞，跟官方 casualty log 矛盾。
- 一份低溫恢復艙轉移授權（CAIRN record 106），讓 Farrow 的結局出現第三種可能——玩家此時應該意識到這件事永遠不會有乾淨答案。
- 部分候選人的 augmentation 結果（backups share 的傷亡紀錄，2525 年）。
- CAIRN 這個節點本身的真實身分：2547 SPINDLE decommission 留下的 staging mirror，除役排程沒執行完，不是現役最高機密資料中心——解釋了為什麼資安這麼糟。
仍不知道：LONGSHORE 開場真正要問的具體問題還沒有答案——誰在 2547 年動了 Farrow 的案件、具體動了什麼、為什麼（Disposition Order 101 只交代整批資料「保留、限閱、不銷毀」的官方決定，不是這個）。

## ARCHIVE root 之後（讀到 cairn_disposition_review.txt）
新增知道：**只有一件新事情**，但這件事才是整個委託真正要找的答案——SPINDLE 除役的標準檔案檢查把 07-B（Farrow）的低溫懸置單位排進了正式的「繼續保管或最終處置」審查清單；一份正式審查會強迫把 augmentation 紀錄、訓練紀錄、原始結案紀錄這三份彼此不該被同一批人同時讀到的文件攤開在一起。Petrov 在審查真正觸發前，未經授權，私自把保管狀態改成「繼續、無需處理」，跳過了整個審查流程——這就是玩家從 Act I 開始追的那個 transfer_ref 異常「為什麼在 2547 年被重新處理過」的具體答案。
文件**不會**重講一次起源、掩蓋手法、訓練與 augmentation 結果——那些玩家應該已經從 Act II/III 的其他文件裡自己拼出來了。Farrow 的結局也**不會**在這裡被解答，三份矛盾來源永遠沒有標準答案。
玩家此時應該能回答 LONGSHORE 開場提出的三個具體問題，而不是被文件直接告知一個總結論。
