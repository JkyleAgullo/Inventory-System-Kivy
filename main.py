from kivy.uix.popup import Popup

import DataManager
from Cashier import add_to_receipt
from Receipt import Receipt
from Inventory import Inventory
from kivy.config import Config
from kivy.app import App
from kivymd.icon_definitions import md_icons
from kivymd.uix.textfield import MDTextField


Config.set('graphics', 'resizable', False)
import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label

# GLOBAL VARIABLES
MAX_INV = 100
MAX_PROD_STOCK = 50
marker = -1
receipt_marker = -1
my_inv = [Inventory() for _ in range(MAX_INV)]
customer_receiptt = [Receipt() for _ in range(MAX_INV)]


class Cashier(Widget):
    labels = {}
    receipt_marker = -1
    product_name = StringProperty("try")
    name = ObjectProperty(None)
    qty = ObjectProperty(None)
    # insert the string property of the price of the product for printing
    Builder.load_file('cashier.kv')
    """
        def name_validate(self,widget):
        self.product_name = widget.text
        name = self.name.text
        inventory_pos = locate_product(name) #product dapat ung ipapasa, if nme palitn mo ung nsa locate function to name
        price=my_inv[inventory_pos].orig_price
        self.add_widget(Label(text=str(price), font_size='20', pos=(50, 400), color=(0, 0, 0, .7)))
        
        
        def qty_validate(self, widget):
        self.qty_input_string = widget.text

    """

    # change the first element into a label
    my_array = ['Product Name']
    my_array2 = ['Quantity']
    price_array = ['Price']

    def btn(self, widget):  # punch button
        product = Inventory()
        receipt = Receipt()
        product_qty = int(self.qty.text)
        receipt.set_qty(product_qty)

        productName = self.name.text
        product_name = productName.upper()
        product.name = product_name

        inventory_pos = locate_product(product)  # product dapat ung ipapasa, if nme palitn mo ung nsa locate function to name
        # print(inventory_pos)

        if inventory_pos == -1:
            popup_content = Label(text="PRODUCT DOES NOT EXIST")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.qty.text=""
            self.ids.txt.text=""
        else:
            price = my_inv[inventory_pos].retail_price * int(self.qty.text)

            Cashier.my_array.append(self.name.text)
            Cashier.my_array2.append(self.qty.text)
            Cashier.price_array.append(price)
            self.product_name = widget.text
            self.add_widget(Label(text=str(price), font_size='20', pos=(400, 502), color=(1, 1, 1, 1)))
            if my_inv[inventory_pos].qty == 0 or my_inv[inventory_pos].qty - receipt.get_qty() < 0:
                if my_inv[inventory_pos].qty == 0 or my_inv[inventory_pos].qty - receipt.get_qty() < 0:
                    popup_content = Label(text="Insufficient quantity")
                    popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
                    popup.open()
                    self.ids.qty.text = ""
                    self.ids.txt.text = ""

            else:
                receipt.set_price(my_inv[inventory_pos].retail_price)
                receipt.set_total_price(round(receipt.get_price() * receipt.get_qty(), 2))
                receipt.set_product_name(product_name)
                receipt.set_qty(product_qty)
                if customer_receiptt[0].get_product_name() is None:
                    print("pasok")
                    Cashier.add_to_receipt(receipt)
                    #print(receipt.get_product_name())

                else:
                    receipt_pos = locate_product_receipt(receipt)
                    if receipt_pos == -1:
                        Cashier.add_to_receipt(receipt)
                    else:
                        # print(receipt_pos)
                        customer_receiptt[receipt_pos].set_qty(customer_receiptt[receipt_pos].get_qty() + receipt.get_qty())
                        customer_receiptt[receipt_pos].set_total_price(customer_receiptt[receipt_pos].get_total_price() + round(receipt.get_total_price(), 2))

        self.ids.qty.text = ""
        self.ids.txt.text = ""

    def save(self):
        customer_receipt = [item for item in customer_receiptt if item.get_product_name() is not None]
        print(len(customer_receiptt))
        inventory = [item for item in my_inv if item.name is not None]

        for i in range(len(customer_receipt)):
            for j in range(len(inventory)):
                if customer_receipt[i].get_product_name() == inventory[j].name:
                    my_inv[j].qty -= customer_receipt[i].get_qty()
                    my_inv[j].sales_qty += customer_receiptt[i].get_qty()
                    my_inv[j].total_price = my_inv[j].qty * my_inv[j].orig_price
                    my_inv[j].total_sales_amount += my_inv[j].retail_price * customer_receiptt[i].get_qty()
                    my_inv[j].profit += my_inv[j].retail_price * customer_receiptt[i].get_qty()
                    DataManager.record_sales(customer_receipt[i])
                    print("recorded")
        DataManager.save()

    def add_to_receipt(receipt):
        print("DITO PUMASOK")
        Cashier.receipt_marker += 1
        customer_receiptt[Cashier.receipt_marker] = Receipt(
            receipt.get_product_name(),
            receipt.get_price(),
            receipt.get_qty(),
            receipt.get_total_price()
        )

    # displaying to receipt
    def Array_display(self, array):  # prod name
        i = 10
        self.cols = len(array[0])
        # print(Cashier.my_array[1]) #try lang
        # for row in array:
        for element in array:
            i = i - 30
            self.add_widget(Label(text=str(element), font_size='20', pos=(720, 640 + i), color=(1, 1, 1, 1)))

    def Array_display2(self, array):  # prod qty
        i = 10
        self.cols = len(array[0])
        self.labels = {}  # Clear existing label references
        for index, element in enumerate(array):
            i = i - 30
            label = Label(text=str(element), font_size='20', pos=(850, 640 + i), color=(1, 1, 1, 1))
            self.add_widget(label)
            self.labels[index] = label

    def Array_price(self, array):
            i = 10
            self.cols = len(array[0])
            # for row in array:
            for index, element in enumerate(array):
                i = i - 30

                self.add_widget(Label(text=str(element), font_size='20', pos=(940, 640 + i), color=(1, 1, 1, 1)))


class MyApp(MDApp):
    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Cashier'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"

        return Cashier()
    #    return AdminADD()


def main():
    global my_inv
    my_inv = DataManager.retrieve()
    print("done main")
    price = my_inv[1].retail_price
    print(price)


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
    receipt = [item for item in customer_receiptt if item.get_product_name() is not None]
    for i in range(len(receipt)):
        if receipt[i].get_product_name().lower() == product.get_product_name().lower():
            return i
    return -1


if __name__ == "__main__":
    main()
    MyApp().run()
