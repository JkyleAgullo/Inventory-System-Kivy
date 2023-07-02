from kivy.config import Config
Config.set('graphics', 'resizable', False)
import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label




class Cashier(Widget):
    product_name= StringProperty("try")

    # insert the string property of the price of the product for printing
    Builder.load_file('cashier.kv')
    def name_validate(self,widget):
        self.product_name = widget.text


    def qty_validate(self, widget):
        self.qty_input_string = widget.text

    my_array = [
        [1],[2]
    ]

    def Array_display(self, array):
        self.cols = len(array[0])

        for row in array:
            for element in row:
                self.add_widget(Label(text=str(element), font_size='28'))



class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Cashier'
        return Cashier()
    #    return AdminADD()




MyApp().run()
#Try().run()