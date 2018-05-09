from datetime import datetime
import re
import string


def has_enough_length(password):
    enough_password_length = 8
    return len(password) > enough_password_length


def has_upper_and_lower_letters(password):
    lower = any([char.islower() for char in password])
    upper = any([char.isupper() for char in password])
    return lower and upper


def has_numerical_digits(password):
    has_digit = any([digit.isdigit() for digit in password])
    return has_digit


def has_special_characters(password):
    return not password.isalnum()


def load_blacklist(filepath):
    with open(filepath) as file:
        readed_black_list = file.readlines()
    readed_black_list = [line.rstrip() for line in readed_black_list]
    return readed_black_list


def is_not_in_black_list(password, black_list):
    return password not in black_list


def has_not_personal_information(password, personal_data):
    last_name, first_name, patronymic, company_name = personal_data
    has_not_personal_information = True
    has_not_company_name = True
    if (last_name in password or
       first_name in password or
       patronymic in password):
        has_not_personal_information = False
    if company_name in password and (company_name != ""):
        has_not_company_name = False
    return has_not_personal_information, has_not_company_name


def get_abbreviation(last_name, first_name, patronymic):
    first_symbol = 0
    if patronymic != "":
        abbreviation = (
            last_name[first_symbol] +
            first_name[first_symbol] +
            patronymic[first_symbol]
        )
    else:
        abbreviation = (
            last_name[first_symbol] +
            first_name[first_symbol]
        )
    return abbreviation


def has_not_abbreviation(password, last_name, first_name, patronymic):
    abbreviation = get_abbreviation(last_name, first_name, patronymic)
    has_not_abbreviation = abbreviation not in password
    return has_not_abbreviation


def get_numbers_from_password(password):
    digit_list = [letter for letter in password if letter.isdigit()]
    return digit_list


def check_date(digit):
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
            continue
    return isdate


def has_not_date_in_password(password):
    local_password = password
    digit_list = get_numbers_from_password(password)
    local_password = "".join(digit_list)
    good_password = not bool(check_date(local_password))
    return good_password


def has_not_a_telephone_number(password):
    digit_list = get_numbers_from_password(password)
    has_not_a_phone = True
    string_length_one = 11
    string_length_two = 7
    string_length_three = 6
    bad_first_digit_one = "0"
    bad_first_digit_two = "1"
    first_digit_one = "7"
    first_digit_two = "8"
    first_symbol = 0

    if len(digit_list) == string_length_one:
        if (digit_list[first_symbol] == first_digit_one or
           digit_list[first_symbol] == first_digit_two):
            has_not_a_phone = False

    if (len(digit_list) == string_length_two or
       len(digit_list) == string_length_three):
        if (digit_list[first_symbol] != bad_first_digit_one and
           digit_list[first_symbol] != bad_first_digit_two):
            has_not_a_phone = False
    return has_not_a_phone


def has_not_license_plate_numbers(password):
    plase_number = ""
    has_not_plate_number = True
    regular_expression_one = r"[a-z]\d{3}[a-z]{2}"
    regular_expression_two = r"[A-Z]\d{3}[A-Z]{2}"
    find_plate_one = re.search(regular_expression_one, password)
    find_plate_two = re.search(regular_expression_two, password)
    if find_plate_one or find_plate_two:
        has_not_plate_number = False
    return has_not_plate_number
