#!/bin/bash
###############################################################################
# BLACK ARCHIVE - Lab Shutdown Script (Linux / macOS / WSL)
###############################################################################
echo "[*] Stopping BLACK ARCHIVE lab..."
docker compose down
echo "[+] Lab stopped."
