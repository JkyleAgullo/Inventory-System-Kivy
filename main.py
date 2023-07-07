from kivy.config import Config

import Authen
from Account import Account

Config.set('graphics', 'resizable', False)
import DataManager
import DateManager
from Inventory import Inventory
from Receipt import Receipt
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.icon_definitions import md_icons

# GLOBAL VARIABLES
MAX_INV = 100
MAX_PROD_STOCK = 50
marker = -1
receipt_marker = -1
my_inv = [Inventory() for _ in range(MAX_INV)]
customer_receiptt = [Receipt() for _ in range(MAX_INV)]
admin_acc = Account()
cashier_acc = Account()


class Cashier(Screen):
    labels = {}
    global receipt_marker
    product_name = StringProperty("try")
    name = ObjectProperty(None)
    qty = ObjectProperty(None)

    # change the first element into a label
    my_array = ['Product Name']
    my_array2 = ['Quantity']
    price_array = ['Price']

    def btn(self, widget):  # punch button
        product = Inventory()
        receipt = Receipt()
        product_qty = int(self.ids.qty.text)
        receipt.set_qty(product_qty)

        productName = self.ids.txt.text
        product_name = productName.upper()
        product.name = product_name
        print(product_qty)

        inventory_pos = locate_product(product)  # product dapat ung ipapasa, if nme palitn mo ung nsa locate function to name
        # print(inventory_pos)

        if inventory_pos == -1:
            popup_content = Label(text="PRODUCT DOES NOT EXIST")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.qty.text = ""
            self.ids.txt.text = ""
        else:
            price = my_inv[inventory_pos].retail_price * int(self.ids.qty.text)

            self.my_array.append(self.ids.txt.text)
            self.my_array2.append(self.ids.qty.text)
            self.price_array.append(price)

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
                    self.add_to_receipt(receipt)
                    # print(receipt.get_product_name())

                else:
                    receipt_pos = locate_product_receipt(receipt)
                    if receipt_pos == -1:
                        self.add_to_receipt(receipt)
                    else:
                        # print(receipt_pos)
                        customer_receiptt[receipt_pos].set_qty(customer_receiptt[receipt_pos].get_qty() + receipt.get_qty())
                        customer_receiptt[receipt_pos].set_total_price(customer_receiptt[receipt_pos].get_total_price() + round(receipt.get_total_price(), 2))

        self.ids.qty.text = ""
        self.ids.txt.text = ""

    def reset(self):
        Cashier()

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

    def add_to_receipt(self,receipt):
        global receipt_marker
        print("DITO PUMASOK")
        receipt_marker += 1
        customer_receiptt[receipt_marker] = Receipt(
            receipt.get_product_name(),
            receipt.get_price(),
            receipt.get_qty(),
            receipt.get_total_price()
        )

    # displaying to receipt
    def Array_display(self):  # prod name
        array = self.my_array
        i = 10
        #self.cols = len(array[0])
        # print(Cashier.my_array[1]) #try lang
        # for row in array:
        for element in array:
            i = i - 30
            self.add_widget(Label(text=str(element), font_size='20', pos=(220, 340 + i), color=(1, 1, 1, 1)))
            print(element)

    def Array_display2(self):  # prod qty
        array = self.my_array2
        i = 10
        self.cols = len(array[0])
         #try lang
        # for row in array:
        for element in array:
            i = i - 30
            self.add_widget(Label(text=str(element), font_size='20', pos=(350, 340 + i), color=(1, 1, 1, 1)))

    def Array_price(self):
        array = self.price_array
        i = 10
        self.cols = len(array[0])
        # for row in array:
        print(len(array))
        for index, element in enumerate(array):
            i = i - 30

            label = Label(text=str(element), font_size='23', pos=(440, 340 + i), color=(1, 1, 1, 1))
            self.add_widget(label)


class AdminDB(Screen):
    # todo: design admin dashboard
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SplashWindow(Screen):
    def update_progress(self, value):
        self.ids.progress_bar.value = value
        if value >= 100:
            app = App.get_running_app()
            app.root.transition = NoTransition()
            app.root.current = "first"


