import sqlite3
import bcrypt

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
        
# Хешування пароля
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

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

# Ініціалізація бази даних
init_db()    
        
