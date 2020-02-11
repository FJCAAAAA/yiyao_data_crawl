#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetXinGuan.py
@Author: Fengjicheng
@Date  : 2020/2/10
@Desc  : 腾讯健康新冠肺炎自查对话爬取
'''
import requests
import urllib3
import time
import json
import random


class GetTengxunXinGuan(object):
    def __init__(self):
        self.url = 'https://wechat.wecity.qq.com/api/Diagnosis_DiagnosisPreServer_NCovDiagnosis/NewCovDiagnosis'
        self.data = {
            'args': {'req': {'questions': [], 'strategy': 'v3'},
            'header': {'requestId': ''}},
            'service': 'Diagnosis_DiagnosisPreServer_NCovDiagnosis',
            'func': 'NewCovDiagnosis',
            'context': {'userId': '7a7279e1a6c9426e98ddcb44ad350f0f'}
        }

    def get_one_qa(self, data):
        header = {
            'Host': 'wechat.wecity.qq.com',
            'Connection': 'close',
            # 'Content-Length': '1304',
            'Accept': 'application/json, text/plain, */*',
            'sub-businessid': 'th-activity',
            'Origin': 'https://feiyan.wecity.qq.com',
            'businessid': 'tencent-health-h5',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1166 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/4113 MicroMessenger/7.0.10.1580(0x27000A5D) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 miniProgram',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://feiyan.wecity.qq.com/wuhan/dist/selftest.html',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'com.tencent.mm'
        }
        while True:
            num = 0
            num += 1
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(self.url, data=data, headers=header, timeout=(20, 20), verify=False)
            if num > 5:
                break
            if response:
                print('%s请求成功'%(self.url))
                break
            else:
                print('请求失败%s，1秒后再次请求'%(self.url))
                print(response.content.decode('utf-8'))
                time.sleep(1)
        time.sleep(1)
        return response.content.decode('utf-8')

    def get_all_qa(self):
        next_data = self.data.copy()

        while True:
            res = self.get_one_qa(json.dumps(next_data))
            res_dict = json.loads(res)
            details = res_dict.get('args').get('rsp').get('conclusions').get('details')
            if details:  # 如果不为空，说明是最后一次请求，参数包含所有的问答，返回是结论
                qa = next_data.get('args').get('req').get('questions')
                qa_list = [{'question_query': x.get('question_query'), 'candidate_symp': x.get('candidate_symp'), 'symp_list': x.get('symp_list')} for x in qa]

                return {'qa': qa_list, 'report': res_dict}
            else:
                question = res_dict.get('args').get('rsp').get('question')
                candidate_symp = question.get('candidate_symp')
                # print(candidate_symp)
                if question.get('question_type') == 0:
                    anser = random.choice(candidate_symp if isinstance(candidate_symp, list) else [])
                    question['symp_list'].append(anser)
                elif question.get('question_type') == 1:
                    candidate_symp_1 = candidate_symp[:-1]  # 不包含 "以上都没有"
                    candidate_symp_2 = candidate_symp[-1]  # ["以上都没有"]
                    candidate_symp_3 = random.choice([candidate_symp_1, candidate_symp_2])
                    if isinstance(candidate_symp_3, list):
                        anser_list = random.sample(candidate_symp_3, random.choice(range(1,len(candidate_symp_3)+1)))
                        question['symp_list'] = anser_list
                    else:
                        question['symp_list'].append(candidate_symp_3)
                next_data['args']['req']['questions'].append(question)
                # print(next_data)



if __name__ == '__main__':
    obj = GetTengxunXinGuan()
    result = obj.get_all_qa()
    # result = {'qa': [{'question_query': '请问您的年龄阶段是？', 'candidate_symp': ['小于5岁', '5～60岁', '60岁以上'], 'symp_list': ['5～60岁']}, {'question_query': '好的，请问您是否为孕妇？', 'candidate_symp': ['是', '否'], 'symp_list': ['否']}, {'question_query': '了解，请问您是否患有以下慢性疾病？', 'candidate_symp': ['慢性心脑血管疾病', '慢性呼吸道疾病', '慢性肝、肾病', '免疫力低下', '其它慢性病', '以上都没有'], 'symp_list': ['以上都没有']}, {'question_query': '好的，最近两周内，是否有以下相关情况或接触史？', 'candidate_symp': ['有武汉及周边地区的旅行或居住史', '接触过武汉及周边（或其他病例聚集区）发热伴呼吸道症状的患者', '接触过的家人、同事或朋友同时出现发热或呼吸道症状', '接触、探视过疑似病例或确诊病例', '与疑似病例或确诊病例同乘一趟交通工具', '以上都没有'], 'symp_list': ['以上都没有']}, {'question_query': '了解，请问您是否发热？', 'candidate_symp': ['是', '否'], 'symp_list': ['否']}, {'question_query': '收到，请问最近两周内是否还有其它症状？', 'candidate_symp': ['乏力', '咳嗽', '结膜炎', '胸闷、憋喘或呼吸困难', '鼻塞', '流鼻涕', '咽痛', '头痛', '肌肉酸痛', '腹泻', '以上都没有'], 'symp_list': ['以上都没有']}], 'report': {'code': 0, 'msg': 'success', 'ret': 0, 'args': {'rsp': {'code': 0, 'message': '', 'question': {'question_type': 0, 'question_rounds': 0, 'question_query': '结论', 'candidate_symp': ['是', '否'], 'symp_list': [], 'no': 0}, 'status': 0, 'answer': '新型冠状病毒感染肺炎可能性很小\\n您没有明显发热症状，且无相关流行病学接触史，因此不用过于担心，建议居家观察，出行戴口罩，勤洗手，做好新型冠状病毒感染肺炎的预防。', 'severity_level': 0, 'answer_index': 1, 'conclusions': {'age': '5～60岁', 'is_pregnant': False, 'details': {'is_pregnant': {'type': 'is_pregnant', 'yes_or_no': False, 'str_yes': '否', 'str_no': '是'}, 'his_diesase': {'type': 'his_diesase', 'yes_or_no': False, 'str_yes': '', 'str_no': '慢性呼吸道疾病、免疫力低下、其它慢性病、慢性肝、肾病、慢性心脑血管疾病'}, 'his_contact': {'type': 'his_contact', 'yes_or_no': False, 'str_yes': '', 'str_no': '1、有武汉及周边地区的旅行或居住史\\n2、接触过武汉及周边（或其他病例聚集区）发热伴呼吸道症状的患者\\n3、与疑似病例或确诊病例同乘一趟交通工具\\n4、接触过的家人、同事或朋友同时出现发热或呼吸道症状\\n5、接触、探视过疑似病例或确诊病例'}, 'fever': {'type': 'fever', 'yes_or_no': False, 'str_yes': '否', 'str_no': '是'}, 'symp': {'type': 'symp', 'yes_or_no': False, 'str_yes': '', 'str_no': '肌肉酸痛、鼻塞、咽痛、咳嗽、腹泻、胸闷、憋喘或呼吸困难、头痛、乏力、结膜炎、流鼻涕'}, 'fever_temp': {'type': 'fever_temp', 'yes_or_no': False, 'str_yes': '≤ 37.3℃', 'str_no': '> 37.3℃'}, 'symp_severe': {'type': 'symp_severe', 'yes_or_no': False, 'str_yes': '症状未加重', 'str_no': '是'}}, 'title': '新型冠状病毒感染肺炎可能性很小', 'answer': '\\n您没有明显发热症状，且无相关流行病学接触史，因此不用过于担心，建议居家观察，出行戴口罩，勤洗手，做好新型冠状病毒感染肺炎的预防。', 'report_time': '1581398896923'}, 'type_conclusion': {'age': '5～60岁', 'is_pregnant': '否', 'his_diesase': '', 'his_diesase_deny': '慢性呼吸道疾病、免疫力低下、其它慢性病、慢性肝、肾病、慢性心脑血管疾病', 'his_contact': '', 'his_contact_deny': '1、有武汉及周边地区的旅行或居住史\\n2、接触过武汉及周边（或其他病例聚集区）发热伴呼吸道症状的患者\\n3、与疑似病例或确诊病例同乘一趟交通工具\\n4、接触过的家人、同事或朋友同时出现发热或呼吸道症状\\n5、接触、探视过疑似病例或确诊病例', 'fever': '是', 'fever_template': '否', 'symp': '', 'symp_deny': '肌肉酸痛、鼻塞、咽痛、咳嗽、腹泻、胸闷、憋喘或呼吸困难、头痛、乏力、结膜炎、流鼻涕', 'symp_severe': '是', 'title': '新型冠状病毒感染肺炎可能性很小', 'answer': '\\n您没有明显发热症状，且无相关流行病学接触史，因此不用过于担心，建议居家观察，出行戴口罩，勤洗手，做好新型冠状病毒感染肺炎的预防。', 'report_time': '1581398896923'}}}}}
    print(json.dumps(result, ensure_ascii=False))
