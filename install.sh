#!/bin/bash

set -e

echo "Installing TERMINAL..."

sudo apt update
sudo apt install -y python3 python3-pip python3-venv git python3-full

cd terminal-game

# create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

echo "DONE. Run with:"
echo "source venv/bin/activate && python game.py"
