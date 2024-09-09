from cryptography.fernet import Fernet

# we have to run only oncy to generate key and store it in key.key
def generate_key():
    #Generate and save an encryption key
    key = Fernet.generate_key()
    with open('secure_storage/key.key', 'wb') as key_file:
        key_file.write(key)


def load_key():
    #Load the previously generated key
    return open('secure_storage/key.key', 'rb').read()


def encrypt_password(password):
    #Encrypt a password
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password(encrypted_password):
    #Decrypt an encrypted password
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()