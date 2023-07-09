import os
from datetime import date
from Inventory import Inventory
from Category import Category
from Security import Security
from Receipt import Receipt
import DateManager
import Admin
import main
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class ExpiredProduct:
    def __init__(self, name=None, qty=0, profit_loss=0.0):
        self.name = name
        self.qty = qty
        self.profit_loss = profit_loss

inventory_folder = "product"
product_history_folder = "product/product_history"
exp_product_history_folder = "product/expired_product_history"
exp_date_product_folder = "product/expiration_date"
sales_history_folder = "product\sales_history"
data_line = None
time = None
colon_index = 0
ctr = 0


def del_expired_product():
    inventory = [item for item in main.my_inv if item.name is not None]
    expired_product = [ExpiredProduct() for _ in range(main.MAX_INV)]
    current_date = DateManager.get_date()
    exp_date_product_dir = os.path.join(os.getcwd(), exp_date_product_folder, (current_date + ".txt"))
    exp_product_dir = os.path.join(os.getcwd(), exp_product_history_folder, (current_date + ".txt"))
    ctr = -1

    try:
        if os.path.exists(exp_date_product_dir):
            with open(exp_date_product_dir, "r") as reader:
                while True:
                    data_line = reader.readline().strip()
                    if not data_line:
                        break

                    if ":" in data_line:
                        ctr += 1
                        colon_index = data_line.index(":")
                        expired_product[ctr].name = data_line[colon_index + 1:].strip()

                        data_line = reader.readline().strip()
                        colon_index = data_line.index(":")
                        expired_product[ctr].qty = int(data_line[colon_index + 1:].strip())

                        reader.readline()

                    # reduce data or delete if zero qty
                    for i in range(len(inventory)):
                        if expired_product[ctr].name.lower() == main.my_inv[i].name.lower():
                            main.my_inv[i].qty -= expired_product[ctr].qty
                            main.my_inv[i].total_price = main.my_inv[i].qty * main.my_inv[i].orig_price
                            main.my_inv[i].profit -= expired_product[ctr].qty * main.my_inv[i].orig_price
                            expired_product[ctr].profit_loss = expired_product[ctr].qty * main.my_inv[i].orig_price
                            if main.my_inv[i].qty <= 0:
                                del_product(i)
                                break

                # clear NoneType values
                if ctr > -1:
                    expired_product = [item for item in expired_product if item.name is not None]
                    expired_product = Inventory.sort(expired_product)
                    with open(exp_product_dir, "a") as writer:
                        for item in expired_product:
                            writer.write("Product Name: " + item.name.upper() + "\n")
                            writer.write("Quantity: " + str(item.qty) + "\n")
                            writer.write("Profit Loss: " + str(item.profit_loss) + "\n\n")
                    # save
                    save()

            os.remove(exp_date_product_dir)
    except FileNotFoundError:
        popup_content = Label(text=" PRODUCT FILE DIRECTORY DOES NOT EXIST")
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

        print("PRODUCT FILE DIRECTORY DOES NOT EXIST")


def del_product(index_position):
    if index_position == main.marker:
        main.my_inv[index_position] = None
    else:
        for i in range(index_position, main.marker):
            main.my_inv[index_position] = Inventory()
            main.my_inv[index_position] = main.my_inv[index_position + 1]
        main.my_inv[main.marker] = None
    main.marker -= 1


def erase_content_file(file):
    try:
        with open(file, "w") as writer:
            writer.write("")
    except Exception as e:
        popup_content = Label(text="Error occurred during erasing file content: " + str(e))
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
        print("Error occurred during erasing file content: ", e)


def record_expiration_date_product(product):
    my_product = [Inventory() for _ in range(main.MAX_INV)]
    is_exist = False
    ctr = -1

    record_expiration_date_dir = os.path.join(os.getcwd(), exp_date_product_folder, (product.exp_date + ".txt"))

    if not os.path.exists(record_expiration_date_dir):
        open(record_expiration_date_dir, "w").close()

    try:
        with open(record_expiration_date_dir, "r") as reader:
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
                    my_product[ctr].qty = int(data_line[colon_index + 1:].strip())

                    reader.readline()

                    if my_product[ctr].name.lower() == product.name.lower():
                        my_product[ctr].qty += product.qty
                        is_exist = True

        if is_exist is False:
            ctr += 1
            my_product[ctr] = product
        # removing all None initialized
        my_product = [item for item in my_product if item.name is not None]
        if ctr > 0:
            my_product = Inventory.sort(my_product)

        erase_content_file(record_expiration_date_dir)

        with open(record_expiration_date_dir, "a") as writer:
            for item in my_product:
                writer.write("Product Name: " + item.name + "\n")
                writer.write("Quantity: " + str(item.qty) + "\n\n")

    except Exception as e:
        popup_content = Label(text="ERROR OCCURRED DURING RECORDING EXPIRATION DATE: " + str(e))
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
        print("ERROR OCCURRED DURING RECORDING EXPIRATION DATE: ", e)


