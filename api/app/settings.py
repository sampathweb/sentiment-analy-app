import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    #Upload of files
    ALLOWED_EXTENSIONS = set(['txt', 'csv', 'tsv'])
    DATA_DIR = BASE_DIR + '/uploads/'
    # DB Connection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/app.sqlite'
    SECRET_KEY = 'All Models are Wrong.  Some are Useful - George E. P. Box'
