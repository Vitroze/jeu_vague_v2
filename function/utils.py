import os
import inquirer

def clear():
    os.system("cls")

def request_option(choice: dict):
    while True:
        choose = inquirer.prompt([
            inquirer.List(
                "id",
                message = "Quel option souhaitez-vous choisir ?",
                choices=[(option.get("name"), index) for index, option in enumerate(choice)]
            )
        ])

        if choose != None and choose.get("id") is None:
            continue

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
    request_user = request_user.get("request")

    if request_user != None and len(request_user) < 3:
        return request_string(text)

    return request_user