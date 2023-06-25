import kivy.utils
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window



class MyGrid(Widget):
    pass

class Trylang(Widget):
    pass



class MyApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        return MyGrid()

class Try(App):
    def build(self):
        return MyGrid()



#MyApp().run()
Try().run()