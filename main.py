import pandas as pd
import nltk
import unicodedata

from collections import Counter
import pickle
import numpy as np
import mystats, analyze


# 0. pickle file 만드는 코드. 최초 1회만 실행.
#
#import kss
#from pykospacing import Spacing
#from tqdm import tqdm
#nltk.download("punkt")
#https://ebbnflow.tistory.com/246

## 파일 읽기
#filename = "petition.csv"
#data = pd.read_csv(filename)
#data = data[["article_id", "title", "content"]]

## 자료 기초 기술
"""doc_len = []  #문서 길이
doc_len_net = [] #문서 음절 수

for row in data.iterrows():
    content = row[1][2]
    content_net = []
    try:
        for syl in content:
            try:
                if unicodedata.name(syl).startswith("HANGUL"):
                    content_net.append(syl)
            except:
                continue
    except:
        print(row)
        continue

    doc_len.append(len(content))
    doc_len_net.append(len(content_net))

print("doc num", len(doc_len)) #doc num 395546
print("doc len", np.mean(doc_len), np.median(doc_len), np.std(doc_len)) #doc len 524.2710253674668 273.0 3027.1638516690828
print("doc len net", np.mean(doc_len_net), np.median(doc_len_net), np.std(doc_len_net)) #doc len net 367.15037189100633 197.0 840.446737502712

doc_sent_num = []
doc_sent_lens = []
doc_sent_lens_net = []
spacing = Spacing()

for row in tqdm(data.iterrows()):
    doc = row[1][2]
    doc_sent_tokenized = [spacing(sent) for sent in kss.split_sentences(doc)]
    doc_sent_num.append(len(doc_sent_tokenized)) # doc의 문장 개수 집계

    sent_net = []
    doc_sent_len = []
    doc_sent_len_net = []

    #문장 돌면서
    for sent in doc_sent_tokenized:
        doc_sent_len.append(len(sent)) # 문장별 문장 길이 수집

        for syl in sent:
            try:
                if unicodedata.name(syl).startswith("HANGUL"):
                    sent_net.append(syl)
            except:
                continue

        doc_sent_len_net.append(len(sent_net)) #문장별 음절 수 수집
        
    doc_sent_lens.extend(doc_sent_len) # 해당 doc의 문장의 길이들 수집
    doc_sent_lens_net.extend(doc_sent_len_net) #해당 doc의 문장의 음절 수들 수집

print("doc sent num", np.mean(doc_sent_num), np.median(doc_sent_num), np.std(doc_sent_num)) #doc len 524.2710253674668 273.0 3027.1638516690828
print("doc sent len", np.mean(doc_sent_lens), np.median(doc_sent_lens), np.std(doc_sent_lens)) #doc len 524.2710253674668 273.0 3027.1638516690828
print("doc sent len net", np.mean(doc_sent_lens_net), np.median(doc_sent_lens_net), np.std(doc_sent_lens_net)) #doc len net 367.15037189100633 197.0 840.446737502712


# 오류 수집
print("-----------COLLECT ERRORS")
errors_data, errors_data_geureo, errors_data_euddeuk, errors_data_ol, error_sent_tokenized = analyze.get_search_result_data(data, find_error = True)
with open("error_files.txt", "wb") as f:
    pickle.dump((errors_data, errors_data_geureo, errors_data_euddeuk, errors_data_ol, error_sent_tokenized), f)

print("-----------complete1: pickle dump")


print("-----------COLLECT NONERRORS")
nonerrors_data, nonerrors_data_geureo, nonerrors_data_euddeuk, nonerrors_data_ol, nonerror_sent_tokenized = analyze.get_search_result_data(data, find_error = False)    
with open("nonerror_files.txt", "wb") as f:
    pickle.dump((nonerrors_data, nonerrors_data_geureo, nonerrors_data_euddeuk, nonerrors_data_ol, nonerror_sent_tokenized), f)

print("-----------complete2: pickle dump")
"""


#1. error form, nonerror form 확인
# pickle file 읽고 확인하기

with open("error_files.txt", "rb") as f:
    error_files = pickle.load(f)

with open("nonerror_files.txt", "rb") as f:
    nonerror_files = pickle.load(f)


errors_data, errors_data_geureo, errors_data_euddeuk, errors_data_ol, error_sent_tokenized = error_files
nonerrors_data, nonerrors_data_geureo, nonerrors_data_euddeuk, nonerrors_data_ol, nonerror_sent_tokenized = nonerror_files

