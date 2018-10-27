from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import random
import time

class ShoulderWindow(BoxLayout):
    def display_text(self,angle):
        self.ids.my_textinput.text = angle

    def get_angle(self):
        #angle =  dummy_function()
        self.display_text(str(random.randint(0,180)))

    def measure(self):
        if self.ids.start_stop.text == 'Start':
            self.display_text('Measurement')
            self.ids.start_stop.text = 'Stop'

        elif self.ids.start_stop.text == 'Stop':
            self.get_angle()
            self.ids.start_stop.text = 'Start'
            self.ids.start_stop.disabled = True
            self.ids.redo.disabled = False
            self.ids.validate.disabled = False

        else:
            self.display_angle('Error')
    
    def redo(self):
        self.display_text('Input a value')
        self.ids.start_stop.text = 'Start'
        self.ids.start_stop.disabled = False
        self.ids.redo.disabled = True
        self.ids.validate.disabled = True

        

        

    

class ShoulderTestApp(App):
    def build(self):

        return ShoulderWindow()

    

    


if __name__ == '__main__':
    ShoulderTestApp().run()