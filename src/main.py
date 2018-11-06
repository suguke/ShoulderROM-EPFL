from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file('screenmeasure.kv')
Builder.load_file('protocol.kv')
Builder.load_file('manager.kv')
Builder.load_file('screenresult.kv')
Builder.load_file('screenpatient.kv')
Builder.load_file('screenquestions.kv')


import random
import csv

class Protocol(BoxLayout):
    pass

class ScreenPatient(Screen):
    
    def set_patient(self):
        id = self.ids.patient_code.text
        if id.isdigit():
            self.manager.set_patient(self.ids.patient_code.text)
        else:
            self.ids.patient_code.text = 'Invalide input'

class ScreenQuestions(Screen):
    pass


class ScreenMeasure(Screen):
    
    state = 1
    state_list = ['', 'Flexion', 'Abduction', 'External Rotation', 'Internal Rotation', '']

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
        self.ids.next.disabled = False
        self.ids.back.disabled = False

        if self.state == 0:
            self.state = 1
            self.set_state()
            self.manager.current = 'Questions Screen'
        elif self.state == 1:
            self.ids.back.text = 'Retour aux questions'   
        elif self.state ==4:
            self.ids.next.text = 'Résultats'
        elif self.state == 5:
            self.state = 4
            self.set_state()
            self.manager.current = 'Results Screen'
        else:
            self.ids.next.text = 'Suivant'
            self.ids.back.text = 'Précédant'

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
        

        if self.state == 1:
            self.ids.table.ids.flexion_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.flexion_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 2:
            self.ids.table.ids.abduction_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.abduction_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 3:
            self.ids.table.ids.ext_rot_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.ext_rot_right.text = self.ids.angle_right.text[18:-1] + '°'
        elif self.state == 4:
            self.ids.table.ids.int_rot_left.text = self.ids.angle_left.text[17:-1] + '°'
            self.ids.table.ids.int_rot_right.text = self.ids.angle_right.text[18:-1] + '°'
        else: 
            self.ids.state_label.text == 'Error'
        
        self.display_angle_left('')
        self.display_angle_right('')
        
        self.update_navigation()
        self.cleaninput()

class ScreenResult(Screen):
    pass

class Manager(ScreenManager):
    screen_patient = ObjectProperty(None)
    screen_questions = ObjectProperty(None)
    screen_measure = ObjectProperty(None)
    screen_result = ObjectProperty(None)
    data_dic = {}
    patient_id = ''

    def set_store(self):
        self.data_dic['Flexion, Left Arm'] = self.screen_measure.ids.table.ids.flexion_left.text
        self.data_dic['Flexion, Right Arm'] = self.screen_measure.ids.table.ids.flexion_right.text
        self.data_dic['Abduction, Left Arm'] = self.screen_measure.ids.table.ids.abduction_left.text
        self.data_dic['Abduction, Right Arm'] = self.screen_measure.ids.table.ids.abduction_right.text
        self.data_dic['External Rotation, Left Arm'] = self.screen_measure.ids.table.ids.ext_rot_left.text
        self.data_dic['External Rotation, Right Arm'] = self.screen_measure.ids.table.ids.ext_rot_right.text
        self.data_dic['Internal Rotation Left Arm'] = self.screen_measure.ids.table.ids.int_rot_left.text
        self.data_dic['Internal Rotation Right Arm'] = self.screen_measure.ids.table.ids.int_rot_right.text
    
    def get_store(self):
        self.screen_result.ids.result.ids.flexion_left.text = self.data_dic.get('Flexion, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.flexion_right.text = self.data_dic.get('Flexion, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.abduction_left.text = self.data_dic.get('Abduction, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.abduction_right.text = self.data_dic.get('Abduction, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.ext_rot_left.text = self.data_dic.get('External Rotation, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.ext_rot_right.text = self.data_dic.get('External Rotation, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.int_rot_left.text = self.data_dic.get('Internal Rotation Left Arm', 'Not found')
        self.screen_result.ids.result.ids.int_rot_right.text = self.data_dic.get('Internal Rotation Right Arm', 'Not found') 

    def score(self):
        score_value = str(random.randint(0, 100)) + '%'
        self.data_dic['Score'] = score_value
        return score_value

    def save(self):

        with open('../Results/shoulderROM_score.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.data_dic.keys())
            writer.writeheader()
            writer.writerow(self.data_dic)

    def set_patient(self, id):
        self.patient_id = id


class ShoulderTestApp(App):
    def build(self):
        return Manager()

if __name__ == '__main__':
    ShoulderTestApp().run()