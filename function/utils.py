import os

def clear():
    os.system("cls")

def show_option(options: dict):
    id = 0
    for option in options:
        print(f"{id}. {option["name"]}")
        id += 1

def request_option(choice: dict):
    while True:
        choose = input("Quel option souhaitez-vous choisir ?")
        if not is_number(choose):
            continue

        choose = int(choose)
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
    request_user = input(text + " : ")
    if not request_user or len(request_user) < 3:
        return request_string(text)

    return request_user