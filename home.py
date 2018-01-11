import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import json
import db_ops

from elements import Elements


class Home(App):

    def build(self):
        elements = Elements()
        main_frame = BoxLayout()
        main_frame.add_widget(elements)
        return main_frame

    def on_stop(self):
        db_ops.client.close()

if __name__ == '__main__':
    # Window.maximize()
    # Window.minimum_width = 900
    # Window.minimum_height = 600
    Home().run()
