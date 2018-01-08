import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
import json

from elements import Elements


class Home(App):
    
    def build(self):
        elements = Elements()
        main_frame = BoxLayout()
        main_frame.add_widget(elements)
        return main_frame

if __name__ == '__main__':
    Home().run()
