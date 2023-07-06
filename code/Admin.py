import os
import glob
import getpass
from Inventory import Inventory
from Category import Category
from Security import Security
import DataManager
import DateManager
import main
import Authen
import Terminal
global choice
global status

def admin():
    product = Inventory()
    while True:
        while True:
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("=-=-= ADMIN INVENTORY =-=-=")
            Terminal.gotoxy(19, 13)
            print("(1) Add Product")
            Terminal.gotoxy(19, 15)
            print("(2) Display")
            Terminal.gotoxy(19, 17)
            print("(3) Settings")
            Terminal.gotoxy(19, 19)
            print("(0) Log out")
            Terminal.gotoxy(15, 22)
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            Terminal.gotoxy(15, 25)
            choice = Authen.input_validation()
            if choice != -1 or 0 <= choice <= 3:
                break

        Terminal.clear_screen()
        if choice == 0:
            break
        elif choice == 1:
            Terminal.gotoxy(15, 10)
            print("=-=-= ADD PRODUCT =-=-=")
            product.category = Category.set_get_category()
            print(product.category)
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("=-=-= ADD PRODUCT =-=-=")
            Terminal.gotoxy(15, 13)
            print("Category: " + product.category)
            Terminal.gotoxy(15, 15)
            product.name = input("Product Name: ").upper()
            Terminal.gotoxy(15, 17)
            product.orig_price = round(float(input("Price (each): ")), 2)
            Terminal.gotoxy(15, 19)
            product.qty = int(input("Quantity: "))
            # set total price
            product.total_price = product.qty * product.orig_price
            Terminal.gotoxy(15, 21)
            product.retail_price = round(float(input("Retail price (each): ")), 2)
            # Get the current date/time
            product.date = DateManager.get_date()
            # Set and get expiration date
            product.exp_date = DateManager.set_get_expiration_date(product.category)

            # locate if already exist or not
            pos = main.locate_product(product)
            if pos == -1:
                product.sales_qty = 0
                product.total_sales_amount = 0
                product.profit = product.total_price * -1
                status = add_product(product)
            else:
                # if exist update the product
                status = update_product(product, pos)

            # status check
            if status == 1:
                Terminal.gotoxy(15, 24)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-")
                Terminal.gotoxy(15, 26)
                print("ADDED SUCCESSFULLY")
                DataManager.record_product(product)
                DataManager.save()
                Terminal.gotoxy(15, 28)
                input("Press enter to continue...")
            else:
                Terminal.gotoxy(15, 24)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-")
                Terminal.gotoxy(15, 26)
                print("ADD FAILED")
                Terminal.gotoxy(15, 28)
                input("Press enter to continue...")
        elif choice == 2:
            display()
        elif choice == 3:
            settings()

def add_product(my_product):
    if main.is_full() == 1:
        print("\nARRAY IS FULL", end="\n\n")
        input("Press enter to continue...")
    else:
        if my_product.qty <= main.MAX_PROD_STOCK:
            main.marker += 1
            inventory_data = Inventory(
                my_product.category, my_product.name, my_product.date,
                my_product.exp_date, my_product.orig_price, my_product.qty,
                my_product.total_price, my_product.retail_price, my_product.sales_qty,
                my_product.total_sales_amount, my_product.profit
            )
            main.my_inv[main.marker] = inventory_data
            return 1
        else:
            print("\nQUANTITY LIMIT EXCEEDED", end="\n\n")
            input("Press enter to continue...")
            return -1
    return -1


def update_product(my_product, index_pos):
    if (main.my_inv[index_pos].qty + my_product.qty) > main.MAX_PROD_STOCK:
        print("QUANTITY LIMIT EXCEEDED FOR: " + main.my_inv[index_pos].name)
        return -1
    else:
        main.my_inv[index_pos].date = my_product.date
        main.my_inv[index_pos].exp_date = my_product.exp_date
        main.my_inv[index_pos].orig_price = my_product.orig_price
        main.my_inv[index_pos].qty += my_product.qty
        main.my_inv[index_pos].total_price = my_product.orig_price * main.my_inv[index_pos].qty
        main.my_inv[index_pos].retail_price = my_product.retail_price
        main.my_inv[index_pos].profit -= my_product.qty * my_product.orig_price
        return 1


