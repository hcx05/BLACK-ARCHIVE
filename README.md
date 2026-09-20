# BLACK ARCHIVE

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

如果 `docker compose version` 報錯（`docker: 'compose' is not a docker command`）：`docker-compose` 這個 apt 套件在不同發行版/版本上有時只裝了舊版 standalone v1（只有 `docker-compose` 指令，沒有 `docker compose` 子指令）。改用官方 Docker repository 裝 v2 plugin：
```bash
sudo apt install -y docker-compose-plugin   # 如果套件庫裡有的話最簡單
# 或依照 https://docs.docker.com/engine/install/ 加入官方 repo 後
# sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
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

第一次啟動要抓套件、裝 nginx/php/mariadb/samba 這些東西，會花幾分鐘。`start.sh` 結尾會自動檢查 FRONTIER/RELAY 對外開的那幾個 port 是否真的通（`docker compose ps` 顯示三個 container 都 `Up` 不保證 container 裡面用 supervisord 跑的個別服務都活著，可能 nginx 或 webmail 早就 crash-loop 了，容器本身還是 `Up`）：
```bash
docker compose ps
```

### 4. 停止 / 重啟
```bash
./stop.sh                          # 或 docker compose down
docker compose up -d --build       # 改過程式碼後要重新 build 再啟動
docker compose up -d --force-recreate   # 沒改程式碼，只是想重置成乾淨狀態
```

FRONTIER 預設對外開在 `8080`（portal）、`8025`（webmail），RELAY 開在 `2222`（SSH）；如果是從另一台攻擊機打，把 `localhost` 換成跑 docker 那台受害機的 IP 就好（兩台機器要能互相 ping 通）。

## 免責聲明

**此環境為刻意設計的漏洞靶場，僅供授權安全訓練使用。**

- 不要將此環境暴露到 internet 或不受信任的網路
- 不要對未經授權的系統使用這裡的技巧
- 僅在隔離、受控的環境中使用

