import pandas as pd
import re
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
import numpy as np
import jieba.posseg as pseg

def get_data():
    data = pd.read_csv("data_treat.csv")
    print(data.info())
    length = data.shape[0]
    # print(length)

    for i in range(length):
        data["Taste"].loc[i] = re.split("、", data["Taste"].loc[i])
        data["Type"].loc[i] = re.split("、", data["Type"].loc[i])
        data["Effect"].loc[i] = re.split("、", data["Effect"].loc[i])

    return data, length

#保留特征序列的向量化方法,只有方剂的药物组成特征会用到，由于到时候只针对药物组成特征，所以需要修改（删除）代码
class feature_to_vector_seq:
    def __init__(self, data, length):
        self.data = data
        self.length = length

    #计算各特征的最大数量
    def max_length(self, str):
        max_length = 0
        for i in range(self.length):
            if len(data[str].loc[i]) > max_length:
                max_length = len(data[str].loc[i])
        # print(max_length)
        return max_length

    # 各特征数量补全
    def length_to_max(self, str):
        max_length = self.max_length(str)
        for i in range(self.length):
            while len(data[str].loc[i]) < max_length:
                data[str].loc[i].append("missing")
        # print(data[str])
        return max_length

    def feature_to_vector(self):
        feature_list = ["Taste", "Type", "Effect"]
        label_encoder = LabelEncoder()
        onehot_encoder = OneHotEncoder(sparse=False)
        onehot_encoded_all = []
        #向量化每个特征
        for f in feature_list:
            #将特征补全
            max_length = self.length_to_max(f)
            # 将所有药物的相应特征连接在一起，再转换成整数编码
            d = data[f].loc[0]
            # print("d:",np.shape(d))
            for i in range(1, self.length):
                d.extend(data[f].loc[i])
            # print(d)
            integer_encoded = label_encoder.fit_transform(d)
            #转换成整数编码后按照max_length reshape成每个药物的特征数组
            integer_encoded = integer_encoded.reshape(-1, max_length)
            onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
            # print(onehot_encoded)
            # print(type(onehot_encoded))
            # print(np.shape(onehot_encoded))
            onehot_encoded_all.append(onehot_encoded)
        print(onehot_encoded_all)
        print(len(onehot_encoded_all))

        #将多个特征数组拼接在一起
        onehot_encoded_all_joint = onehot_encoded_all[0]
        # print(onehot_encoded_all_joint)
        # print(np.shape(onehot_encoded_all_joint))
        # print(type(onehot_encoded_all_joint))
        for j in range(1, len(onehot_encoded_all)):
            onehot_encoded_all_joint = np.append(onehot_encoded_all_joint, onehot_encoded_all[j], axis=1)
        # print(onehot_encoded_all_joint)
        # print(np.shape(onehot_encoded_all_joint))
        # print(type(onehot_encoded_all_joint))
        return onehot_encoded_all_joint

    #将得到的特征向量矩阵转换成pandas的DataFrame格式并导出到CSV文件
    def data_to_pandas(self, data):
        data = pd.DataFrame(data)
        # print(data)
        data.to_csv("feature_vector_seq.csv")

#不保留特征序列的向量化
class feature_to_vector:
    def __init__(self, data, length):
        self.data = data
        self.length = length

    #计算各特征的最大数量
    def max_length(self, str):
        max_length = 0
        for i in range(self.length):
            if len(data[str].loc[i]) > max_length:
                max_length = len(data[str].loc[i])
        # print(max_length)
        return max_length

    # 各特征数量补全
    def length_to_max(self, str):
        max_length = self.max_length(str)
        for i in range(self.length):
            while len(data[str].loc[i]) < max_length:
                data[str].loc[i].append("missing")
        # print(data[str])
        return max_length

    def feature_to_vector(self):
        feature_list = ["Taste", "Type", "Effect"]
        label_encoder = LabelEncoder()
        onehot_encoder = OneHotEncoder(sparse=False)
        onehot_encoded_all = []
        #向量化每个特征
        for f in feature_list:
            #将特征补全
            max_length = self.length_to_max(f)
            # print(max_length)
            # 将所有药物的相应特征连接在一起，再转换成整数编码
            d = data[f].loc[0]
            # print("d:",np.shape(d))
            for i in range(1, self.length):
                d.extend(data[f].loc[i])
            # print(d)
            integer_encoded = label_encoder.fit_transform(d)
            #转换成整数编码后再将每个特征转换为one-hot
            integer_encoded = integer_encoded.reshape(-1, 1)
            onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
            # print(onehot_encoded)
            # print(np.shape(onehot_encoded))
            # 将每个样本的单独的one-hot向量整合到一个数组中
            vector_length = np.shape(onehot_encoded[0])
            onehot_encoded_list = []
            onehot_encoded_temp = np.zeros(vector_length)
            temp = 0
            for i in range(len(onehot_encoded)):
                if temp < max_length:
                    index = np.argmax(onehot_encoded[i])
                    onehot_encoded_temp[index] = 1
                    temp += 1
                else:
                    onehot_encoded_list.append(onehot_encoded_temp)
                    onehot_encoded_temp = np.zeros(vector_length)
                    index = np.argmax(onehot_encoded[i])
                    onehot_encoded_temp[index] = 1
                    temp = 1
            # print(onehot_encoded_list)
            # print(len(onehot_encoded_list))
            onehot_encoded_all.append(onehot_encoded_list)

        # 将多个特征数组拼接在一起
        onehot_encoded_all_joint = onehot_encoded_all[0]
        # print(onehot_encoded_all_joint)
        # print(np.shape(onehot_encoded_all_joint))
        for j in range(1, len(onehot_encoded_all)):
            onehot_encoded_all_joint = np.append(onehot_encoded_all_joint, onehot_encoded_all[j], axis=1)
        # print(onehot_encoded_all_joint)
        print(np.shape(onehot_encoded_all_joint))
        return onehot_encoded_all_joint

    #将得到的特征向量矩阵转换成pandas的DataFrame格式并导出到CSV文件
    def data_to_pandas(self, data):
        data = pd.DataFrame(data)
        # print(data)
        data.to_csv("feature_vector.csv")

if __name__ == "__main__":
    data, length = get_data()

    #保留特征序列的向量化
    # feature_to_vector_seq = feature_to_vector_seq(data, length)
    # onehot_encoded_all_joint = feature_to_vector_seq.feature_to_vector()
    # feature_to_vector_seq.data_to_pandas(onehot_encoded_all_joint)

    #不保留特征序列的向量化
    feature_to_vector = feature_to_vector(data, length)
    onehot_encoded_all_joint = feature_to_vector.feature_to_vector()
    feature_to_vector.data_to_pandas(onehot_encoded_all_joint)