import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen





class AdminDB(Widget):

    text_input_string = StringProperty("try")
    qty_input_string = StringProperty("1")

    # insert the string property of the price of the product for printing
    Builder.load_file('cashier.kv')
    def text_validate(self, widget):
        self.text_input_string = widget.text
    def qty_validate(self, widget):
        self.qty_input_string = widget.text



class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        self.title = 'Inventory Admin'
        return AdminDB()
    #    return AdminADD()




MyApp().run()
#Try().run()