def display():
    while True:
        choice = display_menu()
        if choice == -1:
            Terminal.gotoxy(15, 25)
            print("| PLEASE CHOOSE AMONG THE CHOICES ONLY |")
            Terminal.gotoxy(15, 27)
            input("Press enter to continue...")
        elif choice == 1:
            display_inventory()
        elif choice == 2:
            display_sales_history()
        elif choice == 3:
            display_expired_history()
        if choice == 0:
            break


def display_menu():
    Terminal.clear_screen()
    Terminal.gotoxy(15, 10)
    print("=-=-= DISPLAY SETTINGS =-=-=")
    Terminal.gotoxy(15, 13)
    print("(1) Inventory")
    Terminal.gotoxy(15, 15)
    print("(2) Sales History")
    Terminal.gotoxy(15, 17)
    print("(3) Expired Product History")
    Terminal.gotoxy(15, 19)
    print("(0) Back")
    Terminal.gotoxy(15, 22)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    Terminal.gotoxy(15, 25)
    choice = Authen.input_validation()
    return choice


def display_inventory():
    Terminal.clear_screen()
    i = 0
    my_inventory = [item for item in main.my_inv if item.name is not None]
    my_inventory = sorted(my_inventory, key=lambda x: x.name)

    # is empty
    if main.marker == -1:
        Terminal.gotoxy(50, 13)
        print("| NOTHING IS IN THE INVENTORY | ")
        Terminal.design_box(48, 11, 5, 35)
        Terminal.gotoxy(50, 17)
        input("Press enter to continue...")
    else:
        Terminal.gotoxy(17, 13)
        print("MAX PRODUCT: ", str(main.MAX_INV))
        Terminal.gotoxy(17, 14)
        print("MAX STOCK PER PRODUCT: ", str(main.MAX_PROD_STOCK))
        Terminal.gotoxy(86, 13)
        print("INVENTORY REPORT")
        Terminal.design_box(60, 12, 3, 69)
        Terminal.gotoxy(15, 17)
        print("No")
        Terminal.gotoxy(25, 17)
        print("Date")
        Terminal.gotoxy(38, 17)
        print("Product Name")
        Terminal.gotoxy(56, 17)
        print("Orig Price")
        Terminal.gotoxy(71, 17)
        print("Quantity")
        Terminal.gotoxy(84, 17)
        print("Total Amount")
        Terminal.gotoxy(102, 17)
        print("Retail Price")
        Terminal.gotoxy(120, 17)
        print("Sales Quantity")
        Terminal.gotoxy(139, 17)
        print("Total Sales Amount")
        Terminal.gotoxy(165, 17)
        print("Profit")

        # border
        for i in range(main.marker + 3):
            if i == 1:
                for j in range(13, 179):
                    Terminal.gotoxy(j, 16)
                    print("-")
                    Terminal.gotoxy(j, 18)
                    print("-")
                    Terminal.gotoxy(j, 18 + main.marker + 2)
                    print("-")
            else:
                Terminal.gotoxy(13, 17 + i)
                print("|")
                Terminal.gotoxy(19, 17 + i)
                print("|")
                Terminal.gotoxy(34, 17 + i)
                print("|")
                Terminal.gotoxy(53, 17 + i)
                print("|")
                Terminal.gotoxy(68, 17 + i)
                print("|")
                Terminal.gotoxy(81, 17 + i)
                print("|")
                Terminal.gotoxy(98, 17 + i)
                print("|")
                Terminal.gotoxy(117, 17 + i)
                print("|")
                Terminal.gotoxy(136, 17 + i)
                print("|")
                Terminal.gotoxy(159, 17 + i)
                print("|")
                Terminal.gotoxy(178, 17 + i)
                print("|")

        # displaying product status
        for i in range(main.marker + 1):
            Terminal.gotoxy(15, 19 + i)
            print(str(i + 1))
            Terminal.gotoxy(22, 19 + i)
            print(my_inventory[i].date)
            Terminal.gotoxy(38, 19 + i)
            print(my_inventory[i].name)
            formatted_orig_price = "%.2f" % my_inventory[i].orig_price
            Terminal.gotoxy(58, 19 + i)
            print(formatted_orig_price)
            Terminal.gotoxy(73, 19 + i)
            print(my_inventory[i].qty)
            formatted_total_price = "%.2f" % my_inventory[i].total_price
            Terminal.gotoxy(87, 19 + i)
            print(formatted_total_price)
            formatted_retail_price = "%.2f" % my_inventory[i].retail_price
            Terminal.gotoxy(105, 19 + i)
            print(formatted_retail_price)
            Terminal.gotoxy(124, 19 + i)
            print(my_inventory[i].sales_qty)
            formatted_sales_amount = "%.2f" % my_inventory[i].total_sales_amount
            Terminal.gotoxy(143, 19 + i)
            print(formatted_sales_amount)
            formatted_profit = "%.2f" % my_inventory[i].profit
            Terminal.gotoxy(165, 19 + i)
            print(formatted_profit)

        Terminal.gotoxy(20, 23 + i)
        input("Press enter to continue...")


