from dotenv import load_dotenv
from function.logger import print_success, print_debug, print_error
from time import sleep
import pymongo as DataBase
import os

load_dotenv()

URL_MONGODB, DATABASE_NAME = os.getenv("MONGODB_URL"), os.getenv("MONGODB_NAME_DATABASE")
DB = None
IS_CONNECT = False
PRINT_TITLE = "Base de donnée"

def show_no_connection():
    print_error(PRINT_TITLE, "La base de donnée n'est pas connecté")

def show_already_connection():
    print_success(PRINT_TITLE, "La base de donnée est déjà connecté")

def is_connected(fc):
    def callback(*args, **kwars):
        if not IS_CONNECT:
            show_no_connection()
            return

        return fc(*args, **kwars)

    return callback

def is_not_connected(fc):
    def callback(*args, **kwars):
        if IS_CONNECT:
            show_already_connection()
            return

        return fc(*args, **kwars)

    return callback

def check_config():
    if not URL_MONGODB or len(URL_MONGODB) < 3:
        print_error(PRINT_TITLE, "Renseignez URL de conenxion de la base de donnée")
        return False

    if not DATABASE_NAME or len(DATABASE_NAME) < 1:
        print_error(PRINT_TITLE, "Renseignez le nom de la base de donnée")
        return False

    return True

@is_not_connected
def connect():
    global DB

    if not check_config():
        exit()
        return

    client = DataBase.MongoClient(URL_MONGODB)
    DB = client[DATABASE_NAME]

    print_debug(PRINT_TITLE, "Tentative de connexion a la base de donnée.")

    send_ping(client)

    collection_list = DB.list_collection_names()
    connect_success()

    try:
        create_tables(collection_list)
    except Exception:
        print_error(PRINT_TITLE, "Impossible de crée ou de récupérer les tables")
        exit()

    print_success(PRINT_TITLE, "Création/Récupération des tables avec succès.")
    sleep(1)

def connect_success():
    global IS_CONNECT
    print_success(PRINT_TITLE, "Connexion réussit !")
    IS_CONNECT = True
    print_debug(PRINT_TITLE, "Initialisation des tables...")

def send_ping(client):
    try:
        client.admin.command('ping')
    except Exception:
        print_error(PRINT_TITLE, "Impossible de communiquer avec la base de donnée [TIMED-OUT]")
        exit()
        return

@is_connected
def create_table(name, collection_list):
    name = f"{DATABASE_NAME}_{name}"
    if name not in collection_list:
        DB.create_collection(name)

@is_connected
def create_tables(collection_list):
    create_table("config", collection_list)
    create_table("playerdata", collection_list)
    create_table("items", collection_list)

@is_connected
def get_database():
    return DB

@is_connected
def get_collection(name):
    name = f"{DATABASE_NAME}_{name}"
    return DB[name]

#print(get_collection("config"))