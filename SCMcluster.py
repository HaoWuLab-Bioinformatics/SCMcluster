import sklearn.cluster
import numpy as np
import SNN_Cliq
import pandas as pd
import lable_transform
from sklearn import metrics
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import SpectralClustering
from sklearn.feature_selection import VarianceThreshold
import SOM_CLUST

def variance_select(Cmatrix,p):
    selector = VarianceThreshold(p)
    after_data = selector.fit_transform(Cmatrix)
    return after_data
def co_clust(dmat,data,n_clusters):
 n=[]
 for i in range(n_clusters):
     n.append(1)
 estimators = [
               SNN_Cliq,
               SOM_CLUST.CyrusSOM(net=n,epochs=25)
               ]

 #Declare the weight of each vote
 vote = 1 / len(estimators)
# (n,m)=data.T.shape
 (n,m)=data.shape
 print(n)
#co_association matrix is 5X5 (5 patterns)
 co_association = np.zeros((n, n))
 print(co_association)

#for each of your estimators
 for est in estimators:
    #fit the data and grab the labels
    if est==SNN_Cliq:
        print("snn")
        labels=SNN_Cliq.snn_cliq(dmat, 0.5, 0.7,15)
        print(len(labels))
        ari = metrics.adjusted_rand_score(lable_transform.lable, labels)
        NMI = metrics.adjusted_mutual_info_score(lable_transform.lable, labels)
        print('ari:', ari)
        print('NMI:', NMI)

    else:
      print("other")
      labels =est.transform_fit(data)
      print(len(labels))
      ari = metrics.adjusted_rand_score(lable_transform.lable, labels)
      NMI = metrics.adjusted_mutual_info_score(lable_transform.lable, labels)
      print('ari:', ari)
      print('NMI:', NMI)

    #find all associations and transform it into a numpy array
    res = [[int(i == j) for i in labels] for j in labels]
    res = np.array(res)
    print("vote",vote)
    print("res",res)
    #Vote and update the co_association matriz
    res = res * vote
    co_association = co_association + res
    print(co_association)
 return co_association

if __name__ == "__main__":

 d=pd.read_csv("./data/.after_selection_allcontain_baron.txt", index_col=0, sep='\t')
 data=d.values.T
 print(data.shape)
 a=variance_select(data,0.03)
 print(a.shape)
 dmat = euclidean_distances(variance_select(data,0.03))
 print(dmat.shape)
 n_clusters= input("Please input cluster numbers:\n")
 #co--返回的关联矩阵赋值
 co=co_clust(dmat,data,int(n_clusters))
 print(co.shape)
 pre_labels = list(SpectralClustering(n_clusters=int(n_clusters), affinity='precomputed', assign_labels='discretize').fit_predict(
         co))  # 获取聚类标签 discretize/kmeans,‘nearest_neighbors
 print(len(pre_labels))

 lable_transform

 AMI = metrics.adjusted_mutual_info_score(lable_transform.lable, pre_labels)

 ari=metrics.adjusted_rand_score(lable_transform.lable, pre_labels)

 print('ari:', ari)

 NMI=metrics.normalized_mutual_info_score(lable_transform.lable, pre_labels)
 print('NMI:', NMI)
 print('AMI:', AMI)

 RI=metrics.adjusted_rand_score(lable_transform.lable, pre_labels)
 print('RI:', RI)

 FMI=metrics.fowlkes_mallows_score(lable_transform.lable, pre_labels)
 print('FMI:', FMI)
