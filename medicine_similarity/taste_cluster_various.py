import numpy as np
from kmodes.kmodes import KModes
from sklearn.cluster import KMeans, Birch, SpectralClustering
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import metrics

file_path = "../data/feature_vector.csv"    # 需要进行聚类的数据特征向量


def get_data(path):
    data = pd.read_csv(path)
    # print(data.info())
    # print(data)
    data = np.asarray(data)  # DataFrame转array
    data = data[:, 1:]
    # print(data, data.shape)
    return data


def cluster_kmodes(n_clusters, data):
    """
    kmodes聚类方法，处理离散的原始one-hot特征向量
    :param n_clusters:质心数量
    :param data:需要进行聚类的数据
    :return:
    """
    # visual_data(data)  #可视化原数据
    kmodes = KModes(n_clusters=n_clusters, init="Huang", n_init=10, verbose=1)
    clusters = kmodes.fit_predict(data)
    print("Calinski-Harabasz Score", metrics.calinski_harabaz_score(data, clusters))
    # print("每个样本点所属类别索引", clusters)  # 输出每个样本的类别
    # print("簇中心",kmodes.cluster_centroids_)    # 输出聚类结束后的簇中心
    data_labeled_to_csv(clusters, "data/data_labeld_kmodes.csv")
    # visual_cluster(n_clusters, data, clusters)


def cluster_kmeans(n_clusters):
    """
    kmeans聚类方法，处理经过PCA处理的特征向量
    :param n_clusters:质心数量
    :return:
    """
    data = get_data("../data/feature_vector_pca.csv")
    # visual_data(data)
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(data)
    # print("聚类性能", kmeans.inertia_)
    print("Calinski-Harabasz Score", metrics.calinski_harabaz_score(data, clusters))
    # print("每个样本点所属类别索引", clusters)
    # print("簇中心", kmeans.cluster_centers_)
    data_labeled_to_csv(clusters, "data/data_labeld_kmeans.csv")
    # visual_cluster(n_clusters, data, clusters)


def cluster_birch(n_clusters):
    """
    birch聚类方法，处理经过PCA处理的特征向量
    :param n_clusters:质心数量
    :return:
    """
    data = get_data("../data/feature_vector_pca.csv")
    birch = Birch(n_clusters=n_clusters, threshold=0.4, branching_factor=50)
    clusters = birch.fit_predict(data)
    print("Calinski-Harabasz Score", metrics.calinski_harabaz_score(data, clusters))
    print("每个样本点所属类别索引", clusters)
    # print("簇中心", birch.cluster_centers_)
    data_labeled_to_csv(clusters, "data/data_labeld_birch.csv")
    # visual_cluster(n_clusters, data, clusters)


def cluster_spectralclustering(n_clusters):
    """
    SpectralClustering聚类算法
    :param n_clusters:质心数量
    :return:
    """
    data = get_data("../data/feature_vector_pca.csv")
    spectral = SpectralClustering(n_clusters=n_clusters, gamma=0.01)
    clusters = spectral.fit_predict(data)
    # 遍历超参以寻找最优参数
    # for index, gamma in enumerate((0.01, 0.1, 1, 10)):
    #     for index2, k in enumerate((15, 20, 25, 30)):
    #         clusters = SpectralClustering(n_clusters=k, gamma=gamma).fit_predict(data)
    #         print("Calinski-Harabasz Score with gamma=", gamma, "n_clusters=", k, "score:",
    #               metrics.calinski_harabaz_score(data, clusters))
    print("Calinski-Harabasz Score", metrics.calinski_harabaz_score(data, clusters))
    print("每个样本点所属类别索引", clusters)
    data_labeled_to_csv(clusters, "data/data_labeld_birch.csv")
    # visual_cluster(n_clusters, data, clusters)


def visual_data(data):
    """
    对原始结果进行可视化
    :param data:原始样本数据
    :return:
    """
    length = len(data[0])
    # print(type(data))
    x_length, y_length, z_length = length//3, 2*(length//3), 3*(length//3)
    # 各个轴可以是同样长度的数组，不必须是单一的数值，尚不清楚数组如何转换为指定坐标的值
    x, y, z = data[:, :x_length], data[:, x_length:y_length], data[:, y_length:z_length]
    # print(x, y, z)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, marker="o", c="y")  # 如果要进行3D绘图，要用ax调用scatter才行
    plt.show()


