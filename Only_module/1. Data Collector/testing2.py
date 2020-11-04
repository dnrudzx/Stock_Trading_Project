#155660
import datetime
import pandas_datareader.data as web

start = datetime.datetime(2020,10,20)
end = datetime.datetime(2020,10,29)

data = web.DataReader('155660.KS','yahoo',start,end)

#print(data)
print(data['Adj Close'])
data2 = data['Adj Close']
print(len(data2))
#print(data['Adj Close'][0])
for i in range(1,8):
    print(data2[i] - data2[i-1])
    #if data2[i] - data2[i-1] < 0:
    #    break
print(i)

'''
for code in codes:
    try:
        data = web.DataReader(str(code)+'.KS','yahoo',start,end)
        print(code)
        print(data)
        print('#######################################################')
    except:
        continue
'''