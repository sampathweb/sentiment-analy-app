from __future__ import division
import re
from collections import defaultdict
import numpy as np


class FeatureVectorizer(object):

    def __init__(self, features=None, positive_cat=None, negative_cat=None):
        self.features = features
        self.positive_cat = positive_cat
        self.negative_cat = negative_cat

    def _get_features(self, item):
        # Split the words by non-alpha characters. Excludes words of one char and more than 25 chars
        splitter = re.compile('\\W*')
        features = [s.lower() for s in splitter.split(item) if len(s) > 2 and len(s) < 25]
        return features

    def extract_features(self, item):
        item_features = self._get_features(item)
        p = len(self.features)  # One additional for Target Col
        data = np.zeros((1, p))
        for p_idx, feature in enumerate(self.features):
            if feature in item_features:
                data[0, p_idx] = 1
        return data


class BagWordsOneCat(FeatureVectorizer):

    def __init__(self, positive_cat, min_freq=0.01, diff_freq=0):
        '''Initializes feature and target counts'''
        # Features Count has dictionary of feature and its count by target class
        # Target Count contains each class and its count
        self.positive_cat = positive_cat
        self.negative_cat = None
        self.features = []
        self.feat_counts = defaultdict(lambda: [0, 0])
        self.cat_counts = [0, 0]
        self.doc_cat = []
        self.doc_features = []
        self.min_freq = min_freq
        self.diff_freq = diff_freq

    def categories(self):
        return self.cat_counts.keys()

    def train(self, item, cat):
        features = self._get_features(item)
        if cat == self.positive_cat:
            cat_val = 1
        else:
            cat_val = 0
            if not self.negative_cat:
                self.negative_cat = cat
        # Increment the count for every feature with this category
        for feat in features:
            self.feat_counts[feat][cat_val] += 1
        # Increment the count for this category
        self.cat_counts[cat_val] += 1
        self.doc_cat.append(cat)
        self.doc_features.append(features)
        return True

    def prune_features(self):
        for feature, cat_count in self.feat_counts.items():
            freq_y_0 = cat_count[0] / self.cat_counts[0]
            freq_y_1 = cat_count[1] / self.cat_counts[1]
            diff_freq = abs(freq_y_0 - freq_y_1) / (freq_y_0 + freq_y_1)
            # print feature, freq_y_0, freq_y_1
            if (freq_y_0 > self.min_freq or freq_y_1 > self.min_freq) and \
                    diff_freq > self.diff_freq:
                self.features.append(feature)

    def to_array(self):
        # Prune the elements
        self.prune_features()
        # create a numpy array of elements
        p = len(self.features) + 1  # One additional for Target Col
        n = len(self.doc_cat)
        data = np.zeros((n, p))
        target = np.zeros((n, 1))
        for n_idx, doc_features in enumerate(self.doc_features):
            if self.doc_cat[n_idx] == self.positive_cat:
                target[n_idx, 0] = 1
            for p_idx, feature in enumerate(self.features):
                if feature in doc_features:
                    data[n_idx, p_idx] = 1
        return data, target

    def get_feature_vectorizer(self):
        feature_vectorizer = FeatureVectorizer(self.features, self.positive_cat, self.negative_cat)
        return feature_vectorizer

if __name__ == '__main__':
    filename = 'movie-reviews-dataset-test.tsv'
    # Train the Classifier
    clf = BagWordsOneCat('positive')
    with open(filename) as f:
        for line in f:
            data_row = line.split('\t')
            clf.train(data_row[1], data_row[0])
    # Score the Classifier
    data, target = clf.to_array()
