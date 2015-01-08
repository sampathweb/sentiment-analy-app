'''Endpoint for getting prediction results using available datasets'''

from flask import Blueprint, jsonify, request
from app.classifiers import clf_models
from app.decorators import jsonp

predictors = Blueprint('predictors', __name__, url_prefix='/predictors')


@predictors.route('/')
@jsonp
def predict():
    '''Returns Predicted Category for the form data'''
    data = {}
    data['text'] = request.args.get('text')
    data['dataset'] = request.args.get('dataset')
    data['models'] = []
    # Get classifier and run Predict on it
    print 'In Predict Function'
    for clf_name in ['NaiveBayes', 'LogisticReg', 'MetaMind']:
        clf = clf_models.get_classifier(data['dataset'], clf_name)
        if clf:
            model_prediction = {}
            model_prediction['model_name'] = clf_name
            model_prediction['prediction'] = clf.predict(data['text'])
            data['models'].append(model_prediction)
    return jsonify(predicted=data)
