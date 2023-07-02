from Inventory import Inventory
from Receipt import Receipt
from Account import Account
from Security import Security
import Authen
import DataManager
import Cashier
import Admin
import Terminal

# GLOBAL VARIABLES
MAX_INV = 100
MAX_PROD_STOCK = 50
marker = -1
receipt_marker = -1
my_inv = [Inventory() for _ in range(MAX_INV)]
customer_receipt = [Receipt() for _ in range(MAX_INV)]
valid_input = False
back_to_login = False
admin_acc = Account()
cashier_acc = Account()

def main():
    global my_inv
    global admin_acc
    global cashier_acc

    # set up / retrieval of data
    Security.set_encryption_key()
    my_inv = DataManager.retrieve()
    DataManager.del_expired_product()
    admin_acc, cashier_acc = Authen.retrieve_account()

    # flow of inventory system
    while True:
        input = Authen.login()
        if input == 0:
            exit()
        elif input == 1:
            Cashier.cashier()
        elif input == 2:
            Admin.admin()



def is_full():
    inventory = [item for item in my_inv if item is not None]
    if len(inventory) == MAX_INV - 1:
        return 1
    else:
        return 0

def locate_product(product):
    inventory = [item for item in my_inv if item.name is not None]
    for i in range(len(inventory)):
        if inventory[i].name.lower() == product.name.lower():
            return i
    return -1

def locate_product_receipt(product):
    receipt = [item for item in customer_receipt if item.get_product_name() is not None]
    for i in range(len(receipt)):
        if receipt[i].get_product_name().lower() == product.get_product_name().lower():
            return i
    return -1


if __name__ == '__main__':
    main()

