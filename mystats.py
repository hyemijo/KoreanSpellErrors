from konlpy.tag import Kkma
from konlpy.utils import pprint
from collections import Counter

kkma = Kkma()

def tokenize_morpheme(data_type):
    data_type_tokenized = []
    data_type_sorted = sorted(Counter(data_type).items(), key=lambda x : x[1], reverse=True)
    #print(data_type_sorted)
    result_tokenized = ""
    num = len(data_type)

    for i, (form, freq) in enumerate(data_type_sorted):
        result_tokenized = kkma.pos(form)
        for j in range(freq):
            data_type_tokenized.append(result_tokenized)
        
        #print(f"{i+1}.\t{freq}\t{round(freq/num, 3)}\t{form}\t{result_tokenized}")
    return data_type_tokenized