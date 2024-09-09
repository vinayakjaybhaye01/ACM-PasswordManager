from rich import print as printc
from rich.console import Console
console = Console()

from getpass import getpass
import hashlib
import random 
import string
import json
from cryptography.fernet import Fernet



def generateDeviceSecret(length = 10):
    return ''.join(random.choices(string.ascii_uppercase +string.digits, k = length))

# def generateDeviceSecret():
#     """Generate and save an encryption key"""
#     key = Fernet.generate_key()
#     return key

def insertToDataBase(hashed_mp, deviceSec):
    data = {
        "hashed_master_password": hashed_mp,
        "device_secret": deviceSec
    }
    with open('database.json', 'w') as file:
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
    
    
    #Generate device secret
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device Secret generated")


    #insert masterpassword and devicesecret to json files(database)
    insertToDataBase(hashed_mp, ds)

