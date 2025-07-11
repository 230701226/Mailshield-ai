# custom_features.py

import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
class TextLengthExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([[len(text)] for text in X])

class LinkCountExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([[len(re.findall(r'http[s]?://', text))] for text in X])