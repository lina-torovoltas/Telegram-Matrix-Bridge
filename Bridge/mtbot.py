import yaml
import json
import socket
import asyncio
import threading
from nio import AsyncClient, RoomMessageText, LoginError



# Load configuration from the config file
def load_config(config_file="config.yaml"):
    with open(config_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()


# Socket and bot configuration
HOST_IP = config["HOST_IP"]
PORT_SEND = int(config["MATRIX_TO_TELEGRAM"])
PORT_LISTEN = int(config["TELEGRAM_TO_MATRIX"])
HOME_SERVER = config["BOT_HOME_SERVER"]
BOT_NAME = config["MATRIX_BOT_NAME"]
BOT_PASSWORD = config["MATRIX_BOT_PASSWORD"]
ROOM_ID = config["MATRIX_ROOM_ID"]

# Initialize Matrix client
client = AsyncClient(HOME_SERVER, BOT_NAME)



# Send a message via UDP socket
def send_message(username, message):
    data = {
        "username": username,
        "message": message
    }
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as send_socket:
        send_socket.sendto(json.dumps(data).encode(), (HOST_IP, PORT_SEND))
        print(f"Message sent to port {PORT_SEND}")


# Async function to send messages to the Matrix room
async def send_matrix_notice(room_id, message):
    await client.room_send(
        room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": message,
            "format": "org.matrix.custom.html",
            "formatted_body": message
        }
    )


# UDP server to receive incoming messages
def start_udp_server(loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST_IP, PORT_LISTEN))
    print(f"Server listening on port {PORT_LISTEN}...")
    
    while True:
        data, address = sock.recvfrom(4096)
        try:
            message_data = json.loads(data.decode())
            print(f"Message received from {address}: {message_data}")
            username = message_data["username"]
            message = message_data["message"]
            text = f"@{username}: \n\n{message}"
            
            asyncio.run_coroutine_threadsafe(
                send_matrix_notice(ROOM_ID, text),
                loop
            )
        except json.JSONDecodeError:
            print(f"JSON decoding error from {address}")


# Handle incoming Matrix messages
async def message_handler(room, event):
    # Ignore messages from the bot itself
    if event.sender == client.user_id:
        return

    # Check if the message is from the correct room
    if room.room_id != ROOM_ID:
        if event.body.startswith("!id"):
            await send_matrix_notice(room.room_id, room.room_id)
        return

    print(f"Room: {room.room_id}, User: {event.sender}, Message: {event.body}")

    send_message(event.sender, event.body)


# Main bot function
async def main():
    try:
        # Matrix login
        login = await client.login(password=BOT_PASSWORD)
        if isinstance(login, LoginError):
            print(f"Login failed: {login.message}")
            return
        print("Login successful, starting server...")

        # Add event callback for message handling
        client.add_event_callback(message_handler, RoomMessageText)

        # Start the UDP server in a separate thread
        loop = asyncio.get_running_loop()
        udp_thread = threading.Thread(target=start_udp_server, args=(loop,), daemon=True)
        udp_thread.start()

        # Start syncing with the Matrix server
        await client.sync_forever(timeout=30000, full_state=True)
    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        await client.close()



# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
