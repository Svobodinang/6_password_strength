import calendar
import sys
import getpass
import os
from checks_password import (
    has_enough_length,
    has_upper_and_lower_letters,
    has_numerical_digits,
    has_special_characters,
    is_not_in_black_list,
    has_not_personal_information,
    has_not_abbreviation,
    has_not_date_in_password,
    has_not_a_telephone_number,
    has_not_license_plate_numbers,
    load_blacklist,
)


def user_input_password():
    password = getpass.getpass("Введите Пароль: ")
    return password


def user_input_personal_data():
    last_name = input("Укажите свою фамилию: ")
    first_name = input("Имя: ")
    patronymic = input("Отчество(при наличии): ")
    company = input("Введите называние компании, "
                    "в которой работаете(при наличии): ")
    return last_name, first_name, patronymic, company


def get_password_strength(password, personal_data, filepath):
    complexity = 0
    error_list = []
    last_name, first_name, patronymic, company_name = personal_data
    personal_information_present, company_name_present = (
        has_not_personal_information(password, personal_data)
    )
    black_list = load_blacklist(filepath)

    all_checks_password = [
        (has_enough_length(password), 0),
        (has_upper_and_lower_letters(password), 1),
        (has_numerical_digits(password), 2),
        (has_special_characters(password), 3),
        (is_not_in_black_list(password, black_list), 4),
        (personal_information_present, 5),
        (company_name_present, 6),
        (has_not_abbreviation(
            password,
            last_name,
            first_name,
            patronymic,
        ), 7),
        (has_not_date_in_password(password), 8),
        (has_not_a_telephone_number(password), 9),
        (has_not_license_plate_numbers(password), 10),
    ]
    for check, error in all_checks_password:
        if check:
            complexity += 1
        else:
            error_list.append(error)
    return complexity, error_list


def output_complexity(complexity, error_indexes_list):
    print("Сложность вашего пароль: ", complexity)
    errors = [
        "Пароль должен состоять более чем из 8 символов",
        "Испульзуйте буквы разного регистра",
        "Используйте не только буквы, но и цифры",
        "Используйте различные знаки, например: ^, &, #",
        "Используйте менее распространенные пароли",
        "Не используйте в пароле свою персональную информацию",
        "Не используйте название компании в пароле",
        "Не используйте аббревиатуру в пароле",
        "Не указывайте даты в пароле",
        "Не используйте номера телефонов в пароле",
        "Не используйте номерные знаки в пароле",
    ]
    for index in error_indexes_list:
        print(errors[index])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Вы не ввели путь к файлу с самыми популярными паролями")
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        exit("Такого файла не существует")

    last_name, first_name, patronymic, company_name = (
        user_input_personal_data()
    )
    if not last_name or not first_name:
        exit("Вы ввели не все персональные данные")
    password = user_input_password()
    if password == "":
        exit("Вы не ввели пароль")
    personal_data = last_name, first_name, patronymic, company_name
    complexity, error_list = (
        get_password_strength(password, personal_data, file_path)
    )
    output_complexity(complexity, error_list)
