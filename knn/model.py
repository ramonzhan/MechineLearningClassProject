# -*- encoding: utf-8 -*-
"""
@Description: 1）载入数据；2）初始化k值；3）预测类别，遍历每一个训练样本计算距离；4）按距离排序，取topk个最近地训练数据；
5）取频率最高地类别作为测试数据的预测类别。
是一个lazy的算法，无显式的训练过程。原始的knn算法复杂度比较高。我们使用比较巧妙的数据结构来减小测试时的时间复杂度（KD树）
其关键之一在于距离函数（距离度量）的选择，我们可以选择Lp距离（欧氏距离、曼哈顿距离、切比雪夫距离）
关键点之二在于时间复杂度。
@Time : 2021-3-13 21:03 
@File : model.py 
@Software: PyCharm
"""
import numpy as np
from utils import find_majority


class KNN(object):
    def __init__(self, k):
        self.k = k
        self.train_instences = None
        self.train_labels = None

    def train(self, instences, labels):   # lazy 算法，没有显式的训练过程，只是把训练数据记住。把训练数据全部输入进来
        self.train_instences = instences
        self.train_labels = labels

    def distence_calculation(self, instence):
        # 仅简单实现了欧式距离
        distences = list()
        for train_instance in self.train_instences:
            distence = np.sqrt(np.sum((train_instance - instence) ** 2))
            distences.append(distence)
        return distences

    def eval(self, instence):  # 输入一个测试样本，返回预测的标签
        # 1. 找到最近的k个邻居
        distences = self.distence_calculation(instence)
        topk_indexs = np.argsort(distences)[:self.k]    # 选取前k项
        topk_labels = self.train_labels[topk_indexs]
        label = find_majority(topk_labels)
        return label
