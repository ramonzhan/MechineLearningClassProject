# -*- encoding: utf-8 -*-
"""
@Description: 
@Time : 2021-3-19 10:10 
@File : model.py 
@Software: PyCharm
"""
import numpy as np
from itertools import product


class NaiveBayes(object):
    def __init__(self, feat_dim, laplace_smoothing=True, lam=0):
        self.lam = 1 if laplace_smoothing else lam
        self.label_list = None
        self.priori_prob = dict()
        self.likelihood_list = []
        self.feat_dim = feat_dim

    def train(self, train_feat, train_labels):
        print("start training")
        instance_num = len(train_labels)
        self.label_list = list(set(train_labels))
        # priori probability (count)
        self.priori_prob = {label: np.sum(train_labels == label) for label in self.label_list}
        # likelihood
        for feat_dim_idx in range(self.feat_dim):
            # product[0]: feature, product[1]: label
            product_list = list(product(list(set(train_feat[:, feat_dim_idx])), self.label_list))
            likelihood = {
                productvalue: np.sum(
                    np.logical_and(train_feat[:, feat_dim_idx] == productvalue[0], train_labels == productvalue[1])
                ) / self.priori_prob[productvalue[1]]
                for productvalue in product_list
            }
            self.likelihood_list.append(likelihood)
        # priori probability (real)
        self.priori_prob = {label: count / instance_num for label, count in self.priori_prob.items()}
        print("finished training")

    def inference(self, instance):
        pred_list = []
        for label in self.label_list:
            pred = self.priori_prob[label]
            for feat_dim_idx, likelihood in enumerate(self.likelihood_list):
                pred = pred * likelihood[(instance[feat_dim_idx], label)]
            pred_list.append(pred)
        max_idx = np.argmax(pred_list)
        return self.label_list[max_idx]
