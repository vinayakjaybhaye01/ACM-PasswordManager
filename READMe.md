Required modules in requirements.txt


Features & Working: (All instructions are shown while running script)

Master Password Authentication:

The first time you run the application, it prompts you to set up a master password.
Every subsequent use requires entering the master password for authentication.
Add Password:

Add new account credentials (account name, username, and password).
Option to generate a strong random password automatically or enter your own.

Passwords are encrypted using the Fernet symmetric encryption before storage.
Update Password:

Modify existing passwords for a specific account by entering the account name.
The new password is encrypted before replacing the old password.

Delete Password:
Remove an account’s credentials from the database by specifying the account name.
Confirmation is required before deletion.

View Passwords:
View a list of stored accounts along with their usernames.

Option to reveal and decrypt specific account passwords.
Decrypted passwords are automatically copied to the clipboard using pyperclip for quick access.
Password Storage:

Passwords and other data are stored in JSON files inside a secure storage directory (secure_storage/passwords.json and secure_storage/database.json).

Clipboard Support:
The revealed passwords are copied to the clipboard to avoid displaying them in plain text, enhancing security.

