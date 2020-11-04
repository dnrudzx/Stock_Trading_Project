'''
목표 : 시장정보 데이터를 받아와 필요한 정보(종목코드 / 기업명 / 자본금 / 액면가)를 추출
1)  시장정보 데이터 받아오기 :
        KRX 홈페이지 - 시장정보 - 주식 - 상장현황 - csv버튼(http://marketdata.krx.co.kr/mdi#document=040601)
2)  시장정보 데이터 꺼내기 :
3)  필요한 정보만 추출하기 :
4)  저장하기 :
'''
import pandas as pd
#2)  시장정보 데이터 꺼내기 :
data = pd.read_csv('./../Data/data.csv')[['종목코드', '기업명','자본금(원)','액면가(원)','통화구분']]
#3)  필요한 정보만 추출하기 :
result = {'종목코드':[],'기업명':[],'자본금':[],'액면가':[]}
leng = len(data['종목코드'])
for i in range(leng):
    if data['통화구분'][i] == '원(KRW)':
        #result['종목코드'].append(str(data['종목코드'][i]).rjust(6,'0'))   #해도 소용 x
        result['종목코드'].append(data['종목코드'][i])
        result['기업명'].append(data['기업명'][i])
        result['자본금'].append(data['자본금(원)'][i])
        #result['액면가'].append(data['액면가(원)'][i])    가운데 , 없애기 위해 수정
        result['액면가'].append(''.join(data['액면가(원)'][i].split(',')))
#4)  저장하기 :
data = pd.DataFrame(result)
data.to_csv('./../Data/종목코드.csv', index=True, encoding='cp949')