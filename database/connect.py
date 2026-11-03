from dotenv import load_dotenv
#from function.logger import print_success, print_debug, print_error
import pymongo as DataBase
import os

load_dotenv()

URL_MONGODB, DATABASE_NAME = os.getenv("MONGODB_URL"), os.getenv("MONGODB_NAME_DATABASE")
DB = None


def connect():
    global DB

    client = DataBase.MongoClient(URL_MONGODB)
    DB = client[DATABASE_NAME]
    try:
        client.admin.command('ping')
    except Exception:
        print("Impossible de communiquer avec la base de donnée [TIMED-OUT]")
        return

    collection_list = DB.list_collection_names()

    create_tables(collection_list)

def create_table(name, collection_list):
    name = f"{DATABASE_NAME}_{name}"
    if name not in collection_list:
        DB.create_collection(name)

def create_tables(collection_list):
    create_table("config", collection_list)
    create_table("playerdata", collection_list)
    create_table("items", collection_list)

def get_database():
    return DB

def get_collection(name):
    name = f"{DATABASE_NAME}_{name}"
    return DB[name]

connect()
#print(get_collection("config"))