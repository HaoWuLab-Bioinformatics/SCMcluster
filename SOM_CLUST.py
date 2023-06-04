import numpy as np
import random
import pandas as pd
# import co_association
from sklearn.metrics.pairwise import cosine_distances
import lable_transform
from sklearn import metrics
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics.pairwise import euclidean_distances
np.random.seed(22)
def variance_select(Cmatrix,p):
    selector = VarianceThreshold(p)
    after_data = selector.fit_transform(Cmatrix.T)
    return after_data
class CyrusSOM(object):
    def __init__(self,net=[1,1,1,1,1,1,1,1,1,1],epochs = 50,r_t = [None,None],eps=1e-6):
        """
        :param net: 竞争层的拓扑结构，支持一维及二维，1表示该输出节点存在，0表示不存在该输出节点
        :param epochs: 最大迭代次数
        :param r_t:   [C,B]    领域半径参数，r = C*e**(-B*t/eoochs),其中t表示当前迭代次数
        :param eps: learning rate的阈值
        """

        self.epochs = epochs  #最大迭代次数
        print( self.epochs)

        self.C = r_t[0]
        print(self.C)

        self.B = r_t[1]
        print(self.B)

        self.eps = eps


        self.output_net = np.array(net)
        if len(self.output_net.shape) == 1:
            self.output_net = self.output_net.reshape([-1,1])
        self.coord = np.zeros([self.output_net.shape[0],self.output_net.shape[1],2])
        for i in range(self.output_net.shape[0]):
            for j in range(self.output_net.shape[1]):
                self.coord[i,j] = [i,j]
        print(self.coord)


    def __r_t(self,t):
        if not self.C:
            return 0.5
        else:
            return self.C*np.exp(-self.B*t/self.epochs)

    def __lr(self,t,distance):
        return (self.epochs-t)/self.epochs*np.exp(-distance)
    def standard_x(self,x):
        x = np.array(x)
        for i in range(x.shape[0]):
            x[i,:] = [value/(((x[i,:])**2).sum()**0.5) for value in x[i,:]]
        return x
    def standard_w(self,w):
        for i in range(w.shape[0]):
            for j in range(w.shape[1]):
                if (((w[i,j,:])**2).sum()**0.5) == 0:
                    w[i, j, :] = 0
                else:
                    w[i,j,:] = [value/(((w[i,j,:])**2).sum()**0.5) for value in w[i,j,:]]
        return w
    def cal_similar(self,x,w):
        similar = (x*w).sum(axis=2)
        coord = np.where(similar==similar.max())
        return [coord[0][0],coord[1][0]]

    def update_w(self,center_coord,x,step):
        for i in range(self.coord.shape[0]):
            for j in range(self.coord.shape[1]):
                distance = (((center_coord-self.coord[i,j])**2).sum())**0.5
                if distance <= self.__r_t(step):
                    self.W[i,j] = self.W[i,j] + self.__lr(step,distance)*(x-self.W[i,j])

    def transform_fit(self,x):
        self.train_x = self.standard_x(x) #输入数据归一化
        self.W = np.zeros([self.output_net.shape[0],self.output_net.shape[1],self.train_x.shape[1]])  #生成权值矩阵
        print(self.W.shape)
        for i in range(self.W.shape[0]):  #按竞争层的拓扑结构遍历权值矩阵
            for j in range(self.W.shape[1]):
                self.W[i,j,:] = self.train_x[random.choice(range(self.train_x.shape[0])),:] #权值初始化
        self.W = self.standard_w(self.W) #权值归一化
        for step in range(int(self.epochs)): #按epoch训练
            j = 0
            print('epoch',step)
            print('__lr',self.__lr(step,0))
            if self.__lr(step,0) <= self.eps:
                break
            for index in range(self.train_x.shape[0]):
                # print("*"*8,"({},{})/{} W:\n".format(step,j,self.epochs),self.W)
                center_coord = self.cal_similar(self.train_x[index,:],self.W) #求最大内积的点
                self.update_w(center_coord,self.train_x[index,:],step) #获胜神经元更新邻域内的权值
                self.W = self.standard_w(self.W)
                j += 1
        label = []
        for index in range(self.train_x.shape[0]):
            center_coord = self.cal_similar(self.train_x[index, :], self.W)
            label.append(center_coord[1]*self.coord.shape[1] + center_coord[0])
        class_dict = {}
        for index in range(self.train_x.shape[0]):
            if label[index] in class_dict.keys():
                class_dict[label[index]].append(index)
            else:
                class_dict[label[index]] = [index]
        cluster_center = {}
        for key,value in class_dict.items():
            cluster_center[key] = np.array([x[i, :] for i in value]).mean(axis=0)
        self.cluster_center = cluster_center

        return label


    def fit(self,x):
        self.train_x = self.standard_x(x)
        self.W = np.random.rand(self.output_net.shape[0], self.output_net.shape[1], self.train_x.shape[1])
        self.W = self.standard_w(self.W)
        for step in range(int(self.epochs)):
            j = 0
            if self.__lr(step,0) <= self.eps:
                break
            for index in range(self.train_x.shape[0]):
                print("*"*8,"({},{})/{} W:\n".format(step, j, self.epochs), self.W)
                center_coord = self.cal_similar(self.train_x[index, :], self.W)
                self.update_w(center_coord, self.train_x[index, :], step)
                self.W = self.standard_w(self.W)
                j += 1
        label = []
        for index in range(self.train_x.shape[0]):
            center_coord = self.cal_similar(self.train_x[index, :], self.W)
            label.append(center_coord[1] * self.coord.shape[1] + center_coord[1])
        class_dict = {}
        for index in range(self.train_x.shape[0]):
            if label[index] in class_dict.keys():
                class_dict[label[index]].append(index)
            else:
                class_dict[label[index]] = [index]
        cluster_center = {}
        for key, value in class_dict.items():
            cluster_center[key] = np.array([x[i, :] for i in value]).mean(axis=0)
        self.cluster_center = cluster_center

    def predict(self,x):
        self.pre_x = self.standard_x(x)
        label = []
        for index in range(self.pre_x.shape[0]):
            center_coord = self.cal_similar(self.pre_x[index, :], self.W)
            label.append(center_coord[1] * self.coord.shape[1] + center_coord[1])
        return label




