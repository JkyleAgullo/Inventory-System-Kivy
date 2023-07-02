import kivy.utils
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar


class AdminDB(Screen):
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


class LoginWindow(Screen):
    pass


class AdminADD(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("screen.kv")


class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1080, 720)
        return kv

    def on_start(self):
        # Schedule the progress bar updates
        Clock.schedule_interval(self.update_progress_bar, 0.1)

    def update_progress_bar(self, dt):
        # Increment the progress bar value
        current_value = self.root.get_screen('splash').ids.progress_bar.value
        new_value = current_value + 1
        self.root.get_screen('splash').update_progress(new_value)
        if new_value >= 100:
            # Stop the progress bar updates when the value reaches 100
            Clock.unschedule(self.update_progress_bar)


if __name__ == "__main__":
    MyApp().run()