def clusters_label_class(n_clusters, data, clusters):
    """
    将聚类后的样本分别存入各标签数组中
    :param n_clusters:质心数量
    :param data:原始数据样本
    :param clusters:聚类结果（即每个样本所属的标签）
    :return:
    """
    data_labeled_lists = []
    # print(data, clusters)
    length = len(data)
    for i in range(n_clusters):
        data_labeled_lists.append([])
    # print(data_labeled_lists)
    for i in range(length):
        data_labeled_lists[clusters[i]].append(data[i].tolist())
    # 列表转数组
    for i in range(n_clusters):
        data_labeled_lists[i] = np.asarray(data_labeled_lists[i])
    data_labeled_lists = np.asarray(data_labeled_lists)
    # print(data_labeled_lists)
    # 验证是否所有样本均归类
    num_count = 0
    for data_labeled_list in data_labeled_lists:
        for data_labeled in data_labeled_list:
            num_count += 1
    # print("Right!" if num_count==length else "Error!")
    return data_labeled_lists


def visual_cluster(n_clusters, data, clusters):
    """
    聚类结果可视化
    :param n_clusters:质心数量
    :param data:原始数据样本
    :param clusters:聚类结果（即每个样本所属的标签）
    :return:
    """
    data_labeled_lists = clusters_label_class(n_clusters, data, clusters)   # 将聚类后的样本分别存入各标签数组中
    length = len(data[0])
    x_length, y_length, z_length = length//3, 2*(length//3), 3*(length//3)
    colors = ['b', 'g', 'r', 'k', 'c', 'm', 'y', 'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
              'beige', 'bisque', 'black', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
              'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue',
              'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(n_clusters):
        x, y, z = data_labeled_lists[i][:, :x_length], data_labeled_lists[i][:, x_length:y_length], \
                  data_labeled_lists[i][:, y_length:z_length]
        # print(x, y, z)
        ax.scatter(x, y, z, marker="o", c=colors[i])
    plt.show()


def data_labeled_to_csv(clusters, filename):
    """
    输出聚类结果：将每个样本的标签合并到原始data中、根据label重新排序，再输出到csv中
    :param clusters:聚类结果
    :param filename:输出的目标文件路径
    :return:
    """
    data = pd.read_csv("../data/data_treat.csv", index_col=0)
    # print(data.info())
    data.insert(1, "Label", None)
    length = data.shape[0]
    # 验证长度是否对齐
    # length_test = len(clusters)
    # print("Right!" if length==length_test else "Error!")
    for i in range(length):
        data["Label"][i] = clusters[i]
    data = data.sort_values(by='Label', ascending=True)  # 这里要注意sort_value是返回一个已排序的对象，而不是原地进行修改
    data.to_csv(filename, index=False, encoding="utf-8")


def opti_para_select(cluster_name, data):
    """
    专门用于寻找最优参数的函数
    :param cluster_name:聚类方法名称
    :param data:需要进行聚类的数据
    :return:
    """
    if cluster_name == SpectralClustering:
        max_score = 0
        opti_gamma, opti_n_clusters = 0, 0
        for gamma in (0.01, 0.1, 1):
            for n_clusters in (15, 20, 25, 30):
                clusters = SpectralClustering(n_clusters=n_clusters, gamma=gamma).fit_predict(data)
                score = metrics.calinski_harabaz_score(data, clusters)
                # print("Calinski-Harabasz Score with gamma=", gamma, "n_clusters=", n_clusters,"score:", score)
                if max_score < score:
                    max_score = score
                    opti_gamma, opti_n_clusters = gamma, n_clusters
        print("max_score:", max_score, "opti_gamma:", opti_gamma, "opti_n_clusters:", opti_n_clusters)

    if cluster_name == "k_modes":
        max_score = 0
        opti_n_clusters = 0
        for n in range(2, 50):
            kmodes = KModes(n_clusters=n, init="Huang", n_init=10, verbose=1)
            clusters = kmodes.fit_predict(data)
            score = metrics.calinski_harabaz_score(data, clusters)
            print("Calinski-Harabasz Score——", "n_clusters=", n, "score:", score)
            if max_score < score:
                max_score = score
                opti_n_clusters = n
        print("max_score:", max_score, "opti_n_clusters:", opti_n_clusters)


def cluster_various_main():
    """
    主聚类函数
    :return:
    """
    data_treat = get_data(file_path)
    # opti_para_select("k_modes", data_treat)
    num_clusters = 6
    cluster_kmodes(num_clusters, data_treat)

if __name__ == "__main__":
    # data_treat = get_data(file_path)
    # opti_para_select("k_modes", data_treat)
    # num_clusters = 6
    # cluster_kmodes(num_clusters, data_treat)

    # cluster_kmeans(num_clusters)
    # cluster_birch(num_clusters)
    # cluster_SpectralClustering(num_clusters)

    cluster_various_main()