def record_product(product):
    my_product = [Inventory() for _ in range(Category.get_category_length())]
    is_exist = False
    ctr = -1

    record_product_dir = os.path.join(os.getcwd(), product_history_folder, (DateManager.get_date() + ".txt"))

    if not os.path.exists(record_product_dir):
        open(record_product_dir, "w").close()

    try:
        with open(record_product_dir, "r") as reader:
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
                    my_product[ctr].exp_date = data_line[colon_index + 1:].strip()
                    
                    data_line = reader.readline().strip()
                    colon_index = data_line.index(":")
                    my_product[ctr].qty = int(data_line[colon_index + 1:].strip())

                    reader.readline()

                    if my_product[ctr].name.lower() == product.name.lower():
                        my_product[ctr].qty += product.qty
                        is_exist = True

        if is_exist is False:
            ctr += 1
            my_product[ctr] = product
            
        # removing all None initialized
        my_product = [item for item in my_product if item.name is not None]
        if ctr > 0:
            my_product = Inventory.sort(my_product)

        erase_content_file(record_product_dir)

        with open(record_product_dir, "w") as writer:
            for item in my_product:
                writer.write("Product Name: " + item.name + "\n")
                writer.write("Expiration Date: " + item.exp_date + "\n")
                writer.write("Quantity: " + str(item.qty) + "\n\n")
    except Exception as e:
        print(e)

    record_expiration_date_product(product)


def record_sales(product):
    my_product = [Receipt() for _ in range(Category.get_category_length())]
    is_exist = False
    ctr = -1

    sales_product_dir = os.path.join(os.getcwd(), sales_history_folder, (DateManager.get_date() + ".txt"))
    if not os.path.exists(sales_product_dir):
        open(sales_product_dir, "w").close()

    with open(sales_product_dir, "r") as reader:
        while True:
            data_line = reader.readline().strip()
            if not data_line:
                break

            if ":" in data_line:
                ctr += 1
                colon_index = data_line.index(":")
                product_name = data_line[colon_index + 1:].strip()
                my_product[ctr].set_product_name(product_name)

                data_line = reader.readline().strip()
                colon_index = data_line.index(":")
                sales_qty = int(data_line[colon_index + 1:].strip())
                my_product[ctr].set_qty(sales_qty)

                data_line = reader.readline().strip()
                colon_index = data_line.index(":")
                total_sales_amount = float(data_line[colon_index + 1:].strip())
                my_product[ctr].set_total_price(total_sales_amount)

                reader.readline()

                if my_product[ctr].get_product_name().lower() == product.get_product_name().lower():
                    my_product[ctr].set_qty(my_product[ctr].get_qty() + product.get_qty())
                    my_product[ctr].set_total_price(my_product[ctr].get_total_price() + product.get_total_price())
                    is_exist = True

        if is_exist is False:
            ctr += 1
            my_product[ctr] = product

        # removing all None initialized
        my_product = [item for item in my_product if item.get_product_name() is not None]
        if ctr > 0:
            my_product = Receipt.sort(my_product)

        erase_content_file(sales_product_dir)

        with open(sales_product_dir, "w") as writer:
            for item in my_product:
                writer.write("Product Name: " + item.get_product_name() + "\n")
                writer.write("Sales Quantity: " + str(item.get_qty()) + "\n")
                writer.write("Total Sales Amount: " + str(item.get_total_price()) + "\n\n")



