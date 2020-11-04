'''
설명 : 같은 자본금을 기준으로 액면가가 낮은 주식일수록 공격성이 높다고 생각된다
        500원 단위로 분할하여 서로 다른 파일에 저장하는 것을 목표로 한다
'''
import pandas as pd
#종목코드 정보 가져오기
data = pd.read_csv('../Data/종목코드.csv', encoding='cp949')
#다 세었는지 확인하기 위한 변수
max = len(data['종목코드'])
count = 0
#액면가를 나누는 기준(500원 기준)
before = 0
now = 500

while now <= 5000:
    save = {'종목코드':[],'기업명':[],'자본금':[],'액면가':[]}
    for i in range(max):
        #if before < int(data['액면가'][i]) <= now:
        if before < data['액면가'][i] and data['액면가'][i] <= now:
            save['종목코드'].append(data['종목코드'][i])
            save['기업명'].append(data['기업명'][i])
            save['자본금'].append(data['자본금'][i])
            save['액면가'].append(data['액면가'][i])
            count += 1
    if len(save['종목코드']) > 0:
        save = pd.DataFrame(save)
        save.to_csv('./../Data/액면가 분할/{}to{}.csv'.format(str(before),str(now)), index=True, encoding='cp949')
    before += 500
    now += 500