from rich import print as printc
from rich.console import Console
console = Console()

from getpass import getpass
import hashlib
import json
from cryptography.fernet import Fernet




def insertToDataBase(hashed_mp):
    data = {
        "hashed_master_password": hashed_mp
    }
    with open('secure_storage/database.json', 'w') as file:
        json.dump(data, file)
    printc("[green][+][/green] Data stored in database.json")


#Interact with json files as they act as database
def config():
#get a masterpassword
    while 1:
        mp = getpass("Enter Your MasterPassword")
        if mp == getpass("Re-Type MasterPassword: ") and mp != "":
            break
        printc("[yellow][-] Please try again.[/yellow]")
    
    #Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")
       

    #insert masterpassword to json file(database.json)
    insertToDataBase(hashed_mp)

