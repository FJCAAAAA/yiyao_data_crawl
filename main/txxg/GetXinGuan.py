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
import traceback


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

    file = open('txt/新冠肺炎自查qa.json', 'a', encoding='utf-8')
    while True:
        try:
            obj = GetTengxunXinGuan()
            file.write(json.dumps(obj.get_all_qa(), ensure_ascii=False) + '\n')
            file.flush()
            print('###爬取成功，时间：{}###'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
        except Exception:
            print(traceback.format_exc())
            continue
