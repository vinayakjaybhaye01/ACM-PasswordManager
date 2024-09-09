from getpass import getpass
import hashlib
import json
from rich import print as printc
from utils.config import config  # Import config() function
from utils.helper import encrypt_password, decrypt_password
from cryptography.fernet import Fernet
import os
import random 
import string

# generate a password
def generate_password(length=12, complexity='medium'):
    """Generate a strong random password"""
    characters = string.ascii_letters + string.digits
    if complexity == 'high':
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Authenticate the user by checking the master password
def authenticate():
    try:
        with open('database.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        printc("[red][-][/red] No master password found. Setting up...")
        config()  # Call config to set up the master password if it doesn't exist
        return authenticate()

    hashed_mp = data.get('hashed_master_password', '')

    while True:
        mp = getpass("Enter Master Password to Authenticate: ")
        entered_hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

        if entered_hashed_mp == hashed_mp:
            printc("[green][+][/green] Authentication successful!")
            return True
        else:
            printc("[red][-][/red] Incorrect password. Please try again.")


# Add password logic (stored in passwords.json)
def add_password():
    if authenticate():
        account_name = input("Enter the Account Name: ")
        username = input("Enter the Username: ")

        generate = input("Do you want to generata a strong password ? (y/n): ").lower()
        if generate == 'y':
            password = generate_password();
        else:
            password = getpass("Enter the Password: ")
        
        # encrypt password
        encrypted_password = encrypt_password(password)

        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"passwords": []}

        # Store the password (encryption part can be added)
        new_entry = {
            "account_name": account_name,
            "username": username,
            "password": encrypted_password.decode()  # For now plain-text, encryption can be added
        }

        data["passwords"].append(new_entry)

        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)

        printc("[green][+][/green] Password added successfully!")


# Update an existing password
def update_password():
    if authenticate():
        account_name = input("Enter the Account Name to Update: ")

        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            printc("[red][-][/red] No passwords found!")
            return

        for entry in data["passwords"]:
            if entry["account_name"] == account_name:
                new_password = getpass("Enter the New Password: ")
                encrypted_newpass = encrypt_password(new_password)
                entry["password"] = encrypted_newpass.decode()  # Update the password
                break
        else:
            printc(f"[red][-][/red] No account found with name: {account_name}")
            return

        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)

        printc(f"[green][+][/green] Password for {account_name} updated successfully!")


# Delete a password
def delete_password():
    if authenticate():
        account_name = input("Enter the Account Name to Delete: ")

        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            printc("[red][-][/red] No passwords found!")
            return

        for entry in data["passwords"]:
            if entry["account_name"] == account_name:
                confirm = input(f"Are you sure you want to delete the password for {account_name}? (y/n): ")
                if confirm.lower() == 'y':
                    data["passwords"].remove(entry)
                    break
        else:
            printc(f"[red][-][/red] No account found with name: {account_name}")
            return

        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)

        printc(f"[green][+][/green] Password for {account_name} deleted successfully!")

# View all saved passwords
def view_passwords():
    if authenticate():
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            printc("[red][-][/red] No passwords found!")
            return

        printc("[cyan][*][/cyan] Saved Passwords:")
        for entry in data["passwords"]:
            printc(f"[blue]Account Name:[/blue] {entry['account_name']}")
            printc(f"[blue]Username:[/blue] {entry['username']}")
            # Passwords are not shown directly for security reasons
            printc("[blue]Password:[/blue] [hidden]")
            print()  

        while True:
            reveal = input("Do you want to reveal a specific password? (y/n): ").lower()
            if reveal == 'y':
                account_name = input("Enter the Account Name to Reveal Password: ")
                for entry in data["passwords"]:
                    if entry["account_name"] == account_name:
                        printc(f"[blue]Account Name:[/blue] {entry['account_name']}")
                        printc(f"[blue]Username:[/blue] {entry['username']}")
                        encrypted_password = entry['password']
                        decrypted_password = decrypt_password(encrypted_password)
                        printc(f"[blue]Password:[/blue] {decrypted_password}")
                        break
                else:
                    printc(f"[red][-][/red] No account found with name: {account_name}")
            elif reveal == 'n':
                break
            else:
                printc("[red][-][/red] Invalid choice, please enter 'y' or 'n'.")


# Main menu
def main():
    while True:
        print("\nPassword Manager Options:")
        print("1. Add Password")
        print("2. Update Password")
        print("3. Delete Password")
        print("4. View Passwords")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_password()
        elif choice == '2':
            update_password()
        elif choice == '3':
            delete_password()
        elif choice == '4':
            view_passwords()
        elif choice == '5':
            break
        else:
            printc("[red][-][/red] Invalid choice, try again.")


if __name__ == "__main__":
    main()
