from colorama import Fore
from password import generate_password, verify_password
from dataBase import save_password_to_db, save_password_to_file, hash_password, list_saved_accounts, delete_password


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
            print(Fore.RED + "\n\nНевірний вибір. Вкажіть цифру від 1 до 6" + Fore.WHITE)

