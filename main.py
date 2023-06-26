import kivy.utils
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


kv = Builder.load_file("my.kv")

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        Window.size=(1080,720)
        self.title='Inventory_Admin'
        return kv




MyApp().run()
#Try().run()