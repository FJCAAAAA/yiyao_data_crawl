#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : DiseSymProb.py
@Author: Fengjicheng
@Date  : 2020/1/6
@Desc  : 通过寻医问药问答网站获取疾病症状概率
'''

from SearchDis import Xunyiwenyao
from SearchDisQa import XunyiwenyaoQa
import pickle
import json


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

dict1 = {
	"扁桃体炎": {
		"面部肿胀": 17.0,
		"可闻性喘鸣不伴听诊器": 42.0,
		"流泪增多": 5.0,
		"眼睛瘙痒": 3.0,
		"咳痰": 13.0,
		"多汗症": 14.0,
		"面部疼痛": 3.0,
		"吞咽困难": 112.0,
		"耳痛": 88.0,
		"多涎": 96.0,
		"颈部肿胀": 49.0,
		"口腔糜烂和溃疡": 42.0,
		"疲劳": 53.0,
		"牙疼": 2.0,
		"斜颈": 13.0,
		"呼吸困难": 28.0,
		"心动过速": 21.0,
		"胸闷": 10.0,
		"脉搏加快": 14.0,
		"发声困难": 38.0,
		"恶心": 24.0,
		"运动耐量降低": 12.0,
		"体重减少": 5.0,
		"面部皮肤温度升高": 16.0,
		"颈前疼痛": 6.0,
		"咽干": 1.0,
		"胸痛": 2.0,
		"头晕": 3.0,
		"咳血": 10.0,
		"下肢红斑": 1.0
	},
	"鼻炎": {
		"打喷嚏": 65.0,
		"口腔瘙痒": 65.0,
		"流鼻涕": 65.0,
		"鼻腔瘙痒": 65.0,
		"鼻塞": 64.0,
		"清喉增加": 64.0,
		"喉咙瘙痒": 65.0,
		"面部肿胀": 48.0,
		"鼻窦疼痛": 62.0,
		"嗅觉丧失": 18.0,
		"流泪增多": 35.0,
		"眼睛瘙痒": 14.0,
		"耳胀": 48.0,
		"颈淋巴结肿大": 15.0,
		"面部疼痛": 37.0,
		"食欲不振": 11.0,
		"发烧": 33.0,
		"咳嗽": 40.0,
		"声音嘶哑": 14.0,
		"咽喉痛": 22.0,
		"咽喉红斑": 21.0,
		"嗅觉减退": 49.0,
		"咳血": 8.0,
		"呼吸困难": 10.0,
		"胸闷": 4.0,
		"恶心": 5.0,
		"心动过速": 3.0,
		"咳痰": 8.0,
		"味觉减弱": 43.0,
		"头痛": 39.0,
		"眼眶周围疼痛": 16.0,
		"耳痛": 33.0,
		"疲劳": 26.0,
		"鼻出血": 27.0,
		"多汗症": 3.0,
		"气压变化时无法清除耳朵": 22.0,
		"打鼾": 19.0,
		"发声困难": 5.0,
		"体重减少": 2.0,
		"眼眶后疼痛": 3.0,
		"寒战": 8.0,
		"肌痛": 7.0,
		"吞咽痛": 3.0,
		"口腔贴片": 2.0,
		"牙疼": 2.0,
		"面部皮肤温度升高": 1.0,
		"咽干": 1.0
	}
}

def get_prob():
    obj = Xunyiwenyao()
    dise_sym_dict = load_pickle('dise_sym_num_dict.p')
    dise_sym_prob_dict = dise_sym_dict.copy()
    file = open('qa_len.txt', 'a', encoding='utf-8')
    for dise, sym_dict in dise_sym_dict.items():
        dise_qa = obj.get_all_page(dise)
        file.write(' '.join([dise, str(dise_qa)]) + '\n')
        file.flush()
        for sym, v in sym_dict.items():
            sym_qa = obj.get_all_page(' '.join([dise, sym]))
            file.write(' '.join([dise, sym, str(sym_qa)]) + '\n')
            file.flush()
            dise_sym_prob = '{:.2f}'.format(sym_qa / dise_qa)
            dise_sym_prob_dict[dise][sym] = dise_sym_prob
    result = json.dumps(dise_sym_prob_dict, ensure_ascii=False)
    with open('prob_result.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print(result)


def get_qa():
    obj = XunyiwenyaoQa()
    dise_sym_dict = dict1
    for dise, sym_dict in dise_sym_dict.items():
        for sym, v in sym_dict.items():
            if dise == '感冒':
                if sym not in ['头痛', '鼻窦疼痛', '咽喉红斑', '流鼻涕', '打喷嚏', '咳嗽', '咳痰', '鼻腔瘙痒', '咽喉痛']:
                    obj.get_all_qa(' '.join([dise, sym]))
            else:
                obj.get_all_qa(' '.join([dise, sym]))

if __name__ == '__main__':
    get_qa()
