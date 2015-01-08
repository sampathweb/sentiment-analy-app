import numpy as np
from scipy.optimize import fmin_bfgs


class LogisticReg(object):
    '''Fit and predict a Two Class Logistic Regression'''

    def __init__(self, vectorizer=None, theta=None):
        # Theta and Vectorizer can be pre-loaded
        self.theta = theta
        self.vectorizer = vectorizer

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def predict_proba(self, x):
        '''Returns a tuple of probabilities for y=0 and y=1'''
        if len(self.theta) > 0:
            proba_y1 = self.sigmoid(np.dot(self.theta[:-1], x[0]))
            proba_y0 = 1 - proba_y1
        else:
            proba_y0, proba_y1 = 0, 0
        return proba_y0, proba_y1

    def predict(self, x):
        '''Returns Positive or Negative Category depending on probability of y=1 > 0.5 or otherwise'''
        if self.vectorizer:
            x = self.vectorizer.extract_features(x)
        proba_y0, proba_y1 = self.predict_proba(x)
        if proba_y1 > 0.5:
            y_val = 1
        else:
            y_val = 0
        return self.get_class_name(y_val)

    def get_class_name(self, y_val):
        '''Returns the Class Name for the Predicted Value'''
        if y_val == 1:
            return self.vectorizer.positive_cat
        return self.vectorizer.negative_cat

    def log_likelihood(self, X, Y, w, C=0.1):
        return np.sum(np.log(self.sigmoid(Y * np.dot(X, w)))) - C / 2 * np.dot(w, w)

    def log_likelihood_grad(self, X, Y, w, C=0.1):
        K = len(w)
        N = len(X)
        s = np.zeros(K)
        for i in range(N):
            s += Y[i] * X[i] * self.sigmoid(-Y[i] * np.dot(X[i], w))
        s -= C * w
        return s

    def fit(self, X, Y, C=0.1):
        def f(w):
            return -1 * self.log_likelihood(X, Y, w, C)

        def fprime(w):
            return -1 * self.log_likelihood_grad(X, Y, w, C)

        K = X.shape[1]
        initial_guess = np.zeros(K)

        # Scipy to do gradient based BFGS method
        self.theta = fmin_bfgs(f, initial_guess, disp=False, maxiter=20)
        return self  # Return fitted model

    def accuracy(self, X, Y):
        n_correct = 0
        for i in range(len(X)):
            if self.predict(X[i]) == Y[i]:
                n_correct += 1
        return n_correct * 1.0 / len(X)
