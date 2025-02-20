from cryptography.fernet import Fernet

# Генерація та збереження ключа шифрування
def generate_encryption_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# Завантаження ключа шифрування
def load_encryption_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()


# Функція шифрування пароля
def encrypt_password(password):
    key = load_encryption_key()
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()


# Функція розшифрування пароля
def decrypt_password(encrypted_password):
    key = load_encryption_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()