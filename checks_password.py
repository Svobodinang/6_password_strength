from datetime import datetime


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


def get_abbreviation(last_name, name, patronymic):
    if patronymic != "":
        abbreviation = last_name[0] + name[0] + patronymic[0]
    else:
        abbreviation = last_name[0] + name[0]
    return abbreviation


def have_abbreviation(password, last_name, name, patronymic):
    abbreviation = get_abbreviation(last_name, name, patronymic)
    have_abbreviation = False
    if password.find(abbreviation) != -1:
        have_abbreviation = True
    return have_abbreviation


def get_numbers_from_password(password):
    list_digit = []
    for letter in password:
        if letter.isdigit():
            list_digit.append(letter)
    return list_digit


def have_a_date_in_password(password):
    digit = password
    list_digit = get_numbers_from_password(password)
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
    list_digit = get_numbers_from_password(password)
    have_a_phone = False
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
