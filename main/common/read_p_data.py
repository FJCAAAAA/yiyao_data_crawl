import pickle
import json


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


a = load_pickle('C:/Users/fengjicheng/Documents/JD/office_dongdong/fengjicheng/RecvFile/dise_sym_num_dict.p')
print(json.dumps(a, ensure_ascii=False))
