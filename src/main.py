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
import pandas as pd

class Protocol(BoxLayout):
    pass

class ScreenPatient(Screen):
    p_id = False
    c_id = False
    
    def set_patient(self):
        self.p_id = False
        id = self.ids.patient_code.text
        if id.isdigit() and len(id) == 7:
            self.p_id = self.manager.set_patient(id)[0]
            if self.p_id == False:
                self.ids.patient_code.text = 'Invalid: unknown patient'
            else:
                self.ids.consultation_code.disabled = False
        else:
            self.ids.patient_code.text = 'Invalid: 7 digits'
            self.p_id = False
        self.disable_button()
        

    def set_consultation(self):
        self.c_id = False
        id = self.ids.consultation_code.text
        if id.isdigit() and len(id) == 8:
            self.c_id = self.manager.set_consultation(id, self.ids.patient_code.text)
            if self.c_id == False:
                self.ids.consultation_code.text = 'Invalid: double consultation'
        else:
            self.ids.consultation_code.text = 'Invalid: 8 digits'
            self.c_id = False
        self.disable_button()
    
    def disable_button(self):
        if self.p_id and self.c_id:
            self.ids.go.disabled = False
        else:
            self.ids.go.disabled = True
    
    def validate(self):
        self.manager.current = 'Questions Screen'

