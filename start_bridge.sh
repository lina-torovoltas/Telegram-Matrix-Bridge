#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# function for launching a Telegram bot in tmux with auto-restart
start_tg_bot() {
    while true; do
        tmux new-session -d -s tg_session -c "$SCRIPT_DIR"

        # Checks for the existence of a virtual environment and creates it if it doesn't exist
        if [ ! -d "venv" ]; then
            tmux send-keys -t tg_session 'python -m venv venv' C-m
        fi
        tmux send-keys -t tg_session 'source venv/bin/activate' C-m
        tmux send-keys -t tg_session "pip install -r requirements.txt" C-m
        tmux send-keys -t tg_session 'python Bridge/tgbot.py' C-m
        
        # Waits an hour before restarting
        sleep 3600
        tmux kill-session -t tg_session
    done
}

# Function for launching Matrix bot in tmux with auto-restart
start_mt_bot() {
    while true; do
        tmux new-session -d -s mt_session -c "$SCRIPT_DIR"

	# Checks for the existence of a virtual environment and creates it if it doesn't exist
        if [ ! -d "venv" ]; then
            tmux send-keys -t mt_session 'python -m venv venv' C-m
        fi
        tmux send-keys -t mt_session 'source venv/bin/activate' C-m
        tmux send-keys -t mt_session "pip install -r requirements.txt" C-m
        tmux send-keys -t mt_session 'python Bridge/mtbot.py' C-m
        
        # Waits an hour before restarting
        sleep 3600
        tmux kill-session -t mt_session
    done
}

# Starts both bots
start_tg_bot &
start_mt_bot &
