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


class AdminDB(Screen):
    #todo: design admin dashboard
    text_input_string = StringProperty("try")
    qty_input_string = StringProperty("1")

    # insert the string property of the price of the product for printing

    def text_validate(self, widget):
        self.text_input_string = widget.text

    def qty_validate(self, widget):
        self.qty_input_string = widget.text


class SplashWindow(Screen):
    def update_progress(self, value):
        self.ids.progress_bar.value = value
        if value >= 100:
            app = App.get_running_app()
            app.root.transition = NoTransition()
            app.root.current = "login"


class AdminADD(Screen):
    #todo: add design to admin add
    pass


class AdminDisplay(Screen):
    #todo: add design to display
    pass


class AdminSettings(Screen):
    #todo: add design to settings
    pass


class WindowManager(ScreenManager):
    pass


class AdminLoginTry(Screen):
    def clear(self):
        self.ids.user.text = ""
        self.ids.password.text = ""


Builder.load_file('screen.kv')


# Builder.load_file('Mainpanel.kv')

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

    def update_progress_bar(self, dt):
        # Increment the progress bar value
        current_value = self.root.get_screen('splash').ids.progress_bar.value
        new_value = current_value + 50
        self.root.get_screen('splash').update_progress(new_value)
        if new_value >= 100:
            # Stop the progress bar updates when the value reaches 100
            Clock.unschedule(self.update_progress_bar)


if __name__ == "__main__":
    MyApp().run()