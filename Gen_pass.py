import random
import string 

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

def input_password():
    if __name__ == "__main__":
        length = int(input("Введіть довжину пароля: "))
        use_digits = input("Використовувати цифри? (+/-): ").strip() == '+'
        use_symbols = input("Використовувати символи? (+/-): ").strip() == '+'
        use_uppercase = input("Використовувати великі літери? (+/-): ").strip() == '+'
    
    password = generate_password(length, use_digits, use_symbols, use_uppercase)
    print(f"Згенерований пароль: {password}")
    
    
    
input_password()
    
    
    