import DataManager
import os
from Inventory import Inventory
from Category import Category
import DateManager
import main
import Authen
import Terminal
username = ""
password = ""
global choice
global status
def admin():
    product = Inventory()
    while True:
        while True:
            Terminal.clear_screen()
            Terminal.gotoxy(19, 10)
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
            Terminal.gotoxy(19, 25)
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
                input()
            else:
                Terminal.gotoxy(15, 24)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=-")
                Terminal.gotoxy(15, 26)
                print("ADD FAILED")
                input()
        elif choice == 2:
            display()

def add_product(my_product):
    if main.is_full() == 1:
        print("ARRAY IS FULL")
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
            print("QUANTITY LIMIT EXCEEDED")
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
    choice = display_menu()
    if choice == -1:
        Terminal.gotoxy(15, 25)
        print("| PLEASE CHOOSE AMONG THE CHOICES ONLY |")
    elif choice == 1:
        display_inventory()
    elif choice == 2:
        display_sales_history()


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
    Terminal.gotoxy(15, 20)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    Terminal.gotoxy(15, 23)
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
        print("Press any key to continue...")
        input()
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
        print("Press Enter to continue...")
        input()


def display_sales_history():
    sales_history_dir = os.path.join(os.getcwd(), DataManager.sales_history_folder)


def settings_menu():
    ...