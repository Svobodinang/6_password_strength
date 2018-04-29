import calendar
from datetime import datetime


def input_password():
    password = input("Введите пароль: ")
    return password


def input_personal_data():
    last_name = input("Укажите свою фамилию: ")
    name = input("Имя: ")
    patronymic = input("Отчество(при наличии): ")
    company = input("Введите называние компании, " +
                    "в которой работаете(при наличии): ")
    return last_name, name, patronymic, company


def get_abbreviation(last_name, name, patronymic):
    if patronymic != "":
        abbreviation = last_name[0] + name[0] + patronymic[0]
    else:
        abbreviation = last_name[0] + name[0]
    return abbreviation


def upper_and_lower_letters(password):
    lower = False
    upper = False
    for letter in password:
        if letter.islower() and not lower:
            lower = True
        if letter.isupper() and not upper:
            upper = True

    if lower and upper:
        return True


def one_or_more_numerical_digits(password):
    digit = False
    for letter in password:
        if letter.isdigit():
            digit = True
            break
    return digit


def special_characters(password):
    special_characters = False
    for letter in password:
        if not letter.isdigit() and not letter.isalpha():
            special_characters = True
            break
    return special_characters


def in_black_list(password, filepath):
    with open(filepath) as black_list:
        readed_black_list = black_list.read()
    bad_password = False
    split_text = readed_black_list.split(" ")
    for word in split_text:
        if str(password) == str(word):
            bad_password = True
    return bad_password


def have_personal_information(password, personal_data):
    last_name, name, patronymic, company_name = personal_data
    have_personal_information = False
    have_company_name = False
    if (password.find(last_name) != -1) or \
       (password.find(name) != -1) or \
       (password.find(patronymic) != -1):
        have_personal_information = True
    if password.find(company_name) != -1 and company_name != "":
        have_company_name = True
    return have_personal_information, have_company_name


def have_abbreviation(password, last_name, name, patronymic):
    abbreviation = get_abbreviation(last_name, name, patronymic)
    have_abbreviation = False
    if password.find(abbreviation) != -1:
        have_abbreviation = True
    return have_abbreviation


def have_a_date_in_password(password):
    digit = password
    list_digit = []
    for letter in digit:
        if letter.isdigit():
            list_digit.append(letter)
    digit = "".join(list_digit)
    if date_check(digit):
        return True
    else:
        return False


def date_check(digit):
    format_one = "%y%m%d"
    format_two = "%Y%m%d"
    format_three = "%d%m%y"
    format_four = "%d%m%Y"
    isdate = False
    list_formats = [format_one, format_two, format_three, format_four]
    for format_d in list_formats:
        try:
            date = datetime.strptime(digit, format_d)
            isdate = True
            break
        except ValueError:
            isdate = isdate
    return isdate


def have_a_telephone_number(password):
    digit = password
    list_digit = []
    have_a_phone = False
    for letter in digit:
        if letter.isdigit():
            list_digit.append(letter)

    if len(list_digit) == 11:
        if list_digit[0] == "8" or list_digit[0] == "7":
            have_a_phone = True
    if len(list_digit) == 7 or len(list_digit) == 6:
        if list_digit[0] != "0" and list_digit[0] != 1:
            have_a_phone = True
    return have_a_phone


def have_license_plate_numbers(password):
    plase_number = ""
    have_plate_number = False
    for index in range(len(password)):
        if password[index].isdigit() and index > 0 and len(password) >= 6:
            if password[index - 1].isalpha() and \
               password[index + 1].isdigit() and \
               password[index + 2].isdigit() and \
               password[index + 3].isalpha() and \
               password[index + 4].isalpha():
                have_plate_number = True
    return have_plate_number


def get_password_strength(password, personal_data):
    complexity = 0
    error_list = []
    last_name, name, patronymic, company_name = personal_data
    if upper_and_lower_letters(password):
        complexity += 1
    else:
        error_list.append(1)
    if one_or_more_numerical_digits(password):
        complexity += 1
    else:
        error_list.append(2)
    if special_characters(password):
        complexity += 1
    else:
        error_list.append(3)
    if not in_black_list(password, "password_blacklist.txt"):
        complexity += 1
    else:
        error_list.append(4)
    personal_information_present, company_name_present = \
        have_personal_information(password, personal_data)
    if not personal_information_present:
        complexity += 1
    else:
        error_list.append(5)
    if not company_name_present:
        complexity += 1
    else:
        error_list.append(6)
    if not have_abbreviation(password, last_name, name, patronymic):
        complexity += 1
    else:
        error_list.append(7)
    if not have_a_date_in_password(password):
        complexity += 1
    else:
        error_list.append(8)
    if not have_a_telephone_number(password):
        complexity += 1
    else:
        error_list.append(9)
    if not have_license_plate_numbers(password):
        complexity += 1
    else:
        error_list.append(10)
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
