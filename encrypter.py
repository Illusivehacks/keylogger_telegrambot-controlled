from cryptography.fernet import Fernet

# Generate a key (store this securely, e.g., in an environment variable)
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Replace with your actual bot token and chat ID
bot_token = "7636564556:AAHkefNr-e88-ebt3-fN2LJwNzS2aonKVFc"
chat_id = "6215932196"

# Encrypt the bot token and chat ID
encrypted_bot_token = cipher_suite.encrypt(bot_token.encode())
encrypted_chat_id = cipher_suite.encrypt(chat_id.encode())

print(f"Encryption Key (store securely): {encryption_key}")
print(f"Encrypted Bot Token: {encrypted_bot_token}")
print(f"Encrypted Chat ID: {encrypted_chat_id}")


