#!/bin/bash

set -e

echo "Installing TERMINAL..."

sudo apt update
sudo apt install -y python3 python3-pip python3-venv git python3-full

cd terminal-game

# create venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

echo "Setting up system service..."

sudo tee /etc/systemd/system/terminal-game.service > /dev/null <<EOF
[Unit]
Description=Terminal Horror Game
After=plymouth-quit.service systemd-user-sessions.service
Wants=plymouth-quit.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/terminal-game

ExecStartPre=/home/pi/terminal-game/venv/bin/python /home/pi/terminal-game/boot_loader.py
ExecStart=/home/pi/terminal-game/venv/bin/python /home/pi/terminal-game/game.py

Restart=always
StandardInput=tty
TTYPath=/dev/tty1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable terminal-game.service

echo "INSTALL COMPLETE."
echo "Reboot to start Terminal."
