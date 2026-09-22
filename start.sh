#!/bin/bash
###############################################################################
# BLACK ARCHIVE - Lab Startup Script (Linux / macOS / WSL)
###############################################################################
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════╗"
echo "║              BLACK ARCHIVE                    ║"
echo "║   Intentionally Vulnerable - Training Only    ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker is not installed.${NC}"
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo -e "${RED}[ERROR] Docker Compose (v2) is not available.${NC}"
    exit 1
fi

if ! docker info &> /dev/null 2>&1; then
    echo -e "${RED}[ERROR] Docker daemon is not running. Please start Docker.${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Building base image...${NC}"
docker build -t black-archive-base:latest ./lab/base/

echo -e "${YELLOW}[*] Building and starting all services...${NC}"
docker compose up -d --build

echo ""
echo -e "${YELLOW}[*] Waiting for host-exposed ports to come up...${NC}"
# `docker compose ps` showing "Up" only means the container's process (supervisord)
# is alive - each host runs several services under it, and one of them can be
# crash-looping while the container itself stays Up. Check the ports that are
# actually exposed to this machine; anything internal-only can't be smoke
# tested from here without a pivot, which is the point of the lab.
check_port() {
    local host="$1" port="$2" name="$3" tries=20
    while ! (exec 3<>"/dev/tcp/$host/$port") 2>/dev/null; do
        tries=$((tries - 1))
        if [ "$tries" -le 0 ]; then
            echo -e "  ${RED}[FAIL]${NC} $name ($host:$port) did not come up"
            return 1
        fi
        sleep 1
    done
    exec 3>&- 2>/dev/null
    echo -e "  ${GREEN}[ OK ]${NC} $name ($host:$port)"
}
health_ok=true
check_port localhost 8080 "FRONTIER portal" || health_ok=false
check_port localhost 8025 "FRONTIER webmail" || health_ok=false

echo ""
if [ "$health_ok" = true ]; then
    echo -e "${GREEN}[+] BLACK ARCHIVE is running.${NC}"
else
    echo -e "${RED}[!] BLACK ARCHIVE did not come up cleanly - see [FAIL] lines above.${NC}"
    echo -e "${YELLOW}    Check container logs: docker compose logs frontier${NC}"
fi
echo ""
echo -e "${CYAN}=== Reachable from your attacking machine ===${NC}"
echo "  http://localhost:8080   (portal)"
echo "  http://localhost:8025   (webmail)"
echo ""
echo -e "${YELLOW}Everything else is internal-only. You'll need to find your own way in.${NC}"
echo -e "${YELLOW}[!] This environment is intentionally vulnerable. Do not expose it to untrusted networks.${NC}"
