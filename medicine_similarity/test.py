import pandas as pd
import numpy as np

# 寻找两个元祖的交集大小，查看一个元祖被包括于另一个元祖
# l1 = [1, 2, 3, 4, 5]
# l2 = [3, 4, 5, 6, 7]
# s1 = set(l1)
# s2 = set(l2)
# inter = s1 & s2
# print("inter:", type(inter))
#
# l3 = [1, 2, 3, 4, 5, 6, 7, 8]
# s3 = set(l3)
# if s1.issubset(s3):
#     print("YES!!!!")

# dict = {"1":[1, 2, 3]}
# print()

# data = pd.DataFrame(columns=["test1", "test2"])
# data["test1"].loc[0] = 0
# print(data)

# data = pd.DataFrame(np.zeros((2, 3)), columns=["a", "b", "c"])
# data["b"].loc[1] = 1
# print(type(data), data)
# data_new = pd.concat([data["a"], data["b"]], axis=1)
# print(type(data_new), data_new)
# data_new.to_csv()   # 为何拼接而成的DataFrame无法调用to_csv函数，与普通的DataFrame有什么区别

# 对打上聚类结果标签的性味归经数据根据label进行排序
def sort_label():
    path_source = "data/taste_group.csv"
    path_target = "data/taster_group_new.csv"
    data_source = pd.read_csv(path_source)
    data_new = data_source.sort_values(by='Label', ascending=True)  # 根据label进行排序
    data_new.to_csv(path_target, encoding="utf-8")
# sort_label()

# 测试dataframe遍历的索引
# path = "data/data_labeld_kmodes.csv"
# data = pd.read_csv(path)
# # print(data.loc[1])
# series = data["Function"]
# index = 5
# print(series[index])
# print(data["名称"].iloc[index])

# 测试根据字典value进行排序
# dict = {"a": 4, "b": 3, "c": 6}
# dict_sort = sorted_items = sorted(dict.items(), key=lambda x: x[1])
# print(dict_sort)

# 测试dataframe的搜索
# data = pd.DataFrame([[1, 2, 3, 4], [2, 4, 6, 8], [2, 9, 12, 36]], columns=["a", "b", "c", "d"])
# print(data)
# num = data["d"].loc[data["a"] == 2].iloc[0]  # 搜索到能匹配的行，返回一个series
# index = data.loc[data["a"] == 2].index[0]   # 获取索引(与loc方法对应)，index中的索引代表被搜索到的所有行中的第几行
# num_new = data["a"].iloc[index]
# print(num, type(num))
# print(index)
# print(num_new)
# 测试dataframe中的loc和iloc
data = pd.DataFrame([[1, 2, 3, 4], [2, 4, 6, 8], [2, 9, 12, 36]], index=[2, 4, 8], columns=["a", "b", "c", "d"])
print(data)
index = data["b"].loc[data["a"] == 2].iloc[0]   # 获取索引，index中的索引代表被搜索到的所有行中的第几行
print(index)
print(data[1:2])    # 切片默认是用下标进行搜索（即行号，对应iloc）
print(data.loc[1:2])    # 用loc进行切片即是索引
# 测试读取csv后自动生成的索引
# data.to_csv("test.csv", index=False)
# data = pd.read_csv("test.csv")
# print(data)
# print(data.loc[1])
# print(data.iloc[1])
