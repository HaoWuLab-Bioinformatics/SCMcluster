import numpy as np
import pandas as pd
import scipy.io
import os
df=pd.read_csv('./(seed10)amplify_all_baron0.015.txt',index_col=0,sep='\t')
# df=pd.read_csv('./data/camp1_data.txt',index_col=0,sep='\t')
# d=pd.read_csv('data/pancreas_marker316.txt', sep='\t', header=None)
d=pd.read_csv('./data/all_markers.txt',header=None,sep='\t')
print(d)
def equalsIgnoreCase(a, b):#忽略大小写比较
    if isinstance(a, str):
        if isinstance(b, str):
            return len(a) == len(b) and a.upper() == b.upper()
    return False
n=0
new=pd.DataFrame()
for i in range(0,len(d.index)):#筛选出表达集里有的marker
    for j in range(0,len(df.index)):
        # print(df.index[j])
        # print(d.iloc[i,0])
        if(equalsIgnoreCase(df.index[j],d.iloc[i,0])):
            n=n+1
            print(n,df.index[j])
            print(df.loc[df.index[j],:])
            new=new.append(df.loc[df.index[j],:])

print(new)
new.to_csv("contain_(seed10)amplify_all_baron0.01+5.txt",sep='\t')