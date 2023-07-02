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




class Cashier(Widget):
    product_name= StringProperty("try")
    name = ObjectProperty(None)
    # insert the string property of the price of the product for printing
    Builder.load_file('cashier.kv')
    def name_validate(self,widget):
        self.product_name = widget.text


    def qty_validate(self, widget):
        self.qty_input_string = widget.text

    my_array = ['Item','two']

    def btn(self):
        Cashier.my_array.append(self.name.text)
        print(self.name.text)
    def Array_display(self, array):
        i=10
        self.cols = len(array[0])
        print(Cashier.my_array[0]) #try lang
        for row in array:
            for element in row:
                i=i+30
                self.add_widget(Label(text=str(element), font_size='28',pos=(100,300+i)))




class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Cashier'
        return Cashier()
    #    return AdminADD()




MyApp().run()
#Try().run()