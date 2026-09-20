# BLACK ARCHIVE

一個由 Halo 故事改編的 ARG / cyber-investigation 靶場。你不是來解 CTF 題目的——你是一名獨立駭客，接下一個看似普通的委託：驗證一批殖民地兒童的死亡紀錄是否造假。深入下去以後，你會發現自己碰到的不只是資料造假。

> Find out what happened to them.

## 這是什麼

- 一個 3-host 的 offensive security lab（`FRONTIER` / `RELAY` / `ARCHIVE`），技術難度約 HTB Easy ～ 偏難 Easy。
- 同時是一個非線性的調查敘事：證據分散在網站、mail、資料庫、檔案分享、備份與內部文件之間，需要玩家自己拼線。
- Root 不是終點——它只是取得最後一批受限資料的手段。
- 詳細的作品定位與設計原則見 `BLACK_ARCHIVE_Modification_Plan.md`、`story-dev/`（含 spoiler，開發用文件）。

## 快速開始

### 1. 抓這個 repo

在要跑 lab 的那台機器（受害機，不是攻擊機）上：

```bash
git clone git@github.com:hcx05/BLACK-ARCHIVE.git
cd BLACK-ARCHIVE
```

沒設定 SSH key 的話用 HTTPS：

```bash
git clone https://github.com/hcx05/BLACK-ARCHIVE.git
cd BLACK-ARCHIVE
```

下面所有指令都是在這個 repo 的根目錄（也就是 `docker-compose.yml` 所在的位置）底下執行。

### 2. 在受害機上裝好 Docker（第一次設置才需要）

這台機器（跑 lab 的那台，不是攻擊機）要有 Docker + Docker Compose v2。Kali / Debian / Ubuntu 系統：

```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

`usermod` 之後**要重新登入這個 shell session 才會生效**（登出重進，或開一個新的終端機視窗；只是 `su - $USER` 也可以）。如果不想重開 session，可以在單一指令前面暫時借用 docker 群組權限：

```bash
sg docker -c "docker info"
```

確認裝好了：
```bash
docker --version
docker compose version
docker info      # 這行如果報錯，通常是 docker daemon 沒啟動或群組權限還沒生效
```

### 3. 啟動 lab
```bash
chmod +x start.sh stop.sh
./start.sh
```

或手動：
```bash
docker build -t black-archive-base:latest ./lab/base/
docker compose up -d --build
```

第一次啟動要抓套件、裝 nginx/php/mariadb/samba 這些東西，會花幾分鐘。看到三個 container 都是 `Up` 就代表好了：
```bash
docker compose ps
```

### 4. 停止 / 重啟
```bash
./stop.sh                          # 或 docker compose down
docker compose up -d --build       # 改過程式碼後要重新 build 再啟動
docker compose up -d --force-recreate   # 沒改程式碼，只是想重置成乾淨狀態
```

### 開始之前

在碰任何 exploit 之前，先看 [`briefing/00_longshore_contact.html`](briefing/00_longshore_contact.html)（純文字來源在同資料夾的 `.md`）——那是你唯一會拿到的委託內容，之後不會再有人告訴你下一步該做什麼。這是一個純靜態網頁，不需要架任何伺服器：把檔案下載下來直接用瀏覽器打開（`file://` 路徑）就能看，跟開一個 PDF 一樣，只是格式是 HTML。如果想要一個可以直接分享的連結而不想自己架站，也可以參考線上版本：https://claude.ai/artifact/3Wy9d8TySzLM5yFcqMnK8t

FRONTIER 預設對外開在 `8080`（portal）、`8025`（webmail），RELAY 開在 `2222`（SSH）；如果是從另一台攻擊機打，把 `localhost` 換成跑 docker 那台受害機的 IP 就好（兩台機器要能互相 ping 通）。

## 架構

```
Attacker (Kali)
    │
    ▼
┌─── DMZ (172.20.1.0/24) ──────────────────────────┐
│  frontier (172.20.1.10) → localhost:8080 / :8025 │
│  relay    (172.20.1.12) → localhost:2222 (SSH)   │
│    dual-homed, pivot point ──────────────────┐   │
└──────────────────────────────────────────────┼───┘
                                               │ 
┌─── Internal (10.10.0.0/24, internal-only) ───┘───┐ 
│  archive (10.10.0.15) — 只能透過 relay 抵達      │
└──────────────────────────────────────────────────┘
```

三台主機不是三個獨立 CTF box，而是同一套 UNSC 舊系統的三層。

## 免責聲明

**此環境為刻意設計的漏洞靶場，僅供授權安全訓練使用。**

- 不要將此環境暴露到 internet 或不受信任的網路
- 不要對未經授權的系統使用這裡的技巧
- 僅在隔離、受控的環境中使用

