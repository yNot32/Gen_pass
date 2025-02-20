import random
import string
import bcrypt
import sqlite3
from cryptography.fernet import Fernet

# Ініціалізація бази даних
def init_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            username TEXT NOT NULL,
            hashed_password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Генерація пароля
def generate_password(length=12, use_digits=True, use_symbols=True, use_uppercase=True):
    try:
        lower_case_letters = string.ascii_lowercase
        digits = string.digits if use_digits else ''
        symbols = string.punctuation if use_symbols else ''
        upper_letters = string.ascii_uppercase if use_uppercase else ''

        all_characters = lower_case_letters + digits + symbols + upper_letters

        if not all_characters:
            raise ValueError("Пароль повинен містити хоча б один символ.")

        password = ''.join(random.choice(all_characters) for _ in range(length))
        return password
    except ValueError as e:
        print(f"Помилка генерації пароля: {e}")
        raise


# Хешування пароля
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


# Збереження пароля у файл
def save_password_to_file(service, username, hashed_password):
    try:
        with open("passwords.txt", "a") as file:
            file.write(f"Сервіс: {service}, Користувач: {username}, Хешований пароль: {hashed_password.decode()}\n")
        print("Пароль збережено у файл.")
    except Exception as e:
        print(f"Помилка при збереженні пароля у файл: {e}")


# Збереження пароля у базу даних
def save_password_to_db(service, username, hashed_password):
    try:
        with sqlite3.connect("passwords.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (service, username, hashed_password)
                VALUES (?, ?, ?)
            """, (service, username, hashed_password))
            conn.commit()
        print("Пароль збережено у базу даних.")
    except sqlite3.Error as e:
        print(f"Помилка при збереженні пароля у базу даних: {e}")


# Перевірка пароля (автентифікація)
def verify_password(service, username, input_password):
    try:
        with sqlite3.connect("passwords.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hashed_password FROM passwords WHERE service = ? AND username = ?
            """, (service, username))
            result = cursor.fetchone()

            if result is None:
                print("Обліковий запис не знайдено.")
                return False

            stored_hashed_password = result[0].encode()
            if bcrypt.checkpw(input_password.encode(), stored_hashed_password):
                print("Пароль вірний.")
                return True
            else:
                print("Неправильний пароль.")
                return False
    except sqlite3.Error as e:
        print(f"Помилка при перевірці пароля: {e}")
        return False


# Перегляд збережених облікових записів
def list_saved_accounts():
    try:
        with sqlite3.connect("passwords.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT service, username FROM passwords")
            accounts = cursor.fetchall()

            if not accounts:
                print("Збережених облікових записів немає.")
                return

            print("\nЗбережені облікові записи:")
            for service, username in accounts:
                print(f"Сервіс: {service}, Користувач: {username}")
    except sqlite3.Error as e:
        print(f"Помилка при отриманні списку облікових записів: {e}")


# Видалення пароля з бази даних
def delete_password(service, username):
    try:
        with sqlite3.connect("passwords.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE service = ? AND username = ?", (service, username))
            conn.commit()

            if cursor.rowcount > 0:
                print("Пароль успішно видалено.")
            else:
                print("Запис не знайдено.")
    except sqlite3.Error as e:
        print(f"Помилка при видаленні пароля: {e}")


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


# Ініціалізація бази даних
init_db()

# Ваш існуючий код (всі функції)

# Ініціалізація бази даних
init_db()

# Функція для відображення головного меню
def main_menu():
    while True:
        print("\nМеню менеджера паролів")
        print("1. Згенерувати новий пароль")
        print("2. Зберегти новий пароль")
        print("3. Перевірити пароль")
        print("4. Переглянути збережені облікові записи")
        print("5. Видалити пароль")
        print("6. Вийти")

        choice = input("Виберіть опцію (1-6): ")

        if choice == '1':
            length = int(input("Введіть довжину пароля: "))
            use_digits = input("Використовувати цифри? (+/-): ").lower() == '+'
            use_symbols = input("Використовувати символи? (+/-): ").lower() == '+'
            use_uppercase = input("Використовувати великі літери? (+/-): ").lower() == '+'
            password = generate_password(length, use_digits, use_symbols, use_uppercase)
            print(f"Згенерований пароль: {password}")

        elif choice == '2':
            service = input("Введіть назву сервісу: ")
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            hashed_password = hash_password(password)
            save_password_to_db(service, username, hashed_password.decode())
            save_password_to_file(service, username, hashed_password)

        elif choice == '3':
            service = input("Введіть назву сервісу: ")
            username = input("Введіть ім'я користувача: ")
            input_password = input("Введіть пароль для перевірки: ")
            verify_password(service, username, input_password)

        elif choice == '4':
            list_saved_accounts()

        elif choice == '5':
            service = input("Введіть назву сервісу для видалення: ")
            username = input("Введіть ім'я користувача для видалення: ")
            delete_password(service, username)

        elif choice == '6':
            print("Вихід з програми.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

# Запуск програми
if __name__ == "__main__":
    main_menu()
