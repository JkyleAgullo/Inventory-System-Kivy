import os
import main
from Security import Security
from Account import Account
import Terminal
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Global Variables
account_dir = "accounts"
console = None
username = None
password = None
eusern = None
epass = None
admin_fp = None
cashier_fp = None

def input_validation():
    while True:
        try:
            choice = int(input("Select: "))
            return choice
        except ValueError:
            return -1

def login():
    while True:
        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-= INVENTORY LOGIN =-=-=")
        Terminal.gotoxy(15, 13)
        print("(1) Cashier")
        Terminal.gotoxy(15, 15)
        print("(2) Admin")
        Terminal.gotoxy(15, 17)
        print("(0) Exit")
        Terminal.gotoxy(15, 20)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        Terminal.gotoxy(15, 22)
        choice = input_validation()

        if choice == 0:
            main.back_to_login = False
            return 0

        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-=-= LOG IN =-=-=-=")
        Terminal.gotoxy(15, 13)
        username = input("Enter username: ")
        Terminal.gotoxy(15, 15)
        password = input("Enter password: ")

        if choice == 1:
            if username == main.cashier_acc.get_username():
                if password == main.cashier_acc.get_password():
                    return 1    # if found
        elif choice == 2:
            if username == main.admin_acc.get_username():
                if password == main.admin_acc.get_password():
                    return 2    # if found
        # if not found
        Terminal.gotoxy(15, 18)
        print("=-=-=-=-=-=-=-=-=-=-=-")
        Terminal.gotoxy(15, 20)
        print("INVALID USERNAME OR PASSWORD")
        Terminal.gotoxy(15, 22)
        input("Press enter to continue...")

def save_account():
    admin_fp = Security.encrypt(Security.get_admin_filename(), Security.get_secret_key())
    cashier_fp = Security.encrypt(Security.get_cashier_filename(), Security.get_secret_key())

    # ADMIN ACCOUNT
    try:
        with open(os.path.join(os.getcwd(), account_dir, f"{admin_fp}.txt"), "w") as writer:
            if main.admin_acc.get_username() is not None:
                eusern = Security.encrypt(main.admin_acc.get_username(), Security.get_secret_key())
                epass = Security.encrypt(main.admin_acc.get_password(), Security.get_secret_key())
                writer.write(eusern + '\n')
                writer.write(epass + '\n')
            else:
                popup_content = Label(text="NO ADMIN ACCOUNTS YET")
                popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
                print("No ADMIN accounts yet")
    except IOError as e:
        print("Error during admin file writing: ", e)

    # CASHIER ACCOUNT
    try:
        with open(os.path.join(os.getcwd(), account_dir, f"{cashier_fp}.txt"), "w") as writer:
            if main.cashier_acc.get_username() is not None:
                eusern = Security.encrypt(main.cashier_acc.get_username(), Security.get_secret_key())
                epass = Security.encrypt(main.cashier_acc.get_password(), Security.get_secret_key())
                writer.write(eusern + '\n')
                writer.write(epass + '\n')
            else:
                popup_content = Label(text="NO CASHIERACCOUNTS YET")
                popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
                print("No CASHIER accounts yet")
    except IOError as e:
        popup_content = Label(text="ERROR DURING CASHIER FILE WRITING")
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
        print("Error during cashier file writing: ", e)

def retrieve_account():
    admin_fp = Security.encrypt(Security.get_admin_filename(), Security.get_secret_key())
    cashier_fp = Security.encrypt(Security.get_cashier_filename(), Security.get_secret_key())
    admin_dir = os.path.join(os.getcwd(), account_dir, f"{admin_fp}.txt")
    cashier_dir = os.path.join(os.getcwd(), account_dir, f"{cashier_fp}.txt")

    # ADMIN ACCOUNT
    file_size = os.stat(admin_dir).st_size
    if not file_size == 0:
        try:
            with open(admin_dir, "r") as reader:
                for line in reader:
                    if line != '':
                        eusern = line.strip()
                        epass = next(reader).strip()
                        username = Security.decrypt(eusern, Security.get_secret_key())
                        password = Security.decrypt(epass, Security.get_secret_key())
                        main.admin_acc = Account(username, password)
        except IOError as e:
            popup_content = Label(text="ERROR DURING ADMIN ACCOUNT RETRIEVING")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            print("Error occurred during admin account retrieving: ", e)

    # CASHIER ACCOUNT
    file_size = os.stat(cashier_dir).st_size
    if not file_size == 0:
        try:
            with open(cashier_dir, "r") as reader:
                for line in reader:
                    if line != '':
                        eusern = line.strip()
                        epass = next(reader).strip()
                        username = Security.decrypt(eusern, Security.get_secret_key())
                        password = Security.decrypt(epass, Security.get_secret_key())
                        main.cashier_acc = Account(username, password)
        except IOError as e:
            popup_content = Label(text="ERROR DURING ADMIN ACCOUNT RETRIEVING")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            print("Error occurred during admin account retrieving: ", e)

    return main.admin_acc, main.cashier_acc
