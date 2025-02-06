# Telegram-Matrix-bridge
This bot serves as a bridge between Telegram and Matrix, allowing messages to be transferred between the two platforms.

## Installation
Before you begin installation, make sure you have permissions to execute commands. Follow these steps:

1. **Install dependencies**:  
   Ensure that you have the following components installed:
   - `tmux`: A terminal multiplexer for managing sessions.
   - `python3`: The Python programming language interpreter.
   - `python3-venv`: A module for creating Python virtual environments.

   To install these components, you can use your package manager. For example, on Debian/Ubuntu, run:
   ```bash
   sudo apt update
   sudo apt install tmux python3 python3-venv
   ```
   
2. **Configure settings**:  
   Fill out the `config.yaml` file, following the comments inside to correctly specify the settings for connecting to your Telegram and Matrix bots.

3. **Prepare the script**:  
   To make the script executable, you need to set the appropriate permissions. To do this, run the following command:
   ```bash
   chmod +x start_bridge.sh
   ```
4. **Run the bot**:  
   Now you can start the bot by running the following command:
   ```bash
   ./start_bridge.sh
   ```
