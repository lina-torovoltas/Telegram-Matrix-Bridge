#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create the first tmux session for Telegram bot
tmux new-session -d -s telegram_bot -c "$SCRIPT_DIR"

# Check for the presence of a virtual environment and create it if it doesn’t exist
if [ ! -d "venv" ]; then
    tmux send-keys -t tg_session 'python -m venv venv' C-m
fi
tmux send-keys -t tg_session 'source venv/bin/activate' C-m
tmux send-keys -t tg_session "pip install -r requirements.txt" C-m
tmux send-keys -t tg_session 'python Bridge/tgbot.py' C-m

# Create a second tmux session for Matrix bot
tmux new-session -d -s matrix_bot -c "$SCRIPT_DIR"

# Check for the presence of a virtual environment and create it if it doesn’t exist
if [ ! -d "venv" ]; then
    tmux send-keys -t mt_session 'python -m venv venv' C-m
fi
tmux send-keys -t mt_session 'source venv/bin/activate' C-m
tmux send-keys -t mt_session "pip install -r requirements.txt" C-m
tmux send-keys -t mt_session 'python Bridge/mtbot.py' C-m
