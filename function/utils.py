import os
import inquirer

def clear():
    os.system("cls")

def convert_option(choice: dict) -> list:
    choice = [(option.get("name"), index) for index, option in enumerate(choice)]
    choice.append(("Quitter", len(choice) + 1))
    return choice

def request_option(choice: dict):
    while True:
        option_list = convert_option(choice)
        choose = inquirer.prompt([
            inquirer.List(
                "id",
                message = "Quel option souhaitez-vous choisir ?",
                choices=option_list
            )
        ])

        if choose is None or choose.get("id") == len(option_list):
            exit()

        choose = choose.get("id")
        if not choice_valid_by_key(choose, choice):
            continue

        return choose

def is_number(number: str) -> bool:
    return number.isdigit()

def choice_valid_by_key(input: int, choice:dict)->bool:
    try:
        return choice[input] != None
    except:
        return False

def is_valid_list(list_input: list)->bool:
    return list_input and type(list_input) == list and len(list_input) > 0

def request_string(text:str):
    request_user = inquirer.prompt([
        inquirer.Text("request", message=text)
    ])

    if request_user is None:
        exit()

    request_user = request_user.get("request")
    if len(request_user) < 3:
        return request_string(text)

    return request_user