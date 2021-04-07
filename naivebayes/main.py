# -*- encoding: utf-8 -*-
"""
@Description: 
@Time : 2021-3-19 10:10 
@File : main.py 
@Software: PyCharm
"""
from utils import read_tennis
from model import NaiveBayes
from sklearn.metrics import accuracy_score


train_features, train_labels, test_features, test_labels = read_tennis()
feat_dim = train_features.shape[1]
nb = NaiveBayes(feat_dim=feat_dim)
# train
nb.train(train_feat=train_features, train_labels=train_labels)
# test
print("start testing")
pred_label_list = []
for test_feat in test_features:
    pred_label = nb.inference(test_feat)
    pred_label_list.append(pred_label)

print("Accuracy: [{}%]".format(accuracy_score(test_labels, pred_label_list)))
