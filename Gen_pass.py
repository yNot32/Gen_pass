import random
import string 
import bcrypt

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

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def input_password():
    if __name__ == "__main__":
        length = int(input("Введіть довжину пароля: "))
        use_digits = input("Використовувати цифри? (+/-): ").strip() == '+'
        use_symbols = input("Використовувати символи? (+/-): ").strip() == '+'
        use_uppercase = input("Використовувати великі літери? (+/-): ").strip() == '+'
    
    password = generate_password(length, use_digits, use_symbols, use_uppercase)
    hashed_password = hash_password(password)
    
    print(f"Згенерований пароль: {password}")
    print(f"Хешований пароль: {hashed_password}")  
    
input_password()
    
    
    