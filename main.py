import DataManager
from Receipt import Receipt
from Inventory import Inventory
from kivy.config import Config
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
customer_receipt = [Receipt() for _ in range(MAX_INV)]

class Cashier(Widget):

    price = my_inv[1].retail_price
    print(price)
    product_name= StringProperty("try")
    name = ObjectProperty(None)
    qty = ObjectProperty(None)
    # insert the string property of the price of the product for printing
    Builder.load_file('cashier.kv')
    def name_validate(self,widget):
        self.product_name = widget.text
        name = self.name.text
        inventory_pos = locate_product(name) #product dapat ung ipapasa, if nme palitn mo ung nsa locate function to name
        price=my_inv[inventory_pos].orig_price
        self.add_widget(Label(text=str(price), font_size='20', pos=(50, 400), color=(0, 0, 1, 1)))

    def qty_validate(self, widget):
        self.qty_input_string = widget.text

    #change the first element into a label
    my_array = ['Product Name']
    my_array2 = ['Quantity']
    price_array = ['Price']
    def btn(self): #punch button
        name = self.name.text
        inventory_pos = locate_product(name)  # product dapat ung ipapasa, if nme palitn mo ung nsa locate function to name
        price = my_inv[inventory_pos].orig_price
        Cashier.my_array.append(self.name.text)
        Cashier.my_array2.append(self.qty.text)
        Cashier.price_array.append(price)
        name = self.name.text
        #locate the prodname

        print(name)

    def Array_display(self, array):
        i=10
        self.cols = len(array[0])
        print(Cashier.my_array[1]) #try lang
        #for row in array:
        for element in array:
            i=i-30
            self.add_widget(Label(text=str(element), font_size='20',pos=(20,640+i),color=(0, 0, 0, 1)))
    def Array_display2(self, array):
        i=10
        self.cols = len(array[0])
        #for row in array:
        for element in array:
            i=i-30
            self.add_widget(Label(text=str(element), font_size='20',pos=(150,640+i),color=(0, 0, 0, 1)))
    def Array_price(self, array):
        i=10
        self.cols = len(array[0])
        #for row in array:
        for element in array:
            i=i-30
            self.add_widget(Label(text=str(element), font_size='20',pos=(240,640+i),color=(0, 0, 0, 1)))


class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Cashier'
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
    receipt = [item for item in customer_receipt if item.get_product_name() is not None]
    for i in range(len(receipt)):
        if receipt[i].get_product_name().lower() == product.get_product_name().lower():
            return i
    return -1


if __name__ == "__main__":
    main()
    MyApp().run()