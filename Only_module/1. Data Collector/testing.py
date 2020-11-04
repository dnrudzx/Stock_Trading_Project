import pandas as pd
import datetime
import pandas_datareader.data as web

#모든 종목코드
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0][['종목코드']]
#6자리 종목코드
codes = [i for i in df['종목코드'] if i>=100000]
#시작일 / 종료일
start = datetime.datetime(2020,10,23)
end = datetime.datetime(2020,10,29)

for code in codes:
    try:
        data = web.DataReader(str(code)+'.KS','yahoo',start,end)['Adj Close']
        for i in range(1,len(data)):
            if data[i] - data[i-1] < 0:
                break
        if i == len(data) - 1:
            print(code)
            print(data)
            print('#######################################################')
    except:
        continue
