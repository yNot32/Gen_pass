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
    lower_case_later = string.ascii_lowercase
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbol else ''
    upper_letters = string.ascii_uppercase if use_uppercase else ''
    
    all_characters = lower_case_later + digits + symbols + upper_letters 
    
    if not all_characters:
        raise ValueError("Пароль повинен мати хоч 1 символ")
    
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Сохранение пароля в файл
def save_password_to_file(service, username, hashed_password):
    with open("password,txt", "a") as file:
        file.write(f"Service: {service}, Username: {username}, Hashed Password: {hashed_password.decode()}\n")
        
# Сохранение пароля в базу данных
def save_password_to_db(service, username, hashed_password): 
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (service, username, hashed_password)
        VALUES (?, ?, ?)
    """, (service, username, hashed_password))
    conn.commit()
    conn.close()       
        

#Ввод и обработка пароля
def input_password():
    if __name__ == "__main__":
        service = input("Введіть сервіс: ")
        username = input("Введіть ім'я користувача: ")
        length = int(input("Введіть довжину пароля: "))
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
    
init_db()
    
# Ввод пароля
input_password()
    
    
    