def display_sales_history():
    sales_history_folder_path = os.path.join(os.getcwd(), DataManager.sales_history_folder)
    text_files = glob.glob(sales_history_folder_path + '/*.txt')
    Terminal.clear_screen()
    if len(text_files) == 0:
        print("| SALES HISTORY IS EMPTY |")
    else:
        while True:
            file_date = []
            i = 0
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("=-=-= SALES HISTORY =-=-=")
            for i, file_path in enumerate(text_files, 1):
                file_name = os.path.basename(file_path)     # Get the file name from the file path
                date = os.path.splitext(file_name)[0]       # Remove the file extension to get the date
                file_date.append(date)
                Terminal.gotoxy(15, 11+(i*2))
                print(f"({i}) " + file_date[i-1])
            Terminal.gotoxy(15, 13+(i*2))
            print(f"(0) Back")
            Terminal.gotoxy(15, 16+(i*2))
            print("=-=-=-=-=-=-=-=-=-=-=-=-=")
            Terminal.gotoxy(15, 19+(i*2))
            choice = Authen.input_validation()

            if choice == 0:
                break
            elif 1 <= choice <= len(text_files):
                selected_date = file_date[choice-1]
                display_file(DataManager.sales_history_folder, selected_date)
            else:
                Terminal.gotoxy(15, 18 + (i * 2))
                print("PLEASE CHOOSE AMONG THE CHOICES ONLY")


def display_expired_history():
    expired_history_folder_path = os.path.join(os.getcwd(), DataManager.exp_product_history_folder)
    text_files = glob.glob(expired_history_folder_path + '/*.txt')
    Terminal.clear_screen()

    if len(text_files) == 0:
        Terminal.gotoxy(15, 10)
        print("| EXPIRED PRODUCT HISTORY IS EMPTY |")
        Terminal.gotoxy(15, 12)
        input("Press enter to continue...")
    else:
        while True:
            file_date = []
            i = 0
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("=-=-= EXPIRED PRODUCT HISTORY =-=-=")
            for i, file_path in enumerate(text_files, 1):
                file_name = os.path.basename(file_path)     # Get the file name from the file path
                date = os.path.splitext(file_name)[0]       # Remove the file extension to get the date
                file_date.append(date)
                Terminal.gotoxy(15, 11+(i*2))
                print(f"({i}) " + file_date[i-1])
            Terminal.gotoxy(15, 13+(i*2))
            print(f"(0) Back")
            Terminal.gotoxy(15, 16+(i*2))
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
            Terminal.gotoxy(15, 19+(i*2))
            choice = Authen.input_validation()

            if choice == 0:
                break
            elif 1 <= choice <= len(text_files):
                selected_date = file_date[choice-1]
                display_file(DataManager.exp_product_history_folder, selected_date)
            else:
                Terminal.gotoxy(15, 22 + (i * 2))
                print("PLEASE CHOOSE AMONG THE CHOICES ONLY")
                Terminal.gotoxy(15, 24 + (i * 2))
                input("Press enter to continue...")