class ScreenQuestions(Screen):
         
    def validate(self):
        self.manager.set_store_questions()
        self.manager.current = 'Measurement Screen'


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
            if self.ids.table.ids.flexion_left.text == '' or \
            self.ids.table.ids.flexion_right.text == '' or self.ids.table.ids.abduction_left.text == '' or\
             self.ids.table.ids.abduction_right.text == '' or self.ids.table.ids.ext_rot_left.text == '' or\
              self.ids.table.ids.ext_rot_right.text == '' or self.ids.table.ids.int_rot_left.text == '' or\
               self.ids.table.ids.int_rot_right.text == '':
                self.ids.next.disabled = True
        elif self.state == 5:
            self.state = 4
            self.set_state()
            self.manager.current = 'Results Screen'
        else:
            self.ids.next.text = 'Suivant'
            self.ids.back.text = 'Précédent'


        

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
    df_patients = ''
    df_consultations = ''


    def set_store_questions(self):
        self.data_dic['Pain, Left Arm'] = self.screen_questions.ids.list1_l.text
        self.data_dic['Pain, Right Arm'] = self.screen_questions.ids.list1_r.text
        self.data_dic['Activity 1, Left Arm'] = self.screen_questions.ids.list2_l.text
        self.data_dic['Activity 1, Right Arm'] = self.screen_questions.ids.list2_r.text
        self.data_dic['Activity 2, Left Arm'] = self.screen_questions.ids.list3_l.text
        self.data_dic['Activity 2, Right Arm'] = self.screen_questions.ids.list3_r.text
        self.data_dic['Activity 3, Left Arm'] = self.screen_questions.ids.list4_l.text
        self.data_dic['Activity 3, Right Arm'] = self.screen_questions.ids.list4_r.text
        self.data_dic['Activity 4, Left Arm'] = self.screen_questions.ids.list5_l.text
        self.data_dic['Activity 4, Right Arm'] = self.screen_questions.ids.list5_r.text

    def set_store_measures(self):
        self.data_dic['Flexion, Left Arm'] = \
            self.screen_measure.ids.table.ids.flexion_left.text[:-1]
        self.data_dic['Flexion, Right Arm'] = \
            self.screen_measure.ids.table.ids.flexion_right.text[:-1]
        self.data_dic['Abduction, Left Arm'] = \
            self.screen_measure.ids.table.ids.abduction_left.text[:-1]
        self.data_dic['Abduction, Right Arm'] = \
            self.screen_measure.ids.table.ids.abduction_right.text[:-1]
        self.data_dic['External Rotation, Left Arm'] = \
            self.screen_measure.ids.table.ids.ext_rot_left.text[:-1]
        self.data_dic['External Rotation, Right Arm'] = \
            self.screen_measure.ids.table.ids.ext_rot_right.text[:-1]
        self.data_dic['Internal Rotation, Left Arm'] = \
            self.screen_measure.ids.table.ids.int_rot_left.text[:-1]
        self.data_dic['Internal Rotation, Right Arm'] = \
            self.screen_measure.ids.table.ids.int_rot_right.text[:-1]
    
    def set_store(self):
        self.set_store_measures()
        self.set_store_questions()

    def get_store(self):
        self.screen_result.ids.result.ids.flexion_left.text = \
            self.data_dic.get('Flexion, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.flexion_right.text = \
            self.data_dic.get('Flexion, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.abduction_left.text = \
            self.data_dic.get('Abduction, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.abduction_right.text = \
            self.data_dic.get('Abduction, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.ext_rot_left.text = \
            self.data_dic.get('External Rotation, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.ext_rot_right.text = \
            self.data_dic.get('External Rotation, Right Arm', 'Not found')
        self.screen_result.ids.result.ids.int_rot_left.text = \
            self.data_dic.get('Internal Rotation, Left Arm', 'Not found')
        self.screen_result.ids.result.ids.int_rot_right.text = \
            self.data_dic.get('Internal Rotation, Right Arm', 'Not found') 
        self.score()

    def score(self):
        score_left = self.get_score_questions ('Left')
        score_right = self.get_score_questions('Right')
        score_diff = abs(score_left - score_right)

        self.data_dic['Score Left'] = score_left
        self.data_dic['Score Right'] = score_right
        self.screen_result.ids.left.text = str(score_left)
        self.screen_result.ids.right.text = str(score_right)
        self.screen_result.ids.diff.text = str(score_diff)

    def get_score_questions(self, side):
        score = 0
        q = self.data_dic.get('Pain, ' + side + ' Arm')

        if q == 'Aucune':
            score += 15
        elif q == 'Legere':
            score += 10
        elif q == 'Moderee':
            score += 5
        elif q == 'Severe':
            score += 0
        else:
            score += 999

        q = self.data_dic.get('Activity 1, ' + side + ' Arm')

        if q == 'Aucune':
            score += 4
        elif q == 'Legere':
            score += 3
        elif q == 'Moderee':
            score += 2
        elif q == 'Severe':
            score += 1
        elif q == 'Impossible':
            score += 0
        else:
            score += 999
        
        q = self.data_dic.get('Activity 2, ' + side + ' Arm')

        if q == 'Aucune':
            score += 4
        elif q == 'Legere':
            score += 3
        elif q == 'Moderee':
            score += 2
        elif q == 'Severe':
            score += 1
        elif q == 'Impossible':
            score += 0
        else:
            score += 999
        
        q = self.data_dic.get('Activity 3, ' + side + ' Arm')

        if q == 'Jamais':
            score += 2
        elif q == 'Occasionnellement':
            score += 1
        elif q == 'Toutes les nuits':
            score += 0
        else:
            score += 999

        q = self.data_dic.get('Activity 4, ' + side + ' Arm')

        if q == 'Au-dessus de la tete':
            score += 10
        elif q == 'Tete':
            score += 8
        elif q == 'Cou':
            score += 6
        elif q == 'Xiphoide':
            score += 4
        elif q == 'Taille':
            score += 2
        else:
            score += 999

        q = int(self.data_dic.get('Flexion, ' + side + ' Arm'))

        if q < 0:
            score += 999
        elif q <= 30:
            score += 0
        elif q <= 60:
            score += 2
        elif q <= 90:
            score += 4
        elif q <= 120:
            score += 6
        elif q <= 150:
            score += 8
        elif q > 150:
            score += 10
        else: 
            score += 999

        q = int(self.data_dic.get('Abduction, ' + side + ' Arm'))

        if q < 0:
            score += 999
        elif q <= 30:
            score += 0
        elif q <= 60:
            score += 2
        elif q <= 90:
            score += 4
        elif q <= 120:
            score += 6
        elif q <= 150:
            score += 8
        elif q > 150:
            score += 10
        else: 
            score += 999

        q = int(self.data_dic.get('External Rotation, ' + side + ' Arm'))

        if q < 0:
            score += 999
        elif q <= 15:
            score += 0
        elif q <= 30:
            score += 2
        elif q <= 45:
            score += 4
        elif q <= 60:
            score += 6
        elif q <= 75:
            score += 8
        elif q > 75:
            score += 10
        else: 
            score += 999

        q = int(self.data_dic.get('Internal Rotation, ' + side + ' Arm'))

        if q < 0:
            score += 999
        elif q <= 15:
            score += 0
        elif q <= 30:
            score += 2
        elif q <= 45:
            score += 4
        elif q <= 60:
            score += 6
        elif q <= 75:
            score += 8
        elif q > 75:
            score += 10
        else: 
            score += 999

        return score

    def save(self):

        with open('../Results/shoulderROM_score.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.data_dic.keys())
            writer.writeheader()
            writer.writerow(self.data_dic)

    def set_patient(self, id):
        return pd.Series(int(id)).isin(self.df_patients.index)
        
    def set_consultation(self, id, patient):
        if self.set_patient(patient)[0] and (not pd.Series(int(id)).isin(self.df_consultations.index)[0]):
            self.df_consultations.loc[int(id)] = ['', '']
            list_consult = self.df_patients.loc[int(patient), 'consultation_list']
            list_consult.add(int(id))
            self.df_patients.loc[int(patient), 'consultation_list'] =  list_consult
            return True
        else:
            return False


class ShoulderTestApp(App):
    def build(self):
        #### Temporary solution : custom Pandas dataframes
        m = Manager()
        df_patients = pd.DataFrame(
            {'patient_code': [1001111, 1001112, 1001113],
             'consultation_list': [{10120010, 10120011, 10120012, 10120013}, \
             {10120021}, {10120031, 10120032}]},
        )
        df_patients.set_index('patient_code', inplace=True)
        m.df_patients = df_patients
        df_consultations = pd.DataFrame(
                { 'consultation_code' : [10120010, 10120011, 10120012, 10120013, \
                10120021, 10120031, 10120032],
                  'score_left': [10, 15, 13, 42, 37, 38, 28],
                  'score_right': [40, 39,37,12,13,11,27]                    
                })     
        df_consultations.set_index('consultation_code', inplace=True)
        m.df_consultations = df_consultations
        ####
        return m

if __name__ == '__main__':
    ShoulderTestApp().run()