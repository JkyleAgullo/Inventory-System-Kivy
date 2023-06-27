import kivy.utils
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp




class MyApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)

        self.title = 'Inventory_Admin'

        return Builder.load_file("try.kv")


MyApp().run()
# Try().run()