def display_file(file_folder, date):
    data_line = None
    colon_index = 0
    my_product = [Inventory() for _ in range(Category.get_category_length())]
    is_exist = False
    ctr = -1
    combined_data = {}

    file = os.path.join(os.getcwd(), file_folder, (date + ".txt"))
    try:
        if not os.path.exists(file):
            raise FileNotFoundError
        else:
            try:
                with open(file, "r") as reader:
                    while True:
                        data_line = reader.readline().strip()
                        if not data_line:
                            break

                        if ":" in data_line:
                            ctr += 1
                            colon_index = data_line.index(":")
                            my_product[ctr].name = data_line[colon_index + 1:].strip()

                            data_line = reader.readline().strip()
                            colon_index = data_line.index(":")
                            my_product[ctr].sales_qty = int(data_line[colon_index + 1:].strip())

                            data_line = reader.readline().strip()
                            colon_index = data_line.index(":")
                            my_product[ctr].profit = float(data_line[colon_index + 1:].strip())

                            reader.readline()

                    # removing NoneType values
                    my_product = [item for item in my_product if item.name is not None]

                    for item in my_product:
                        name = item.name
                        sales_qty = item.sales_qty
                        profit_loss = item.profit

                        if name in combined_data:
                            combined_data[name][0] += sales_qty
                            combined_data[name][1] += profit_loss
                        else:
                            combined_data[name] = [sales_qty, profit_loss]

                    if ctr != -1:
                        if ctr > 0:
                            # combining the redundant product name
                            combined_data = dict(combined_data)
                        Terminal.clear_screen()
                        Terminal.gotoxy(15, 10)
                        print("Product Name")
                        Terminal.gotoxy(35, 10)
                        print("Expired Quantity")
                        Terminal.gotoxy(60, 10)
                        print("Total Amount")

                        last_iteration = (len(combined_data)*2) + 5
                        for i in range((len(combined_data)*2) + 5):
                            i += 9
                            if i in {9, 11, last_iteration-1+9}:
                                for j in range(64):
                                    Terminal.gotoxy(12+j, i)
                                    print("-")
                            else:
                                Terminal.gotoxy(12, i)
                                print("|")
                                Terminal.gotoxy(31, i)
                                print("|")
                                Terminal.gotoxy(55, i)
                                print("|")
                                Terminal.gotoxy(75, i)
                                print("|")

                        for i, (name, item) in enumerate(combined_data.items(), start=1):
                            Terminal.gotoxy(15, 11 + (i*2))
                            print(name.upper())
                            Terminal.gotoxy(35, 11 + (i*2))
                            print(item[0])
                            Terminal.gotoxy(60, 11 + (i*2))
                            print(item[1])
                        Terminal.gotoxy(12, 18 + (i*2))
                        print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                        Terminal.gotoxy(12, 20 + (i*2))
                        input("Press enter to continue...")
                    else:
                        Terminal.clear_screen()
                        Terminal.gotoxy(15, 10)
                        print("=-=-=-=-=-=-=-=-=-=-=-=-=")
                        Terminal.gotoxy(15, 13)
                        print(f"FILE ({file}) IS EMPTY")
                        Terminal.gotoxy(15, 15)
                        input("Press enter to continue...")
            except Exception as e:
                print(e)
    except FileNotFoundError:
        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=")
        Terminal.gotoxy(15, 13)
        print(f"FILE {file} NOT FOUND")
        Terminal.gotoxy(15, 15)
        input("Press enter to continue...")


def settings_menu():
    Terminal.clear_screen()
    Terminal.gotoxy(15, 10)
    print("=-=-= SETTINGS =-=-=")
    Terminal.gotoxy(15, 13)
    print("(1) Cashier")
    Terminal.gotoxy(15, 15)
    print("(2) Admin")
    Terminal.gotoxy(15, 17)
    print("(3) Change Encryption Key")
    Terminal.gotoxy(15, 19)
    print("(0) Back")
    Terminal.gotoxy(15, 22)
    print("=-=-=-=-=-=-=-=-=-=-")
    Terminal.gotoxy(15, 25)
    choice = Authen.input_validation()
    return choice


