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
echo -e "${GREEN}[+] BLACK ARCHIVE is running.${NC}"
echo ""
echo -e "${CYAN}=== Reachable from your attacking machine ===${NC}"
echo "  http://localhost:8080   (portal)"
echo "  http://localhost:8025   (webmail)"
echo "  ssh -p 2222 <user>@localhost"
echo ""
echo -e "${YELLOW}Everything else is internal-only. You'll need to find your own way in.${NC}"
echo -e "${YELLOW}[!] This environment is intentionally vulnerable. Do not expose it to untrusted networks.${NC}"
