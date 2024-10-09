import numpy as np


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
    

    
class AutoScaling:

    def __init__(self, axis=0):
        self.axis = axis
    
    def fit_transform(self, X):

        if self.axis == 1:
            X = X.T

        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0, ddof=1)

        X_scaled = (X - self.mean_) / (self.std_)

        if self.axis == 1:
            X_scaled = X_scaled.T
        return X_scaled
    
    def transform(self, X,):

        if self.axis == 1:
            X = X.T

        X_scaled = (X - self.mean_) / (self.std_)

        if self.axis == 1:
            X_scaled = X_scaled.T
        return X_scaled
    

class MinMaxScaler:

    def __init__(self, axis=0):
        self.axis = axis

    def fit_transform(self, X):

        if self.axis == 1:
            X = X.T


        self.min_ = np.min(X, axis=0)
        self.max_ = np.max(X, axis=0)

        scaled_df = (X - self.min_) / (self.max_ - self.min_)

        if self.axis == 1:
            scaled_df = scaled_df.T
        return scaled_df
    
    def transform(self, X):

        if self.axis == 1:
            X = X.T
        scaled_df = (X - self.min_) / (self.max_ - self.min_)

        if self.axis == 1:
            scaled_df = scaled_df.T

        return scaled_df 
    