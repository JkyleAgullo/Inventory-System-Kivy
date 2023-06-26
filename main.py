import kivy.utils
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window


kv = Builder.load_file("my.kv")






class MyApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        self.title='Inventory_Admin'
        return kv




MyApp().run()
#Try().run()