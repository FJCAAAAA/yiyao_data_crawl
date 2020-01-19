#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AdaGetSymName.py
@Author: Fengjicheng
@Date  : 2019/12/11
@Desc  : 查询Ada对应症状名称
'''

import json
import re
import traceback
from tqdm import tqdm
from AdaGetQA import Ada

symptoms_list = ['amnesia', 'blister in the oral cavity', 'tender scalp', 'muscular tenderness of the lower back muscles', 'dyspnoea', 'pruritus, generalised', 'sneezing', 'dyspepsia/indigestion', 'scleral icterus', 'fear of losing control', 'dysphagia', 'erosion and ulceration of the lower extremity', 'patch in the mouth', 'anterior neck pain', 'generalised muscular wasting', 'upper extremity paresis', 'asthenopia', 'pruritus, ears', 'facial pallor', 'generalised hematomas', 'lowered skin temperature of the finger', 'preauricular swelling', 'chest tightness', 'muscle cramps in the lower extremity', 'muscular tenderness of the chest muscles', 'fear of panic attack recurrence', 'preauricular pain', 'temporal tenderness', 'muscular tenseness of the back muscles', 'erythema of upper extremity', 'muscular tenderness of the neck muscles', 'swelling of the external chest wall', 'tingling or numbness of the lower leg', 'painful gums', 'tingling or numbness of the lower extremity', 'otalgia', 'increased drive', 'aural fullness', 'hearing deficit', 'muscular tenseness of the chest muscles', 'raised bumps on the lower extremity', 'hyposmia', 'skin rash of the face', 'ear swelling', 'impaired colour vision', 'dizziness', 'pale limbs', 'impaired vision', 'sialorrhoea', 'erosions and ulcerations of the oral cavity', 'acute change in mental status', 'blister on the trunk', 'rapid pulse', 'underweight', 'back pain', 'wound healing disturbances', 'tremor', 'toe pain', 'mood lability', 'impaired control over the use of alcohol or other substances', 'dry mouth', 'swelling lateral ankle', 'digital pallor', 'throat tightness', 'blue lips', 'erythema of the tonsil', 'learning difficulty', 'ankle pain', 'soft tissue lump in the groin', 'shoulder asymmetry', 'periorbital swelling', 'loss of appetite', 'swelling of the hand', 'tonsillar exudate', 'muscle cramps in the back', 'anxiety', 'specific fear', 'feeling of heavy legs', 'staring episode', 'decreased urine output', 'skin temperature, regionally lowered', 'swelling, toe joint', 'pain in lower jaw', 'weight gain', 'hallucination', 'torticollis', 'arrest in activity', 'muscle cramps', 'cervical lymphadenopathy', 'blue toes', 'lowered skin temperature of the leg', 'involuntary repetitive motor episodes', 'difficulty falling or staying asleep', 'abdominal tenderness', 'posterior neck pain', 'gait impairment', 'photosensitivity of the skin', 'erosion and ulceration of the trunk', 'haematochezia', 'dry throat', 'nausea', 'recurrent respiratory tract infections', 'pain of the oral cavity', 'blue skin, arm', 'erythema of the lower leg', 'visible jugular veins', 'limited range of motion of the shoulder', 'dysphonia', 'high blood pressure', 'lower leg pain', 'erythema of the skin, generalised', 'pruritus, eyes', 'spots or discolouration of the teeth', 'hyperhidrosis of the face', 'skin rash of the lower extremity', 'soft tissue lump on the shin', 'audible wheezing without stethoscope', 'post-orbital pain', 'pruritus, throat', 'elevated skin temperature of the lower extremity', 'spots on the lower extremity', 'body temperature, decreased', 'hand pain', 'spots on the lower leg', 'pruritus, oral cavity', 'tachypnoea', 'upper extremity pain', 'oral mucosal bleeding', 'lower extremity pain', 'finger pain', 'diminished sense of taste', 'headache', 'calf pain', 'swelling of the upper arm', 'sore throat', 'euphoria', 'dry skin, generalised', 'cough', 'erythema of the cheeks', 'ocular discharge', 'brittle nails', 'muscular tenderness of the masticatory muscle', 'haematemesis', 'whispering voice', 'decreased vocal range', 'nocturia', 'repetitive or stereotyped behaviours', 'alopecia', 'neck pain', 'tragal tenderness', 'erythema of the trunk', 'sudden intense fear', 'stooped posture', 'swelling of the lower extremity', 'excessive bleeding', 'snoring', 'lower back pain', 'increased sleep duration', 'increased throat clearing', 'tingling or numbness of the trunk', 'sticky eyelid', 'flushing', 'erythema of the throat', 'finger joint pain', 'swollen finger paronychium', 'trismus', 'otorrhoea', 'thumb pain', 'swelling of the upper extremity', 'red eye', 'upper back pain', 'change in stool colour', 'avoidance behaviour', 'anhedonia', 'generalised muscular tenseness', 'myalgia', 'limited range of motion in lumbar spine', 'muscle cramps in the arm and hand', 'conception difficulties in men', 'heartburn', 'blepharospasm', 'inability to bear weight', 'lower extremity paresis', 'swelling of the foot', 'fever', 'inability to clear the ear with changing barometric pressure', 'swelling of the scalp, localised', 'foamy urine', 'swelling of the lower leg', 'dark urine', 'tingling or numbness of the first three fingers', 'height loss', 'hyperhidrosis, generalised', 'blue fingers', 'muscular tenseness of the masticatory muscles', 'flank pain', 'impaired concentration', 'loose pellet in the mouth', 'complete loss of consciousness', 'tingling or numbness of the hand', 'imbalance', 'pallor of upper extremity', 'odynophonia', 'erythema of the face', 'photophobia', 'swelling of the forearm', 'swelling of the shin', 'swelling, ankle joint', 'abdominal pain', 'bradypnoea', 'eye pain', 'generalised limited range of motion', 'toothache', 'hoarseness', 'skin rash of the lower leg', 'easy bruising', 'skin rash, generalised', 'early satiety', 'periorbital pain', 'erythema of the neck', 'pallor of lower extremity', 'bad taste in mouth', 'periodic cessation of breathing during sleep', 'acid reflux', 'mental irritability', 'elevated skin temperature of the face', 'difficulties in chewing', 'haematoma on the trunk', 'pruritus, nasal cavity', 'generalised arthralgia', 'palpitation', 'slow pulse', 'malaise', 'pain in upper jaw', 'chest pain', 'nasal pain', 'decreased sleep duration', 'odynophagia', 'foreign body sensation in the eye', 'heat intolerance', 'raised bumps on the extensor sides of the extremities', 'verrucous skin lesion on the head and neck', 'lowered skin temperature of the limbs', 'nasal discharge', 'blue skin, leg', 'convulsion', 'tenderness, ankle', 'toenail discolouration', 'impaired fine motor skills', 'weight loss', 'polydipsia', 'confusion', 'increased tearing', 'muscular tenderness of the lower extremity', 'swelling of the whole neck', 'erosion and ulceration of the foot', 'perfectionism', 'vomiting', 'excessive daytime sleepiness', 'aphonia', 'temporomandibular joint pain', 'white tongue', 'gasping during sleep', 'hyperactivity', 'erythema of the forearm', 'limited range of motion of the neck', 'limited range of motion of the spine', 'epistaxis', 'swelling of the eyelid', 'anisocoria', 'pain in the axilla', 'nasal congestion', 'facial pain', 'blue skin, foot', 'vocal fatigue', 'fatigue', 'blue skin, hand', 'facial swelling', 'mucosal erythema of the tongue', 'foot pain', 'chills', 'recurrent skin infections', 'morning stiffness', 'increased appetite', 'diarrhoea', 'erythema of lower extremity', 'sinus pain', 'red-coloured urine', 'reduced exercise tolerance']
obj = Ada()
pattern1 = re.compile(':')

def get_all_ada_sym():
    ada_symptoms_list = []
    symptoms_dict = {}
    for sym in tqdm(symptoms_list):
        qa = obj.get_ada_sym(sym)
        qa_data_list = json.loads(qa).get('data')
        if len(qa_data_list) > 0:
            ada_sym = qa_data_list[0].get('key')
            ada_sym_name = pattern1.split(ada_sym)[1]
        else:
            ada_sym_name = ''
        ada_symptoms_list.append(ada_sym_name)
        symptoms_dict[sym] = ada_sym_name
    print(ada_symptoms_list)
    print(json.dumps(symptoms_dict))

if __name__ == '__main__':
    try:
        get_all_ada_sym()
    except Exception:
        print(traceback.format_exc())

