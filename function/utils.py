import os
import inquirer
import hashlib
import hmac
from meta.exceptions import UserQuit

def clear():
    os.system("cls")

def convert_option(choice: dict, key:str = None) -> list:
    choice = [(option.get(key is not None and key or "name"), index) for index, option in enumerate(choice)]
    choice.append(("Quitter", len(choice) + 1))
    return choice

def request_option(choice: dict, key:str = None):
    while True:
        option_list = convert_option(choice, key)
        choose = inquirer.prompt([
            inquirer.List(
                "id",
                message = "Quel option souhaitez-vous choisir ?",
                choices=option_list
            )
        ])

        if choose is None or choose.get("id") == len(option_list):
            raise UserQuit("Vous avez quitté pendant la sélection d'une option")

        choose = choose.get("id")
        if not choice_valid_by_key(choose, choice):
            continue

        return choose

def is_number(number: str) -> bool:
    return number.isdigit()

def choice_valid_by_key(input: int, choice:dict)->bool:
    try:
        return choice[input] != None
    except Exception:
        return False

def is_valid_list(list_input: list)->bool:
    return list_input and isinstance(list_input, list) and len(list_input) > 0

def request_string(text:str, limit_char=3, default=None):
    request_user = inquirer.prompt([
        inquirer.Text("request", message=text, default=default)
    ])

    if request_user is None:
        raise UserQuit("Vous avez quitté pendant la demande d'écriture")

    request_user = request_user.get("request")
    if len(request_user) == 0 and default:
        return default

    if len(request_user) < limit_char:
        return request_string(text, limit_char, default)

    return request_user

def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value

def bounds(value, value_min=None, value_max=None):
    if value_min and value_max:
        return clamp(value, value_min, value_max)
    elif value_min is None and value_max:
        return min(value, value_max)
    elif value_max is None and value_min:
        return max(value, value_min)
    else:
        return value

def request_number(text:str, min=None, max=None, default=None)->int:
    request_user = request_string(text, 1, default)
    if not is_number(request_user):
        return request_number(text, min, max, default)

    request_user = int(request_user)
    return bounds(request_user, min, max)

def request_bool(text:str, default=None):
    if default:
        text = f"{text} (Défaut : {default})"

    request_user = inquirer.prompt([
        inquirer.Confirm("request", message=text, default=default)
    ])

    if request_user is None:
        raise UserQuit("Vous avez quitté pendant la demande d'une confirmation")

    request_user = request_user.get("request")
    return request_user

def transform_input_topassword(input_user:str, salt_hex, iteration):
    input_user = hashlib.pbkdf2_hmac(
        "sha256", input_user.encode("utf-8"), salt_hex, iteration
    )

    return input_user

def request_password(text:str):
    request_user = inquirer.prompt([
        inquirer.Password("request", message=text)
    ])

    if request_user is None:
        raise UserQuit("Vous avez quitté pendant la saisi d'un mot de passe")

    request_user = request_user.get("request")
    if len(request_user) < 3:
        return request_password(text)

    return request_user


def password_is_correct(input_user:str, password:str):
    iteration, salt_hex, key_hex = password.split("$")

    iteration = int(iteration)
    salt_hex = bytes.fromhex(salt_hex)
    key_hex = bytes.fromhex(key_hex)

    input_user = transform_input_topassword(input_user, salt_hex, iteration)

    return hmac.compare_digest(key_hex, input_user)


def clear_text(text: str)->str:
    """Mettre en minuscule, supprimer les espaces en trops"""
    return text.lower().strip()