# 오류/기본형 빈도 자료
"""print("**********ERROR***********")
print("========errors:", f"geureo: {len(errors_data_geureo)}, euddeuk: {len(errors_data_euddeuk)}, ol: {len(errors_data_ol)}")
datas_error = (errors_data_geureo, errors_data_euddeuk, errors_data_ol)
analyze.print_data(datas_error)

print("**********NONERROR***********")
print("========nonerrors:", f"geureo: {len(nonerrors_data_geureo)}, euddeuk: {len(nonerrors_data_euddeuk)}, ol: {len(nonerrors_data_ol)}")
datas_nonerror = (nonerrors_data_geureo, nonerrors_data_euddeuk, nonerrors_data_ol)
analyze.print_data(datas_nonerror)"""



# 오류,기본형 형태소 분석 빈도 조사
def extend_list_elements(mylist):
    extended_list = []

    for e in mylist:
        extended_list.extend(e)

    return extended_list

def pprint_list(mylist):
    for e in mylist:
        print(e)

def get_freqdict_list(mylist):
    mylist = extend_list_elements(mylist)
    return sorted(Counter(mylist).items(), key=lambda x: x[1], reverse=True)

def get_freqdict_josa_eomi(freqdict_list):
    ej = [ ((form, tag), freq) for ((form, tag), freq) in freqdict_list if tag.startswith("E") or tag.startswith("J")]
    j = [ ((form, tag), freq) for ((form, tag), freq) in freqdict_list if tag.startswith("J")]
    e = [ ((form, tag), freq) for ((form, tag), freq) in freqdict_list if tag.startswith("E")]
    return (ej, j, e)

"""errors_data_geureo_tokenized = mystats.tokenize_morpheme(errors_data_geureo)
errors_data_euddeuk_tokenized = mystats.tokenize_morpheme(errors_data_euddeuk)
errors_data_ol_tokenized = mystats.tokenize_morpheme(errors_data_ol)

nonerrors_data_geureo_tokenized = mystats.tokenize_morpheme(nonerrors_data_geureo)
nonerrors_data_euddeuk_tokenized = mystats.tokenize_morpheme(nonerrors_data_euddeuk)
nonerrors_data_ol_tokenized = mystats.tokenize_morpheme(nonerrors_data_ol)

# output_morpheme_freqdict_init.txt
f1 = get_freqdict_list(errors_data_geureo_tokenized)
f2 =  get_freqdict_list(errors_data_euddeuk_tokenized)
f3 = get_freqdict_list(errors_data_ol_tokenized)

print("***************ERROR")
for i, f in enumerate((f1, f2, f3)):
    print(f"==============DATA{i+1}")
    print(sum([e[1] for e in f]))
    #pprint_list(get_freqdict_josa_eomi(f))
    pprint_list(f)
    print()
    print()


f4 = get_freqdict_list(nonerrors_data_geureo_tokenized)
f5 =  get_freqdict_list(nonerrors_data_euddeuk_tokenized)
f6 = get_freqdict_list(nonerrors_data_ol_tokenized)

print("***************NONERROR")
for i, f in enumerate((f4, f5, f6)):
    print(f"==============DATA{i+1}")
    print(sum([e[1] for e in f]))
    #pprint_list(get_freqdict_josa_eomi(f))
    pprint_list(f)
    print()
    print()"""



# 검토 마친 오류/비오류 목록 -> 객체로 저장
def get_morph_data(filename):
    with open(filename, "r", encoding = "utf-8") as f:
        morph = f.readlines()
        morph_data = []
        for line in morph:
            line = line.strip().split("\t")
            
            try:
                line[1] = int(line[1])
                line[4] = [tuple([i.strip() for i in e.split(",")]) for e in line[4].split("-")]
                morph_data.append((line[1], line[3], line[4]))
            except:
                continue
    return morph_data

error_morph_data = get_morph_data("output_error_morph_tokenized_kkma.txt")
nonerror_morph_data = get_morph_data("output_nonerror_morph_tokenized_kkma.txt")

error_morph_data_geureo = []
error_morph_data_euddeuk = []
error_morph_data_ol = []
nonerror_morph_data_geureo = []
nonerror_morph_data_euddeuk = []
nonerror_morph_data_ol = []

for i in error_morph_data:
    if i[1].startswith("그"):
        error_morph_data_geureo.append(i)
    elif i[1].startswith("어"):
        error_morph_data_euddeuk.append(i)
    elif i[1].startswith("옳"):
        error_morph_data_ol.append(i)
    else:
        print("error", i)

