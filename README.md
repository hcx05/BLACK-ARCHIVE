# BLACK ARCHIVE

一個由 Halo 故事改編的 ARG / cyber-investigation 靶場。你不是來解 CTF 題目的——你是一名獨立駭客，接下一個看似普通的委託：驗證一批殖民地兒童的死亡紀錄是否造假。深入下去以後，你會發現自己碰到的不只是資料造假。

> Find out what happened to them.

## 這是什麼

- 一個 3-host 的 offensive security lab（`FRONTIER` / `RELAY` / `ARCHIVE`），技術難度約 HTB Easy ～ 偏難 Easy。
- 同時是一個非線性的調查敘事：證據分散在網站、mail、資料庫、檔案分享、備份與內部文件之間，需要玩家自己拼線。
- Root 不是終點——它只是取得最後一批受限資料的手段。
- 詳細的作品定位與設計原則見 `作品核心要求`、`故事劇情`、`BLACK_ARCHIVE_Modification_Plan.md`（含 spoiler，開發用文件）。

## 致謝 / 來源

技術架構與漏洞機制基於 [VulnCastle](https://github.com/0x6d61/vulncastle)（by 0x6d61，MIT License）改造而成。原版是 7-host 企業靶場；本作品把它重構為 3-host 架構並替換全部敘事內容，漏洞機制本身盡量保持一致。

## 快速開始

### 需求
- [Docker](https://docs.docker.com/get-docker/)（含 Docker Compose v2）

### 啟動
```bash
chmod +x start.sh stop.sh
./start.sh
```

或手動：
```bash
docker build -t black-archive-base:latest ./lab/base/
docker compose up -d --build
```

### 停止
```bash
./stop.sh
```
或 `docker compose down`

### 開始之前

在碰任何 exploit 之前，先讀 [`briefing/00_longshore_contact.md`](briefing/00_longshore_contact.md)——那是你唯一會拿到的委託內容，之後不會再有人告訴你下一步該做什麼。FRONTIER 預設對外開在 `8080`（portal）、`8025`（webmail），RELAY 開在 `2222`（SSH）；如果是從另一台攻擊機打，把 `localhost` 換成跑 docker 那台機器的 IP 就好。

## 架構

```
Attacker (Kali)
    │
    ▼
┌─── DMZ (172.20.1.0/24) ───────────────────────────┐
│  frontier (172.20.1.10) → localhost:8080 / :8025    │
│  relay    (172.20.1.12) → localhost:2222 (SSH)      │
│    dual-homed, pivot point ──────────────────┐      │
└───────────────────────────────────────────────┼──────┘
                                                │
┌─── Internal (10.10.0.0/24, internal-only) ────┘
│  archive (10.10.0.15) — 只能透過 relay 抵達        │
└──────────────────────────────────────────────────┘
```

三台主機不是三個獨立 CTF box，而是同一套 UNSC 舊系統的三層。

## 免責聲明

**此環境為刻意設計的漏洞靶場，僅供授權安全訓練使用。**

- 不要將此環境暴露到 internet 或不受信任的網路
- 不要對未經授權的系統使用這裡的技巧
- 僅在隔離、受控的環境中使用

## 授權說明

這個 repo 混合了兩種不同性質的內容，授權狀態不一樣，**不宣告整個 repo 為 MIT**：

- **`lab/` 底下的靶機程式碼與 Dockerfile／設定**：改編自 [VulnCastle](https://github.com/0x6d61/vulncastle)，該專案在自己的 README 聲明 MIT License（雖然 repo 內沒有附獨立 `LICENSE` 檔案）。這部分的漏洞機制與工程手法沿用其授權條件，並在本文件保留致謝。
- **故事、人物、Halo/UNSC/ONI/SPARTAN-II 相關敘事內容**：非官方 Halo 同人創作，使用的是 Microsoft／343 Industries 擁有的智慧財產。這部分**不屬於作者原創版權範圍，作者無權將其授權給任何人使用**，僅作為非商業同人專案存在，與 Microsoft／343 Industries 無關、未經其授權或認可。

如果要重新散布或修改此 repo，請分開處理這兩部分：程式碼／靶機架構部分可視為延續 VulnCastle 的 MIT 條件；故事內容請視為同人創作，不要當作可自由再授權的素材。
