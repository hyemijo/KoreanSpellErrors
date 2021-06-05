# KoreanSpellErrors
## 1. 주제
- 표의주의에 이끌린 표기 오류의 굴절 양상 분석 ― ‘그렇하다’, ‘어떻하다’, ‘옳바르다’를 중심으로

## 2. 파일 설명
- error_files.txt: 원자료에 대해 탐색 규칙을 적용하여 수집한 표기 오류 데이터 (bin file)
    - 그렇하다: '그렇 + 초성 ㅎ 꼴'의 어절  
    - 어떻하다: '어떻 + 초성 ㅎ' 꼴의 어절  
    - 옳바르다: '옳 + 초성 ㅂ' 꼴의 어절  
- nonerror_files.zip: 원자료에 대해 탐색 규칙을 적용하여 수집한 어휘소의 단어형 데이터 (bin file)
    - 그러하다: '그러 + 초성 ㅎ' 꼴의 어절  
    - 어떡하다: '어떡 + 초성 ㅎ' 꼴의 어절  
    - 올바르다: '올바 + 초성 ㄹ' 꼴의 어절
- output_error_files.txt: 원자료에 탐색 규칙을 적용하여 찾아낸 표기 오류 어절 목록  

- output_nonerror_files.txt: 원자료에 탐색 규칙을 적용하여 찾아낸 표기 오류 어절 목록  
  
- output_error_morph_tokenized_reviewed.txt: kkma 형태소 분석기를 이용한 표기 오류의 형태소 단위 분석 결과물을 수동으로 검토한 파일
- output_nonerror_morph_tokenized_reviewed.txt: kkma 형태소 분석기를 이용한 어휘소의 단어형(올바른 표기)의 형태소 단위 분석 결과물을 수동으로 검토한 파일
- output_morpheme_freqdict.txt: 표기 오류(error: 그렇하다, 어떻하다, 옳바르다 꼴)와 어휘소의 단어형(nonerror: 그러하다, 어떡하다, 올바르다)에 대해 집계한 형태소의 빈도표
- output_morph_freqdict.txt: 표기 오류(error: 그렇하다, 어떻하다, 옳바르다 꼴)와 어휘소의 단어형(nonerror: 그러하다, 어떡하다, 올바르다)에 대해 집계한 기초 통계량이 담긴 파일
- output_morph_freqdict_sort_by_tag.txt: 형식 형태소를 집계 항목별로 빈도순으로 나열한 파일
    - X: 접사
    - EP: 선어말 어미
    - EF: 종결 어미
    - EC: 연결 어미
    - ET: 전성 어미
    - J: 조사
 
 
 



## 3. 참고 사이트
- [만료된 국민청원 데이터](https://github.com/akngs/petitions)
- [kkma 한글 형태소 분석기](http://kkma.snu.ac.kr/documents/?doc=postag)
- [Korean Sentence Splitter](https://github.com/hyunwoongko/kss)
- [KoNLPy](https://konlpy.org/en/latest/)

 
