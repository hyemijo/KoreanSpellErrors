import unicodedata
import kss
from pykospacing import Spacing
from tqdm import tqdm
from collections import Counter

# 오류 수집 함수
def decompose(syllable):
    LEADING = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    VOWEL = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
    TRAILING = ('' , ) + tuple("ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")
    n_cnt = len(VOWEL) * len(TRAILING)
    t_cnt = len(TRAILING)

    try:
        if unicodedata.name(syllable).startswith('HANGUL SYLLABLE'): #1
            s_ind = ord(syllable) - ord('가') #2
            l_ind = s_ind // n_cnt
            v_ind = s_ind % n_cnt // t_cnt
            t_ind = s_ind % n_cnt % t_cnt
            jamos = ''
            jamos += LEADING[l_ind] + VOWEL[v_ind] + TRAILING[t_ind] #3
            return jamos
        else: #4
            return syllable
        
    except: #5
        return syllable


def sent_tokenize(data, spaced= True):
    data_sent_tokenized = []
    spacing = Spacing()

    for doc in tqdm(data.iterrows()): # 각 문서마다
        doc_tokenized = []

        content = doc[1]["content"]
        content_sent_tokenized = kss.split_sentences(content)

        for sent in content_sent_tokenized:
            if spaced:
                sent = spacing(sent)
            doc_tokenized.append(sent) #spaced/unspaced된 문장 모으기
        data_sent_tokenized.append(doc_tokenized) #sent tokenized & spaced된 doc 모으기

    return data_sent_tokenized


def get_error(error_form, error_form_jamo, error_form_idx, sent):
    # 특수문자, 공백 제외해야.
    errors = []

    check_error_syl = sent[error_form_idx + len(error_form)]
    #print(f"check error syl: {check_error_syl}")
    check_error_choseong = decompose(check_error_syl)[0]
    #print(f"--{check_error_choseong}--{error_form_jamo}")

    if (check_error_choseong == error_form_jamo):
        return_form = ""
        for char in sent[error_form_idx:]:
            if unicodedata.name(char).startswith("HANGUL"):
                    return_form += char
            else:
                return return_form
    
    return


def find_result_sent(error_form, error_form_jamo, sent):
    sent_error = []
    error_length = len(error_form)
    try:
        for i, char in enumerate(sent):
            check_error = sent[i:i+error_length]
            if (check_error == error_form):
                error = get_error(error_form, error_form_jamo, i, sent)
            
                if error:
                    #print("error", error)
                    sent_error.append(error)
                    #print("sent_error", sent_error)
    except:
        return sent_error

    return sent_error


def get_search_result_sent(sent, geureo_stem, geureo_xsv, euddeuk_stem, euddeuk_xsv, ol_stem, ol_xsv):
    result_sent = []

    result_geureo = find_result_sent(geureo_stem, geureo_xsv, sent) #find_error_sent("그렇", "ㅎ", sent) #geureo(sent)
    result_euddeuk =  find_result_sent( euddeuk_stem, euddeuk_xsv, sent) #find_error_sent("어떻", "ㅎ", sent) #euddeuk(title)
    result_ol = find_result_sent(ol_stem, ol_xsv, sent) #find_error_sent("옳", "ㅂ", sent) #ol(title)
    
    result_sent.append(result_geureo)
    result_sent.append(result_euddeuk)
    result_sent.append(result_ol)

    return result_sent

def get_result_sent(content, find_error=True):
    # 모드 조정. 오류 검색 or 정확한 표기 검색
    if find_error: 
            result_sent = get_search_result_sent(content, "그렇", "ㅎ", "어떻", "ㅎ", "옳", "ㅂ") #find_errors(content)
    else:
        # 올바른 형태가 과연 1개뿐인지? ex. 그렇하다. -> 그렇다? 그러하다?
        # "올바른" 형태인지 판별? ex. 어떡해 할지 -> 부정확. # 어떡하다. <-> 어떻하다. 어떠하다, 어떻게의 개입.
        result_sent = get_search_result_sent(content, "그러", "ㅎ", "어떡", "ㅎ", "올바", "ㄹ") #find_errors(content)

    return result_sent

def get_search_result_data(data, find_error = True):
    result_sent_tokenized = []
    result_data = []
    result_data_geureo = [] #그렇하다 꼴. 그렇 + ㅎ // 그러 + ㅎ
    result_data_euddeuk = [] #어떻하다 꼴 어떻 + ㅎ // 어떡 + ㅎ
    result_data_ol = []  #옳바르다 꼴 옳 + ㅂ // 올 + ㅂ
    spacing = Spacing()

    for row in tqdm(data.iterrows()):
        doc = row[1]["content"]
        result_doc = [[], [], []]

        #doc 대상 검색
        result_sent = get_result_sent(doc, find_error)

        #doc에서 오류 1개라도 검출되면?
        if (result_sent[0] or result_sent[1] or result_sent[2]):
            
            doc_sent_tokenized = [spacing(sent) for sent in kss.split_sentences(doc)] # 해당 doc을 sent tokenize한 후
            result_sent_tokenized.append(doc_sent_tokenized)

            for sent in doc_sent_tokenized: # doc의 각 sent마다
                result_sent = get_result_sent(sent, find_error)

                #오류 재검색
                if result_sent[0]:
                    result_data_geureo.extend(result_sent[0])
                    result_doc[0].extend(result_sent[0])
                if result_sent[1]:
                    result_data_euddeuk.extend(result_sent[1])
                    result_doc[1].extend(result_sent[1])
                if result_sent[2]:
                    result_data_ol.extend(result_sent[2])
                    result_doc[2].extend(result_sent[2])
        else:
            continue    

        result_data.append(result_doc)

    return result_data, result_data_geureo, result_data_euddeuk, result_data_ol, result_sent_tokenized



def print_data(datas):
    for i, data in enumerate(datas):
        print(f"==============DATA {i+1}")
        data = [item.split()[0] for item in data if item]

        print(sorted(Counter(data).items(), key=lambda x : x[1], reverse=True))
        print()
        print()

        for i in data:
            try:
                print(i)
            except:
                pass
        print("=================")
        print()
        print()