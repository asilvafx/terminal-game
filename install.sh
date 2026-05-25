#!/bin/bash

set -e

echo ""
echo "======================================"
echo "   INSTALLING TERMINAL HORROR GAME"
echo "======================================"
echo ""

cd /home/pi

# -------------------------------
# 1. SYSTEM PACKAGES
# -------------------------------
echo "[1/6] Installing system packages..."
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv python3-full

# -------------------------------
# 2. CLONE OR UPDATE REPO
# -------------------------------
echo "[2/6] Setting up repository..."

if [ -d "/home/pi/terminal-game" ]; then
    rm -rf /home/pi/terminal-game
fi

git clone https://github.com/asilvafx/terminal-game.git
cd terminal-game

# -------------------------------
# 3. PYTHON ENV
# -------------------------------
echo "[3/6] Creating virtual environment..."

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------
# 4. ENABLE AUTO LOGIN (pi user)
# -------------------------------
echo "[4/6] Enabling auto-login..."

sudo raspi-config nonint do_boot_behaviour B2

# B2 = Console Autologin

# -------------------------------
# 5. CLEAN BOOT CONFIG (NO LOGS)
# -------------------------------
echo "[5/6] Configuring clean boot..."

BOOT_CFG="/boot/firmware/cmdline.txt"

if [ -f "$BOOT_CFG" ]; then
    sudo sed -i 's/$/ quiet splash loglevel=0 vt.global_cursor_default=0 logo.nologo consoleblank=0/' $BOOT_CFG
fi

# -------------------------------
# 6. SYSTEMD SERVICE (AUTO START GAME)
# -------------------------------
echo "[6/6] Installing system service..."

sudo tee /etc/systemd/system/terminal-game.service > /dev/null <<EOF
[Unit]
Description=Terminal Horror Game
After=multi-user.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/terminal-game

ExecStartPre=/home/pi/terminal-game/venv/bin/python /home/pi/terminal-game/boot_loader.py
ExecStart=/home/pi/terminal-game/venv/bin/python /home/pi/terminal-game/game.py

Restart=always

StandardInput=tty
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes
TTYVTDisallocate=yes

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable terminal-game.service

# -------------------------------
# INSTALL DONE SCREEN
# -------------------------------
clear

echo ""
echo "======================================"
echo "   INSTALLATION COMPLETE"
echo "======================================"
echo ""
echo "Terminal is now installed."
echo ""
echo "NEXT BOOT WILL:"
echo " - Hide system logs"
echo " - Show loading animation"
echo " - Start TERMINAL automatically"
echo ""
echo "Press ENTER to reboot now..."
read

sudo reboot
