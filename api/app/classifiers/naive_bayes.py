from __future__ import division
import re
from collections import defaultdict


class NaiveBayes(object):

    def __init__(self):
        '''Initializes feature and target counts'''
        # Features Count has dictionary of feature and its count by target class
        # Target Count contains each class and its count
        self.feat_counts = defaultdict(dict)
        self.cat_counts = defaultdict(int)
        self.doc_count = 0

    def get_features(self, doc):
        '''Retuns a dictionary of unique set of words in the document'''
        # Split the words by non-alpha characters. Excludes words of one char and more than 25 chars
        splitter = re.compile('\\W*')
        words = [s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 25]
        return dict([(w, 1) for w in words])

    def categories(self):
        return self.cat_counts.keys()

    def train(self, item, cat):
        features = self.get_features(item)
        # Increment the count for every feature with this category
        for feat in features:
            self.feat_counts[feat][cat] = self.feat_counts[feat].get(cat, 0) + features[feat]
        # Increment the count for this category
        self.cat_counts[cat] += 1
        self.doc_count += 1
        return True

    def feat_prob(self, f, cat):
        '''Returns the Feature Probability "given" Category'''
        if self.cat_counts[cat]:
            return self.feat_counts[f].get(cat, 0) / self.cat_counts[cat]
        return 0

    def cat_prob(self, cat):
        '''Returns Category Probability for all Training Data'''
        if self.doc_count:
            return self.cat_counts.get(cat, 0) / self.doc_count
        return 0

    def predict(self, item):
        probs = {}
        # Find the category with the highest probability
        max_prob = 0.0
        best_cat = None
        features = self.get_features(item)
        for cat in self.categories():
            probs[cat] = self.cat_prob(cat) * sum([self.feat_prob(feat, cat) for feat in features])
            if probs[cat] > max_prob:
                best_cat = cat
                max_prob = probs[cat]

        return best_cat
