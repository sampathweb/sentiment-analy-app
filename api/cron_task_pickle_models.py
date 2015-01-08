'''
Cron Task to Build Logisitc Regression and other Models offline
'''

import pickle
from flask import current_app
from app import create_app, db
from app.classifiers import clf_models

app = create_app('app.settings.Config')

from app.models import Dataset


def pickle_log_reg(dataset):
    '''Build Logistic Regression Model and Pickle the Model for Prediction'''
    filename = current_app.config['DATA_DIR'] + dataset.test_file
    clf = clf_models.train_logistic_reg_classifier(filename)
    dataset.lr_pickle_file = dataset.name + '-lr.pkl'
    pickle.dump(clf, open(current_app.config['PICKLE_DIR'] + dataset.lr_pickle_file, 'wb'))
    db.session.add(dataset)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        datasets = db.session.query(Dataset).all()
        # Build Logisitc Reg Model for those datasets that need to be updated
        for dataset in datasets:
            # if not dataset.lr_pickle_file:
            pickle_log_reg(dataset)
