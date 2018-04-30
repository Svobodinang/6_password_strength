import calendar
from checks_password import short_password, \
                            have_just_upper_or_just_lower_letters, \
                            dont_have_numerical_digits, \
                            dont_have_special_characters, \
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
    first_name = input("Имя: ")
    patronymic = input("Отчество(при наличии): ")
    company = input("Введите называние компании, %s" %
                    "в которой работаете(при наличии): ")
    return last_name, first_name, patronymic, company


def get_password_strength(password, personal_data):
    complexity = 0
    error_list = []
    last_name, first_name, patronymic, company_name = personal_data
    personal_information_present, company_name_present = \
        have_personal_information(password, personal_data)

    all_checks_password = [short_password(password),
                           have_just_upper_or_just_lower_letters(password),
                           dont_have_numerical_digits(password),
                           dont_have_special_characters(password),
                           in_black_list(password, "password_blacklist.txt"),
                           personal_information_present,
                           company_name_present,
                           have_abbreviation(password,
                                             last_name,
                                             first_name,
                                             patronymic),
                           have_a_date_in_password(password),
                           have_a_telephone_number(password),
                           have_license_plate_numbers(password)]
    index = 0
    for check_password in all_checks_password:
        if not check_password:
            complexity += 1
        else:
            error_list.append(index)
        index += 1
    return complexity, error_list


def output_complexity(complexity, error_list):
    print("Сложность вашего пароль: ", complexity)
    names_error = ["Пароль должен состоять более чем из 8 символов",
                   "Испульзуйте буквы разного регистра",
                   "Используйте не только буквы, но и цифры",
                   "Используйте различные знаки, например: ^, &, #",
                   "Используйте менее распространенные пароли",
                   "Не используйте в пароле свою персональную информацию",
                   "Не используйте название компании в пароле",
                   "Не используйте аббревиатуру в пароле",
                   "Не указывайте даты в пароле",
                   "Не используйте номера телефонов в пароле",
                   "Не используйте номерные знаки в пароле"]
    for index in range(10):
        for error in error_list:
            if index == error:
                print(names_error[index])


if __name__ == '__main__':
    personal_data = input_personal_data()
    if personal_data[0] == "" or personal_data[1] == "":
        exit("Вы ввели не все персональные данные")
    password = input_password()
    if password == "":
        exit("Вы не ввели пароль")
    complexity, error_list = get_password_strength(password, personal_data)
    output_complexity(complexity, error_list)