def settings():
    is_change = False

    while True:
        choice = settings_menu()
        if choice == -1:
            Terminal.gotoxy(15, 25)
            print("| PLEASE CHOOSE AMONG THE CHOICES ONLY |")
        elif choice == 0:
            break
        elif choice == 1 or choice == 2:
            Terminal.clear_screen()
            while True:
                is_change = False
                Terminal.clear_screen()
                Terminal.gotoxy(15, 10)
                if choice == 1:
                    print("=-=-= CASHIER SETTINGS =-=-=")
                elif choice == 2:
                    print("=-=-= ADMIN SETTINGS =-=-=")
                Terminal.gotoxy(15, 13)
                print("(1) Change Username")
                Terminal.gotoxy(15, 15)
                print("(2) Change Password")
                Terminal.gotoxy(15, 17)
                print("(0) Exit")
                Terminal.gotoxy(15, 20)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                Terminal.gotoxy(15, 23)
                settings_choice = Authen.input_validation()

                if settings_choice == 0:
                    break
                else:
                    if choice == 1:
                        if settings_choice == 1:
                            Terminal.clear_screen()
                            Terminal.gotoxy(15, 10)
                            print("Current username: " + main.cashier_acc.get_username())
                            Terminal.gotoxy(15, 12)
                            username = input("Enter new name: ")
                            if username == main.cashier_acc.get_username():
                                Terminal.gotoxy(15, 15)
                                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                Terminal.gotoxy(15, 17)
                                print("NEW USERNAME MUST NOT BE THE SAME AS CURRENT USERNAME")
                                input()
                            else:
                                is_change = True
                                main.cashier_acc.set_username(username)
                        elif settings_choice == 2:
                            Terminal.clear_screen()
                            Terminal.gotoxy(15, 10)
                            print("Current password: " + main.cashier_acc.get_password())
                            Terminal.gotoxy(15, 12)
                            password = input("Enter new password: ")
                            Terminal.gotoxy(15, 14)
                            re_password = input("Re-enter new password: ")
                            if password == main.cashier_acc.get_password():
                                Terminal.gotoxy(15, 17)
                                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                Terminal.gotoxy(15, 19)
                                print("NEW PASSWORD MUST NOT BE THE SAME AS CURRENT PASSWORD")
                                input()
                            else:
                                if password == re_password:
                                    is_change = True
                                    main.cashier_acc.set_password(password)
                                else:
                                    Terminal.gotoxy(15, 17)
                                    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                    Terminal.gotoxy(15, 19)
                                    print("PASSWORD DOES NOT MATCHED")
                                    input()
                    elif choice == 2:
                        if settings_choice == 1:
                            Terminal.clear_screen()
                            Terminal.gotoxy(15, 10)
                            print("Current username: " + main.admin_acc.get_username())
                            Terminal.gotoxy(15, 12)
                            username = input("Enter new name: ")
                            if username == main.admin_acc.get_username():
                                Terminal.gotoxy(15, 15)
                                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                Terminal.gotoxy(15, 17)
                                print("NEW USERNAME MUST NOT BE THE SAME AS CURRENT USERNAME")
                                input()
                            else:
                                is_change = True
                                main.admin_acc.set_username(username)
                        elif settings_choice == 2:
                            Terminal.clear_screen()
                            Terminal.gotoxy(15, 10)
                            print("Current password: " + main.admin_acc.get_password())
                            Terminal.gotoxy(15, 12)
                            password = input("Enter new password: ")
                            Terminal.gotoxy(15, 14)
                            re_password = input("Re-enter new password: ")
                            if password == main.admin_acc.get_password():
                                Terminal.gotoxy(15, 17)
                                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                Terminal.gotoxy(15, 19)
                                print("NEW PASSWORD MUST NOT BE THE SAME AS CURRENT PASSWORD")
                                input()
                            else:
                                if password == re_password:
                                    is_change = True
                                    main.admin_acc.set_password(password)
                                else:
                                    Terminal.gotoxy(15, 17)
                                    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                                    Terminal.gotoxy(15, 19)
                                    print("PASSWORD DOES NOT MATCHED")
                                    input()

                # if changed happens
                if settings_choice != 0 and is_change is True:
                    Terminal.gotoxy(15, 17)
                    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    Terminal.gotoxy(15, 19)
                    print("CHANGED SUCCESSFULLY")
                    Authen.save_account()
                    input()

        elif choice == 3:
            is_change = False
            security_obj = Security()
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("Current encryption key: " + str(Security.get_secret_key()))
            Terminal.gotoxy(15, 12)
            new_key = int(input("Enter new key: "))

            if new_key == Security.get_secret_key():
                Terminal.gotoxy(15, 15)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                Terminal.gotoxy(15, 17)
                print("NEW KEY MUST NOT BE THE SAME AS CURRENT KEY")
                input()
            else:
                is_change = True
                security_obj.change_secret_key(new_key)
                Authen.save_account()
                DataManager.save()

            if is_change is True:
                Terminal.gotoxy(15, 17)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                Terminal.gotoxy(15, 19)
                print("CHANGED SUCCESSFULLY")
                Authen.save_account()
                Terminal.gotoxy(15, 21)
                input("Press enter to continue...")


