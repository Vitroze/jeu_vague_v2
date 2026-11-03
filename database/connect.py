from dotenv import load_dotenv
from function.logger import print_success, print_debug, print_error
from time import sleep
import pymongo as DataBase
import os

load_dotenv()

URL_MONGODB, DATABASE_NAME = os.getenv("MONGODB_URL"), os.getenv("MONGODB_NAME_DATABASE")
DB = None
IS_CONNECT = False

def show_no_connection():
    print_error("Base de donnée", "La base de donnée n'est pas connecté")

def is_connected(fc):
    def callback(*args, **kwars):
        if not IS_CONNECT:
            show_no_connection()
            return

        return fc(*args, **kwars)

    return callback

def connect():
    global DB
    global IS_CONNECT

    client = DataBase.MongoClient(URL_MONGODB)
    DB = client[DATABASE_NAME]

    print_debug("Base de donnée", "Tentative de connexion a la base de donnée.")

    try:
        client.admin.command('ping')
    except Exception:
        print_error("Base de donnée", "Impossible de communiquer avec la base de donnée [TIMED-OUT]")
        exit()
        return

    collection_list = DB.list_collection_names()

    print_success("Base de donnée", "Connexion réussit !")
    IS_CONNECT = True
    print_debug("Base de donnée", "Initialisation des tables...")

    try:
        create_tables(collection_list)
    except Exception:
        print_error("Base de donnée", "Impossible de crée ou de récupérer les tables")

    print_success("Base de donnée", "Création/Récupération des tables avec succès.")
    sleep(1)

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