import pandas as pd
import numpy as np

def getdata(path):
    data = pd.read_csv(path, header=0)
    #print(data)
    #character = data.iloc[:, 1]
    #print(character)
    character = data.drop(['S'],axis=1)
    chara_max = character.max()
    chara_min = character.min()
    chara_range = chara_max - chara_min
    normal_chara = (character - chara_min) / chara_range
    #print(normal_chara.head(5))
    return normal_chara

def getdat(path):
    data = pd.read_csv(path, header=0)
    label = data.iloc[:, 1]
    return label

def knn(inX, normal_chara, label, k):
    data_sub = normal_chara - inX
    data_square = data_sub.applymap(np.square)
    data_sum = data_square.sum(axis=1)
    data_sqrt = data_sum.map(np.sqrt)
    dis_sort = data_sqrt.argsort()
    k_label = label[dis_sort[:k]]
    label_sort = k_label.value_counts()
    res_label = label_sort.index[0]
    return res_label

if __name__ == '__main__':
    label = getdat('.\indian.csv')
    nm_1 = getdata('.\indian.csv')
    #print(label)
    nm_2 = nm_1.iloc[0:400,:]
    inX = nm_1.ix[500]
    print(knn(inX,nm_1, label, 3))