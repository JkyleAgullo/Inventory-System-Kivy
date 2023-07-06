from kivy.config import Config

import DataManager
import DateManager
from Inventory import Inventory
from Receipt import Receipt

Config.set('graphics', 'resizable', False)
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty
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
            app.root.current = "login"


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
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""


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
    my_inv = DataManager.retrieve()
    #print("done main")




if __name__ == "__main__":
    MyApp().run()
