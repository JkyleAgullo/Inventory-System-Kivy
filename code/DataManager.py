import os
from datetime import date
from Inventory import Inventory
from Category import Category
from Receipt import Receipt
import DateManager
import Admin
import main


inventory_dir = os.path.join(os.getcwd(), "product/inventory.txt")
product_history_folder = "product/product_history"
exp_product_history_folder = "product/expired_product_history"
exp_date_product_folder = "product/expiration_date"
sales_history_folder = "product/sales_history"
data_line = None
time = None
colon_index = 0
ctr = 0


def del_expired_product():
    inventory = [item for item in main.my_inv if item.name is not None]
    prod_name = ""
    prod_qty = 0
    prod_profit_loss = 0.0
    current_date = DateManager.get_date()
    exp_date_product_dir = os.path.join(os.getcwd(), exp_date_product_folder, (current_date + ".txt"))
    exp_product_dir = os.path.join(os.getcwd(), exp_product_history_folder, (current_date + ".txt"))

    try:
        if os.path.exists(exp_date_product_dir):
            with open(exp_date_product_dir, "r") as reader:
                while True:
                    data_line = reader.readline().strip()
                    if not data_line:
                        break

                    if ":" in data_line:
                        colon_index = data_line.index(":")
                        prod_name = data_line[colon_index + 1:].strip()

                        data_line = reader.readline().strip()
                        colon_index = data_line.index(":")
                        prod_qty = int(data_line[colon_index + 1:].strip())

                        reader.readline()

                for i in range(len(inventory)):
                    if prod_name.lower() == main.my_inv[i].name.lower():
                        main.my_inv[i].qty -= prod_qty
                        main.my_inv[i].total_price = main.my_inv[i].qty * main.my_inv[i].orig_price
                        main.my_inv[i].profit -= prod_qty * main.my_inv[i].orig_price
                        prod_profit_loss = prod_qty * main.my_inv[i].orig_price
                        if main.my_inv[i].qty == 0:
                            del_product(i)
                            break

                save()

            with open(exp_product_dir, "a") as writer:
                writer.write("Product Name: " + prod_name.upper() + "\n")
                writer.write("Quantity: " + str(prod_qty) + "\n")
                writer.write("Profit Loss: " + str(prod_profit_loss) + "\n\n")

        os.remove(exp_date_product_dir)
    except FileNotFoundError:
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
            my_product = sorted(my_product, key=lambda x: x.name)

        erase_content_file(record_expiration_date_dir)

        with open(record_expiration_date_dir, "a") as writer:
            for item in my_product:
                writer.write("Product Name: " + item.name + "\n")
                writer.write("Quantity: " + str(item.qty) + "\n\n")

    except Exception as e:
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
            my_product = sorted(my_product, key=lambda x: x.name)

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
            my_product = sorted(my_product, key=lambda x: x.get_product_name())

        erase_content_file(sales_product_dir)

        with open(sales_product_dir, "w") as writer:
            for item in my_product:
                writer.write("Product Name: " + item.get_product_name() + "\n")
                writer.write("Sales Quantity: " + str(item.get_qty()) + "\n")
                writer.write("Total Sales Amount: " + str(item.get_total_price()) + "\n\n")



def retrieve():
    my_product = Inventory()

    try:
        if os.path.exists(inventory_dir):
            with open(inventory_dir, "r") as reader:
                while True:
                    data_line = reader.readline().strip()
                    if not data_line:
                        break

                    my_product.category = data_line
                    my_product.name = reader.readline().strip()
                    my_product.date = reader.readline().strip()
                    my_product.exp_date = reader.readline().strip()

                    data_line = reader.readline().strip()
                    if data_line:
                        try:
                            data_line = data_line.split(" ")
                            my_product.orig_price = float(data_line[0])
                            my_product.qty = int(data_line[1])
                            my_product.total_price = float(data_line[2])
                            my_product.retail_price = float(data_line[3])
                            my_product.sales_qty = int(data_line[4])
                            my_product.total_sales_amount = float(data_line[5])
                            my_product.profit = float(data_line[6])
                            reader.readline()

                            Admin.add_product(my_product)
                        except ValueError as e:
                            print("INVALID NUMERIC VALUE IN INVENTORY FILE: ", e)
            return main.my_inv
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("INVENTORY FILE NOT FOUND")


def save():
    my_inventory = [item for item in main.my_inv if item.name is not None]
    my_inventory = sorted(my_inventory, key=lambda x: x.name)
    try:
        with open(inventory_dir, "w") as writer:
            if len(my_inventory) == 0:
                print("INVENTORY IS EMPTY")
            else:
                for product in my_inventory:
                    if product.name is not None:
                        writer.write(product.category + "\n")
                        writer.write(product.name + "\n")
                        writer.write(product.date + "\n")
                        writer.write(product.exp_date + "\n")
                        writer.write(str(product.orig_price) + ' ')
                        writer.write(str(product.qty) + ' ')
                        writer.write(str(product.total_price) + ' ')
                        writer.write(str(product.retail_price) + ' ')
                        writer.write(str(product.sales_qty) + ' ')
                        writer.write(str(product.total_sales_amount) + ' ')
                        writer.write(str(product.profit) + "\n\n")
    except Exception as e:
        print("ERROR OCCURRED DURING INVENTORY SAVING:", e)