from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import random

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
            self.ids.step_label.text = self.state_list[self.state]
            
        elif direction == 'back':
            self.state -= 1
            self.ids.step_label.text = self.state_list[self.state]                
             
        else:
            self.ids.state_label.text = 'Error'
        
        self.update_navigation()
        self.ids.start_stop.disabled = False           

    def update_navigation(self):
        if self.state == 0:
            self.ids.back.disabled = True
            self.ids.next.disabled = False
        elif self.state == 3:
            self.ids.back.disabled = False
            self.ids.next.disabled = True
        else:
            self.ids.back.disabled = False
            self.ids.next.disabled = False


    def display_state(self,state):
        self.ids.state_label.text = state

    def display_angle_left(self, angle):
        self.ids.angle_left.text = 'Left Arm Angle : ' + angle

    def display_angle_right(self, angle):
        self.ids.angle_right.text = 'Right Arm Angle : ' + angle

    def get_angle(self):
        #angle =  dummy_function()
        angle_l = str(random.randint(0,180)) + '°'
        angle_r = str(random.randint(0,180)) + '°'
        self.display_angle_left(angle_l)
        self.display_angle_right(angle_r)

    def measure(self):
        if self.ids.start_stop.text == 'Start':
            self.display_state('Measurement')
            self.ids.start_stop.text = 'Stop'
            self.ids.back.disabled = True
            self.ids.next.disabled = True

        elif self.ids.start_stop.text == 'Stop':
            self.display_state('Done')
            self.get_angle()
            self.ids.start_stop.text = 'Start'
            self.ids.start_stop.disabled = True
            self.ids.redo.disabled = False
            self.ids.validate.disabled = False
            self.ids.overinput_left.disabled = False
            self.ids.overinput_right.disabled = False
        else:
            self.display_state('Error')
    
    def redo(self):
        self.display_state('Cleared')
        self.display_angle_left('')
        self.display_angle_right('')
        self.ids.start_stop.text = 'Start'
        self.ids.start_stop.disabled = False
        self.ids.redo.disabled = True
        self.ids.validate.disabled = True
        self.ids.overinput_left.disabled = True
        self.ids.overinput_right.disabled = True
        self.ids.next.disabled = True
        self.ids.back.disabled = True
        self.cleaninput()

    def overwriteLeft(self):
        self.display_angle_left(self.ids.overinput_left.text + '°')
    
    def overwriteRight(self):
        self.display_angle_right(self.ids.overinput_right.text + '°')
        
    def cleaninput(self):
        self.ids.overinput_left.text = ''
        self.ids.overinput_right.text = ''      

    def validate(self):
        self.display_state('Validated')
        self.ids.redo.disabled = True
        self.ids.validate.disabled = True
        self.ids.overinput_left.disabled = True
        self.ids.overinput_right.disabled = True
        

        if self.state == 0:
            self.ids.table.ids.flexion_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.flexion_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 1:
            self.ids.table.ids.abduction_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.abduction_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 2:
            self.ids.table.ids.ext_rot_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.ext_rot_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 3:
            self.ids.table.ids.int_rot_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.int_rot_right.text = self.ids.angle_right.text[18:-1] + '°'
        else: 
            self.ids.state_label.text == 'Error'
        
        self.display_angle_left('')
        self.display_angle_right('')
        
        self.update_navigation()
        self.cleaninput()

class ShoulderTestApp(App):
    def build(self):
        return ShoulderWindow()

if __name__ == '__main__':
    ShoulderTestApp().run()