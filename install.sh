#!/bin/bash

set -e

echo "Installing TERMINAL..."

# system deps
sudo apt update
sudo apt install -y python3 python3-pip git

# clone repo if not already inside
if [ ! -d "terminal-game" ]; then
    git clone https://github.com/YOUR_USERNAME/terminal-game.git
fi

cd terminal-game

# python deps
pip3 install -r requirements.txt

# env setup
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️ Edit .env and add your Replicate API key"
fi

# install systemd service
sudo cp terminal.service /etc/systemd/system/terminal.service

sudo systemctl daemon-reexec
sudo systemctl enable terminal.service

echo "INSTALL COMPLETE."
echo "Run: sudo systemctl start terminal.service"