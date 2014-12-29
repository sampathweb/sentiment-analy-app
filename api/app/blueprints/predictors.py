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
    # Get classifier and run Predict on it
    nb_clf = clf_models.get_classifier(data['dataset'])
    if nb_clf:
        data['predicted_cat'] = nb_clf.predict(data['text'])
    else:
        data['predicted_cat'] = None
    return jsonify(predicted=data)
