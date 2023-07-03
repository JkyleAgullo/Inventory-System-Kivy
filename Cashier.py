from Receipt import Receipt
from Inventory import Inventory
import Terminal
import Authen
import DataManager
import main
global total_max
global receipt_marker
add_another_product = False
def cashier():
    total_max = -1
    receipt_marker = -1

    while True:
        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-=-= CASHIER =-=-=-=")
        Terminal.gotoxy(15, 13)
        print("(1) New Customer")
        Terminal.gotoxy(15, 15)
        print("(0) Log out")
        Terminal.gotoxy(15, 18)
        print("=-=-=-=-=-=-=-=-=-=-=-=")
        Terminal.gotoxy(15, 20)
        choice = Authen.input_validation()

        if choice == 0:
            break
        elif choice == 1:
            global add_another_product
            add_another_product = True
            punch()
        else:
            Terminal.gotoxy(15, 20)
            print("PLEASE CHOOSE AMONG THE CHOICES ONLY")


def punch():
    main.receipt_marker = -1
    global add_another_product

    while add_another_product:
        product = Inventory()
        receipt = Receipt()

        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-= PUNCH PRODUCT =-=-=")
        Terminal.gotoxy(15, 13)
        product_name = input("Product Name: ").upper()
        receipt.set_product_name(product_name)
        Terminal.gotoxy(15, 15)
        product_qty = int(input("Quantity: "))
        receipt.set_qty(product_qty)
        product.name = product_name
        inventory_pos = main.locate_product(product)

        if inventory_pos == -1:
            Terminal.gotoxy(15, 18)
            print("=-=-=-=-=-=-=-=-=-=-=-=-=")
            Terminal.gotoxy(15, 20)
            print("PRODUCT DOES NOT EXIST")
            Terminal.gotoxy(15, 22)
            input("Press enter to continue...")
        else:
            if main.my_inv[inventory_pos].qty == 0 or main.my_inv[inventory_pos].qty - receipt.get_qty() < 0:
                Terminal.gotoxy(15, 18)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=")
                Terminal.gotoxy(15, 20)
                print("INSUFFICIENT AMOUNT")
                Terminal.gotoxy(15, 22)
                input("Press enter to continue...")
            else:
                receipt.set_price(main.my_inv[inventory_pos].retail_price)
                receipt.set_total_price(round(receipt.get_price() * receipt.get_qty(), 2))

                if main.customer_receipt[0].get_product_name() is None:
                    add_to_receipt(receipt)
                else:
                    receipt_pos = main.locate_product_receipt(receipt)
                    if receipt_pos == -1:
                        add_to_receipt(receipt)
                    else:
                        main.customer_receipt[receipt_pos].set_qty(main.customer_receipt[receipt_pos].get_qty() + receipt.get_qty())
                        main.customer_receipt[receipt_pos].set_total_price(main.customer_receipt[receipt_pos].get_total_price() + round(receipt.get_total_price(), 2))

        while True:
            Terminal.clear_screen()
            Terminal.gotoxy(15, 10)
            print("=-=-=-=-=-=-=-=-=-=-=-=-=")
            Terminal.gotoxy(15, 13)
            print("Add product?")
            Terminal.gotoxy(15, 14)
            print("[1] Yes  [0] No")
            Terminal.gotoxy(15, 16)
            choice = Authen.input_validation()
            if choice == 0:
                add_another_product = False
                break
            elif choice == 1:
                add_another_product = True
                break
            else:
                Terminal.clear_screen()
                Terminal.gotoxy(15, 10)
                print("=-=-=-=-=-=-=-=-=-=-=-=-=")
                Terminal.gotoxy(15, 13)
                print("PLEASE CHOOSE AMONG THE CHOICES ONLY")
                Terminal.gotoxy(15, 15)
                input("Press enter to continue...")


    if main.receipt_marker != -1:
        Terminal.clear_screen()
        Terminal.gotoxy(15, 10)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=")
        Terminal.gotoxy(15, 13)
        print("Continue Transaction?")
        print("[1] Yes  [0] No")
        Terminal.gotoxy(15, 16)
        choice = Authen.input_validation()

        if choice == 1:
            display_receipt()

            customer_receipt = [item for item in main.customer_receipt if item.get_product_name() is not None]
            inventory = [item for item in main.my_inv if item.name is not None]

            for i in range(len(customer_receipt)):
                for j in range(len(inventory)):
                    if customer_receipt[i].get_product_name() == inventory[j].name:
                        main.my_inv[j].qty -= main.customer_receipt[i].get_qty()
                        main.my_inv[j].sales_qty += main.customer_receipt[i].get_qty()
                        main.my_inv[j].total_price = main.my_inv[j].qty * main.my_inv[j].orig_price
                        main.my_inv[j].total_sales_amount += main.my_inv[j].retail_price * main.customer_receipt[i].get_qty()
                        main.my_inv[j].profit += main.my_inv[j].retail_price * main.customer_receipt[i].get_qty()
                        DataManager.record_sales(customer_receipt[i])
            DataManager.save()


def add_to_receipt(receipt):
    main.receipt_marker += 1
    main.customer_receipt[main.receipt_marker] = Receipt(
        receipt.get_product_name(),
        receipt.get_price(),
        receipt.get_qty(),
        receipt.get_total_price()
    )


def display_receipt():
    i = 0
    overall_price = 0.0
    my_receipt = [item for item in main.customer_receipt if item.get_product_name() is not None]

    Terminal.clear_screen()
    Terminal.gotoxy(35, 14)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-= RECEIPT =-=-=-=-=-=-=-=-=-=-=-=-=-=")
    Terminal.gotoxy(20, 17)
    print("Product Name")
    Terminal.gotoxy(38, 17)
    print("Price")
    Terminal.gotoxy(56, 17)
    print("Quantity")
    Terminal.gotoxy(74, 17)
    print("Total Amount")

    for item in my_receipt:
        Terminal.gotoxy(20, 20 + i)
        print(item.get_product_name())
        Terminal.gotoxy(38, 20 + i)
        print(item.get_price())
        Terminal.gotoxy(56, 20 + i)
        print(item.get_qty())
        Terminal.gotoxy(74, 20 + i)
        print(item.get_total_price())
        overall_price += item.get_total_price()

    formatted_overall_price = "{:.2f}".format(round(overall_price, 2))
    Terminal.gotoxy(20, 21 + i)
    print("Total Price: " + formatted_overall_price)
    Terminal.gotoxy(35, 24 + i)
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    Terminal.gotoxy(35, 27 + i)
    input("Press enter to continue...")

