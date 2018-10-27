from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import random

class ShoulderWindow(BoxLayout):
    pass

class ShoulderTestApp(App):
    def build(self):
        return ShoulderWindow()


if __name__ == '__main__':
    ShoulderTestApp().run()