class AdminADD(Screen):
    product = Inventory()
    global marker
    # todo: add design to admin add

    current_datetime = StringProperty("")

    def getInput(self):

        productName = (self.ids.prodName.text)
        productPrice = (self.ids.prodPrice.text)
        productQty = (self.ids.prodQuantity.text)
        productRetail = (self.ids.prodRetail.text)
        productCategory = (self.ids.prodCategory.text)
        #print(productName)
        #print(productPrice)
        #print(productQty)
        #print(productRetail)

        AdminADD.product.category = productCategory.upper()
        AdminADD.product.name=productName.upper()
        AdminADD.product.orig_price = round(float(productPrice),2)
        AdminADD.product.qty = int(productQty)
        AdminADD.product.retail_price = round(float(productRetail),2)
        # Get the current date/time
        AdminADD.product.date = DateManager.get_date()
        # Set and get expiration date
        AdminADD.product.exp_date = DateManager.set_get_expiration_date(AdminADD.product.category)
        AdminADD.product.total_price = AdminADD.product.qty * AdminADD.product.orig_price

        pos = locate_product(AdminADD.product)
        if pos == -1:
            AdminADD.product.sales_qty = 0
            AdminADD.product.total_sales_amount = 0
            AdminADD.product.profit = AdminADD.product.total_price * -1
            status = AdminADD.add_product(AdminADD.product)
        else:
            # if exist update the product
            status = AdminADD.update_product(AdminADD.product, pos)

        if status == 1:
            DataManager.record_product(AdminADD.product)
            DataManager.save()
            popup_content = Label(text="ADDED SUCCESSFULLY")
            popup = Popup(title='DONE', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()

        else:
            popup_content = Label(text="FAILED TO ADD")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
        self.ids.prodName.text = ""
        self.ids.prodPrice.text = ""
        self.ids.prodQuantity.text = ""
        self.ids.prodRetail.text = ""
        self.ids.prodCategory.text = ""


    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")

    def add_product(product):
        global marker
        if is_full() == 1:
            popup_content = Label(text="INVENTORY FULL")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()

        else:
            if product.qty <= MAX_PROD_STOCK:
                marker += 1
                inventory_data = Inventory(
                    product.category, product.name, product.date,
                    product.exp_date, product.orig_price, product.qty,
                    product.total_price, product.retail_price, product.sales_qty,
                    product.total_sales_amount, product.profit
                )
                my_inv[marker] = inventory_data
                return 1
            else:
                popup_content = Label(text="QUANTITY EXCEEDED")
                popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
            return -1
        return -1

    def update_product(product, index_pos):
        if (my_inv[index_pos].qty + product.qty) > MAX_PROD_STOCK:
            print("QUANTITY LIMIT EXCEEDED FOR: " + my_inv[index_pos].name)
            return -1
        else:
            my_inv[index_pos].date = product.date
            my_inv[index_pos].exp_date = product.exp_date
            my_inv[index_pos].orig_price = product.orig_price
            my_inv[index_pos].qty += product.qty
            my_inv[index_pos].total_price = product.orig_price * my_inv[index_pos].qty
            my_inv[index_pos].retail_price = product.retail_price
            my_inv[index_pos].profit -= product.qty * product.orig_price
            return 1


class AdminDisplay(Screen):
    # todo: add design to display
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class AdminSettings(Screen):
    # todo: add design to settings
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class WindowManager(ScreenManager):
    pass


class AdminLoginTry(Screen):

    def on_pre_enter(self):
        self.ids.user.text = ""
        self.ids.password.text = ""
    def submit(self, screen):
        global admin_acc
        global cashier_acc
        acc = 0

        username = (self.ids.user.text)
        password = (self.ids.password.text)


        if username == cashier_acc.get_username():
            if password == cashier_acc.get_password():
                acc = 1  # if found"""

        elif username == admin_acc.get_username():
            if password == admin_acc.get_password():
                acc = 2

        if acc == 2:
            screen_manager = screen.manager
            screen_manager.current = 'first'
        elif acc == 1:
            screen_manager = screen.manager
            screen_manager.current = 'cashier'
        else:
            popup_content = Label(text="Wrong username or password")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.user.text = ""
            self.ids.password.text = ""

    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""



class DisplayInventory(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class DisplaySales(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class DisplayExpired(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsCashier(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsAdmin(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsKey(Screen):
    current_datetime = StringProperty("")

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")






Builder.load_file('screen.kv')


class MyApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Admin'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        return WindowManager()

    #    return AdminADD()

    def on_start(self):
        # Schedule the progress bar updates
        Clock.schedule_interval(self.update_progress_bar, 0.1)

        Clock.schedule_interval(self.update_datetime, 1)

    def update_datetime(self, dt):
        self.root.get_screen('first').update_datetime()
        self.root.get_screen('second').update_datetime()
        self.root.get_screen('third').update_datetime()
        self.root.get_screen('fourth').update_datetime()

    def update_progress_bar(self, dt):
        # Increment the progress bar value
        current_value = self.root.get_screen('splash').ids.progress_bar.value
        new_value = current_value + 50
        self.root.get_screen('splash').update_progress(new_value)
        if new_value >= 100:
            # Stop the progress bar updates when the value reaches 100
            Clock.unschedule(self.update_progress_bar)


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

def main():
    global my_inv
    global admin_acc
    global cashier_acc

    admin_acc, cashier_acc = Authen.retrieve_account()
    my_inv = DataManager.retrieve()
    #print("done main")




if __name__ == "__main__":
    main()
    MyApp().run()
