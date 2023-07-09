import webbrowser

from kivy.config import Config
from kivy.uix.textinput import TextInput

Config.set('graphics', 'resizable', False)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# from kivymd.
from kivymd.material_resources import dp
from kivymd.uix.datatables import MDDataTable

import Authen
from Account import Account
from Security import Security
import os
import glob

import DataManager
import DateManager
from Inventory import Inventory
from Receipt import Receipt
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
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
    customer_receiptt = [Receipt() for _ in range(MAX_INV)]
    global receipt_marker
    productName = StringProperty("")
    productPrice = StringProperty("0.00")
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
        # print("position: "+ str(product_qty))

        inventory_pos = locate_product(product)
        print(inventory_pos)

        if inventory_pos == -1:
            popup_content = Label(text="PRODUCT DOES NOT EXIST")
            popup = Popup(title='Warning', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.qty.text = ""
            self.ids.txt.text = ""
        else:
            price = my_inv[inventory_pos].retail_price * int(self.ids.qty.text)
            self.productName = my_inv[inventory_pos].name
            self.productPrice = str(price)

            self.my_array.append(self.ids.txt.text)
            self.my_array2.append(self.ids.qty.text)
            self.price_array.append(price)

            self.product_name = widget.text
            self.price = widget.text
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
                        customer_receiptt[receipt_pos].set_qty(
                            customer_receiptt[receipt_pos].get_qty() + receipt.get_qty())
                        customer_receiptt[receipt_pos].set_total_price(
                            customer_receiptt[receipt_pos].get_total_price() + round(receipt.get_total_price(), 2))

        self.ids.qty.text = ""
        self.ids.txt.text = ""

    def reset(self):
        self.productName = ""  # Reset the productName property
        self.productPrice = "0.00"  # Reset the productPrice property
        self.ids.txt.text = ""  # Clear the input field with id 'txt'
        self.ids.qty.text = ""  # Clear the input field with id 'qty'
        self.my_array = ['Product Name']  # Reset the my_array list
        self.my_array2 = ['Quantity']  # Reset the my_array2 list
        self.price_array = ['Price']  # Reset the price_array list

        for child in self.children[:]:
            if isinstance(child,
                          Label) and child.text != 'Product Name' and child.text != 'Quantity' and child.text != 'Price':
                self.remove_widget(child)

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

    def add_to_receipt(self, receipt):
        global receipt_marker

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
        # self.cols = len(array[0])
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
        # try lang
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
            app.root.current = "login"


class AdminADD(Screen):
    product = Inventory()
    global marker
    # todo: add design to admin add

    current_datetime = StringProperty("")

    def getInput(self):

        current_id = self.focus.current

    def getInput(self):

        productName = (self.ids.prodName.text)
        productPrice = (self.ids.prodPrice.text)
        productQty = (self.ids.prodQuantity.text)
        productRetail = (self.ids.prodRetail.text)
        productCategory = (self.ids.prodCategory.text)
        # print(productName)
        # print(productPrice)
        # print(productQty)
        # print(productRetail)

        AdminADD.product.category = productCategory.upper()
        AdminADD.product.name = productName.upper()
        AdminADD.product.orig_price = round(float(productPrice), 2)
        AdminADD.product.qty = int(productQty)
        AdminADD.product.retail_price = round(float(productRetail), 2)
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


class FileInfoButton(Button):
    file_name = StringProperty('')
    file_folder = StringProperty('')
    date = StringProperty('')
    directory = ""

    def __init__(self, **kwargs):
        self.directory = kwargs.pop("directory", "")
        super(FileInfoButton, self).__init__(**kwargs)


class FileStatsScreen(Screen):
    pass


class DisplayInventory(Screen):
    current_datetime = StringProperty("")

    def on_pre_enter(self):
        global my_inv
        if my_inv:
            self.display_table(my_inv)
            print(my_inv[0].name)
        else:
            print("my_inv is empty")

    def display_table(self, invent):
        global my_inv
        my_inv = Inventory.sort(my_inv)
        data = []
        invent = [item for item in my_inv if item.name is not None]
        for item in invent:
            if item is not None:
                row = [
                    item.category,
                    item.name,
                    item.date,
                    item.exp_date,
                    str(item.orig_price),
                    str(item.qty),
                    str(item.total_price),
                    str(item.retail_price),
                    str(item.sales_qty),
                    str(item.total_sales_amount),
                    str(item.profit)
                ]

                print(item.name)
                data.append(row)

        table = MDDataTable(
            column_data=[
                ("Category", dp(40)),
                ("Name", dp(30)),
                ("Date", dp(30)),
                ("Expiration Date", dp(30)),
                ("Original Price", dp(20)),
                ("Quantity", dp(20)),
                ("Total Price", dp(20)),
                ("Retail Price", dp(20)),
                ("Sales Quantity", dp(20)),
                ("Total Sales Amount", dp(20)),
                ("Profit", dp(20))
            ],
            row_data=data,
            use_pagination=True,
            rows_num=10,
            pagination_menu_pos="auto",
        )
        self.ids.inventory.clear_widgets()
        self.ids.inventory.add_widget(table)

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class DisplaySales(Screen):
    current_datetime = StringProperty("")

    def on_enter(self, *args):
        self.display_sales_history()

    def display_sales_history(self):
        sales_history_folder_path = os.path.join(os.getcwd(), DataManager.sales_history_folder)
        self.text_files = glob.glob(sales_history_folder_path + '\*.txt')
        self.ids.files_grid.clear_widgets()
        print(self.text_files)
        if len(self.text_files) == 0:
            label = Label(text='| SALES HISTORY IS EMPTY |')
            self.ids.files_grid.add_widget(label)
            print(sales_history_folder_path)
        else:
            for i, file_path in enumerate(self.text_files, 1):
                file_name = os.path.basename(file_path)
                date = os.path.splitext(file_name)[0]
                directory = os.path.dirname(file_path)

                button = FileInfoButton(file_name=file_name, file_folder=DataManager.sales_history_folder, date=date,
                                        directory=directory)
                button.bind(on_release=lambda instance, path=file_path: self.open_file_content_popup(path))
                # button.bind(on_release=lambda instance: self.open_file_content_popup(file_path))
                # button.bind(on_release=lambda instance: self.open_file_content_popup(file_path))
                self.ids.files_grid.add_widget(button)

    def open_file_content_popup(self, file_path):
        popup = FileContentPopup(file_path=file_path)
        popup.size_hint = (0.8, 0.8)  # Set the size hint to occupy 80% of the parent's size
        popup.size = (400, 300)  # Set the size explicitly to (400, 300) pixels
        popup.open()

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class FileContentPopup(Popup):
    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self.title = "File Contents"
        with open(file_path, "r") as file:
            content = file.read()
        self.content = Label(text=content)


class DisplayExpired(Screen):
    current_datetime = StringProperty("")

    def on_enter(self, *args):
        self.display_sales_history()

    def display_sales_history(self):
        sales_history_folder_path = os.path.join(os.getcwd(), DataManager.exp_product_history_folder)
        self.text_files = glob.glob(sales_history_folder_path + '/*.txt')
        self.ids.files_grid.clear_widgets()
        print(self.text_files)
        if len(self.text_files) == 0:
            label = Label(text='| SALES HISTORY IS EMPTY |')
            self.ids.files_grid.add_widget(label)
            print(sales_history_folder_path)
        else:
            for i, file_path in enumerate(self.text_files, 1):
                file_name = os.path.basename(file_path)
                date = os.path.splitext(file_name)[0]
                directory = os.path.dirname(file_path)

                button = FileInfoButton(file_name=file_name, file_folder=DataManager.sales_history_folder, date=date,
                                        directory=directory)
                button.bind(on_release=lambda instance, path=file_path: self.open_file_content_popup(path))
                # button.bind(on_release=lambda instance: self.open_file_content_popup(file_path))
                # button.bind(on_release=lambda instance: self.open_file_content_popup(file_path))
                self.ids.files_grid.add_widget(button)

    def open_file_content_popup(self, file_path):
        popup = FileContentPopup(file_path=file_path)
        popup.size_hint = (0.8, 0.8)  # Set the size hint to occupy 80% of the parent's size
        popup.size = (400, 300)  # Set the size explicitly to (400, 300) pixels
        popup.open()

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsCashier(Screen):
    current_datetime = StringProperty("")
    is_change = False
    password_verified = BooleanProperty(False)

    def open_input_popup(self, password):
        content = BoxLayout(orientation='vertical')

        password_input = TextInput(multiline=False, password=True)
        content.add_widget(Label(text='Enter Admin Password:'))
        content.add_widget(password_input)
        popup = Popup(title='Password Input', content=content, size_hint=(None, None), size=(400, 200))

        def submit_password(instance):
            entered_password = password_input.text
            if entered_password == admin_acc.get_password():
                self.password_verified = True
                popup.dismiss()
                self.is_change = True
                cashier_acc.set_password(password)
                Authen.save_account()
                self.ids.password.text = ""
                self.ids.password2.text = ""
                popup_content = Label(text="CHANGED SUCCESSFULLY")
                success_popup = Popup(title='SUCCESS', content=popup_content, size_hint=(None, None), size=(400, 200))
                success_popup.open()
            else:
                self.password_verified = False
                popup.dismiss()
                popup_content = Label(text="Incorrect admin password")
                error_popup = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
                error_popup.open()

        submit_button = Button(text='Submit')
        submit_button.bind(on_release=submit_password)
        content.add_widget(submit_button)
        popup.open()

    def submit(self):
        password = self.ids.password.text
        re_password = self.ids.password2.text

        if password == cashier_acc.get_password():
            popup_content = Label(text="NEW PASSWORD MUST NOT BE THE SAME AS CURRENT PASSWORD")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
            self.ids.password2.text = ""
        else:
            if password == re_password:
                self.open_input_popup(password)
            else:
                popup_content = Label(text="PASSWORD NOT MATCH")
                popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
                self.ids.password.text = ""
                self.ids.password2.text = ""

        if self.is_change is True:
            popup_content = Label(text="CHANGED SUCCESSFULLY")
            popup = Popup(title='SUCCESS', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
            self.ids.password2.text = ""

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsAdmin(Screen):
    current_datetime = StringProperty("")
    is_change = False
    password_verified = BooleanProperty(False)
    def open_input_popup(self, password):
        content = BoxLayout(orientation='vertical')

        password_input = TextInput(multiline=False, password=True)
        content.add_widget(Label(text='Enter Admin Password:'))
        content.add_widget(password_input)
        popup = Popup(title='Password Input', content=content, size_hint=(None, None), size=(400, 200))

        def submit_password(instance):
            entered_password = password_input.text
            if entered_password == admin_acc.get_password():
                self.password_verified = True
                popup.dismiss()
                self.is_change = True
                admin_acc.set_password(password)
                Authen.save_account()
                self.ids.password.text = ""
                self.ids.password2.text = ""
                popup_content = Label(text="CHANGED SUCCESSFULLY")
                success_popup = Popup(title='SUCCESS', content=popup_content, size_hint=(None, None), size=(400, 200))
                success_popup.open()
            else:
                self.password_verified = False
                popup.dismiss()
                popup_content = Label(text="Incorrect admin password")
                error_popup = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
                error_popup.open()

        submit_button = Button(text='Submit')
        submit_button.bind(on_release=submit_password)
        content.add_widget(submit_button)
        popup.open()

    def submit(self):
        password = self.ids.password.text
        re_password = self.ids.password2.text

        if password == admin_acc.get_password():
            popup_content = Label(text="NEW PASSWORD MUST NOT BE THE SAME AS CURRENT PASSWORD")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
            self.ids.password2.text = ""
        else:
            if password == re_password:
                self.open_input_popup(password)
            else:
                popup_content = Label(text="PASSWORD NOT MATCH")
                popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
                popup.open()
                self.ids.password.text = ""
                self.ids.password2.text = ""

        if self.is_change is True:
            popup_content = Label(text="CHANGED SUCCESSFULLY")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
            self.ids.password2.text = ""

    def update_datetime(self):
        self.current_datetime = datetime.now().strftime("%m/%d/%Y\n%I:%M:%S %p")


class SettingsKey(Screen):
    current_datetime = StringProperty("")
    is_change = False
    password_verified = BooleanProperty(False)

    def open_input_popup(self, new_key):
        content = BoxLayout(orientation='vertical')
        security_obj = Security()
        password_input = TextInput(multiline=False, password=True)
        content.add_widget(Label(text='Enter Admin Password:'))
        content.add_widget(password_input)
        popup = Popup(title='Password Input', content=content, size_hint=(None, None), size=(400, 200))

        def submit_password(instance):
            entered_password = password_input.text
            if entered_password == admin_acc.get_password():
                self.password_verified = True
                popup.dismiss()
                self.is_change = True
                security_obj.change_secret_key(new_key)
                DataManager.save()
                Authen.save_account()
                popup_content = Label(text="CHANGED SUCCESSFULLY")
                success_popup = Popup(title='SUCCESS', content=popup_content, size_hint=(None, None), size=(400, 200))
                success_popup.open()
            else:
                self.password_verified = False
                popup.dismiss()
                popup_content = Label(text="Incorrect admin password")
                error_popup = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
                error_popup.open()

        submit_button = Button(text='Submit')
        submit_button.bind(on_release=submit_password)
        content.add_widget(submit_button)
        popup.open()

    def submit(self):
        new_key = self.ids.password.text

        if new_key == Security.get_secret_key():
            popup_content = Label(text="NEW KEY MUST NOT BE THE SAME AS CURRENT KEY")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
        else:
            self.open_input_popup(new_key)


        if self.is_change is True:
            popup_content = Label(text="CHANGED SUCCESSFULLY")
            popup = Popup(title='WARNING', content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
            self.ids.password.text = ""
            Authen.save_account()

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
    inventory = [item for item in my_inv if item is not None]
    inventory = [item for item in inventory if item.name is not None]
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

    Security.set_encryption_key()
    admin_acc, cashier_acc = Authen.retrieve_account()
    my_inv = DataManager.retrieve()
    DataManager.del_expired_product()

    # print("done main")


if __name__ == "__main__":
    main()
    MyApp().run()
