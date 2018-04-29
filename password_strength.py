import calendar
from checks_password import upper_and_lower_letters, \
                            one_or_more_numerical_digits, \
                            special_characters, \
                            in_black_list, \
                            have_personal_information, \
                            have_abbreviation, \
                            have_a_date_in_password, \
                            have_a_telephone_number, \
                            have_license_plate_numbers


def input_password():
    password = input("Введите пароль: ")
    return password


def input_personal_data():
    last_name = input("Укажите свою фамилию: ")
    name = input("Имя: ")
    patronymic = input("Отчество(при наличии): ")
    company = input("Введите называние компании, %s" %
                    "в которой работаете(при наличии): ")
    return last_name, name, patronymic, company


def get_password_strength(password, personal_data):
    complexity = 0
    error_list = []
    last_name, name, patronymic, company_name = personal_data
    if upper_and_lower_letters(password):
        complexity += 1
    else:
        error = 1
        error_list.append(error)
    if one_or_more_numerical_digits(password):
        complexity += 1
    else:
        error = 2
        error_list.append(error)
    if special_characters(password):
        complexity += 1
    else:
        error = 3
        error_list.append(error)
    if not in_black_list(password, "password_blacklist.txt"):
        complexity += 1
    else:
        error = 4
        error_list.append(error)
    personal_information_present, company_name_present = \
        have_personal_information(password, personal_data)
    if not personal_information_present:
        complexity += 1
    else:
        error = 5
        error_list.append(error)
    if not company_name_present:
        complexity += 1
    else:
        error = 6
        error_list.append(error)
    if not have_abbreviation(password, last_name, name, patronymic):
        complexity += 1
    else:
        error = 7
        error_list.append(error)
    if not have_a_date_in_password(password):
        complexity += 1
    else:
        error = 8
        error_list.append(error)
    if not have_a_telephone_number(password):
        complexity += 1
    else:
        error = 9
        error_list.append(error)
    if not have_license_plate_numbers(password):
        complexity += 1
    else:
        error = 10
        error_list.append(error)
    return complexity, error_list


def output_complexity(complexity, error_list):
    print("Сложность вашего пароль: ", complexity)
    for error in error_list:
        if error == 1:
            print("Испульзуйте буквы разного регистра")
        if error == 2:
            print("Используйте не только буквы, но и цифры")
        if error == 3:
            print("Используйте различные знаки, например: ^, &, #")
        if error == 4:
            print("Используйте менее распространенные пароли")
        if error == 5:
            print("Не используйте в пароле свою персональную информацию")
        if error == 6:
            print("Не используйте название компании в пароле")
        if error == 7:
            print("Не используйте аббревиатуру в пароле")
        if error == 8:
            print("Не указывайте даты в пароле")
        if error == 9:
            print("Не используйте номера телефонов в пароле")
        if error == 10:
            print("Не используйте номерные знаки в пароле")


if __name__ == '__main__':
    personal_data = input_personal_data()
    if personal_data[0] == "" or personal_data[1] == "":
        exit("Вы ввели не все персональные данные")
    password = input_password()
    if password == "":
        exit("Вы не ввели пароль")
    complexity, error_list = get_password_strength(password, personal_data)
    output_complexity(complexity, error_list)
