import string, random, sqlite3, bcrypt
# import random
# import sqlite3
# import bcrypt

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
    