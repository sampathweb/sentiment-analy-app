'''Endpoint for Dataset file management - Listing, Uploads and Deletes'''

from flask import Blueprint, request, jsonify, current_app
from werkzeug import secure_filename

from app import db
from app.models import Dataset
from app.decorators import crossdomain, jsonp
from app.classifiers import cross_validation as cv

datasets = Blueprint('datasets', __name__, url_prefix='/datasets')


def allowed_file(filename):
    '''Returns True if the filename extension is in the allowed list'''
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@datasets.route('/', methods=['GET'])
@jsonp
def index():
    '''Returns the list of all available datasets'''
    data = db.session.query(Dataset).all()
    cols = ['name', 'source_file', 'protected', 'test_score']
    data = [{col: getattr(d, col) for col in cols} for d in data]
    return jsonify(datasets=data)


@datasets.route('/new/', methods=['POST'])
@crossdomain(origin='*')
def new():
    '''Adds the new dataset provided and splits the file into train / test and makes it ready for modelling'''
    file = request.files.get('file')
    ds_name = request.form.get('name')
    if ds_name and file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        with open(current_app.config['DATA_DIR'] + filename, 'wb') as f_out:
            f_out.write(file.read())
        dataset = Dataset()
        dataset.name = ds_name
        dataset.source_file = filename
        # Split the Files into Train and Test
        dataset.train_file, dataset.test_file = cv.train_test_split(current_app.config['DATA_DIR'], filename)
        db.session.add(dataset)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@datasets.route('/delete/', methods=['POST'])
@crossdomain(origin='*')
def delete():
    '''Deletes the dataset from table.  Currently does not purge files.  it needs to be added'''
    ds_name = request.form.get('name')
    try:
        dataset = db.session.query(Dataset).filter(Dataset.name == ds_name).one()
    except:
        dataset = None
    if ds_name and dataset:
        db.session.delete(dataset)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)
