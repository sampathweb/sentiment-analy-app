from __future__ import division
from flask import current_app
from app import db, trained_models
from app.models import Dataset
from app.classifiers import naive_bayes


def get_classifier(ds_name):
    if ds_name not in trained_models or trained_models[ds_name]:
        trained_models[ds_name] = train_classifier(ds_name)
    return trained_models[ds_name]


def train_classifier(ds_name):
    dataset = db.session.query(Dataset).filter(Dataset.name == ds_name).one()
    if dataset:
        filename = current_app.config['DATA_DIR'] + dataset.train_file
        # Train the Classifier
        clf = naive_bayes.NaiveBayes()
        with open(filename) as f:
            for line in f:
                data_row = line.split('\t')
                clf.train(data_row[1], data_row[0])
        # Score the Classifier
        score_classifier(clf, ds_name)
        return clf


def score_classifier(clf, ds_name):
    accuracy_count = 0
    total_count = 0
    dataset = db.session.query(Dataset).filter(Dataset.name == ds_name).one()
    if dataset:
        filename = current_app.config['DATA_DIR'] + dataset.test_file
        with open(filename) as f:
            for line in f:
                total_count += 1
                data_row = line.split('\t')
                cat_pred = clf.predict(data_row[1])
                if cat_pred == data_row[0]:
                    accuracy_count += 1
        score = accuracy_count / total_count
        # Update the score in DB
        dataset.test_score = score
        db.session.add(dataset)
        db.session.commit()