for i in nonerror_morph_data:
    if i[1].startswith("그"):
        nonerror_morph_data_geureo.append(i)
    elif i[1].startswith("어"):
        nonerror_morph_data_euddeuk.append(i)
    elif i[1].startswith("올"):
        nonerror_morph_data_ol.append(i)
    else:
        print("error", i)

#output_error_morph_tokenized_reviewed.txt
"""
pprint_list(error_morph_data_geureo)
print()
pprint_list(error_morph_data_euddeuk)
print()
pprint_list(error_morph_data_ol)
"""

# output_nonerror_morph_tokenized_reviewed.txt
"""
pprint_list(nonerror_morph_data_geureo)
print()
pprint_list(nonerror_morph_data_euddeuk)
print()
pprint_list(nonerror_morph_data_ol)
"""

def get_total_error_num(data):
    num = 0
    for line in data:
        num += line[0]
    return num

def get_total_morph_num(data):
    sum = 0
    for line in data:
        morph_num = len(line[2])
        sum += (morph_num) * line[0]
    return sum

def get_morph_num(data, init_tag):
    sum = 0
    for line in data:
        for morph in line[2]:
            if morph[1].startswith(init_tag):
                sum += line[0] #TYPE: sum += 1
    return sum


def get_mean_morph_num(data):
    sum = 0
    num = 0
    for line in data:
        morph_num = len(line[2])
        sum += (morph_num) * line[0]
        num += line[0]

    return round(sum / num, 2)

def get_mean_form_len(data):
    sum = 0
    num = 0
    for line in data:
        form_len = len(line[1])
        sum += (form_len * line[0])
        num += line[0]

    return round(sum / num, 2)


data_morph_error  = (error_morph_data_geureo, error_morph_data_euddeuk, error_morph_data_ol)
data_morph_nonerror = (nonerror_morph_data_geureo, nonerror_morph_data_euddeuk, nonerror_morph_data_ol)

"""
# output_morph_freqdict.txt
print("========error")
for data in data_morph_error:
    print("word token num", get_total_error_num(data))
    print("word type num", len(data))
    print("morph token num", get_total_morph_num(data))
    print("mean morph num", get_mean_morph_num(data))
    print("mean form len", get_mean_form_len(data))
    print("X num", get_morph_num(data, "X"))
    #print("E num", get_morph_num(data, "E"))
    print("EP num", get_morph_num(data, "EP"))
    print("EF num", get_morph_num(data, "EF"))
    print("EC num", get_morph_num(data, "EC"))
    print("ET num", get_morph_num(data, "ET"))
    print("J num", get_morph_num(data, "J"))
    
    print()

print()
print()

print("===========nonerror")
for data in data_morph_nonerror:
    print("token num", get_total_error_num(data))
    print("type num", len(data))
    print("morph token num", get_total_morph_num(data))
    print("mean morph num", get_mean_morph_num(data))
    print("mean form len", get_mean_form_len(data))
    print("X num", get_morph_num(data, "X"))
    print("E num", get_morph_num(data, "E"))
    print("EP num", get_morph_num(data, "EP"))
    print("EF num", get_morph_num(data, "EF"))
    print("EC num", get_morph_num(data, "EC"))
    print("ET num", get_morph_num(data, "ET"))
    print("J num", get_morph_num(data, "J"))
    
    print()
"""

def collect_morphs(datas):
    data_morph_list = []

    for data in datas:
        morphs = []
        for line in data:
            freq = line[0]
            morph = line[2]

            for i in range(freq):
                morphs.extend(morph)
        data_morph_list.append(morphs)
    return data_morph_list

def find_key_freqdict(form, tag, freq, search_key):
    mylist = []
    if (tag.startswith(search_key)):
        mylist.append(((form, tag), freq))
    return mylist


morph_errors = collect_morphs(data_morph_error)
morph_nonerrors = collect_morphs(data_morph_nonerror)
search_key = ("X", "EP", "EF", "EC", "ET", "J")
aa = (morph_errors, morph_nonerrors)


# output_morph_freqdict_sort_by_tag.txt
"""
for i, item in enumerate(aa):
    for j, mylist in enumerate(item):
        print(f"=================={i+1} - {j+1}")
        freqdict = sorted(Counter(mylist).items(), key=lambda x: x[1], reverse=True)
        for key in search_key:
            find_key = []
            print(freqdict[0])
            for k, v in freqdict:
                form = k[0]
                tag = k[1]
                freq = v
                find_key.extend(find_key_freqdict(form, tag, freq, key))
            print(f"----{key}: {find_key}")
            print()
        print()
        print()
"""