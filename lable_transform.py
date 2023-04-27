from sklearn import metrics
import numpy as np
import pandas as pd
import tensorflow as tf

def one_hot_matrix(labels, C):
    # input -- labels (true labels of the sets), C (# types)
    # output -- one hot matrix with shape (# types, # samples)
    C = tf.constant(C, name = "C")
    one_hot_matrix = tf.one_hot(labels, C, axis = 0)
    sess = tf.Session()
    one_hot = sess.run(one_hot_matrix)
    sess.close()
    return one_hot
# Make types to labels dictionary
def type_to_label_dict(types):
    # input -- types
    # output -- type_to_label dictionary
    type_to_label_dict = {}
    all_type = list(set(types))
    for i in range(len(all_type)):
        type_to_label_dict[all_type[i]] = i
    return type_to_label_dict
# Convert types to labels
def convert_type_to_label(types, type_to_label_dict):#将细胞对应的lable生成数组
    # input -- list of types, and type_to_label dictionary
    # output -- list of labels
    types = list(types)
    labels = list()
    for type in types:
        labels.append(type_to_label_dict[type])
    return labels

lable=pd.read_csv('data/baron/baron_lables.txt',index_col=0, sep='\t')
# lable=pd.read_csv('./data/camp1_label.txt',index_col=0,sep='\t')
#print(lable.iloc[:,0])
#print(lable)
nt = len(set(lable.iloc[:, 0]))
type_to_label_dict = type_to_label_dict(lable.iloc[:, 0])
#print(type_to_label_dict)
label_to_type_dict = {v: k for k, v in type_to_label_dict.items()}
#print(label_to_type_dict)
lable = convert_type_to_label(lable.iloc[:, 0], type_to_label_dict)
#print(len(lable))
#print(lable)
