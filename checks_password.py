from datetime import datetime
import re
import string


def dont_short_password(password):
    return bool(len(password) > 8)


def has_upper_and_lower_letters(password):
    lower = False
    upper = False
    for letter in password:
        if letter.islower() and not lower:
            lower = True
        if letter.isupper() and not upper:
            upper = True

    good_password = not bool(not lower or not upper)
    return good_password


def has_numerical_digits(password):
    have_digit = False
    for letter in password:
        if letter.isdigit():
            have_digit = True
            break
    
    good_password = bool(have_digit)

    return good_password


def has_special_characters(password):
    good_password = not bool(password.isalnum())
    return good_password

def load_data(filepath):
    with open(filepath) as file:
        readed_file = file.readlines()
    return readed_file


def has_not_in_black_list(password, filepath):
    readed_black_list = load_data(filepath)
    readed_black_list = [line.rstrip() for line in readed_black_list]
    return not (password in readed_black_list)


def has_not_personal_information(password, personal_data):
    last_name, first_name, patronymic, company_name = personal_data
    have_not_personal_information = True
    have_not_company_name = True
    if last_name in password or \
       first_name in password or \
       patronymic in password:
        have_not_personal_information = False
    if company_name in password and (company_name != ""):
        have_not_company_name = False
    return have_not_personal_information, have_not_company_name


def get_abbreviation(last_name, first_name, patronymic):
    first_symbol = 0
    if patronymic != "":
        abbreviation = last_name[first_symbol] + \
                       first_name[first_symbol] + \
                       patronymic[first_symbol]
    else:
        abbreviation = last_name[first_symbol] + \
                       first_name[first_symbol]
    return abbreviation


def has_not_abbreviation(password, last_name, first_name, patronymic):
    abbreviation = get_abbreviation(last_name, first_name, patronymic)
    has_not_abbreviation = not bool(abbreviation in password)
    return has_not_abbreviation


def get_numbers_from_password(password):
    digit_list = [letter for letter in password if letter.isdigit()]
    return digit_list


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
            continue
    return isdate


def has_not_a_date_in_password(password):
    date = password
    digit_list = get_numbers_from_password(password)
    date = "".join(digit_list)
    good_password = not bool(date_check(date))
    return good_password


def has_not_a_telephone_number(password):
    digit_list = get_numbers_from_password(password)
    have_not_a_phone = True
    string_length_one = 11
    string_length_two = 7
    string_length_three = 6
    bad_first_digit_one = "0"
    bad_first_digit_two = "1"
    first_digit_one = "7"
    first_digit_two = "8"
    first_symbol = 0

    if len(digit_list) == string_length_one:
        if digit_list[first_symbol] == first_digit_one or \
           digit_list[first_symbol] == first_digit_two:
            have_not_a_phone = False

    if len(digit_list) == string_length_two or \
       len(digit_list) == string_length_three:
        if digit_list[first_symbol] != bad_first_digit_one and \
           digit_list[first_symbol] != bad_first_digit_two:
            have_not_a_phone = False
    return have_not_a_phone


def has_not_license_plate_numbers(password):
    plase_number = ""
    have_not_plate_number = True
    regular_one = r"[a-z]{1}\d\d\d[a-z]{1}[a-z]{1}"
    regular_two = r"[A-Z]{1}\d\d\d[A-Z]{1}[A-Z]{1}"
    find_plate_one = re.search(regular_one, password)
    find_plate_two = re.search(regular_two, password)
    if find_plate_one or find_plate_two:
        have_not_plate_number = False
    return have_not_plate_number
