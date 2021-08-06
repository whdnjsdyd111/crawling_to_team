import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl

search_keyword = []
header = None
result_set = []
result_format = []


df = pd.DataFrame([[11, 21, 31], [12, 22, 32]], columns=['a', 'b'])
print(df)


while(True):
    print("------------------------------")
    print("1. 페이지 조회[선택자, 태그 찾기]\n2. 페이지 동적 검색\n3. 종료")
    print("------------------------------")

    menu = None

    try:
        menu = int(input("메뉴 입력: "))
        if not (1 <= menu <= 3):
            print("1 ~ 3 메뉴만 선택해 주십시오.\n")
            continue
    except ValueError:
        print("숫자(정수)만 입력해 주십시오.\n")

    if menu == 1:
        url = input("URL 입력 : ")
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.text, "html.parser")
        print(soup.prettify())

        while(True):
            print("------------------------------")
            print("1. 데이터 찾기\n2. 선택자, 태그 찾기\n3. 검색 종료")
            print("------------------------------")

            menu2 = None

            try:
                menu2 = int(input("메뉴 입력: "))
                if not (1 <= menu2 <= 3):
                    print("1 ~ 3 메뉴만 선택해 주십시오.\n")
                    continue
            except ValueError:
                print("숫자(정수)만 입력해 주십시오.\n")

            if menu2 == 1:
                keywords = input("키워드 입력(2개 이상 키워드 검색 시 구분자 '|' 입력 ex] 일|이|삼) : ")
                datas = soup.find_all(text=re.compile(keywords))
                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                for data in datas:
                    print(data.parent)
                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            elif menu2 == 2:
                attr = input("속성 입력(2개 이상 속성 검색 시 구분자 '|' 입력 ex] id|class|name|title ... : ").split('|')

                keywords = input("속성에 따른 키워드 입력(2개 이상 키워드 검색 시 구분자 '|' 입력 ex] 일|이|삼) : ").split('|')

                d = {}

                for i in range(0, len(attr)):
                    d[attr[i]] = keywords[i]

                datas = soup.find_all(attrs=dict(d))

                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                for data in datas:
                    print(data)
                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

                print(dict(d))
                ask = input("해당 검색 속성을 저장하시겠습니까? yes or no : ")

                if ask == 'yes':
                    search_keyword.append(d)
            elif menu2 == 3:
                break

    elif menu == 2:
        url = input("URL 입력(바뀔 쿼리스트링 'query_string' 변경) ex] http://www.google.com/search?q=query_string&keyword=query_string1 : ")

        query_range = input("범위 지정(구분자 '|'), 첫페이지|마지막페이지|증가수 ex) 0|6400|20 : ").split('|')

        header = input("헤더 설정(2개 이상 키워드 검색 시 구분자 '|' 입력) : ").split('/')
        for i in range(0, len(header)):
            result_format.append([])

        while(True):
            print("--------------------------")
            print("현재 저장된 검색 속성")
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            for i in range(0, len(search_keyword)):
                print(search_keyword[i])
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            if len(header) == search_keyword:
                break

            ask = input("속성을 추가하시겠습니까? yes or no : ")

            if ask == 'yes':
                attr = input("속성 입력(2개 이상 속성 검색 시 구분자 '|' 입력 ex] id|class|name|title ... : ").split('|')

                keywords = input("속성에 따른 키워드 입력(2개 이상 키워드 검색 시 구분자 '|' 입력 ex] 일|이|삼) : ").split('|')

                d = {}

                for i in range(0, len(attr)):
                    d[attr[i]] = keywords[i]

                search_keyword.append(d)
            elif ask == 'no':
                break

        for i in range(int(query_range[0]), (int(query_range[1]) + int(query_range[2])), int(query_range[2])):
            webpage = requests.get(url.replace('query_string', str(i)))
            soup = BeautifulSoup(webpage.text, "html.parser")
            search = []
            for j in range(0, len(search_keyword)):
                search.append(soup.find_all(attrs=dict(search_keyword[j])))
            result_set.append(search)

        for i in range(0, len(result_set)):
            for j in range(0, len(result_set[i])):
                for z in range(0, len(result_set[i][j])):
                    result_format[j].append(result_set[i][j][z].getText())

        df = pd.DataFrame([[111, 11], [22, 22]], columns=header)
        df.to_excel('C:/Users/user/Desktop/sample.xlsx', index=False, header=False)

    elif menu == 3:
        break