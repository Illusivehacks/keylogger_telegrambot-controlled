# keylogger_telegrambot-controlled

# 🔐 Telegram Keylogger with Encryption and Status Updates

This script implements a **keylogger** that sends keystrokes and system status updates to a Telegram bot. It leverages encryption for sensitive information and provides real-time online/offline status notifications.  

---

## 🚀 Features

- **Encrypted Configuration**: Securely stores and decrypts the Telegram bot token and chat ID using the `cryptography` library.
- **Real-Time Status Updates**: Sends updates to Telegram for keylogger activity, system reboot, or shutdown detection.
- **Keystroke Monitoring**: Captures and transmits user keystrokes to a Telegram chat.
- **System Event Detection**: Detects and reports reboot, shutdown, or specific commands running on the system.
- **Telegram Integration**: Seamlessly communicates with Telegram using its Bot API.

---

## 📁 File Structure

