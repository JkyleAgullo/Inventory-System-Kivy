
from kivy.uix.widget import Widget
from kivy.app import App



class MyGrid(Widget):
    pass


#        self.cols = 2
#        self.add_widget(Label(text="product name: "))
#        self.name = TextInput(multiline=False)
#        self.add_widget(self.name)


class MyApp(App):
    def build(self):
        return MyGrid()



MyApp().run()