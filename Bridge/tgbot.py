import yaml
import json
import socket
import telebot
from threading import Thread



# Load configurations from the config file
def load_config(config_file="config.yaml"):
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()


# Socket and bot configuration
HOST_IP = config["HOST_IP"]
PORT_SEND = int(config["TELEGRAM_TO_MATRIX"])
PORT_LISTEN = int(config["MATRIX_TO_TELEGRAM"])
BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = int(config.get("TELEGRAM_CHANNEL_ID"))

# Initialize telegram bot
bot = telebot.TeleBot(BOT_TOKEN)



# Send a message to Matrix server
def send_to_matrix(username, message):
    data = {
        "username": username,
        "message": message
    }
    json_data = json.dumps(data).encode("utf-8")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket:
            send_socket.sendto(json_data, (HOST_IP, PORT_SEND))
            print(f"Message sent to Matrix on port {PORT_SEND}")
    except Exception as e:
        print(f"Error sending to Matrix on port {PORT_SEND}: {e}")


# Start server to listen for messages and send to Telegram
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("0.0.0.0", PORT_LISTEN))
        print(f"Server listening on port {PORT_LISTEN}")
        while True:
            data, addr = server_socket.recvfrom(4096)
            if not data:
                continue
            try:
                message_data = json.loads(data.decode("utf-8"))
                username = message_data.get("username", "Unknown")
                message = message_data.get("message", "")

                text = f"{username}: \n{message}"
                bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
                print(f"Message sent to Telegram: {text}")
            except json.JSONDecodeError:
                print("Error parsing JSON")
            except Exception as e:
                print(f"Error processing message: {e}")


# Handle incoming Telegram messages
def handle_telegram_messages(message):
    username = message.from_user.username or "TelegramUser"
    id_chat = message.chat.id
    text = message.text
    if id_chat != CHANNEL_ID:
        if text.startswith("!id"):
            bot.send_message(id_chat, str(id_chat))
        return
    send_to_matrix(username, text)

bot.message_handler(func=lambda message: True)(handle_telegram_messages)



# Run the server and bot in parallel
if __name__ == "__main__":
    server_thread = Thread(target=start_server)
    server_thread.start()
    bot.polling(none_stop=True)
