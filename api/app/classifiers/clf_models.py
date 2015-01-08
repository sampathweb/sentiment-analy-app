from __future__ import division
import pickle
from flask import current_app
from app import db, trained_models
from app.models import Dataset
from app.classifiers.naive_bayes import NaiveBayes
from app.classifiers.bag_words import BagWordsOneCat
from app.classifiers.logistic_reg import LogisticReg
from app.classifiers.meta_mind import MetaMindTextClassifier


def get_classifier(ds_name, clf_name):
    if ds_name not in trained_models:
        trained_models[ds_name] = {}
    if clf_name not in trained_models[ds_name]:
        trained_models[ds_name][clf_name] = train_classifier(ds_name, clf_name)
    return trained_models[ds_name][clf_name]


def train_classifier(ds_name, clf_name):
    dataset = db.session.query(Dataset).filter(Dataset.name == ds_name).one()
    db_update = False
    clf = None
    if dataset:
        train_filename = current_app.config['DATA_DIR'] + dataset.train_file
        test_filename = current_app.config['DATA_DIR'] + dataset.test_file
        if clf_name == 'NaiveBayes':
            clf = train_naive_bayes_classifier(train_filename)
            # If the dataset has not been scored, build the accuracy using test file
            if not dataset.test_score:
                dataset.test_score = score_classifier(clf, test_filename)
                db_update = True
        elif clf_name == 'LogisticReg':
            # Takes too long to train, so only use Pickled Objecs for now
            if dataset.lr_pickle_file:
                lr_pickle_file = current_app.config['PICKLE_DIR'] + dataset.lr_pickle_file
                try:
                    clf = pickle.load(open(lr_pickle_file, 'rb'))
                except:
                    clf = None
            # If the dataset has not been scored, build the accuracy using test file
            # if not dataset.test_score_lr:
            #     dataset.test_score_lr = score_classifier(clf, test_filename)
        elif clf_name == 'MetaMind' and dataset.mm_model_id:
            clf = MetaMindTextClassifier(current_app.config['MM_AUTH_KEY'], dataset.mm_model_id)
        else:
            clf = None
    if db_update:
        db.session.add(dataset)
        db.session.commit()
    return clf


def train_naive_bayes_classifier(filename):
    # Train the Classifier
    clf = NaiveBayes()
    with open(filename) as f:
        for line in f:
            data_row = line.split('\t')
            clf.train(data_row[1], data_row[0])
    return clf


def score_classifier(clf, filename):
    accuracy_count = 0
    total_count = 0
    with open(filename) as f:
        for line in f:
            total_count += 1
            data_row = line.split('\t')
            cat_pred = clf.predict(data_row[1])
            if cat_pred == data_row[0]:
                accuracy_count += 1
    score = accuracy_count / total_count
    return score


def train_logistic_reg_classifier(filename):
    # Build a Bag of Words - Two Category classifier
    # Any higer frequency takes too long to train
    bag_words_vect = BagWordsOneCat('positive', min_freq=0.02, diff_freq=0.2)
    with open(filename) as f:
        for line in f:
            data_row = line.split('\t')
            bag_words_vect.train(data_row[1], data_row[0])
    # Score the Classifier
    X, y = bag_words_vect.to_array()
    clf = LogisticReg(vectorizer=bag_words_vect.get_feature_vectorizer())
    clf.fit(X, y)
    return clf
