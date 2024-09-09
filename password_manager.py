from cryptography.fernet import Fernet
import os

#run only once to generate a key and save it to file key.key
def generate_key():
    """Generate and save an encryption key"""
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)


def load_key():
    """Load the previously generated key"""
    return open('key.key', 'rb').read()


def encrypt_password(password):
    """Encrypt a password"""
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password):
    """Decrypt an encrypted password"""
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()


import json

def add_password(account, username, password):
    """Add a new password entry"""
    encrypted_password = encrypt_password(password)
    new_entry = {
        'account': account,
        'username': username,
        'password': encrypted_password.decode()  # Store as string
    }

    # Save the entry to a JSON file
    with open('passwords.json', 'a') as f:
        json.dump(new_entry, f)
        f.write('\n')  # Separate entries by new lines


def view_passwords():
    """View all saved accounts (without revealing passwords)"""
    master_password = input("Enter your master password: ")
     
    # Getting masterpassword from json file masterpassword.json
    with open('masterpassword.json', 'r') as f:
        data = json.load(f) 
        MASTERPASSWORD = data['masterPassword'];
    
    if master_password == MASTERPASSWORD:  
        with open('passwords.json', 'r') as f:
            for line in f:
                entry = json.loads(line)
                print(f"Account: {entry['account']}, Username: {entry['username']}")
    else:
        print("Incorrect master password.")





def delete_password(account_name):
    """Delete a saved password entry by account name"""
    with open('passwords.json', 'r') as f:
        lines = f.readlines()

    with open('passwords.json', 'w') as f:
        for line in lines:
            entry = json.loads(line)
            if entry['account'] != account_name:
                f.write(line)  # Re-write non-deleted entries
            else:
                password = input("Enter your password :");
                PASSWORD = decrypt_password(entry['password'])
                if(PASSWORD == password):
                   print(f"Deleted password for account: {account_name}")
                else:
                    print("Incorrect Password Entered:")
                    f.write(line)




def update_password(account_name):
    """Update the password for an existing account"""
    with open('passwords.json', 'r') as f:
        lines = f.readlines()

    with open('passwords.json', 'w') as f:
        for line in lines:
            entry = json.loads(line)
            if entry['account'] == account_name:
                PASSWORD = decrypt_password(entry['password'])
                oldpass = input("Enter old password :")
                if(PASSWORD == oldpass):
                    new_password = input("Enter new password :")
                    entry['password'] = encrypt_password(new_password).decode()  # Update password
                    print(f"Updated password for account: {account_name}")
                    f.write(json.dumps(entry) + '\n')
                else:
                    print("Incorrect Password Entered:")

import random
import string

def generate_password(length=12, complexity='medium'):
    """Generate a strong random password"""
    characters = string.ascii_letters + string.digits
    if complexity == 'high':
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



import argparse

parser = argparse.ArgumentParser(description="Terminal-based Password Manager")
parser.add_argument('action', help="add, view, update, delete, generate")
parser.add_argument('--account', help="Account name")
parser.add_argument('--username', help="Username")
parser.add_argument('--password', help="Password")
parser.add_argument('--length', type=int, help="Password length for generation")

args = parser.parse_args()

if args.action == 'add':
    add_password(args.account, args.username, args.password)
elif args.action == 'view':
    view_passwords()
elif args.action == 'delete':
    delete_password(args.account)
elif args.action == 'update':
    update_password(args.account)
elif args.action == 'generate':
    print(generate_password(args.length or 12))
