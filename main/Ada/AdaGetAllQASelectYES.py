#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AdaGetAllQA.py
@Author: Fengjicheng
@Date  : 2019/11/26
@Desc  : 获取Ada app对话信息--数据处理
'''
import requests
import random
import json
import traceback
import time
import datetime
from AdaGetQA import Ada
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

# symptoms_list = ['Headache', 'Cough', 'Sneezing', 'SoreThroat', 'NasalDischarge', 'NasalCongestion', 'Malaise',
#                  'Fever', 'Otalgia', 'Myalgia']
# symptoms_list = ['Amnesia', 'ErosionsAndUlcerationsOfTheOralCavity', 'TenderScalp', 'MuscularTendernessOfTheLowerBackMuscles', 'Dyspnea', 'Anxiety', 'Sneezing', 'DyspepsiaIndigestion', 'FearOfLosingControl', 'Dysphagia', 'ErosionAndOrUlcerationOfThePenis', 'PatchInTheMouth', 'PosteriorNeckPain', 'Myalgia', 'DysesthesiaOfTheLowerExtremity', 'ProminentEars', 'FacialPallor', 'EasyBruising', 'LoweredTemperatureOfTheFinger', 'LumpOnTheFace', 'ChestPain', 'MuscleCrampsInTheBack', 'Myalgia', 'FearOfPanicAttackRecurrence', 'MuscularTendernessOfTheThoracicBackMuscles', 'SkinRashOfTheTrunk', 'MuscularTendernessOfTheNeckMuscles', 'ChestPain', 'TinglingOrNumbnessOfTheLowerLeg', 'PainfulGums', 'Paresthesia', 'Otalgia', 'IncreasedDrive', 'AuralFullness', 'HearingDeficit', 'MuscularTensenessOfTheNeckMuscles', 'RaisedBumpsOnTheFace', 'SkinRashOfTheFace', 'EarSwelling', 'ImpairedColorVision', 'Dizziness', 'PaleLimbs', 'ImpairedVision', 'Sialorrhea', 'ErosionAndorUlcerationOfTheToes', 'Confusion', 'BlisterOnTheTrunk', 'RapidPulse', 'Underweight', 'BackPain', 'PoorWoundHealing', 'Tremor', 'ToePain', 'MoodLability', 'SelfDestructiveBehavior', 'DryMouth', 'AnklePain', 'FacialPallor', 'ThroatTightness', 'BlueLips', 'TonsillopharyngealExudate', 'LearningDifficulty', 'AnklePain', 'BreastLump', 'ShoulderAsymmetry', 'FacialSwelling', 'LossOfAppetite', 'SwellingOfTheHand', 'TonsillopharyngealExudate', 'MuscleCrampsInTheBack', 'Anxiety', 'SpecificFear', 'FeelingOfHeavyLegs', 'StaringEpisode', 'DecreasedUrineOutput', 'LoweredTemperatureOfTheUpperExtremity', 'EarSwelling', 'PainInLowerJaw', 'WeightGain', 'OlfactoryHallucination', 'Torticollis', 'ArrestInActivity', 'MuscleCramps', 'CervicalLymphadenopathy', 'LoweredTemperatureOfTheToes', 'LoweredTemperatureOfTheLowerExtremity', 'RepetitiveOrStereotypedBehaviors', 'DifficultyFallingOrStayingAsleep', 'AbdominalTenderness', 'PosteriorNeckPain', 'GaitImpairment', 'Photophobia', 'ErosionAndOrUlcerationOfThePenis', 'DryThroat', 'Nausea', 'RecurrentRespiratoryTractInfections', 'PainOfTheOralCavity', 'BlueSkinPenis', 'SwellingOfTheLowerExtremity', 'VisibleJugularVeins', 'LimitedRangeOfMotionOfTheShoulder', 'DepressedMood', 'HighBloodPressure', 'LowerLegPain', 'Anxiety', 'SquintingToFocusVision', 'SpotsOrDiscolorationOfTeeth', 'SkinRashGeneralized', 'AnalMassOnExamination', 'HearingDeficit', 'DryThroat', 'BodyTemperatureDecreased', 'SpotOnTheLowerExtremity', 'Fever', 'HandPain', 'SpotOnTheLowerLeg', 'MassInTheOralCavity', 'AbdominalPain', 'OralMucosalBleeding', 'LowerExtremityPain', 'FingerPain', 'DiminishedSenseOfTaste', 'Headache', 'CalfPain', 'SwellingOfTheUpperArm', 'SoreThroat', 'Euphoria', 'DrySkinOfTheFoot', 'Cough', 'ElevatedSkinTemperatureOfTheFace', 'OcularDischarge', 'BrittleNails', 'Myalgia', 'WhisperingVoice', 'DecreasedVocalRange', 'Nocturia', 'Obsession', 'Alopecia', 'NuchalPain', 'AbdominalTenderness', 'SkinRashOfTheTrunk', 'SuddenIntenseFear', 'StoopedPosture', 'SwellingOfTheLowerExtremity', 'ExcessiveBleeding', 'Snoring', 'LowerBackPain', 'IncreasedSleepDuration', 'ThroatClearing', 'TinglingOrNumbnessOfTheTrunk', 'StickyEyelid', 'Flushing', 'FingerJointPain', 'SwellingOfTheFingers', 'Trismus', 'RapidSpeech', 'ThumbPain', 'SwellingOfTheUpperExtremity', 'RedEyes', 'UpperBackPain', 'Diarrhea', 'AvoidanceBehaviour', 'DepressedMood', 'Myalgia', 'Myalgia', 'LimitedRangeOfMotionOfTheNeck', 'MuscleCrampsInTheArmsAndHands', 'Constipation', 'Heartburn', 'InabilityToBearWeight', 'DysesthesiaOfTheLowerExtremity', 'SwellingOfTheFoot', 'Fever', 'InabilityToClearTheEarWithChangingBarometricPressure', 'SwellingOfTheScalpGeneralized', 'FoamyUrine', 'ShinSwelling', 'BrownColoredUrine', 'TinglingOrNumbnessOfTheFirstThreeFingers', 'HeightLoss', 'Anxiety', 'BlueSkinFingers', 'MuscularTensenessOfTheNeckMuscles', 'FlankPain', 'ImpairedConcentration', 'LooseClotInTheMouth', 'Abulia', 'TinglingOrNumbnessOfTheHand', 'Imbalance', 'PainInTheUpperArm', 'SkinRashOfTheFace', 'Photophobia', 'SwellingOfTheForearm', 'ShinSwelling', 'EarSwelling', 'AbdominalPain', 'EyePain', 'LimitedRangeOfMotionOfTheNeck', 'Toothache', 'Hoarseness', 'SkinRashOfTheLowerLeg', 'EasyBruising', 'SkinRashGeneralized', 'EarlySatiety', 'SinusPain', 'PallorOfLowerExtremity', 'BadTasteInMouth', 'ChestPain', 'AcidReflux', 'MentalIrritabilityAdults', 'ElevatedSkinTemperatureOfTheFace', 'Dysphagia', 'HematomaOnTheTrunk', 'PruriticNasalCavity', 'GeneralizedArthralgia', 'Palpitation', 'SlowPulse', 'Malaise', 'PainInUpperJaw', 'ChestPain', 'NasalPain', 'DecreasedSleepDuration', 'ForeignBodySensationInTheEye', 'HeatIntolerance', 'RaisedBumpsOnTheExtensorSidesOfTheExtremities', 'Torticollis', 'LoweredTemperatureOfTheLimbs', 'NasalDischarge', 'BlueSkinPenis', 'Convulsions', 'UpperExtremityPain', 'ToenailDiscoloration', 'ImpairedFineMotorSkills', 'WeightLoss', 'Polydipsia', 'Confusion', 'IncreasedTearing', 'MuscularTendernessOfTheLowerBackMuscles', 'SwellingOfTheNeck', 'ErosionAndOrUlcerationOfThePenis', 'Perfectionism', 'Vomiting', 'ExcessiveDaytimeSleepiness', 'Aphonia', 'TemporomandibularJointPain', 'WhiteTongue', 'GaspingDuringSleep', 'Hyperactivity', 'ForearmPain', 'LimitedRangeOfMotionOfTheNeck', 'LimitedRangeOfMotionOfTheSpine', 'Epistaxis', 'SwellingOfTheEyelid', 'Anisocoria', 'PainInTheAxilla', 'NasalCongestion', 'FacialPain', 'BlueSkinPenis', 'VocalFatigue', 'Fatigue', 'BlueSkinPenis', 'FacialSwelling', 'GlossalPain', 'FootPain', 'Chills', 'RecurrentSkinInfections', 'MorningStiffness', 'IncreasedAppetite', 'Diarrhea', 'SwellingOfTheLowerExtremity', 'SinusPain', 'RedColoredUrine', 'ReducedPerformance']
symptoms_list = ['Chills', 'CalfPain', 'SpotOnTheLowerExtremity', 'ShinSwelling', 'TinglingOrNumbnessOfTheFirstThreeFingers', 'DepressedMood', 'GaitImpairment', 'SwellingOfTheUpperArm', 'AvoidanceBehaviour', 'Paresthesia', 'ExcessiveDaytimeSleepiness', 'SwellingOfTheScalpGeneralized', 'UpperBackPain', 'TinglingOrNumbnessOfTheHand', 'SwellingOfTheForearm', 'SwellingOfTheFingers', 'ThumbPain', 'NasalPain', 'DryMouth', 'LimitedRangeOfMotionOfTheSpine', 'DysesthesiaOfTheLowerExtremity', 'Obsession', 'Abulia', 'SwellingOfTheUpperExtremity', 'WeightGain', 'LimitedRangeOfMotionOfTheShoulder', 'BodyTemperatureDecreased', 'HematomaOnTheTrunk', 'BrownColoredUrine', 'Vomiting', 'SwellingOfTheHand', 'SuddenIntenseFear', 'Anisocoria', 'SlowPulse', 'Trismus', 'VisibleJugularVeins']

obj = Ada()


def init_request():
    # 第一次
    data1 = '{"stateId":"DASHBOARD","answer":{"transitionId":"DASHBOARD","accountLabels":[]}}'
    qa1 = obj.get_one_qa(data1)
    qa1_dict = json.loads(qa1)
    adaCaseKey_qa1 = qa1_dict['items'][0]['answers'][0].get('adaCaseKey')
    if qa1_dict['items'][0]['stateId'] == 'UNFINISHED_CASE':
        data_discard = '{"stateId": "UNFINISHED_CASE","stateMachineIdStack": [],"selectedAnswer": 0,' \
                       '"answer": {"transitionId": "DISCARD_UNFINISHED_CASE","label": "Discard","undo": "NONE",' \
                       '"type": "GENERIC_BUTTON","perform": "REMOTE","adaCaseKey": "%s",' \
                       '"inputRequired": false,"accountLabels": []}}' %(adaCaseKey_qa1)
        obj.get_one_qa(data_discard)
        data_okay = '{"stateId": "DISCARD_CASE","stateMachineIdStack": [],"answer": {"transitionId": "YES",' \
                    '"label": "Okay","undo": "LOCAL","type": "GENERIC_BUTTON","perform": "REMOTE",' \
                    '"inputRequired": false,"accountLabels": []}}'
        obj.get_one_qa(data_okay)

    # 第二次
    data2 = '{"stateId":"DASHBOARD","stateMachineIdStack":[],"answer":{"transitionId":' \
            '"GET_HEALTH_ADVICE","label":"Start symptom assessment","undo":"LOCAL","type":"GENERIC_BUTTON",' \
            '"perform":"REMOTE","inputRequired":false,"accountLabels":[]}}'
    qa2 = obj.get_one_qa(data2)
    try:
        profileKey = json.loads(qa2)['items'][0]['answers'][0]['profileKey']
    except Exception:
        print(traceback.format_exc())
    # 第三次
    data3 = '{"stateId":"WHO_IS_THIS_ASSESSMENT_FOR","stateMachineIdStack":[],"answer":{"transitionId":"PROFILE_SELECTED",' \
            '"label":"Myself","undo":"LOCAL","type":"GENERIC_BUTTON","perform":"REMOTE",' \
            '"profileKey":"%s","inputRequired":false,"accountLabels":[]}}' % (profileKey)
    qa3 = obj.get_one_qa(data3)
    try:
        global adaCaseKey
        adaCaseKey = json.loads(qa3)['items'][0]['answers'][0]['adaCaseKey']
    except Exception:
        print(traceback.format_exc())
    return {'profileKey':profileKey, 'adaCaseKey':adaCaseKey}


def get_from_response(qa):
    qa_dict = json.loads(qa)
    progress = qa_dict['items'][0]['progress']
    stateId = qa_dict['items'][0]['stateId']
    stateMachineIdStack = str(qa_dict['items'][0]['stateMachineIdStack']).replace("\'","\"")
    # 问
    question = qa_dict['items'][0]['question']
    # 答
    answer_list = qa_dict['items'][0]['answers']
    answer_ctt_list = [x['label'] for x in answer_list]
    # 如果问是否还有其他疾病时，回答NO
    if question == 'Do you have any other symptoms?':
        answer = answer_list[1]
    else:
        # 直接选择第一项
        if answer_list[0].get('type') == 'GENERIC_BUTTON':
            answer = answer_list[0]
        else:
            answer_num = 0
            while True:
                answer = random.choice(answer_list)
                answer_num += 1
                if answer_num > 10:
                    print('没有GENERIC_BUTTON类型，退出本次请求')
                    break
                if answer['type'] == 'GENERIC_BUTTON':
                    break
                else:
                    print('非GENERIC_BUTTON类型，重新选择')


    # answer添加 "accountLabels":[]
    answer['accountLabels'] = []
    answer_ctt = answer['label']
    next_data = '{"progress":%s,"stateId":"%s","stateMachineIdStack":%s,"answer":%s}' %(progress, stateId, stateMachineIdStack, json.dumps(answer))

    return {'question': question, 'answer': answer_ctt, 'options': answer_ctt_list, 'next_data': next_data, 'stateId': stateId}

def go_to_request(data, result):
    print(data)
    qa = obj.get_one_qa(data)
    qa_dict = get_from_response(qa)
    question = qa_dict['question']
    answer = qa_dict['answer']
    options = qa_dict['options']
    global new_result
    result['children'].append({'question': question, 'answer': answer, 'options': options})
    new_result = result
    global new_data
    new_data = qa_dict['next_data']
    global new_stateId
    new_stateId = qa_dict['stateId']
def next_and_next():
    while True:
        go_to_request(new_data, new_result)
        if new_stateId == 'ASSESSMENT_ALL_DONE':
            print('已生成报告，准备下载')
            break
    return new_result


def get_all_symptoms():
    global new_result
    global new_data
    file = open('fail_sym.txt', 'a', encoding='utf-8')
    for symptoms in symptoms_list:
        num = 0
        fail_num = 0
        while True:
            if num > 0:
                break
            if fail_num > 5:
                file.write(symptoms + '\n')
                file.flush()
                break
            try:
                new_result = {'symptom': symptoms, 'children': []}
                key_dict = init_request()
                # 第四次
                new_data = '{"stateId":"OBLIGATORY_SEARCH","stateMachineIdStack":[],' \
                        '"answer":{"transitionId":"SEARCH","label":"","undo":"REMOTE","type":"SYMPTOM_SEARCH","perform":"REMOTE",' \
                        '"stateMachineId":"SEARCH","profileKey":"%s","adaCaseKey":"%s",' \
                        '"inputRequired":false,"input":"finding:%s","accountLabels":[]}}' % (
                        key_dict['profileKey'], key_dict['adaCaseKey'], symptoms)
                # go_to_request(data, new_result)
                next_and_next()
                # 下载报告，请求返回字符串，需要转为dict
                report = json.loads(obj.get_report(key_dict['adaCaseKey']))
                # 下载个人信息,请求返回的是字符串，需要去除开头结尾的中括号，然后转为dict
                profiles = json.loads(obj.get_profiles().strip('[|]'))

                new_result['profile'] = profiles
                new_result['report'] = report
                result = json.dumps(new_result).replace(r'\u2019', '\'')
                insert('ada_select_yes',json.loads(result))
                print('%s %s 数据写入mongodb成功' % (datetime.datetime.now(), symptoms))
                # time.sleep(5)
                num += 1
            except Exception:
                print(traceback.format_exc())
                print('本次采集失败，跳过开始下一次')
                fail_num += 1
                continue


if __name__ == '__main__':
    get_all_symptoms()


