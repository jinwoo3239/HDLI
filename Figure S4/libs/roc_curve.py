import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

import matplotlib.pyplot as plt


def ROC_curve_binary_class_analysis(dataset=None, features=None, features_name=None,figsize=(4, 4), is_save_file=False, dpi=600):

    '''
    type of dataset = pd.DataFrame, ['Label', 'Name'] colume should be included in dataaset
    
    '''

    if type(dataset) == pd.DataFrame:
        X = dataset[features].values.reshape(-1, 1)
        y = dataset.Label.values
    else:
        raise ValueError('Invalid dataset(input) type. type of dataset should be pd.DataFrame')
        

    model = LogisticRegression(max_iter=500)

    model.fit(X, y)
    y_proba = model.predict_proba(X)[:, 1]

    fpr, tpr, thresholds = metrics.roc_curve(y, y_proba)
    roc_auc = metrics.auc(fpr, tpr)

    # youden's index
    J = tpr - fpr
    idx = np.argmax(J)

    plt.figure(figsize=figsize)
    plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}')
    plt.scatter(fpr[idx], tpr[idx], label=f"Sensitivity = {tpr[idx]:.2f}\nSpecificity = {1 - fpr[idx]:.2f}")
    plt.title(f'{features}')
    if type(features_name) is not None:
        plt.title(f'{features_name}')
    plt.legend()
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')

    if is_save_file:
        plt.savefig('roc_curve.png', dpi=dpi)



    plt.show()





