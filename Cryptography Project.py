import os
from cryptography.fernet import Fernet
import tkinter as tk

# Create main window
window = tk.Tk()
window.title("Password Manager")
window.geometry("600x500")
window.config(bg="white") # Set color of the background window

# Create the key file even if it does not actually exist
if not os.path.exists("key.key"):
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("key.key", "rb") as key_file:
        key = key_file.read()

# Define perticular function for GUI
def view_passwords():
    password_file_path = password_file_path_entry.get()
    passwords_listbox.delete(0, tk.END)
    with open(password_file_path, 'r') as f:
        for line in f:
            data = line.rstrip()
            account_name, encrypted_password = data.split("|")
            password = decrypt_password(encrypted_password.encode(), key)
            passwords_listbox.insert(tk.END, f"Account: {account_name} | Password: {password}")

def add_password():
    password_file_path = password_file_path_entry.get()
    account_name = account_name_entry.get()
    password = password_entry.get()
    encrypted_password = encrypt_password(password, key).decode()
    with open(password_file_path, 'a') as f:
        f.write(f"{account_name}|{encrypted_password}\n")
    passwords_listbox.insert(tk.END, f"Account: {account_name} | Password: {password}")
    account_name_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def encrypt_password(password, key):
    fer = Fernet(key)
    return fer.encrypt(password.encode())

def decrypt_password(encrypted_password, key):
    fer = Fernet(key)
    return fer.decrypt(encrypted_password).decode()

# Create widgets using GUI
canvas = tk.Canvas(window, height=500, width=600, bg="black")
canvas.pack()

password_file_path_label = tk.Label(window, text="Password File Path:", bg="blue", fg="yellow")
password_file_path_entry = tk.Entry(window)
account_name_label = tk.Label(window, text="Account Name:", bg="blue", fg="yellow")
account_name_entry = tk.Entry(window)
password_label = tk.Label(window, text="Password:", bg="blue", fg="yellow")
password_entry = tk.Entry(window, show="*")
view_passwords_button = tk.Button(window, text="View Passwords", command=view_passwords, bg="red", fg="yellow")
add_password_button = tk.Button(window, text="Add Password", command=add_password, bg="red", fg="yellow")
passwords_listbox = tk.Listbox(window, width=40)

# Adding widgets to the canvas
canvas.create_window(200, 50, window=password_file_path_label)
canvas.create_window(400, 50, window=password_file_path_entry)
canvas.create_window(200, 100, window=account_name_label)
canvas.create_window(400, 100, window=account_name_entry)
canvas.create_window(200, 150, window=password_label)
canvas.create_window(400, 150, window=password_entry)
canvas.create_window(300, 200, window=view_passwords_button)
canvas.create_window(300, 250, window=add_password_button)
canvas.create_window(300, 350, window=passwords_listbox)

# End GUI loop
window.mainloop()
