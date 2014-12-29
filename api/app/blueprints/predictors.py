from flask import Blueprint, jsonify, request
from app.classifiers import clf_models
from app.decorators import jsonp

predictors = Blueprint('predictors', __name__, url_prefix='/predictors')


@predictors.route('/')
@jsonp
def predict():
    data = {}
    data['text'] = request.args.get('text')
    data['dataset'] = request.args.get('dataset')
    nb_clf = clf_models.get_classifier(data['dataset'])
    if nb_clf:
        data['predicted_cat'] = nb_clf.predict(data['text'])
    else:
        data['predicted_cat'] = None
    return jsonify(predicted=data)


# @text_models.route('/score/')
# def score():
#     test_filename = data_uri + 'movie-reviews-test.tsv'
#     test_score = nb_clf.score(test_filename)
#     return jsonify(score=test_score)
