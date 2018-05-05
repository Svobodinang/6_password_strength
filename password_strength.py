import calendar
import sys
import getpass
from checks_password import dont_short_password, \
                            has_upper_and_lower_letters, \
                            has_numerical_digits, \
                            has_special_characters, \
                            has_not_in_black_list, \
                            has_not_personal_information, \
                            has_not_abbreviation, \
                            has_not_a_date_in_password, \
                            has_not_a_telephone_number, \
                            has_not_license_plate_numbers


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


def get_password_strength(password, personal_data):
    complexity = 0
    error_list = []
    last_name, first_name, patronymic, company_name = personal_data
    personal_information_present, company_name_present = \
        has_not_personal_information(password, personal_data)

    all_checks_password = [
        dont_short_password(password),
        has_upper_and_lower_letters(password),
        has_numerical_digits(password),
        has_special_characters(password),
        has_not_in_black_list(password, sys.argv[1]),
        personal_information_present,
        company_name_present,
        has_not_abbreviation(
            password,
            last_name,
            first_name,
            patronymic,
        ),
        has_not_a_date_in_password(password),
        has_not_a_telephone_number(password),
        has_not_license_plate_numbers(password),
    ]
    index = 0
    for check_password in all_checks_password:
        if check_password:
            complexity += 1
        else:
            error_list.append(index)
        index += 1
    return complexity, error_list


def output_complexity(complexity, error_list):
    print("Сложность вашего пароль: ", complexity)
    names_error = [
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
    for index in range(11):
        for error in error_list:
            if index == error:
                print(names_error[index])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit("Вы не ввели путь к файлу с самыми полпулярными паролями")
    personal_data = user_input_personal_data()
    last_name = 0
    first_name = 1
    if personal_data[last_name] == "" or personal_data[first_name] == "":
        exit("Вы ввели не все персональные данные")
    password = user_input_password()
    if password == "":
        exit("Вы не ввели пароль")
    complexity, error_list = get_password_strength(password, personal_data)
    output_complexity(complexity, error_list)
