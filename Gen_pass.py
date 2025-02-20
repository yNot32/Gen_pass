import random
import string 
import bcrypt
import sqlite3

#Инициализация базы данных
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

#Генерация пароля

def generate_password(length = 12, use_digits = True, use_symbol = True, use_uppercase = True):
    try:
        lower_case_later = string.ascii_lowercase
        digits = string.digits if use_digits else ''
        symbols = string.punctuation if use_symbol else ''
        upper_letters = string.ascii_uppercase if use_uppercase else ''
    
        all_characters = lower_case_later + digits + symbols + upper_letters 
    
        if not all_characters:
            raise ValueError("Пароль повинен мати хоч 1 символ")
    
        password = ''.join(random.choice(all_characters) for _ in range(length))
        return password
    except ValueError as e:
        print(f"Ошибка генерации пароля: {e}")
        raise

# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Сохранение пароля в файл
def save_password_to_file(service, username, hashed_password):
    try:
        with open("password,txt", "a") as file:
            file.write(f"Service: {service}, Username: {username}, Hashed Password: {hashed_password.decode()}\n")
        print("Пароль сохранён в файл.")
    except Exception as e:
        print(f"Ошибка при сохранении пароля в файл: {e}")
        
# Сохранение пароля в базу данных
def save_password_to_db(service, username, hashed_password): 
    try:
        # Открытие соединения с базой данных через контекстный менеджер (with)
        with sqlite3.connect("passwords.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (service, username, hashed_password)
                VALUES (?, ?, ?)
            """, (service, username, hashed_password))
            conn.commit()  # Фиксация изменений
        print("Пароль сохранён в базу данных.")
    
    except sqlite3.Error as e:
        print(f"Ошибка при сохранении пароля в базу данных: {e}") 
        

#Ввод и обработка пароля
def input_password():
    try:
        service = input("Введите сервис: ")
        username = input("Введите имя пользователя: ")
    
        while True:
            try:
                length = int(input("Введіть довжину пароля: "))
                if length <= 0:
                    raise ValueError("Длина пароля должна быть положительным числом.")
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Попробуйте еще раз.")
                
        use_digits = input("Використовувати цифри? (+/-): ").strip() == '+'
        use_symbols = input("Використовувати символи? (+/-): ").strip() == '+'
        use_uppercase = input("Використовувати великі літери? (+/-): ").strip() == '+'
    
        password = generate_password(length, use_digits, use_symbols, use_uppercase)
        hashed_password = hash_password(password)
    
        print(f"Згенерований пароль: {password}")
        print(f"Хешований пароль: {hashed_password}")  
        
        # Запрос на сохранение
        save_option = input("Ви хочете зберегти цей пароль в файл чи базу даних? (введіть 'файл' або 'база'): ").strip().lower()
        if save_option == 'файл':
            save_password_to_file(service, username, hashed_password)
            print("Пароль збережено у файл.")
        elif save_option == 'база':
            save_password_to_db(service, username, hashed_password)
            print("Пароль збережено в базу даних.")
        else:
            print("Невірний варіант.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        
# Функция проверки пароля (аутентификация)
def verify_password(service, username, input_password):
    try:
        with sqlite3.connect("password.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hashed_password FROM passwords WHERE service = ? AND username = ?
            """, (service, username))
            result = cursor.fetchone
            
            if result is None:
                print("Обліковий запис не знайдено. ")
                return False
            
            stored_hashed_password = result[0].encode()
            if bcrypt.checkpw(input_password.encode(), stored_hashed_password):
                print("Пароль вірний. ")
                return True
            else:
                print("Неправильний пароль. ")
                return False
    except sqlite3.Error as e:
        print(f"Помилка при перевірці пароля: {e}") 
        return False
    
#Просмотр сохранённых паролей (безопасно)                        
def list_saved_account():
    try:
        with sqlite3.connect("password.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT service, username FROM passwords")
            accounts = cursor.fetchone
            
            if not accounts:
                print("Збережених облікових записів немає.")
                return
            
            print("\n Збережені облікові запсии: ")
            for service, username, in accounts:
                print(f"Сервіс: {service}, Користувач: {username}")
    except sqlite3.Error as e:
        print(f"Помилка при отриманні списку аккаунтів: {e}")
        
#Удаление паролей из базы данных
def delete_password(service, username):
    try:
        with sqlite3.connect("pasword.db") as conn:
            cursor = conn.cursor()
            cursor.execute(""" DELE FROM password WHERE service = ? AND username = ?""", (service, username))
            conn.commit
            
            if cursor.rowcount > 0:
                print("Пароль успішно видалено. ")
            else:
                print("Запис не знайдено. ")
    except sqlite3.Error as e:
        print(f"Помилка при видаленні пароля: {e}")                                    
            
            
    
init_db()
    
# Ввод пароля
input_password()
    
    