'''
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020,1,1)
end = datetime.datetime(2020,10,29)

#gs = web.DataReader('078930.KS','yahoo',start,end)
gs = web.DataReader('078930.KS','yahoo')
#print(gs)                  #데이터 출력
#print(gs.info())           #데이터 양식 출력

import matplotlib.pyplot as plt

#plt.plot(gs['Adj Close'])           #그래프 그리기
plt.plot(gs.index, gs['Adj Close']) #그래프 그리기(x축,y축)

plt.show()                      #그래프 출력
'''
import pandas_datareader as pd
df = pd.get_data_yahoo('000020.KS')
print(df)