from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import random
import re

class Protocol(BoxLayout):
    pass

class ShoulderWindow(BoxLayout):
    
    state = 0
    state_list = ['Flexion', 'Abduction', 'External Rotation', 'Internal Rotation']

    def __init__(self):
        super(ShoulderWindow, self).__init__()
        self.set_state()

    def set_state(self):
        self.ids.step_label.text = self.state_list[self.state]

    def update_state(self, direction):
        if direction == 'next':
            self.state += 1
            self.ids.back.disabled = False
            if self.state == 3:
                self.ids.next.disabled = True
            self.ids.start_stop.disabled = False
            self.ids.step_label.text = self.state_list[self.state]                
            
        elif direction == 'back':
            self.state -= 1
            self.ids.next.disabled = False
            if self.state == 0:
                self.ids.back.disabled = True
            self.ids.start_stop.disabled = False   
            self.ids.step_label.text = self.state_list[self.state]                
             

        else:
            self.ids.state_label.text = 'Error'



    def display_state(self,state):
        self.ids.state_label.text = state

    def display_angle(self, angle):
        self.ids.angle_label.text = 'Angle : ' + angle + ' degrees'

    def get_angle(self):
        #angle =  dummy_function()
        self.display_angle(str(random.randint(0,180)))

    def measure(self):
        if self.ids.start_stop.text == 'Start':
            self.display_state('Measurement')
            self.ids.start_stop.text = 'Stop'

        elif self.ids.start_stop.text == 'Stop':
            self.display_state('Done')
            self.get_angle()
            self.ids.start_stop.text = 'Start'
            self.ids.start_stop.disabled = True
            self.ids.redo.disabled = False
            self.ids.validate.disabled = False
            self.ids.overinput.disabled = False
        else:
            self.display_state('Error')
    
    def redo(self):
        self.display_state('Cleared')
        self.ids.start_stop.text = 'Start'
        self.ids.start_stop.disabled = False
        self.ids.redo.disabled = True
        self.ids.validate.disabled = True
        self.ids.overwrite.disabled = True
        self.ids.overinput.disabled = True
        self.ids.overinput.text = 'Overwrite'


    def overinput(self):
        if re.match('^[0-9]+$', self.ids.overinput.text):
            self.ids.overwrite.disabled = False
        else:
            self.ids.overwrite.disabled = True
    
    def overwrite(self):
        self.display_angle(self.ids.overinput.text)

    def validate(self):
        self.display_state('Validated')
        self.ids.redo.disabled = True
        self.ids.validate.disabled = True
        self.ids.overwrite.disabled = True
        self.ids.overinput.disabled = True
        self.ids.overinput.text = 'Overwrite'

        if self.state == 0:
            self.ids.table.ids.flexion.text = self.ids.angle_label.text[8:-8]
        elif self.state == 1:
            self.ids.table.ids.abduction.text = self.ids.angle_label.text[8:-8]
        elif self.state == 2:
            self.ids.table.ids.ext_rot.text = self.ids.angle_label.text[8:-8]
        elif self.state == 3:
            self.ids.table.ids.int_rot.text = self.ids.angle_label.text[8:-8]
        else: 
            self.ids.state_label.text == 'Error'
        
        self.ids.angle_label.text = 'Angle :'



        

        

    

class ShoulderTestApp(App):
    def build(self):

        return ShoulderWindow()

    

    


if __name__ == '__main__':
    ShoulderTestApp().run()