def retrieve():
    my_product = Inventory()
    inventory_dir = os.path.join(os.getcwd(), inventory_folder, (Security.encrypt(Security.get_inventory_filename(), Security.get_secret_key()) + ".txt"))

    try:
        if os.path.exists(inventory_dir):
            with open(inventory_dir, "r") as reader:
                while True:
                    data_line = reader.readline().strip()
                    if not data_line:
                        break

                    my_product.category = data_line
                    my_product.category = Security.decrypt(my_product.category, Security.get_secret_key())
                    my_product.name = reader.readline().strip()
                    my_product.name = Security.decrypt(my_product.name, Security.get_secret_key())
                    my_product.date = reader.readline().strip()
                    my_product.date = Security.decrypt(my_product.date, Security.get_secret_key())
                    my_product.exp_date = reader.readline().strip()
                    my_product.exp_date = Security.decrypt(my_product.exp_date, Security.get_secret_key())

                    data_line = reader.readline().strip()
                    if data_line:
                        try:
                            data_line = data_line.split(" ")
                            my_product.orig_price = data_line[0]
                            my_product.orig_price = float(Security.decrypt(my_product.orig_price, Security.get_secret_key()))
                            my_product.qty = data_line[1]
                            my_product.qty = int(Security.decrypt(my_product.qty, Security.get_secret_key()))
                            my_product.total_price = data_line[2]
                            my_product.total_price = float(Security.decrypt(my_product.total_price, Security.get_secret_key()))
                            my_product.retail_price = data_line[3]
                            my_product.retail_price = float(Security.decrypt(my_product.retail_price, Security.get_secret_key()))
                            my_product.sales_qty = data_line[4]
                            my_product.sales_qty = int(Security.decrypt(my_product.sales_qty, Security.get_secret_key()))
                            my_product.total_sales_amount = data_line[5]
                            my_product.total_sales_amount = float(Security.decrypt(my_product.total_sales_amount, Security.get_secret_key()))
                            my_product.profit = data_line[6]
                            my_product.profit = float(Security.decrypt(my_product.profit, Security.get_secret_key()))
                            reader.readline()

                            Admin.add_product(my_product)
                        except ValueError as e:
                            print("INVALID NUMERIC VALUE IN INVENTORY FILE: ", e)
            return main.my_inv
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Inventory file not found:", inventory_dir)
        return []

def save():
    my_inventory = [item for item in main.my_inv if item is not None]
    my_inventory = Inventory.sort(my_inventory)
    inventory_dir = os.path.join(os.getcwd(), inventory_folder, (Security.encrypt(Security.get_inventory_filename(), Security.get_secret_key()) + ".txt"))

    try:
        with open(inventory_dir, "w") as writer:
            if len(my_inventory) == 0:
                popup_content = Label(text="INVENTORY IS EMPTY")
                popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
                print("INVENTORY IS EMPTY")
            else:
                for product in my_inventory:
                    if product.name is not None:
                        category = Security.encrypt(product.category, Security.get_secret_key())
                        writer.write(category + "\n")
                        name = Security.encrypt(product.name, Security.get_secret_key())
                        writer.write(name + "\n")
                        date = Security.encrypt(product.date, Security.get_secret_key())
                        writer.write(date + "\n")
                        exp_date = Security.encrypt(product.exp_date, Security.get_secret_key())
                        writer.write(exp_date + "\n")
                        orig_price = Security.encrypt(str(product.orig_price), Security.get_secret_key())
                        writer.write(str(orig_price) + ' ')
                        qty = Security.encrypt(str(product.qty), Security.get_secret_key())
                        writer.write(str(qty) + ' ')
                        total_price = Security.encrypt(str(product.total_price), Security.get_secret_key())
                        writer.write(str(total_price) + ' ')
                        retail_price = Security.encrypt(str(product.retail_price), Security.get_secret_key())
                        writer.write(str(retail_price) + ' ')
                        sales_qty = Security.encrypt(str(product.sales_qty), Security.get_secret_key())
                        writer.write(str(sales_qty) + ' ')
                        total_sales_amount = Security.encrypt(str(product.total_sales_amount), Security.get_secret_key())
                        writer.write(str(total_sales_amount) + ' ')
                        profit = Security.encrypt(str(product.profit), Security.get_secret_key())
                        writer.write(str(profit) + "\n\n")
    except Exception as e:
        popup_content = Label(text="ERROR OCCURRED DURING INVENTORY SAVING:"+str(e))
        popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
        print("ERROR OCCURRED DURING INVENTORY SAVING:", e)