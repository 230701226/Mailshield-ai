from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import re

class TextLengthExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):
        return np.array([[len(text)] for text in X])

class LinkCountExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):
        return np.array([[len(re.findall(r'http[s]?://', text))] for text in X])
