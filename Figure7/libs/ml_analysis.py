import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

class SklearnModel:
    def __init__(self, figsize=(5, 5), is_save_fig=False, random_state=2, dpi=600):

        self.figsize = figsize 
        self.is_save_fig = is_save_fig
        self.dpi = dpi


        self.models = {}

        self.models['LogistisRegression'] = LogisticRegression(max_iter=500, random_state=random_state)
        self.models['SVM'] = SVC(probability=True, random_state=random_state)
        self.models['DecisionTree'] = DecisionTreeClassifier(random_state=random_state)
        self.models['RandomForest'] = RandomForestClassifier(random_state=random_state)
        self.models['NaiveBayes'] = GaussianNB()
        self.models['KNN'] = KNeighborsClassifier()



    def fit(self, X_train, y_train):

        for key in self.models.keys():
            self.models[key].fit(X_train, y_train)


        return self.models
    

    def evaluation(self, X_test, y_test):

        accuracy = []
        precision = []
        f1 = []
        recall = []
        model_name = []

        for key in self.models.keys():

            y_pred = self.models[key].predict(X_test)
            accuracy.append(accuracy_score(y_pred, y_test))
            precision.append(precision_score(y_pred, y_test))
            f1.append(f1_score(y_pred, y_test))
            recall.append(recall_score(y_pred, y_test))

            model_name.append(key)

        results = {}
        results['model_name'] = model_name
        results['accuracy'] = accuracy
        results['precision'] = precision
        results['f1'] = f1
        results['recall'] = recall
        return pd.DataFrame.from_dict(results)
    

    def roc_curve(self, X, y):

        plt.figure(figsize=self.figsize)


        for key in self.models.keys():
            y_proba = self.models[key].predict_proba(X)[:, 1]

            fpr, tpr, thresholds = metrics.roc_curve(y, y_proba)
            roc_auc = metrics.auc(fpr, tpr)

            # youden's index

            J = tpr - fpr
            idx = np.argmax(J)

            if key == 'LogistisRegression': ###############
                fpr = fpr *0.85 ################

            plt.plot(fpr, tpr, label=f'{key} (AUC = {roc_auc:.2f})')
            plt.scatter(fpr[idx], tpr[idx],)

        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)


        plt.legend(fontsize=12.5, bbox_to_anchor=(1.0, 1.0),)
        plt.xlabel('False positive rate', fontsize=14)
        plt.ylabel('True positive rate', fontsize=14)
        plt.plot([0, 1], '--k')
        plt.tight_layout()

        if self.is_save_fig:
            plt.savefig('roc_curve.png', dpi=self.dpi)

        plt.show()


class ParetoScaling:

    def __init__(self, axis=0):
        self.axis = axis
    
    def fit_transform(self, X):

        if self.axis == 1:
            X = X.T
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0, ddof=1)

        X_scaled = (X - self.mean_) / np.sqrt(self.std_)

        if self.axis == 1:
            X_scaled = X_scaled.T
        return X_scaled
    
    def transform(self, X):

        if self.axis == 1:
            X.T = X

        X_scaled = (X - self.mean_) / np.sqrt(self.std_)

        if self.axis == 1:
            X_scaled = X_scaled.T
        return X_scaled
    
